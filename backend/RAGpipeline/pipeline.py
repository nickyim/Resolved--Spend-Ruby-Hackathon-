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
model = ChatOpenAI(openai_api_key=OPENAI_API_KEY, model="gpt-4o-mini")

# Initialize output parser
parser = StrOutputParser()

# Define prompt template
template = """
You are an AI assistant specializing in analyzing and presenting complaint data. Your task is to provide concise, relevant, and factual responses based solely on the given context. Use the following information to address the user's query:

Context: {context}

User's Query: {question}

Instructions:
1. Begin your response with a neutral phrase such as "Based on the complaint data" or "The records indicate".
2. Directly address the user's query using specific information from the provided context.
3. Focus on presenting the most relevant facts, statistics, or trends related to the query.
4. Maintain an objective and analytical tone throughout your response.
5. If the context lacks sufficient information to fully answer the query, clearly state this limitation and provide the best available data.
6. Include relevant timeframes, frequencies, or patterns in the complaint data when applicable.
7. Refrain from overly lengthy responses.
8. Do not speculate beyond the provided data or make assumptions about causality unless explicitly stated in the context.
9. Use simple, clear language without any special formatting or styling.
10. Return responses in simple text with now bold, italyics, and or styling as point 9 indicated.
11. To reiterate Do not use markdown and templates that include '**' or '###'. Simple Text Only.
12. If appropriate, suggest related aspects of the complaint data that the user might find useful for a more comprehensive understanding.
13. Refrain from offering personal opinions or interpretations of the data.
14. Do not include any disclaimers or statements about the representativeness of the data or its limitations.
15. End your response after presenting the relevant information without adding any concluding remarks about the nature or scope of the complaints.
16. Remember points 12 and 13, I will provide disclaimers myself, that is not your job.
"""

prompt = ChatPromptTemplate.from_template(template)

# Initialize embeddings and Pinecone
embeddings = OpenAIEmbeddings(api_key=OPENAI_API_KEY)
pinecone = Pinecone(api_key=PINECONE_API_KEY)
index_name = "rubyhackcomplaints"
namespace = "complaints"

# Create PineconeVectorStore
vector_store = PineconeVectorStore.from_existing_index(
    index_name=index_name, 
    namespace=namespace, 
    embedding=embeddings
)

# Create retriever
retriever = vector_store.as_retriever(search_kwargs={"k": 50})

# Check the number of vectors in the Pinecone index
# index_stats = pinecone.describe_index(index_name)
# print(f"\nIndex stats: {index_stats}\n")

pc = Pinecone(api_key=PINECONE_API_KEY)
index = pc.Index("rubyhackcomplaints")

print('\n decribe the index stats',index.describe_index_stats(), '\n')

def get_relevant_articles(query):
    # Retrieve top articles based on the query
    results = retriever.invoke(query)

    # print(f"\nRaw Pinecone response: {results}\n")

    # print(f"\nRetrieved {len(results)} articles for the query: {query}\n")

    # Print the structure of the first result to debug
    if results:
        print(f"First result structure: {results[0]}\n")

    # Extract the text content from the results
    articles = [result.page_content for result in results]

    # print(f"Extracted text content from the articles:\n{articles}\n")

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

def get_response(query):
    try:
        for chunk in chain.stream({"question": query}):
            # print(f"\nChunk: {chunk}", flush=True)
            yield chunk
    except Exception as e:
        print(f"Error in get_response: {str(e)}")
        raise


# sample_query = "What is the general consensus of complaints associated with Macys and Citibank"

# # Call get_response and print each chunk
# for response_chunk in get_response(sample_query):
#     print(response_chunk)
