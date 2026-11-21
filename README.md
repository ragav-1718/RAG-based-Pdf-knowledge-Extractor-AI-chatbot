PDF AI Assistant
PDF AI Assistant is a Multi-PDF Retrieval-Augmented Generation (RAG) chatbot that enables users to upload up to five PDF documents and interact with them through a conversational interface.

The application extracts text from PDF files, generates embeddings, stores them in a FAISS vector database, retrieves relevant content, and uses a Large Language Model (LLM) to answer user questions based on the uploaded documents.

Features
Upload up to 5 PDF files
Multi-document question answering
Semantic search using vector embeddings
FAISS-powered retrieval
LLM-based response generation
Persistent chat history during a session
Modern web interface built with Streamlit
Tech Stack
Python
Streamlit
LangChain
FAISS
Sentence Transformers
Groq
PyPDF
Architecture
PDF Upload
    |
    v
Text Extraction
    |
    v
Chunking
    |
    v
Embedding Generation
    |
    v
FAISS Vector Store
    |
    v
Semantic Retrieval
    |
    v
LLM Processing
    |
    v
Response Generation
Installation
git clone https://github.com/your-username/pdf-ai-assistant.git
cd pdf-ai-assistant
pip install -r requirements.txt
Create a .env file:

GROQ_API_KEY=your_api_key
Usage
streamlit run app.py
Upload one or more PDF files and start asking questions about their contents.

Project Structure
.
├── app.py
├── requirements.txt
├── README.md
├── space2.jpg
└── src
    ├── chunker.py
    ├── embeddings.py
    ├── vectorstore.py
    └── llm.py
Future Enhancements
Source citations
PDF summarization
OCR support for scanned documents
Conversation export
Multi-session chat management
Author
Ragavan
