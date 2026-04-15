import streamlit as st
from PIL import Image
import io
from generate import generate_image
from steganography import encode, decode
from stego_combined import generate_and_hide

st.set_page_config(page_title="ArtCrypt", page_icon="🔐", layout ="centered")
st.title("ArtCrypt: Generative Stegnographic Suite")
st.caption("Hide secret messages in AI-generated images")

tab1, tab2, tab3 = st.tabs(["🎨 Generate Image", "🔒 Steganography", "✨ Combined (Main)"])

with tab1:
    st.subheader("🎨 Generate Image from a Prompt")
    prompt = st.text_input("Enter your prompt", placeholder="A peaceful mountain lake at sunset")

    if st.button("Generate", key="gen"):
        if not prompt.strip():
            st.warning("Please enter a prompt to generate an image.")   
        else:
            with st.spinner("Generating image..."):
                try:
                    image = generate_image(prompt)
                    st.image(image, caption="Generated Image", use_container_width=True)
                    
                    buf = io.BytesIO()
                    image.save(buf, format='PNG')
                    st.download_button("Download Image", buf.getvalue(), "generated_image.png", "image/png")

                except Exception as e:
                    st.error(f"Error generating image: {e}")


with tab2:
    st.subheader("Hide or Reveal a Message in an Image")

    action = st.radio("What do you want to do?", ["Hide a message", "Reveal a message"])

    uploaded = st.file_uploader("Upload an image (PNG preferred)", type=["png", "jpg", "jpeg"])

    if action == "Hide a message":
        secret = st.text_area("Secret message to hide")
        password = st.text_input("Set a password (optional but recommended)", type="password")
        if st.button("Encode", key="enc") and uploaded and secret:
            img = Image.open(uploaded)
            with st.spinner("Hiding message..."):
                try:
                    result = encode(img, secret, password if password else None)
                    st.image(result, caption="Image with hidden message", use_container_width=True)
                    st.success("Message hidden successfully!")
                    buf = io.BytesIO()
                    result.save(buf, format="PNG")
                    st.download_button("Download Encoded Image", buf.getvalue(), "encoded.png", "image/png")
                except Exception as e:
                    st.error(f"Error: {e}")

    else:  # Reveal
        password = st.text_input("Enter password to decode (leave blank if none was set)", type="password")
        if st.button("Decode", key="dec") and uploaded:
            img = Image.open(uploaded)
            with st.spinner("Extracting message..."):
                message = decode(img, password if password else None)
                if "❌" in message:
                    st.error(message)
                else:
                    st.success("Message found!")
                    st.code(message)
    


with tab3:
    st.subheader("Generate an Image and Hide a Message Inside It")
    st.info("This is Art Crypt's core feature — generate a context-appropriate image and embed your secret message in it.")

    prompt = st.text_input("Describe the image", placeholder="A busy corporate meeting room", key="comb_prompt")
    message = st.text_area("Secret message to hide", key="comb_msg")
    password = st.text_input("Set a password to protect the message", type="password", key="comb_pass")

    if st.button("Generate & Hide", key="comb_btn"):
        if not prompt.strip() or not message.strip() or not password.strip():
            st.warning("Please fill in all three fields including the password.")
        else:
            with st.spinner("Generating image and hiding message..."):
                try:
                    img = generate_image(prompt)
                    result = encode(img, message, password)
                    st.image(result, caption="Your secret is protected and hidden", use_container_width=True)
                    st.success("Done! Only someone with the correct password can decode this.")
                    buf = io.BytesIO()
                    result.save(buf, format="PNG")
                    st.download_button("Download Final Image", buf.getvalue(), "art_crypt_output.png", "image/png")
                except Exception as e:
                    st.error(f"Error: {e}")