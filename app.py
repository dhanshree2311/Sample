pip install flask
from flask import Flask, request, jsonify
import base64
import requests
import streamlit as st

app = Flask(__name__)

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
            payload = {'api_key': 'aRnfmznW3CMShQdCZUWm'}
            headers = {'Content-Type': 'application/x-www-form-urlencoded'}
            response = requests.post('https://classify.roboflow.com/skin-disease-ia-detection/1', params=payload, data=image, headers=headers)
            return jsonify(response.json())
        except Exception as e:
            return jsonify({'error': str(e)}), 500
    else:
        return jsonify({'error': 'Invalid file format'}), 400

@st.cache(allow_output_mutation=True)
def get_file_content_as_string(path):
    url = 'https://raw.githubusercontent.com/streamlit/demo-self-driving/master/' + path
    response = requests.get(url)
    return response.text

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
    app.run(debug=True)
