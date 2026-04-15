import requests
import streamlit as st 
from PIL import Image
import io
from dotenv import load_dotenv

load_dotenv()

HF_API_KEY = st.secrets["HF_API_KEY"]
MODEL_URL = "https://router.huggingface.co/hf-inference/models/black-forest-labs/FLUX.1-schnell"

def generate_image(prompt: str) -> Image.Image:
    headers = {"Authorization": f"Bearer {HF_API_KEY}"}
    payload = {"inputs": prompt}

    response = requests.post(MODEL_URL, headers=headers, json=payload)

    if response.status_code != 200:
        raise Exception(f"API Error: {response.status_code} : {response.text}")
    
    return Image.open(io.BytesIO(response.content))
