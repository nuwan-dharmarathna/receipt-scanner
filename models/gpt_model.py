import openai
import json
import os
from fastapi import HTTPException
from config import OPENAI_API_KEY

# Initialize OpenAI client
client = openai.OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def extract_transaction_details(text):
    """
    Extracts transaction details from a text using OpenAI's GPT-4.
    """

    # Call OpenAI API
    response = client.chat.completions.create(
    model="gpt-4-turbo",
    messages=[
        {"role": "system", "content": "You are an AI assistant that extracts structured transaction details from the given text."},
            {"role": "user", "content": "Analyze the following text and categorize it as either 'income' or 'expense'. "
                                        "Extract the following details accurately:\n"
                                        "- **Transaction Type**: 'income' or 'expense'\n"
                                        "- **Description**: A short summary of the transaction.\n"
                                        "- **Category**: Choose from ['Groceries', 'Restaurants', 'Electricity', 'Water', "
                                        "'Internet', 'Fuel', 'Public Transport', 'Taxi', 'Rent', 'Salary', 'Business Income', "
                                        "'Loan', 'Gym', 'Insurance', 'Refunds', 'Other Income'].\n"
                                        "- **Amount**: The total amount mentioned in the text.\n"
                                        "If any field is missing or unclear, provide your best estimation."
            },
        {
            "role": "user",
            "content": "Analyze the following text and categorize it as either 'income' or 'expense'. Extract the following details accurately:\n\n"
                       "- **Transaction Type**: 'income' or 'expense'\n"
                       "- **Description**: A short summary of the transaction.\n"
                       "- **Category**: ['Groceries', 'Restaurants', 'Electricity', 'Water', 'Internet', 'Fuel', 'Public Transport', 'Taxi', 'Rent', 'Salary', 'Business Income', 'Loan', 'Gym', 'Insurance', 'Refunds', 'Other Income']\n"
                       "- **Amount**: The total amount.Remove all alphabet charactors and provide only the numerical value in float datatype.\n"
                       "If any field is missing, provide your best estimation."
        },
        {
            "role": "assistant",
            "content": f"Here's the text extracted from the receipt: {text}"
        }
    ],
    max_tokens=300
    )
    
    print(f"Raw GPT Response: {response}")  # Log the raw response
    
    # Check if the response is empty
    if not response:
        raise HTTPException(status_code=500, detail="GPT response is empty")

    # Extract the content from the response
    content = response.choices[0].message.content
    print(f"Extracted Content: {content}")  # Log the extracted content

    # Parse the content to extract JSON-like structure
    # Assuming the content is in a format that can be easily parsed
    # You might need to adjust this part depending on the exact format of the content
    try:
        # Example parsing logic (adjust as needed)
        transaction_type = content.split("**Transaction Type**:")[1].split("\n")[0].strip().strip("'")
        description = content.split("**Description**:")[1].split("\n")[0].strip()
        category = content.split("**Category**:")[1].split("\n")[0].strip().strip("'")
        amount = content.split("**Amount**:")[1].split("\n")[0].strip().replace(",", "")

        result = {
            "transactionType": transaction_type,
            "description": description,
            "category": category,
            "amount": float(amount)
        }

        return result

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to parse GPT response: {str(e)}")