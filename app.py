from flask import Flask, request, jsonify, abort
from transformers import AutoModelForTokenClassification, AutoTokenizer, pipeline
import logging
from dotenv import load_dotenv 
import os

load_dotenv()

# Initialize Flask app
app = Flask(__name__)

# Authentication Credentials
USERNAME = os.getenv("USERNAME")
PASSWORD = os.getenv("PASSWORD")

# Load the trained model and tokenizer
model_path = "anirudh333/ner-model"
tokenizer = AutoTokenizer.from_pretrained(model_path)
model = AutoModelForTokenClassification.from_pretrained(model_path)

# Define proper BIO mapping for NER tags
BIO_LABELS = {
    "LABEL_0": "O",
    "LABEL_1": "PERSON - BEGINNING",
    "LABEL_2": "PERSON - INSIDE",
    "LABEL_3": "ORGANIZATION - BEGINNING",
    "LABEL_4": "ORGANIZATION - INSIDE",
    "LABEL_5": "LOCATION - BEGINNING",
    "LABEL_6": "LOCATION - INSIDE",
    "LABEL_7": "MISCELLANEOUS - BEGINNING",
    "LABEL_8": "MISCELLANEOUS - INSIDE"
}

# Create the NER pipeline with simple aggregation
ner_pipeline = pipeline("ner", model=model, tokenizer=tokenizer, aggregation_strategy="simple")


# Configure logging
logging.basicConfig(level=logging.INFO)

@app.route("/", methods=["GET"])
def home():
    return jsonify({"message": "NER API is running"}), 200

def authenticate():
    """Check for Basic Authentication"""
    auth = request.authorization
    if not auth or auth.username != USERNAME or auth.password != PASSWORD:
        abort(401, description="Unauthorized access")

@app.route("/predict", methods=["POST"])
def predict():
    # Require authentication
    authenticate()  # This will abort if authentication fails

    try:
        # Ensure request is in JSON format
        data = request.get_json()
        if not data or "text" not in data:
            return jsonify({"error": "Missing 'text' field in JSON request"}), 400
        
        text = data["text"]
        print(text)
        entities = ner_pipeline(text)
        print(entities)
        # Convert entity labels and ensure float serialization
        formatted_entities = [
            {
                "entity": BIO_LABELS.get(ent["entity_group"], "UNKNOWN"),  # Map labels
                "word": ent["word"],
                "score": float(ent["score"]), 
                "start": ent["start"],
                "end": ent["end"]
            }
            for ent in entities
        ]

        logging.info(f"Processed Text: {text}")
        logging.info(f"Entities Extracted: {formatted_entities}")

        return jsonify({"entities": formatted_entities}), 200
    except Exception as e:
        logging.error(f"Error: {str(e)}")
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8000))
    app.run(host="0.0.0.0", port=port, debug=True)