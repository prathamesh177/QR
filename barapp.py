import streamlit as st
from streamlit_webrtc import webrtc_streamer, VideoTransformerBase
import aspose.barcode as barcode
import cv2
import numpy as np
from PIL import Image


class QRCodeScanner(VideoTransformerBase):
    def transform(self, frame):
        # Convert the frame to an OpenCV image
        img = frame.to_ndarray(format="bgr24")

        # Convert to grayscale for barcode recognition
        gray_img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

        # Save the frame temporarily to process it with Aspose.Barcode
        temp_image_path = "temp_camera_frame.jpg"
        cv2.imwrite(temp_image_path, gray_img)

        # Use Aspose.Barcode to recognize QR codes
        reader = barcode.barcoderecognition.BarCodeReader(temp_image_path)
        recognized_results = reader.read_bar_codes()

        # Draw rectangles and text on the image for detected QR codes
        for result in recognized_results:
            # Get barcode text and type
            code_text = result.code_text
            code_type = result.code_type_name

            # Add text to the image
            cv2.putText(
                img,
                f"{code_type}: {code_text}",
                (10, 30),
                cv2.FONT_HERSHEY_SIMPLEX,
                1,
                (0, 255, 0),
                2,
                cv2.LINE_AA,
            )

        return img


# Streamlit app
st.title("Real-Time QR Code Scanner")

st.write(
    """
    **Instructions**:
    1. Allow the browser to access your camera.
    2. Point the camera at a QR code to scan.
    """
)

# Start the real-time camera stream
webrtc_streamer(
    key="qr-code-scanner",
    video_transformer_factory=QRCodeScanner,
    media_stream_constraints={"video": True, "audio": False},
)
