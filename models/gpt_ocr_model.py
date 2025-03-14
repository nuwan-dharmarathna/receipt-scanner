import openai
import os
import json
import base64
from fastapi import HTTPException

# Initialize OpenAI client
client = openai.OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def extract_transaction_details(image_bytes):
    """
    Extracts transaction details from a receipt image using OpenAI's GPT-4 Turbo Vision API.
    """
    
    # Convert image to Base64
    base64_image = base64.b64encode(image_bytes).decode("utf-8")

    # Call OpenAI API
    response = client.chat.completions.create(
        model="gpt-4-turbo",
        messages=[
            {"role": "system", "content": "You are an AI assistant that extracts structured transaction details from receipt images."},
            {"role": "user", "content": "Analyze the following receipt and categorize it as either 'income' or 'expense'. "
                                        "Extract the following details accurately:\n"
                                        "- **Transaction Type**: 'income' or 'expense'\n"
                                        "- **Description**: A short summary of the transaction.\n"
                                        "- **Category**: Choose from ['Groceries', 'Restaurants', 'Electricity', 'Water', "
                                        "'Internet', 'Fuel', 'Public Transport', 'Taxi', 'Rent', 'Salary', 'Business Income', "
                                        "'Loan', 'Gym', 'Insurance', 'Refunds', 'Other Income'].\n"
                                        "- **Amount**: The total amount in the receipt.\n"
                                        "- **Date**: The transaction date in YYYY-MM-DD format.\n\n"
                                        "If any field is missing or unclear, provide your best estimation."
            },
            {"role": "user", "content": [
                {"type": "text", "text": "Here's the receipt image:"},
                {"type": "image_url", "image_url": {"url": f"data:image/jpeg;base64,{base64_image}"}}
            ]}
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
        date = content.split("**Date**:")[1].split("\n")[0].strip()

        result = {
            "transactionType": transaction_type,
            "description": description,
            "category": category,
            "amount": float(amount),
            "date": date
        }

        return result

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to parse GPT response: {str(e)}")