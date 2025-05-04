# main_rag.py (for Cloud Function: query_gent_services_kb)
import functions_framework
from google.cloud import aiplatform
import numpy as np
import os
import json

# --- Configuration ---
# Path to the knowledge base data file
KB_DATA_PATH = os.path.join(os.path.dirname(__file__), 'data', 'gent_services.json')
# Model to use for embeddings
EMBEDDING_MODEL_NAME = "textembedding-gecko@001" # Or a newer version like text-embedding-005

# --- Globals --- 
# Store document objects (dictionaries) and their embeddings
DOCUMENTS = [] 
DOC_EMBEDDINGS = []
embedding_model = None
model_initialized = False

# --- Initialization Functions ---
def load_documents_from_json(file_path):
    """Loads documents from a JSON file."""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            docs = json.load(f)
        # Basic validation: ensure it's a list of dicts with 'title' and 'content'
        if not isinstance(docs, list) or not all(isinstance(d, dict) and 'title' in d and 'content' in d for d in docs):
            print(f"Error: Invalid format in {file_path}. Expected a list of objects with 'title' and 'content'.")
            return []
        print(f"Successfully loaded {len(docs)} documents from {file_path}")
        return docs
    except FileNotFoundError:
        print(f"Error: Knowledge base file not found at {file_path}")
        return []
    except json.JSONDecodeError:
        print(f"Error: Could not decode JSON from {file_path}")
        return []
    except Exception as e:
        print(f"Error loading documents: {e}")
        return []

def init_model_and_embeddings():
    """Initializes the embedding model and computes document embeddings."""
    global embedding_model, DOC_EMBEDDINGS, DOCUMENTS, model_initialized
    
    if model_initialized:
        return True

    print("Initializing RAG model and embeddings...")
    DOCUMENTS = load_documents_from_json(KB_DATA_PATH)
    if not DOCUMENTS:
        print("Initialization failed: No documents loaded.")
        return False # Failed to load documents

    document_contents = [doc['content'] for doc in DOCUMENTS]
    if not document_contents:
        print("Initialization failed: Documents loaded but no content found.")
        return False

    try:
        # Ensure Vertex AI client is initialized (uses ADC or GOOGLE_APPLICATION_CREDENTIALS)
        # Project/Location might be implicitly picked up, but explicit is safer if needed.
        # aiplatform.init(project=os.getenv('GOOGLE_CLOUD_PROJECT'), location=os.getenv('GOOGLE_CLOUD_LOCATION'))
        embedding_model = aiplatform.TextEmbeddingModel.from_pretrained(EMBEDDING_MODEL_NAME)
        # Get embeddings in batches if necessary (though Vertex AI handles it well)
        DOC_EMBEDDINGS = embedding_model.get_embeddings(document_contents)
        print(f"Computed {len(DOC_EMBEDDINGS)} embeddings for {len(DOCUMENTS)} documents.")
        model_initialized = True
        return True
    except Exception as e:
        print(f"Error initializing Vertex AI model or getting embeddings: {e}")
        # Reset globals if initialization fails partially
        DOCUMENTS = []
        DOC_EMBEDDINGS = []
        embedding_model = None
        model_initialized = False
        return False

# --- Helper Functions ---
def cosine_similarity(a, b):
    """Calculates cosine similarity between two embedding vectors."""
    try:
        # Convert embedding objects to numpy arrays if they aren't already
        vec_a = np.array(a.values) if hasattr(a, 'values') else np.array(a)
        vec_b = np.array(b.values) if hasattr(b, 'values') else np.array(b)
        norm_a = np.linalg.norm(vec_a)
        norm_b = np.linalg.norm(vec_b)
        if norm_a == 0 or norm_b == 0:
            return 0.0
        return float(np.dot(vec_a, vec_b) / (norm_a * norm_b))
    except Exception as e:
        print(f"Error calculating cosine similarity: {e}")
        return 0.0

# --- Cloud Function Entry Point ---

# Attempt initialization on cold start
init_model_and_embeddings()

@functions_framework.http
def query_gent_services_kb(request):
    """HTTP Cloud Function to query the Gent services knowledge base using RAG."""
    global model_initialized
    # Ensure model is ready, attempt re-init if failed on cold start
    if not model_initialized:
        print("Model not ready, attempting initialization...")
        if not init_model_and_embeddings():
            return ("Embedding model or documents not available. Check function logs for errors.", 503) # Service Unavailable

    # Extract query from request
    request_json = request.get_json(silent=True)
    query = None
    if request.args and 'query' in request.args:
        query = request.args.get('query')
    elif request_json and 'query' in request_json:
        query = request_json['query']

    if not query:
        return ("Missing 'query' parameter in request body or query string", 400)

    print(f"Received query: {query}")

    try:
        # Get embedding for the user query
        query_embedding = embedding_model.get_embeddings([query])[0]

        # Calculate similarities between query and document embeddings
        scores = [cosine_similarity(query_embedding, doc_vec) for doc_vec in DOC_EMBEDDINGS]

        if not scores:
             return { "status": "success", "answer": "I couldn't find any relevant information in the knowledge base." }

        # Find the best matching document
        best_index = int(np.argmax(scores))
        best_score = scores[best_index]
        best_doc = DOCUMENTS[best_index]
        best_answer = best_doc['content'] # Return the content of the best matching document
        best_title = best_doc.get('title', 'Unknown Title') # Get title for logging

        print(f"Best match: '{best_title}' (Index: {best_index}, Score: {best_score:.4f})")

        # Optional: Add a similarity threshold
        # SIMILARITY_THRESHOLD = 0.7 
        # if best_score < SIMILARITY_THRESHOLD:
        #     print(f"Score {best_score:.4f} below threshold {SIMILARITY_THRESHOLD}")
        #     return { "status": "success", "answer": "I found some related information, but I'm not sure if it directly answers your question. Could you please rephrase?" }

        return { "status": "success", "answer": best_answer }

    except aiplatform.errors.ApiException as e:
         print(f"Vertex AI API Error during query embedding: {e}")
         return ("Error communicating with Vertex AI to process the query.", 500)
    except Exception as e:
        print(f"Error processing query: {e}")
        import traceback
        traceback.print_exc() # Print stack trace to logs
        return ("An internal error occurred while processing the query.", 500)
