from pymongo.mongo_client import MongoClient # type: ignore
from pymongo.server_api import ServerApi # type: ignore
from openai import OpenAI # type: ignore
import json
import os
from dotenv import load_dotenv # type: ignore

# Load environment variables
load_dotenv()

# MongoDB Configuration
db_password = os.getenv("db_password")
uri = f"mongodb+srv://svishnu1:{db_password}@cluster0.zdttw.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0"
client = MongoClient(uri, server_api=ServerApi('1'))
db = client["client_analysis"]  # Database name

# Collections
risk_collection = db["dailyrisks"]  # Collection with daily risk assessments
sentiment_collection = db["dailysentiments"]  # Collection with daily sentiment assessments
satisfaction_collection = db["clientSatisfaction"]  # Output collection for client satisfaction

# OpenAI API Configuration
openai_client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def generate_gpt_input(client_id, client_name, risk_data, sentiment_data):
    """Create a structured prompt using the risk and sentiment data."""
    prompt = f"""
    ### Instructions:
    You are provided with the daily risk assessment and sentiment analysis for a financial services client. Your goal is to analyze both sources of data to produce an overall client satisfaction score for the given period.

    ### Satisfaction Levels:
    - Very Satisfied = 1
    - Satisfied = 2
    - Neutral = 3
    - Dissatisfied = 4
    - Very Dissatisfied = 5

    Consider both the daily risk score and sentiment values when determining overall satisfaction. Higher risk and negative sentiment trends generally lead to lower satisfaction, while lower risk and positive sentiment trends indicate higher satisfaction. 

    ### Output Format:
    {{
      "client_id": "{client_id}",
      "client_name": "{client_name}",
      "overall_satisfaction_score": "<Overall Satisfaction Score between 0 and 100>",
      "satisfaction_level": "<Satisfied Client/At Risk of Disengagement/High-Priority Client>",
      "numerical_satisfaction_level": "<1/2/3/4/5>",
      "reasons_for_satisfaction": [
        "<Reason 1>",
        "<Reason 2>"
      ]
    }}
    
    ### Input Data:
    #### Risk Data:
    {json.dumps(risk_data, indent=4)}

    #### Sentiment Data:
    {json.dumps(sentiment_data, indent=4)}
    
    ### Now, analyze the provided data and generate the client satisfaction score.
    Only return the response in the JSON format as shown in the output format above.
    """

    return prompt

def sanitize_satisfaction_result(satisfaction_result):
    """Sanitize the satisfaction result to ensure correct numeric values."""
    try:
        # Check if "overall_satisfaction_score" is a string, and convert to float
        if isinstance(satisfaction_result.get("overall_satisfaction_score"), str):
            satisfaction_result["overall_satisfaction_score"] = float(satisfaction_result["overall_satisfaction_score"])
    except ValueError:
        satisfaction_result["overall_satisfaction_score"] = 0.0  # Default to 0.0 if conversion fails

    try:
        # Check if "numerical_satisfaction_level" is a string, and convert to int
        if isinstance(satisfaction_result.get("numerical_satisfaction_level"), str):
            satisfaction_result["numerical_satisfaction_level"] = int(satisfaction_result["numerical_satisfaction_level"])
    except ValueError:
        satisfaction_result["numerical_satisfaction_level"] = 3  # Default to neutral if conversion fails

    return satisfaction_result

def extract_valid_json(raw_response):
    """Extract and format the JSON content from the GPT response, handling extra formatting."""
    try:
        # Locate the first occurrence of a curly brace to find the JSON start
        json_start = raw_response.find("{")
        json_end = raw_response.rfind("}") + 1  # Locate the last closing curly brace
        if json_start != -1 and json_end != -1:
            return raw_response[json_start:json_end]
        else:
            return raw_response
    except Exception as e:
        print(f"Error extracting JSON: {e}")
        return raw_response

def analyze_overall_satisfaction(client_id, client_name, risk_data, sentiment_data):
    """Generate the overall satisfaction score using GPT."""
    # Generate the GPT input prompt
    gpt_prompt = generate_gpt_input(client_id, client_name, risk_data, sentiment_data)

    # Call the GPT model to generate satisfaction output
    response = openai_client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "You are an AI financial analyst."},
            {"role": "user", "content": gpt_prompt}
        ]
    )

    raw_response = response.choices[0].message.content.strip()
    print(f"Raw GPT Response for {client_id}: {raw_response}")  # Debugging: Print raw response

    # Extract valid JSON from the raw response
    extracted_json = extract_valid_json(raw_response)

    # Attempt to parse the response as JSON
    try:
        satisfaction_result = json.loads(extracted_json)
        # Sanitize and ensure correct value types in the satisfaction result
        satisfaction_result = sanitize_satisfaction_result(satisfaction_result)
    except json.JSONDecodeError:
        print(f"Failed to parse the GPT response for {client_id}. Returning raw text.")
        satisfaction_result = {"client_id": client_id, "error": "Invalid response format", "raw_text": raw_response}

    return satisfaction_result

def update_client_satisfaction():
    """Update the client_satisfaction table with overall satisfaction scores."""
    # Get all client IDs from the daily_risk collection
    clients = list(risk_collection.find({}))
    counter = 0
    for client_data in clients:
        if counter <1:
            counter +=1
            client_id = client_data["client_id"]

            print(f"\nProcessing Client: {client_id}")

            # Retrieve the latest risk data for the client
            risk_data = risk_collection.find_one({"client_id": client_id})
            print(f"Risk Data for {client_id}: {risk_data}")

            # Retrieve the latest sentiment data for the client
            sentiment_data = sentiment_collection.find_one({"client_id": client_id})
            print(f"Sentiment Data for {client_id}: {sentiment_data}")

            if risk_data and sentiment_data:
                # Use 'daily_sentiments' to pass the sentiment data structure
                client_name = sentiment_data.get("client_name", "Unknown Client")
                satisfaction_result = analyze_overall_satisfaction(client_id, client_name, risk_data["risk_analysis"], sentiment_data["daily_sentiments"])

                # Store the satisfaction result in the client_satisfaction collection
                satisfaction_collection.update_one(
                    {"client_id": client_id}, 
                    {"$set": satisfaction_result}, 
                    upsert=True
                )
                print(f"Client satisfaction updated for {client_id}.")
            else:
                print(f"Risk or sentiment data missing for {client_id}. Skipping...")
        else:
            break

    print("Overall satisfaction update completed.")

# Run the client satisfaction update function
update_client_satisfaction()
