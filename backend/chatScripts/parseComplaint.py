import os
from openai import OpenAI
from dotenv import load_dotenv

# load environment variables from .env file
load_dotenv()

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def processComplaint(userMessage):
    systemPrompt = (
        "Your job is to determine if a call is a complaint. "
        "If it is a complaint, create a summary of the complaint. "
        "A complaint is defined as an expression of dissatisfaction or a report of a problem. "
        "If the message is not a complaint, respond with 'Not a complaint'. "
        "Examples of complaints: 'My credit card was charged twice for the same transaction.', "
        "'The product I received is defective and not working as expected.' "
        "Examples of non-complaints: 'I would like to know the status of my order.', "
        "'Can you help me with the product features?'"
    )

    response = client.chat.completions.create(
        model='gpt-4o-mini',
        messages=[
            {'role': 'system', 'content': systemPrompt},
            {'role': 'user', 'content': userMessage},
        ]
    )

    # test response
    # print(response.choices[0].message.content) 

    return response.choices[0].message.content

