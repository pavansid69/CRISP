
from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi
import os
from dotenv import load_dotenv

load_dotenv()

db_password = os.getenv("db_password")


# Send a ping to confirm a successful connection
# MongoDB Configuration
from pymongo import MongoClient
import json
import os
from dotenv import load_dotenv

# Load environment variables from .env
load_dotenv()

# MongoDB Configuration
db_password = os.getenv("db_password")

from pymongo import MongoClient
import os
from dotenv import load_dotenv

# Load environment variables from .env
load_dotenv()

# MongoDB Configuration
db_password = os.getenv("db_password")

# MongoDB URI with optional TLS flag for certificate validation
uri = f"mongodb+srv://svishnu1:{db_password}@cluster0.zdttw.mongodb.net/?retryWrites=true&w=majority&tlsAllowInvalidCertificates=true"
client = MongoClient(uri)

# Specify the database and collections
db = client["client_analysis"]  # Use the client_analysis database
source_collection = db["client_interaction"]  # Source collection
target_collection = db["clientInteraction"]  # Target collection

# Fetch all documents from the source collection
source_documents = list(source_collection.find())

# Insert the documents into the target collection
if source_documents:
    # Optional: Remove the "_id" field to prevent duplicate key errors if re-inserting
    for doc in source_documents:
        if "_id" in doc:
            del doc["_id"]

    # Insert documents into the target collection
    result = target_collection.insert_many(source_documents)
    print(f"Successfully inserted {len(result.inserted_ids)} documents into '{target_collection.name}' collection.")
else:
    print(f"No documents found in the '{source_collection.name}' collection.")

# Optional: Save the source collection data as a JSON file for backup or reference
output_file = "client_interaction_export.json"
with open(output_file, "w") as file:
    json.dump(source_documents, file, indent=4, default=str)

print(f"Source collection '{source_collection.name}' has been exported successfully to '{output_file}'.")
