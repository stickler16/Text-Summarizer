from asyncio.windows_events import NULL
from flask import Flask, render_template, request, url_for
import requests


app = Flask(__name__)


@app.route("/", methods=["GET", "POST"])
def Index():
    return render_template("index.html")


@app.route("/Summarize", methods=["GET", "POST"])
def Summarize():
    if request.method == "POST":
        API_URL = "https://api-inference.huggingface.co/models/facebook/bart-large-cnn"
        headers = {"Authorization": "Bearer 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"}

        data = request.form["data"]
        if len(data) < 20:
            return render_template("index.html",result = "Enter atleast 30 words to get a summary")
        
        def query(payload):
            response = requests.post(API_URL, headers=headers, json=payload)
            return response.json()

        max_length = int(request.form["Max_Length"])
        min_length = max_length//4

        output = query(
            {
                "inputs": data,
                "parameters": {"min_length": min_length, "max_length": max_length},
            }
        )
        
        return render_template("index.html", result=output[0]['summary_text'])
    else:
        return render_template("index.html")


if __name__ == "__main__":
    app.debug = False
    app.run()
 