# 🧠 Multi-Domain Support Triage Agent

## 📌 Overview

This project implements a **terminal-based AI support triage agent** that processes customer support tickets across multiple ecosystems (e.g., HackerRank, Claude, etc.).

The agent:

* Classifies tickets into appropriate **product areas**
* Decides whether to **respond or escalate**
* Generates **user-facing responses**
* Provides a **justification** for its decision

---

## ⚙️ Setup Instructions

### 1. Extract the zip files

```bash
unzip code.zip
cd code
```

### 2. Create Virtual Environment

```bash
python -m venv venv
venv\Scripts\activate   # On Windows
# OR
source venv/bin/activate   # On Mac/Linux
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. Configure Environment Variables

Create a `.env` file in the root directory, and copy .env.example to .env and replace the values with your own API keys:

```
GEMINI_API_KEY=your_api_key
GROQ_API_KEY=your_api_key
OPENROUTER_API_KEY=your_api_key

EMBEDDING_MODEL=all-MiniLM-L6-v2
GOOGLE_MODEL=gemini-2.5-flash
GROQ_MODEL=llama-3.3-70b-versatile
OPENROUTER_MODEL=openai/gpt-4o-mini
```

### 5. Adjust the `config.py` file.

Make sure the path to the knowledge base is correct. You can change the paths as per your requirements. Also, you can change the models and keys as needed. 

### 6. Run the Agent

```bash
python main.py
```

Output will be generated as:

```
OUTPUT_DIR/output.csv
```

---

## 🧩 Approach Overview

### 1. Ticket Processing Pipeline

Each ticket goes through the following stages:

#### a. Preprocessing

* Extract fields like `company`, `issue type`, and `description`
* Handle missing values (e.g., fallback for missing company)

#### b. Retrieval (RAG)

* Documents are filtered by **company/domain**
* Relevant knowledge is retrieved using **vector search (FAISS / embeddings)**

#### c. Product Area Classification

* A lightweight classifier maps tickets into categories such as:

  * Product Issue
  * Fraud
  * Inquiry
  * Bug

#### d. Safety & Escalation Logic

* Tickets are escalated if:

  * Sensitive keywords are detected (e.g., fraud, hacked, unauthorized access)
  * No relevant documents are retrieved
  * Confidence in response is low

#### e. Response Generation

* Uses LLM to generate:

  * Clear, user-facing response
  * Grounded strictly in retrieved documents

#### f. Justification Generation

* Short explanation describing:

  * Why the ticket was escalated OR
  * How the response was derived

---

## 📊 Output Format

The agent produces an `output.csv` with:

| Column        | Description                |
| ------------- | -------------------------- |
| status        | `replied` or `escalated`   |
| product_area  | Classified domain/category |
| response      | Final user-facing reply    |
| justification | Reasoning behind decision  |

---

## 🚀 Key Design Decisions

* **RAG-based architecture** for grounded responses
* **Fail-safe escalation** when knowledge is insufficient
* **Modular pipeline** (retrieval, classification, safety, generation)
* **Deterministic structure** for evaluation consistency