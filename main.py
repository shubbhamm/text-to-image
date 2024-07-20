from flask import Flask, request, render_template
import requests
from PIL import Image
from io import BytesIO
import base64
import os

# Get Gemini API key from environment variable
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

app = Flask(__name__)

def generate_image(prompt):
    url = "https://api.gemini.ai/v1/images/generate"  # Hypothetical correct endpoint
    headers = {
        "Authorization": f"Bearer {GEMINI_API_KEY}",
        "Content-Type": "application/json"
    }
    data = {
        "prompt": prompt,
        "n": 1,
        "size": "512x512"
    }
    response = requests.post(url, json=data, headers=headers)
    response.raise_for_status()  # Raise an exception for HTTP errors
    image_url = response.json()['data'][0]['url']
    return image_url

def show_image(image_url):
    response = requests.get(image_url)
    img = Image.open(BytesIO(response.content))
    return img

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        prompt = request.form.get("prompt")
        if prompt:
            try:
                image_url = generate_image(prompt)
                img = show_image(image_url)
                buffered = BytesIO()
                img.save(buffered, format="PNG")
                img_str = base64.b64encode(buffered.getvalue()).decode()
                return render_template("index.html", img_data=img_str, prompt=prompt)
            except Exception as e:
                return render_template("index.html", error=str(e))
        else:
            return render_template("index.html", warning="Please enter a text prompt.")
    return render_template("index.html")

if __name__ == "__main__":
    app.run(debug=True)

