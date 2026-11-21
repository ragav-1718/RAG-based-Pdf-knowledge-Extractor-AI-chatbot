from langchain_community.vectorstores import FAISS


def create_vectorstore(chunks, vectors):

    vectorstore = FAISS.from_embeddings(
        text_embeddings=list(zip(chunks, vectors)),
        embedding=None
    )

    return vectorstore