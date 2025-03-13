# NER API & Streamlit UI Project

## Overview

This project implements a Named Entity Recognition (NER) service using a fine-tuned BERT model. It exposes a REST API built with Flask that processes text inputs and returns recognized entities with their labels and scores. A complementary Streamlit web application serves as a user-friendly interface to interact with the API. Additionally, a Dockerfile is provided for containerization, making deployment straightforward.

## Repository Structure

```
ner-project/
├── app.py                  # Flask API for NER
├── streamlit_app.py        # Streamlit UI to interact with the API
├── Dockerfile              # Dockerfile to containerize the application
├── requirements.txt        # List of required Python packages
├── README.md               # Detailed project documentation
└── .gitignore              # Git ignore file for unnecessary files (e.g., __pycache__, env folders)
```

> **Tip:** You might also add additional folders if needed (e.g., `models/` for your saved model files, `tests/` for test scripts, or `docs/` for further documentation).

## Features

- **NER API:** Exposes endpoints to perform Named Entity Recognition on input text.
- **Streamlit Interface:** A simple web UI to test and interact with the API.
- **Authentication:** Basic HTTP authentication is implemented for secure API access.
- **Docker Support:** Containerize the application for consistent deployment across environments.

## Technologies Used

- **Flask:** For creating the RESTful API.
- **Transformers (Hugging Face):** To load and run the pre-trained BERT model for NER.
- **Streamlit:** For building the interactive web application.
- **Docker:** For containerizing the app.
- **Python:** Primary programming language.

## Getting Started

### Prerequisites

- **Python 3.7+**
- **pip** (Python package manager)
- **Docker** (optional, for containerization)

### Installation

1. **Clone the Repository:**

   ```bash
   git clone https://github.com/your_username/ner-project.git
   cd ner-project
   ```

2. **Create and Activate a Virtual Environment (Optional):**

   ```bash
   python -m venv venv
   source venv/bin/activate   # On Windows: venv\Scripts\activate
   ```

3. **Install Dependencies:**

   Ensure you have a `requirements.txt` file. An example might look like:

   ```txt
   Flask
   transformers
   torch  # or tensorflow if using that backend
   streamlit
   requests
   ```

   Then run:

   ```bash
   pip install -r requirements.txt
   ```

### Running the Application

#### Flask API

1. **Start the API server:**

   ```bash
   python app.py
   ```

2. **API Endpoints:**

   - **GET /**: Health check endpoint. Returns a message confirming the API is running.
   - **POST /predict**: Accepts JSON with a `"text"` field. Returns recognized entities along with their entity types, confidence scores, and text positions.
   - **Authentication:** This endpoint requires basic authentication. The default credentials are:
     - **Username:** `admin`
     - **Password:** `password123`
     
     You can change these in `app.py` as needed.

#### Streamlit UI

1. **Run the Streamlit application in a separate terminal:**

   ```bash
   streamlit run streamlit_app.py
   ```

2. **Usage:**
   
   - Enter the text you want to analyze in the provided text area.
   - Click **"Analyze"** to send a request to the API.
   - The recognized entities will be displayed on the page.

### Docker Instructions

1. **Build the Docker Image:**

   ```bash
   docker build -t ner-api .
   ```

2. **Run the Docker Container:**

   ```bash
   docker run -p 8000:8000 ner-api
   ```

   > **Note:** When running in Docker, adjust the API URL in `streamlit_app.py` if needed.

## Model and Authentication Details

- **Model Loading:** The API loads a BERT model from the directory specified by `model_path` in `app.py` (e.g., `"bert_ner_model"`). Ensure your trained model and tokenizer are correctly saved in this path.
- **Entity Mapping:** The model uses a BIO tagging scheme. The mapping is defined in the `BIO_LABELS` dictionary to convert model labels to human-readable entity names.
- **Authentication:** Basic authentication is required for the `/predict` endpoint to prevent unauthorized access.