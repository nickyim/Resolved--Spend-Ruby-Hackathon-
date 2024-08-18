from langchain_core.prompts import ChatPromptTemplate
from langchain_openai.chat_models import ChatOpenAI
from langchain_core.output_parsers import StrOutputParser
from langchain_pinecone import PineconeVectorStore
from langchain_core.runnables import RunnableParallel, RunnablePassthrough
from langchain_openai import OpenAIEmbeddings
from pinecone import Pinecone
import asyncio
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
PINECONE_API_KEY = os.getenv("PINECONE_API_KEY")

# Initialize OpenAI model
model = ChatOpenAI(openai_api_key=OPENAI_API_KEY, model="gpt-4-turbo-preview")

# Initialize output parser
parser = StrOutputParser()

# Define prompt template
template = """
You are a knowledgeable assistant, tasked with providing concise and relevant answers based on the context below. Use the following context to answer the user's question:

Context: {context}

User's Question: {question}

Instructions:
1. Begin your response with a natural, conversational opener such as "According to our database".
2. Directly address the user's question using insights from the provided context.
3. Highlight only the most relevant and important information related to the question.
4. Use a neutral, informative tone throughout your response.
5. If the context doesn't provide sufficient information to fully answer the question, acknowledge this and provide the best available information.
6. Provide additional context or background information if it helps in understanding the current event.
7. Do not use any styling like bold or italics. Keep format simple!
"""

prompt = ChatPromptTemplate.from_template(template)

# Initialize embeddings and Pinecone
embeddings = OpenAIEmbeddings(api_key=OPENAI_API_KEY)
pinecone = Pinecone(api_key=PINECONE_API_KEY)
index_name = "rubyhackcomplaints"

# Create PineconeVectorStore
vector_store = PineconeVectorStore(index_name=index_name, embedding=embeddings)

# Create retriever
retriever = vector_store.as_retriever(search_kwargs={"k": 11})

def get_relevant_articles(query):
    # Retrieve top articles based on the query
    results = retriever.get_relevant_documents(query)

    # Extract the text content from the results
    articles = [result.page_content for result in results]
    return "\n\n".join(articles)  # Join articles with double newlines for clarity

# Set up the chain
chain = (
    {
        "context": lambda x: get_relevant_articles(x["question"]),
        "question": RunnablePassthrough()
    }
    | prompt
    | model
    | parser
)

async def get_response(query):
    try:
        async for chunk in chain.astream({"question": query}):
            yield chunk
    except Exception as e:
        print(f"Error in get_response: {str(e)}")
        raise

if __name__ == "__main__":
    sample_query = "What is the general consensus of complaints associated with Macys and Citibank"
    
    async def main():
        async for response_chunk in get_response(sample_query):
            print(response_chunk, end="", flush=True)
        print()  # Add a newline at the end
    
    asyncio.run(main())