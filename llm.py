import os
from dotenv import load_dotenv
from langchain_groq import ChatGroq


load_dotenv()


llm = ChatGroq(
    model="openai/gpt-oss-20b",
    groq_api_key=os.getenv("GROQ_API_KEY"),
    temperature=0.2
)


def generate_answer(context, question):

    prompt = f"""
You are a helpful PDF assistant.

Answer the question using only the provided context.

Context:
{context}

Question:
{question}

Answer:
"""

    response = llm.invoke(prompt)

    return response.content