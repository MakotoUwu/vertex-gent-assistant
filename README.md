# 🏙️ Gent City Assistant - Vertex AI Agent

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

Welcome to the Gent City Assistant! This project leverages Google's Vertex AI Agent Development Kit (ADK) to build an intelligent assistant capable of answering questions about Gent city services and public transport.

## ✨ Features

*   **Knowledge Base Querying:** Ask questions about city hall hours, waste collection, building permits, parks, museums, resident registration, and more! (Powered by a RAG Cloud Function using `textembedding-gecko`).
*   **Public Transport Info:**
    *   Check for current disruptions on De Lijn network in Gent.
    *   Get upcoming schedules for specific bus/tram stops or lines.
*   **Natural Language Interaction:** Converse naturally with the agent.
*   **Extensible:** Built using the Vertex AI ADK, making it easy to add more tools and capabilities.

## ⚙️ Workflow Diagram

This diagram illustrates how the agent handles user requests:

```mermaid
graph LR
    A[👤 User Query] --> B{🤖 Gent Agent (agent.py)};
    B --> C{❓ Understand Intent & Select Tool};
    C -->|Query Gent Services| D[🔨 Tool: query_gent_knowledge_base_tool];
    C -->|Check Disruptions| E[🔨 Tool: get_transport_disruptions_tool];
    C -->|Get Schedule| F[🔨 Tool: get_transport_schedule_tool];
    D --> G[☁️ Cloud Function: query-gent-services-kb];
    E --> H[☁️ Cloud Function: get-transport-disruptions];
    F --> I[☁️ Cloud Function: get-transport-schedule];
    G -- RAG Result --> J{✅ Process Result};
    H -- Disruption Info --> J;
    I -- Schedule Info --> J;
    J --> K[💬 Formulate Response];
    K --> L[🗣️ Response to User];
```

## 📁 Project Structure

```
vertex-gent-assistant/
├── .env             # Environment variables (API keys, URLs) - !! DO NOT COMMIT !!
├── .gitignore       # Files ignored by Git
├── agent.py         # Main agent logic using Vertex AI ADK
├── main_rag.py      # Cloud Function source: RAG for Gent services KB
├── main_transport.py# Cloud Function source: De Lijn transport info
├── requirements.txt # Python dependencies
├── data/
│   └── gent_services.json # Sample knowledge base data
├── docs/
│   └── gent_agent_guide_combined.txt # Original guide (for reference)
└── README.md        # This file
```

## 🚀 Setup Instructions

1.  **Clone the Repository:**
    ```bash
    git clone <your-repo-url>
    cd vertex-gent-assistant
    ```

2.  **Create a Virtual Environment:**
    ```bash
    python -m venv venv
    source venv/bin/activate  # On Windows: venv\Scripts\activate
    ```

3.  **Install Dependencies:**
    ```bash
    pip install -r requirements.txt
    ```

4.  **Set Up Environment Variables:**
    *   Copy `.env.example` to `.env` (or create `.env` manually).
    *   Fill in the required values:
        *   `GOOGLE_CLOUD_PROJECT`: Your Google Cloud Project ID.
        *   `DE_LIJN_API_KEY`: Your API key for the De Lijn Open Data API.
        *   Leave `GOOGLE_CLOUD_LOCATION` as `us-central1` (or change if needed).
        *   `GOOGLE_GENAI_USE_VERTEXAI=True` is set.
        *   **Important:** The `QUERY_KB_FUNCTION_URL`, `TRANSPORT_DISRUPTION_FUNCTION_URL`, and `TRANSPORT_SCHEDULE_FUNCTION_URL` will be populated after deploying the Cloud Functions (see Deployment section).

5.  **Google Cloud Authentication:**
    *   Ensure you have the `gcloud` CLI installed.
    *   Authenticate: `gcloud auth login`
    *   Set your project: `gcloud config set project YOUR_PROJECT_ID`
    *   Enable necessary APIs (Cloud Functions, Cloud Build, Vertex AI) in your GCP console if not already enabled.

## ☁️ Deployment (Cloud Functions)

The agent relies on three backend Cloud Functions. Deploy them using the `gcloud` CLI from the project root directory:

*(Remember to replace `YOUR_PROJECT_ID` and `YOUR_DE_LIJN_API_KEY`)*

1.  **RAG KB Function:**
    ```bash
    gcloud functions deploy query-gent-services-kb \
      --gen2 \
      --runtime=python311 \
      --region=us-central1 \
      --source=. \
      --entry-point=query_gent_services_kb \
      --trigger-http \
      --allow-unauthenticated \
      --memory=512MB \
      --set-env-vars=GOOGLE_CLOUD_PROJECT=YOUR_PROJECT_ID,GOOGLE_CLOUD_LOCATION=us-central1
    ```

2.  **Transport Disruptions Function:**
    ```bash
    gcloud functions deploy get-transport-disruptions \
      --gen2 \
      --runtime=python311 \
      --region=us-central1 \
      --source=. \
      --entry-point=get_transport_disruptions \
      --trigger-http \
      --allow-unauthenticated \
      --set-env-vars=DE_LIJN_API_KEY=YOUR_DE_LIJN_API_KEY
    ```

3.  **Transport Schedule Function:**
    ```bash
    gcloud functions deploy get-transport-schedule \
      --gen2 \
      --runtime=python311 \
      --region=us-central1 \
      --source=. \
      --entry-point=get_transport_schedule \
      --trigger-http \
      --allow-unauthenticated \
      --set-env-vars=DE_LIJN_API_KEY=YOUR_DE_LIJN_API_KEY
    ```

➡️ **After deployment, copy the HTTPS trigger URLs provided by `gcloud` and update the corresponding variables in your `.env` file.**

## 💬 Running the Agent

Once setup and deployment are complete:

```bash
python agent.py
```

Follow the prompts to interact with the Gent City Assistant!

## 🤝 Contributing (Optional)

Contributions are welcome! Feel free to open issues or submit pull requests.

## 📜 License

This project is licensed under the MIT License - see the LICENSE file (if created) for details.
