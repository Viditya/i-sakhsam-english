import os
import openai
from flask import Flask, render_template, request, jsonify

app = Flask(__name__)

# Set your OpenAI API key
openai.api_key = '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'
# os.environ["OPENAI_API_KEY"]

def correct_text(input_text):
    # Call the OpenAI API to correct the text
     messages = [
        {"role": "system", "content": "Be my English teacher and tell me mistakes in the following sentence for 10 minutes. Give feedback in Hindi"},
        {"role": "user", "content":"I is goiang"},
        {"role": "assistant", "content": '''मैं जा रहा हूँ। \n
                    यहाँ दिए गए वाक्य में कुछ गलतियाँ हैं। \n
                    1. 'I' का प्रयोग वाक्य के शुरुआत में होना चाहिए, इसलिए 'I' की जगह 'I am' का प्रयोग करें। \n
                    सही रूप में वाक्य बनाने के लिए निम्नलिखित रूप का प्रयोग करेंगे: \n
                    "I am going."
                    '''},
        {"role": "user", "content": input_text},
        ]
     response = openai.ChatCompletion.create(
     model="gpt-3.5-turbo-16k",
     messages=messages,
     temperature = 0,
     max_tokens = 500
    )
     corrected_text = response["choices"][0].message["content"].strip()
     return corrected_text

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        input_text = request.form["input_text"]

        if input_text:
            corrected = correct_text(input_text)
            return render_template("index.html", input_text=input_text, corrected_text=corrected)

    return render_template("index.html")

if __name__ == "__main__":
    app.run(debug=True)
