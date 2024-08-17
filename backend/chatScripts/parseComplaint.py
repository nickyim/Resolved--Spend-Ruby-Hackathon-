import os
from openai import OpenAI
from dotenv import load_dotenv

# load environment variables from .env file
load_dotenv()

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def understandCall (userMessage):
    systemPrompt = 'You are using a chatbot to help you with your complaint. Please describe your complaint in detail. The chatbot will ask you questions to help you provide more information.'

    response = client.chat.completions.create(
        model='gpt-4o-mini',
        messages=[
            {'role': 'system', 'content': systemPrompt},
            {'role': 'user', 'content': userMessage},
        ]
    )

    print(response.choices[0].message.content)

    return response.choices[0].message.content

if __name__ == "__main__":
    user_input = 'My credit card was charged twice for the same transaction.'
    understandCall(user_input)