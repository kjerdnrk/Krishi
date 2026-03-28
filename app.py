import streamlit as st
from PIL import Image
import numpy as np
from ultralytics import YOLO

# Load model
model = YOLO("best (1).pt")

st.title("🌱 Krishi Rakshak - AI Disease Detection")

uploaded_file = st.file_uploader("Upload Plant Image", type=["jpg", "png", "jpeg"])

if uploaded_file:
    image = Image.open(uploaded_file)
    st.image(image, caption="Uploaded Image", use_column_width=True)

    img = np.array(image)

    results = model(img)

    probs = results[0].probs.data.tolist()
    names = results[0].names

    pred_class = results[0].probs.top1
    confidence = probs[pred_class] * 100
    class_name = names[pred_class]

    st.subheader("Prediction")

    if class_name == "Healthy Maize":
        st.success(f"✅ {class_name} ({confidence:.2f}%)")
    else:
        st.warning(f"⚠ {class_name} ({confidence:.2f}%)")

    st.progress(int(confidence))
