# Project 1: AI Anime Recommender (LLMOps Architecture)

## 1. Application Overview (The "What")
This project is a **Retrieval-Augmented Generation (RAG)** application. Users can ask for anime recommendations using natural language, and the AI answers by retrieving context from a custom vector database of anime synopses.

### Tech Stack
* **Frontend:** Streamlit
* **Backend Orchestration:** **LangChain** (The central "brain" framework that wires the frontend, database, and AI together).
* **Vector Database:** ChromaDB 
* **Embeddings:** HuggingFace (`all-MiniLM-L6-v2`)
  * *Note: HuggingFace is the "GitHub of AI" where open-source models are hosted. The `all-MiniLM-L6-v2` model is automatically downloaded by the `sentence-transformers` library to convert English anime synopses into mathematical coordinates (Embeddings) so ChromaDB can search them.*
* **LLM Provider:** **Groq** 
  * We chose Groq because it utilizes custom Language Processing Units (LPUs) for lightning-fast inference. It serves open-source models (like `openai/gpt-oss-20b`), providing near-instant responses with a generous free tier.

---

## 2. Core Application Logic (The RAG Pipeline)
This section explains how the Python application code processes data and generates recommendations.

### 2.1 Data Ingestion (Pre-build)
Before the app can be containerized, the data must be ingested. A Python script (`pipeline/build_pipeline.py`) is executed locally to read an Anime dataset (CSV), generate embeddings using HuggingFace, and permanently save the vectors into a local `chroma_db/` folder. This pre-built folder is then bundled into the final Docker image.

### 2.2 Retrieval Engine
When a user asks a question, LangChain converts their text into a mathematical embedding. It then performs a similarity search against ChromaDB to retrieve the top 5 closest anime synopses that match the user's mood.

### 2.3 Generation Engine
LangChain uses a process called `create_stuff_documents_chain` to take those 5 retrieved anime synopses and "stuff" them into a hidden prompt. This enriched prompt is sent to the Groq LLM, which uses the provided context to generate a highly accurate, conversational recommendation.

---

## 3. Infrastructure & Deployment (The "How")
Instead of deploying to external cloud VMs, this project utilizes a modern, local Cloud-Native architecture directly on Apple Silicon.

### 3.1 Kubernetes via OrbStack
* **The Platform:** We replaced traditional Linux VMs (like Multipass) with **OrbStack**.
* **Why:** OrbStack provides a blazing-fast, native Kubernetes cluster optimized for Apple Silicon (ARM64). It requires almost zero configuration and seamlessly bridges Kubernetes `LoadBalancer` services directly to `localhost:8080`.

### 3.2 GitOps & Secrets Management (Sealed Secrets)
To prevent committing raw API keys (like the Groq API key) to GitHub in plain text, we implemented GitOps security.
* **Controller:** We installed the **Sealed Secrets Controller** via Helm into the OrbStack cluster.
* **Encryption:** We used the `kubeseal` CLI to encrypt the raw API keys into gibberish `.yaml` files.
* **Deployment:** These encrypted files are safely stored in GitHub. When deployed, the Kubernetes controller intercepts the files and decrypts them directly into secure memory.

### 3.3 The Self-Hosted Git Runner
To bridge the gap between GitHub's Cloud and the local Mac cluster, we installed a **GitHub Actions Local Runner** (`actions-runner`).
* **The Role:** The runner sits as a background terminal process (`./run.sh`) on the Mac. It listens for successful cloud builds and executes the final deployment commands (`kubectl apply`) directly into the local OrbStack cluster.

---

## 4. The CI/CD Pipeline (GitHub Actions)
The deployment is fully automated via `.github/workflows/docker-build.yml`.

### Stage 1: Cloud Build (Continuous Integration)
When code is pushed, a GitHub-hosted Ubuntu runner executes the following:
* **Disk Space Optimization:** Uses `jlumbroso/free-disk-space` to aggressively delete 30GB of unused software from the cloud runner, preventing crashes when compiling heavy AI libraries like PyTorch.
* **ARM64 Cross-Compilation:** Uses `setup-qemu-action` to emulate an ARM64 environment in the cloud so the image is compatible with the Apple Silicon Mac.
* **Docker Optimization:** The `Dockerfile` explicitly uses `--no-cache-dir` during PyTorch installation to prevent multi-gigabyte layer bloat inside the container.
* **Caching (`type=gha`):** Implements GitHub Actions caching to store heavy Docker layers, reducing subsequent build times from 45 minutes to just a few seconds.
* **Push to GHCR:** Pushes the finalized image to the GitHub Container Registry. (Permissions were explicitly granted in the GitHub UI to allow the private repository to manage the package).

### Stage 2: Local Deployment (Continuous Deployment)
* The GitHub Cloud hands off the job to the **Self-Hosted Git Runner** on the Mac.
* The runner executes `kubectl apply -f k8s/`, deploying the new image and the Sealed Secrets into the OrbStack cluster.

---

## 5. Enterprise Observability (Grafana Cloud)
To monitor the health and resource consumption of the AI application, we implemented an outbound "Push-Model" monitoring stack.
* **The Dashboard:** We created a **Grafana Cloud** account.
* **The Agent:** We deployed the **Grafana Alloy Agent** into the local OrbStack cluster using `helm`.
* **The Data Flow:** Because the cluster is private, Grafana Cloud cannot connect inward. Instead, the local Helm agents collect CPU and RAM metrics and push them *outward* to the Grafana Cloud web dashboards in real-time.

---

*Note: Because this architecture is fully Cloud-Native and GitOps-driven, there are no internal databases or servers to back up. If the local OrbStack cluster is destroyed, the project can be completely rebuilt on a new machine by regenerating the following 4 cloud tokens:*
1. *Groq API Key (Generated at `console.groq.com`)*
2. *GitHub PAT (Generated in GitHub Developer Settings)*
3. *GitHub Runner Token (Generated in Repo Settings)*
4. *Grafana Cloud Token (Generated in Grafana Cloud)*
