import base64
import streamlit as st
import requests

# Define InferenceHTTPClient or any necessary imports here
# If necessary, you might need to directly include the logic from InferenceHTTPClient

# Instantiate the InferenceHTTPClient
CLIENT = InferenceHTTPClient(
    api_url="https://classify.roboflow.com",
    api_key="OFvGjLQckHIk2eJo4Sgi"
)

def classify_image(image):
    try:
        # Encode the image as base64
        image_data = base64.b64encode(image.read()).decode('utf-8')
        # Send image data for classification
        result = CLIENT.infer(image_data, model_id="skin-disease-ia-detection/1")
        return result
    except Exception as e:
        return {'error': str(e)}

def main():
    st.title('Skin Disease Classification')

    # File upload
    uploaded_file = st.file_uploader("Choose an image...", type=["jpg", "png"])

    # Button to trigger classification
    if st.button('Classify'):
        if uploaded_file is not None:
            # Display uploaded image
            st.image(uploaded_file, caption='Uploaded Image', use_column_width=True)
            # Call classify_image function to perform classification
            result = classify_image(uploaded_file)
            # Display classification result
            st.json(result)
        else:
            st.error("Please upload an image file")

if __name__ == '__main__':
    main()
