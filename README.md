# 🔐 Art Crypt - Generative Steganographic Suite

Art Crypt is a Python-based web application that combines **Generative AI**, **Steganography**, and **Cryptography** to enable secure and covert communication.

## 🚀 Features

-  AI Image Generation using Hugging Face (FLUX.1-schnell)
-  AES-256-CBC Encryption
-  PBKDF2 Key Derivation
-  LSB Steganography
-  Streamlit Web Interface

## ⚙️ Modules

- generate.py → AI Image generation
- steganography.py → LSB encode/decode
- crypto_utils.py → AES encryption/decryption
- stego_combined.py → Full pipeline
- app.py → Streamlit UI

## 🛠️ Installation

```bash
git clone https://github.com/YOUR_USERNAME/art-crypt.git
cd art-crypt
pip install -r requirements.txt
streamlit run app.py
