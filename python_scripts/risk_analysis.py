import re
from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi
from openai import OpenAI
import json
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# MongoDB Configuration
db_password = os.getenv("db_password")
uri = f"mongodb+srv://svishnu1:{db_password}@cluster0.zdttw.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0"
client = MongoClient(uri, server_api=ServerApi('1'))
db = client["client_analysis"]  # Database name
portfolio_collection = db["portfolios"]  # Portfolio collection for clients
risk_collection = db["dailyrisks"]  # Output collection to store risk assessments

# OpenAI API Configuration
openai_client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

# Helper Functions
def calculate_daily_volatility(daily_changes):
    """Calculate daily percentage changes in the portfolio value."""
    daily_volatility = []
    previous_value = None

    for change in daily_changes:
        date = change["date"]

        # Safely extract the portfolio value as an integer
        if isinstance(change["portfolio_value"], dict) and "$numberInt" in change["portfolio_value"]:
            portfolio_value = int(change["portfolio_value"]["$numberInt"])  # Extract the value if it's in dict format
        else:
            portfolio_value = change["portfolio_value"]  # Already an integer

        if previous_value is not None:
            # Calculate daily change percent: (current_value - previous_value) / previous_value * 100
            daily_change_percent = round(((portfolio_value - previous_value) / previous_value) * 100, 2)
            daily_volatility.append({"date": date, "daily_change_percent": daily_change_percent})
        else:
            # Use 0 for the first day since we can't compute daily change without a previous value
            daily_volatility.append({"date": date, "daily_change_percent": 0.0})

        previous_value = portfolio_value

    return daily_volatility
def assess_performance_trends(daily_changes):
    """Analyze the profit/loss trends over time."""
    trends = []
    for change in daily_changes:
        date = change["date"]
        
        # Safely extract the profit/loss value
        if isinstance(change["profit_loss"], dict) and "$numberInt" in change["profit_loss"]:
            profit_loss = int(change["profit_loss"]["$numberInt"])  # Extract the value if it's in dict format
        else:
            profit_loss = change["profit_loss"]  # Already an integer

        trends.append({"date": date, "profit_loss": profit_loss})

    # Check the trend direction
    trend_message = "The portfolio shows steady growth with minor fluctuations."
    first_loss = trends[0]["profit_loss"]
    last_loss = trends[-1]["profit_loss"]
    if last_loss > first_loss:
        trend_message = "The portfolio is trending upwards."
    elif last_loss < first_loss:
        trend_message = "The portfolio is showing signs of decline."
    else:
        trend_message = "The portfolio's performance is stable without significant changes."

    return trends, trend_message

def generate_risk_score(volatility, trends):
    """Generate a risk score based on volatility and trends."""
    # Calculate average daily volatility
    avg_volatility = sum([day["daily_change_percent"] for day in volatility]) / len(volatility)
    
    # Calculate the trend change as the overall profit/loss change over the period
    profit_changes = [t["profit_loss"] for t in trends]
    trend_score = profit_changes[-1] - profit_changes[0]

    # Use a weighted sum to compute the final risk score
    risk_score = round((avg_volatility * 0.6) + (abs(trend_score) * 0.4), 2)

    # Determine the risk level based on the score
    if risk_score < 30:
        risk_level = "Low Risk"
    elif risk_score < 60:
        risk_level = "Moderate Risk"
    else:
        risk_level = "High Risk"

    return risk_score, risk_level

def risk_assessment(client_id, daily_changes):
    """Generate a complete risk analysis for a client's portfolio."""
    # Step 1: Calculate daily volatility
    daily_volatility = calculate_daily_volatility(daily_changes)

    # Step 2: Assess performance trends
    trends, trend_message = assess_performance_trends(daily_changes)

    # Step 3: Generate risk score and risk level
    risk_score, risk_level = generate_risk_score(daily_volatility, trends)

    # Step 4: Create suggested actions based on risk level
    suggested_actions = []
    if risk_level == "High Risk":
        suggested_actions.append("Diversify the portfolio to reduce dependence on a few assets.")
        suggested_actions.append("Consider moving a portion of the portfolio to safer assets.")
    elif risk_level == "Moderate Risk":
        suggested_actions.append("Monitor the primary stock more closely to mitigate unexpected drops.")
        suggested_actions.append("Consider locking in profits periodically to reduce risk.")
    else:
        suggested_actions.append("The portfolio is stable. No immediate action required.")
    
    # Create the final risk analysis output
    risk_analysis_output = {
        "client_id": client_id,
        "date": daily_changes[-1]["date"],
        "risk_analysis": {
            "risk_score": risk_score,
            "risk_level": risk_level,
            "daily_volatility": daily_volatility,
            "trend_analysis": trend_message,
            "suggested_actions": suggested_actions
        }
    }

    return risk_analysis_output

# Process All Clients in the Portfolio Collection
all_clients = list(portfolio_collection.find({}))
counter = 0
for client_data in all_clients:
    if counter <1:
        counter +=1
        client_id = client_data["client_id"]
        daily_changes = client_data.get("daily_changes", [])
        
        # If daily changes are present, perform risk assessment
        if daily_changes:
            risk_output = risk_assessment(client_id, daily_changes)
            
            # Save the risk assessment to the `daily_portfolio_risk` collection
            risk_collection.update_one({"client_id": client_id}, {"$set": risk_output}, upsert=True)
            
            print(f"Risk analysis completed for {client_id}.")
        else:
            print(f"No daily changes found for {client_id}. Skipping...")
    else:
        break

print("Risk analysis completed!")
