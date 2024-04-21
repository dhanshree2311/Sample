from flask import Flask, request, jsonify
from inference_sdk import InferenceHTTPClient
import base64
import streamlit as st
import requests

app = Flask(__name__)
st.set_page_config(layout="wide")

CLIENT = InferenceHTTPClient(
    api_url="https://classify.roboflow.com",
    api_key="OFvGjLQckHIk2eJo4Sgi"
)

@app.route('/classify', methods=['POST'])
def classify():
    if 'image' not in request.files:
        return jsonify({'error': 'No image file provided'}), 400
    
    file = request.files['image']
    if file.filename == '':
        return jsonify({'error': 'No selected file'}), 400
    if file and file.filename.lower().endswith(('.png', '.jpg', '.jpeg')):
        try:
            image = base64.b64encode(file.read()).decode('utf-8')
            result = CLIENT.infer(image, model_id="skin-disease-ia-detection/1")
            return jsonify(result)
        except Exception as e:
            return jsonify({'error': str(e)}), 500
    else:
        return jsonify({'error': 'Invalid file format'}), 400

def main():
    st.title('Skin Disease Classification')

    # File upload
    uploaded_file = st.file_uploader("Choose an image...", type=["jpg", "png"])

    # Button to trigger classification
    if st.button('Classify'):
        if uploaded_file is not None:
            try:
                # Send image file to Flask server for classification
                files = {'image': uploaded_file}
                response = requests.post('http://localhost:5000/classify', files=files)
                if response.status_code == 200:
                    st.json(response.json())
                else:
                    st.error(f"Error: {response.json()['error']}")
            except Exception as e:
                st.error(f"Error: {str(e)}")
        else:
            st.error("Please upload an image file")

if __name__ == '__main__':
    main()
