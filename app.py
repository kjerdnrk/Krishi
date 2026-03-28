import streamlit as st
from streamlit_webrtc import webrtc_streamer, VideoProcessorBase
import av
import numpy as np
from ultralytics import YOLO
import cv2

st.set_page_config(layout="wide")

# Load model
model = YOLO("best (1).pt")

# UI Styling
st.markdown("""
<style>
.main {background-color: #f1f1f1;}
.card {
    background-color: white;
    padding: 15px;
    border-radius: 10px;
    box-shadow: 2px 2px 10px rgba(0,0,0,0.1);
}
</style>
""", unsafe_allow_html=True)

st.title("🌱 Krishi Rakshak - LIVE AI Dashboard")

col1, col2, col3 = st.columns(3)

detection_placeholder = col1.empty()
info_placeholder = col2.empty()
severity_placeholder = col3.empty()

class VideoProcessor(VideoProcessorBase):
    def recv(self, frame):
        img = frame.to_ndarray(format="bgr24")

        results = model(img, verbose=False)
        probs = results[0].probs
        names = results[0].names

        if probs is not None:
            pred_class = probs.top1
            confidence = float(probs.data[pred_class]) * 100
            class_name = names[pred_class]

            label = f"{class_name} {confidence:.1f}%"

            cv2.putText(img, label, (10, 30),
                        cv2.FONT_HERSHEY_SIMPLEX, 1,
                        (0, 255, 0), 2)

            detection_placeholder.markdown(f"### 🔍 Detection\n{class_name}")
            info_placeholder.markdown(f"### 🦠 Info\nConfidence: {confidence:.2f}%")
            severity_placeholder.progress(int(confidence))

        return av.VideoFrame.from_ndarray(img, format="bgr24")

webrtc_streamer(
    key="krishi-live",
    video_processor_factory=VideoProcessor,
    media_stream_constraints={"video": True, "audio": False},
)
