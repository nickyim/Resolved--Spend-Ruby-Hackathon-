import os
import json
from openai import OpenAI
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def classifyProductandSummarize(annotations_text):
    """
    Classifies the product and sub-product categories based on the provided text
    using the OpenAI API. Additionally, generates a summary and determines if the 
    text is a complaint.
    """
    systemPrompt = (
        """
        You are an AI assistant specialized in analyzing and categorizing customer complaints. 
        Your task is to determine if the provided text is a complaint and to classify the 
        product and sub-product categories accordingly. Follow these steps:

        1. Carefully read and analyze the input text, which may describe issues, complaints, 
           or feedback related to different products or services.
        2. Determine if the text is a customer complaint. Look for:
            - Expressions of dissatisfaction
            - Descriptions of negative experiences
            - Requests for resolution or compensation
            - Mentions of product or service failures
        3. If the text is a complaint:
            - Set "isComplaint" to true.
            - Create a brief summary (1-2 sentences) capturing the main issue and any specific details.
            - Suggest a product category (e.g., "Bank Account", "Credit Card") and a sub-product category 
              (e.g., "Checking", "Balance Transfer") based on the content.
        4. If the text is not a complaint:
            - Set "isComplaint" to false.
            - Provide a brief summary of the text.
        5. Return a JSON object in the following format:
        {
            "isComplaint": boolean,
            "summary": "Summary of the text",
            "product": "Product Category",
            "subProduct": "Sub-Product Category"
        }

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

    # Parse the response content into a JSON object and return it
    return json.loads(response.choices[0].message.content)

# Example usage
annotations_text = """
The customer is upset because their credit card was charged twice for the same transaction 
at Macy's, and they are struggling to get a refund from Chase.
"""
classification_result = classifyProductandSummarize(annotations_text)
print(classification_result)
