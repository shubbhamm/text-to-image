

# from flask import Flask, request, jsonify, render_template
# import openai
# import requests
# from PIL import Image
# from io import BytesIO
# import base64

# # Replace with your OpenAI API key
# openai.api_key = "sk-None-lupJ7yTw2jRp5EUM39BGT3BlbkFJb0mT5Ul3z5Oey9yaWXY3"

# app = Flask(__name__)	

# def generate_image(prompt):
#     response = openai.Image.create(
#         prompt=prompt,
#         n=1,
#         size="512x512",
#         response_format="url"
#     )
#     image_url = response['data'][0]['url']
#     return image_url

# def show_image(image_url):
#     response = requests.get(image_url)
#     img = Image.open(BytesIO(response.content))
#     return img

# @app.route("/", methods=["GET", "POST"])
# def index():
#     if request.method == "POST":
#         prompt = request.form.get("prompt")
#         if prompt:
#             try:
#                 image_url = generate_image(prompt)
#                 img = show_image(image_url)
#                 buffered = BytesIO()
#                 img.save(buffered, format="PNG")
#                 img_str = base64.b64encode(buffered.getvalue()).decode()
#                 return render_template("index.html", img_data=img_str, prompt=prompt)
#             except Exception as e:
#                 return render_template("index.html", error=str(e))
#         else:
#             return render_template("index.html", warning="Please enter a text prompt.")
#     return render_template("index.html")

# if __name__ == "__main__":
#     app.run(debug=True)






from flask import Flask, request, render_template
import requests
from PIL import Image
from io import BytesIO
import base64
import os
import openai

# Get OpenAI API key from environment variable
openai.api_key = os.getenv("OPENAI_API_KEY")

app = Flask(__name__)

def generate_image(prompt):
    response = openai.Image.create(
        prompt=prompt,
        n=1,
        size="512x512"
    )
    image_url = response['data'][0]['url']
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

