import streamlit as st
from pypdf import PdfReader
from src.chunker import split_text
from src.embeddings import create_embeddings
from src.vectorstore import create_vectorstore
from src.llm import generate_answer
import re
import base64

st.set_page_config(
    page_title="PDF AI Assistant",
    layout="wide"
)

if "messages" not in st.session_state:
    st.session_state.messages = []

if "vectorstore" not in st.session_state:
    st.session_state.vectorstore = None

if "pdf_loaded" not in st.session_state:
    st.session_state.pdf_loaded = False

if "file_names" not in st.session_state:
    st.session_state.file_names = []


def get_base64(image_path):
    with open(image_path, "rb") as img:
        return base64.b64encode(img.read()).decode()


background = get_base64("space2.jpg")

st.markdown(
    f"""
<style>

.stApp {{
    background-image:
    linear-gradient(
        rgba(0,0,0,0.65),
        rgba(0,0,0,0.75)
    ),
    url("data:image/jpg;base64,{background}");

    background-size: cover;
    background-position: center;
    background-attachment: fixed;
}}

.block-container {{
    max-width: 1100px;
    padding-top: 2rem;
}}

.title {{
    text-align:center;
    color:white;
    font-size:36px;
    font-weight:800;

    text-shadow:
    0 0 10px #00eaff,
    0 0 10px #00eaff,
    0 0 10px #00eaff;
}}

.subtitle {{
    text-align:center;
    color:#cbd5e1;
    font-size:18px;
    margin-bottom:30px;
}}

[data-testid="stChatMessage"] {{
    background:rgba(255,255,255,0.08);
    backdrop-filter:blur(20px);
    border:1px solid rgba(0,234,255,0.3);
    border-radius:18px;
    padding:15px;
    margin-bottom:12px;
}}

[data-testid="stFileUploader"] {{
    background:rgba(255,255,255,0.08);
    backdrop-filter:blur(20px);
    border-radius:20px;
    padding:20px;
}}

section[data-testid="stSidebar"] {{
    background:rgba(10,10,20,0.95);
}}

</style>
""",
    unsafe_allow_html=True
)

st.markdown(
    """
<div class="title">
🚀 PDF AI Assistant
</div>

<div class="subtitle">
Upload PDF Files And Chat With Them
</div>
""",
    unsafe_allow_html=True
)

uploaded_files = st.file_uploader(
    "Upload up to 5 PDFs",
    type=["pdf"],
    accept_multiple_files=True
)

if uploaded_files and len(uploaded_files) > 5:
    st.error("Maximum 5 PDFs allowed")
    st.stop()

current_files = []

if uploaded_files:
    current_files = [pdf.name for pdf in uploaded_files]

if current_files != st.session_state.file_names:

    st.session_state.file_names = current_files
    st.session_state.messages = []
    st.session_state.vectorstore = None
    st.session_state.pdf_loaded = False

with st.sidebar:

    st.title("📚 Documents")

    if uploaded_files:

        for pdf in uploaded_files:
            st.success(pdf.name)

if uploaded_files and not st.session_state.pdf_loaded:

    text = ""

    for pdf in uploaded_files:

        reader = PdfReader(pdf)

        for page in reader.pages:

            page_text = page.extract_text()

            if page_text:
                text += page_text + "\n"

    text = re.sub(r"\s+", " ", text)

    chunks = split_text(text)

    vectors = create_embeddings(chunks)

    vectorstore = create_vectorstore(
        chunks,
        vectors
    )

    st.session_state.vectorstore = vectorstore
    st.session_state.pdf_loaded = True

    st.success("Knowledge Base Ready")

for msg in st.session_state.messages:

    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

query = st.chat_input(
    "Ask anything about your PDFs..."
)

if query and st.session_state.vectorstore:

    st.session_state.messages.append(
        {
            "role": "user",
            "content": query
        }
    )

    with st.chat_message("user"):
        st.markdown(query)

    query_vector = create_embeddings(
        [query]
    )[0]

    results = st.session_state.vectorstore.similarity_search_by_vector(
        query_vector,
        k=5
    )

    context = "\n\n".join(
        [
            doc.page_content
            for doc in results
        ]
    )

    answer = generate_answer(
        context,
        query
    )

    with st.chat_message("assistant"):
        st.markdown(answer)

    st.session_state.messages.append(
        {
            "role": "assistant",
            "content": answer
        }
    )