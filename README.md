# HR Policy Assistant

An intelligent, multi-agent HR Policy Assistant built with LangGraph, FastAPI, and Streamlit. This tool uses Retrieval-Augmented Generation (RAG) to dynamically search company HR policies and evaluate complex employee requests, providing clear decisions with cited rationale.

## 🚀 Features

- **Multi-Agent Architecture**: Built with LangGraph, separating concerns into specialized agents:
  - **Document Retrieval Agent**: Semantically searches the vector database for relevant policies.
  - **Case Evaluation Agent**: Analyzes the case against retrieved policies to determine compliance.
  - **Decision Summary Agent**: Synthesizes the evaluation into a professional, structured markdown summary.
- **RAG Powered**: Uses local ChromaDB and `sentence-transformers` via HuggingFace for fast, secure, and accurate vector embeddings.
- **State-of-the-Art LLM**: Powered by Google's latest Gemini 2.5 models (`gemini-2.5-flash`) via `langchain-google-genai`.
- **Modern UI**: A clean, professional dashboard built with Streamlit featuring tabbed outputs and responsive design.

## 🏗️ Architecture

- **Frontend**: Streamlit
- **Backend API**: FastAPI, Uvicorn
- **AI / Agent Framework**: LangChain, LangGraph
- **Vector Database**: ChromaDB
- **Embedding Model**: `all-MiniLM-L6-v2` (HuggingFace)

## 📁 Project Structure

```
HR Policy Assistant/
├── backend/
│   ├── agents.py           # LangGraph orchestration and agent definitions
│   ├── document_loader.py  # ChromaDB vector store and HuggingFace embedding setup
│   ├── main.py             # FastAPI server endpoints
│   └── requirements.txt    # Backend dependencies
├── frontend/
│   ├── app.py              # Streamlit dashboard UI
│   └── requirements.txt    # Frontend dependencies
├── data/                   # Directory containing HR Policy PDFs
├── .env                    # Environment variables (API keys)
└── generate_pdfs.py        # Utility script to generate mock policy PDFs
```

## 🛠️ Setup Instructions

### 1. Prerequisites
Ensure you have Python 3.9+ installed on your machine. 

### 2. Clone and Create Virtual Environment
Clone this repository and set up a Python virtual environment:
```bash
python -m venv .venv

# On Windows:
.\.venv\Scripts\activate
# On Mac/Linux:
source .venv/bin/activate
```

### 3. Install Dependencies
Install the required packages for both the backend and frontend:
```bash
pip install -r backend/requirements.txt
pip install -r frontend/requirements.txt
```

### 4. Environment Variables
Create a `.env` file in the root directory and add your API keys:
```env
GOOGLE_API_KEY=your_google_gemini_api_key_here
HF_TOKEN=your_huggingface_token_here
```

### 5. Add Policy Data
Ensure your policy PDF files are placed in the `data/` directory. (You can also run `python generate_pdfs.py` to create sample policies if the directory is empty). The vector database (`chroma_db`) will be automatically built the first time you run the backend.

## 🏃‍♂️ How to Run

You will need to run the Backend and Frontend concurrently in two separate terminal windows.

### Start the FastAPI Backend
```bash
# Ensure you are in the project root with the virtual environment activated
set PYTHONPATH=.
python -m uvicorn backend.main:app --host 0.0.0.0 --port 8000
```

### Start the Streamlit Frontend
```bash
# Open a new terminal, activate the virtual environment
cd frontend
python -m streamlit run app.py
```

The application will be accessible at `http://localhost:8501`.

## 📝 Usage

1. Open the Streamlit dashboard in your browser.
2. Enter a hypothetical case in the text area (e.g., *"Jane wants to expense a $100 gym membership"*).
3. Click **"Evaluate Case"**.
4. The system will retrieve relevant guidelines, evaluate the request, and present a structured decision with citations in the respective tabs.

## 📄 License
This project is licensed under the MIT License.
