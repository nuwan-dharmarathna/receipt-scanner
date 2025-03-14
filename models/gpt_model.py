import openai
import json
import os
from fastapi import HTTPException
from config import OPENAI_API_KEY

openai.api_key = OPENAI_API_KEY

async def analyze_receipt(ocr_data):
    print(f"OCR Result: {ocr_data}")
    
    prompt = f"""
    Analyze the following receipt and categorize it as either 'income' or 'expense'. 
    Extract the following details accurately:
    - **Transaction Type**: 'income' or 'expense'
    - **Description**: A short summary of the transaction.
    - **Category**: Choose from ['Groceries', 'Restaurants', 'Electricity', 'Water', 'Internet', 'Fuel', 'Public Transport', 'Taxi', 'Rent', 'Salary', 'Business Income', 'Loan', 'Gym', 'Insurance', 'Refunds', 'Other Income'].
    - **Amount**: The total amount in the receipt.
    - **Date**: The transaction date in YYYY-MM-DD format.

    If any field is missing or unclear, provide your best estimation. Do not return unknown fields.

    Receipt:
    ```
    {ocr_data}
    ```

    Return the result as a JSON object with keys: 'transactionType', 'description', 'category', 'amount', and 'date'.
    Ensure the response is only a JSON object and does not include any additional text.
    """

    try:
        # Call OpenAI API
        response = openai.chat.completions.create(
            model="gpt-4",
            messages=[
                {"role": "system", "content": "You are an assistant for financial transaction analysis."},
                {"role": "user", "content": prompt}
            ]
        )

        # Extract the response content
        gpt_output = response.choices[0].message.content
        print(f"Raw GPT Response: {gpt_output}")  # Log the raw response

        # Check if the response is empty
        if not gpt_output:
            raise HTTPException(status_code=500, detail="GPT response is empty")

        # Extract JSON part from the response
        start_index = gpt_output.find('{')
        end_index = gpt_output.rfind('}') + 1

        if start_index == -1 or end_index == 0:
            raise HTTPException(status_code=500, detail="No JSON object found in GPT response")

        json_str = gpt_output[start_index:end_index]
        print(f"Extracted JSON: {json_str}")  # Log the extracted JSON

        # Parse the JSON
        return json.loads(json_str)
        
    except Exception as e:
        print(f"Error: {str(e)}")  # Log the error
        raise HTTPException(status_code=500, detail=f"Failed to process GPT response: {str(e)}")