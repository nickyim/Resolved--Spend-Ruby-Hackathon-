import os
from openai import OpenAI
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def classifyProduct(annotations_text):
    """
    Classifies the product and sub-product categories based on the provided text
    using the OpenAI API. Specifically tailored to detect and categorize complaints
    related to various services and products.
    """
    systemPrompt = (
        """
        You are an AI assistant specialized in analyzing and categorizing customer complaints. 
        Your task is to determine the most appropriate product and sub-product categories 
        based on the provided text, which could be extracted from various sources 
        (e.g., voice calls, text documents, video transcripts).

        1. Carefully read and analyze the input text, which may describe issues, complaints, 
           or feedback related to different products or services.
        2. Identify if the text refers to a specific product or service category 
           (e.g., "Retail", "Banking", "Telecommunications").
        3. Further classify the text into a sub-product category (e.g., "Credit Card", 
           "Online Order", "Mobile Service").
        4. Return a JSON object in the following format:
        {
            "product": "Product Category",
            "subProduct": "Sub-Product Category"
        }

        Examples of product categories include:
        - "Retail"
        - "Banking"
        - "Telecommunications"
        - "Insurance"
        - "Healthcare"

        Examples of sub-product categories include:
        - "Online Order"
        - "Credit Card"
        - "Mobile Service"
        - "Health Insurance"
        - "Prescription Medication"

        Always ensure that your classifications are accurate and relevant to the content.
        """
    )

    response = client.chat.completions.create(
        model='gpt-4o-mini',
        messages=[
            {'role': 'system', 'content': systemPrompt},
            {'role': 'user', 'content': annotations_text},
        ]
    )

    return response.choices[0].message.content

# Example usage
annotations_text = """
The customer is upset because their credit card was charged twice for the same transaction 
at Macy's, and they are struggling to get a refund from Chase.
"""
classification_result = classifyProduct(annotations_text)
print(classification_result)
