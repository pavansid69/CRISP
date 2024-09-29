import re
from openai import OpenAI
import json
import os
from dotenv import load_dotenv
from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi

# Load environment variables
load_dotenv()

# MongoDB Configuration
db_password = os.getenv("db_password")
uri = f"mongodb+srv://svishnu1:{db_password}@cluster0.zdttw.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0"
client = MongoClient(uri, server_api=ServerApi('1'))
db = client["client_analysis"]  # Database name
collection_interactions = db["clientInteraction"]  # Source collection for client interactions
target_collection = db["dailysentiments"]  # Target collection for daily sentiment outputs

# OpenAI API Configuration
openai_client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def extract_json_from_response(response_text):
    """Extract and return the JSON content from the response text."""
    try:
        # Remove ```json markers or any other markdown formatting
        cleaned_response = re.sub(r'```(json)?', '', response_text).strip()
        # Attempt to parse the cleaned response as JSON
        return json.loads(cleaned_response)
    except json.JSONDecodeError as e:
        print(f"Failed to parse the extracted JSON. Error: {e}")
        print(f"Raw response: {response_text}")  # Print raw response for debugging
        return {"error": "Invalid JSON format", "raw_text": response_text}

def generate_gpt_input(client_data):
    """Format client interaction data for GPT input and save the output."""
    daily_sentiments = []  # Store daily sentiment summaries for the client
    for day in client_data["interactions"]:
        formatted_input = {
            "client_id": client_data["client_id"],
            "client_name": client_data.get("client_name", "Unknown"),
            "date": day["date"],
            "emails": [{"email_id": email["email_id"], "content": email["content"]} for email in day.get("emails", [])],
            "phone_calls": [{"call_id": call["call_id"], "notes": call["notes"]} for call in day.get("phone_calls", [])],
            "chats": [{"chat_id": chat["chat_id"], "message": chat["message"]} for chat in day.get("chats", [])]
        }

        # Generate the sentiment analysis output using GPT
        sentiment_output = analyze_interaction_with_gpt(formatted_input)

        # If sentiment_summary is present in the output, add it to daily_sentiments
        if "daily_sentiments" in sentiment_output and len(sentiment_output["daily_sentiments"]) > 0:
            daily_sentiments.append({
                "date": sentiment_output["daily_sentiments"][0]["date"],
                "sentiment_summary": sentiment_output["daily_sentiments"][0]["sentiment_summary"],
                "reason_for_sentiment": sentiment_output["daily_sentiments"][0].get("reason_for_sentiment", "No reason provided")
            })
        else:
            daily_sentiments.append({
                "date": formatted_input["date"],
                "sentiment_summary": {"error": "No summary generated"},
                "reason_for_sentiment": "No reason provided"
            })

    return daily_sentiments

def analyze_interaction_with_gpt(input_data):
    """Use ChatGPT to analyze interaction data and generate sentiment output."""
    # Create the structured prompt for ChatCompletion API using the new format
    gpt_prompt = f"""
    ### Instructions:
    You are given the daily client interaction logs for a financial services company. Analyze each interaction (emails, phone calls, and chats) and classify the sentiment as Positive, Neutral, or Negative based on the content of the message. Each sentiment should be strictly classified as "Positive," "Neutral," or "Negative" without using "Mixed" or other terms. Additionally, assign a numeric value to each sentiment:
    - Positive = 1
    - Neutral = 2
    - Negative = 3

    Once you have classified each individual interaction, generate a daily sentiment summary in the exact JSON structure below:

    ### Output Format:
    {{
      "client_id": "{input_data['client_id']}",
      "client_name": "{input_data['client_name']}",
      "daily_sentiments": [
        {{
          "date": "{input_data['date']}",
          "sentiment_summary": {{
            "emails": [
              {{ "email_id": "<Email ID>", "sentiment": "<Positive/Neutral/Negative>", "numeric_label": <1/2/3> }}
            ],
            "phone_calls": [
              {{ "call_id": "<Call ID>", "sentiment": "<Positive/Neutral/Negative>", "numeric_label": <1/2/3> }}
            ],
            "chats": [
              {{ "chat_id": "<Chat ID>", "sentiment": "<Positive/Neutral/Negative>", "numeric_label": <1/2/3> }}
            ],
            "overall_daily_sentiment": "<Positive/Neutral/Negative>",
            "overall_sentiment_numeric_label": <1/2/3>
          }},
          "reason_for_sentiment": "Provide a concise reason why the overall daily sentiment is classified as <Positive/Neutral/Negative>."
        }}
      ]
    }}
    
    Respond **only** with the JSON object and no extra explanations.
    
    ### Now, analyze the following data and generate the sentiment summary:
    {json.dumps(input_data, indent=4)}
    """

    response = openai_client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "You are a financial advisor analyzing client sentiment."},
            {"role": "user", "content": gpt_prompt}
        ]
    )

    raw_response = response.choices[0].message.content.strip()
    print(f"Raw response received: {raw_response}")  # Debugging: print the raw response
    return extract_json_from_response(raw_response)

# Fetch all client interactions for the initial phase
client_interactions = list(collection_interactions.find({}))
counter = 0

# Analyze interactions and insert each client's output into the `dailysentiments` collection
for client_data in client_interactions:
  if counter <1:
    counter += 1  # Increment counter to keep track of clients processed
    print(f"Processing client: {client_data['client_id']} - {client_data.get('client_name', 'Unknown')}")
    

    # Prepare the output for each client
    client_entry = {
        "client_id": client_data['client_id'],
        "client_name": client_data.get("client_name", "Unknown"),
        "daily_sentiments": generate_gpt_input(client_data)
    }

    # Insert the generated sentiment analysis into the `dailysentiments` collection
    target_collection.update_one(
        {"client_id": client_entry["client_id"]},  # Use client_id to match the document
        {"$set": client_entry},  # Set or update the document
        upsert=True  # Insert the document if it doesn't exist
    )
    print(f"Client {client_entry['client_id']} data inserted/updated in 'dailysentiments' collection.")
