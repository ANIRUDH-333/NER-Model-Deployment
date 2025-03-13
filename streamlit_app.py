import streamlit as st
import requests
from requests.auth import HTTPBasicAuth
from dotenv import load_dotenv 
import os

load_dotenv()

# Streamlit UI
st.title("NER Entity Recognition")

# Input text
text_input = st.text_area("Enter text for NER")

# Button to send request
if st.button("Analyze"):
    if text_input:
        # Define API endpoint
        api_url = "https://ner-model-deployment.onrender.com/predict"  # Update if deployed

        # Authentication
        auth = HTTPBasicAuth(os.getenv("USERNAME"), os.getenv("PASSWORD"))

        # Send request
        response = requests.post(api_url, json={"text": text_input}, auth=auth)

        # Process response
        if response.status_code == 200:
            entities = response.json().get("entities", [])

            if entities:
                st.success("Entities extracted successfully!")

                # Display entities as "word : entity"
                for entity in entities:
                    st.write(f"**{entity['word']}** : {entity['entity']}")
            else:
                st.warning("No entities found.")
        else:
            st.error(f"Error: {response.status_code} - {response.text}")
    else:
        st.warning("Please enter text before analyzing.")