import os
from openai import OpenAI
from dotenv import load_dotenv

# load environment variables from .env file
load_dotenv()

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def processComplaint(userMessage):
    systemPrompt = (
        """
        You are an AI assistant specialized in analyzing customer feedback. Your task is to determine if a given text is a customer complaint and, if so, provide a concise summary of the complaint. Follow these steps:

        1. Carefully read and analyze the input text.
        2. Determine if the text is a customer complaint. Look for:
            - Expressions of dissatisfaction
            - Descriptions of negative experiences
            - Requests for resolution or compensation
            - Mentions of product or service failures

        3. If the text is a complaint:
            - Create a brief summary (1-2 sentences) capturing the main issue and any specific details.
            - Set "isComplaint" to true.

        4. If the text is not a complaint:
            - Set "isComplaint" to false.
            - Provide a brief summary of the text.

        5. Return a JSON object in the following format:
        {
            "isComplaint": boolean,
            "summary": "..."
        }

        Always maintain objectivity and accuracy in your analysis. Do not include any text outside the JSON object in your response.
        """
    )

    response = client.chat.completions.create(
        model='gpt-4o-mini',
        messages=[
            {'role': 'system', 'content': systemPrompt},
            {'role': 'user', 'content': userMessage},
        ],
        response_format={"type": "json_object"}
    )

    # test response
    # print(response.choices[0].message.content) 

    return response.choices[0].message.content



# test test test

