import streamlit as st
from streamlit_webrtc import webrtc_streamer, VideoProcessorBase
import av
import numpy as np
from ultralytics import YOLO

# Load model
model = YOLO("best (1).pt")

st.title("🌱 Krishi Rakshak - LIVE AI Detection")

class VideoProcessor(VideoProcessorBase):
    def recv(self, frame):
        img = frame.to_ndarray(format="bgr24")

        # Run YOLO
        results = model(img, verbose=False)

        probs = results[0].probs
        names = results[0].names

        if probs is not None:
            pred_class = probs.top1
            confidence = float(probs.data[pred_class]) * 100
            class_name = names[pred_class]

            label = f"{class_name} {confidence:.1f}%"

            # Draw on frame
            import cv2
            cv2.putText(img, label, (10, 30),
                        cv2.FONT_HERSHEY_SIMPLEX, 1,
                        (0, 255, 0), 2)

        return av.VideoFrame.from_ndarray(img, format="bgr24")

webrtc_streamer(
    key="krishi-live",
    video_processor_factory=VideoProcessor,
    media_stream_constraints={"video": True, "audio": False},
)
