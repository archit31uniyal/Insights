from flask import Flask, render_template, request
from llama_cpp import Llama
import numpy as np
from utils import *
from transformers import AutoModelForSequenceClassification, pipeline
import os

app = Flask(__name__)
history = []

@app.route("/", methods=['GET', 'POST'])
def home():
    answer = ""
    submitted_text = None
    url = None

    if request.method == 'POST':
        url = request.form['url']
        reviews = Review(url)
        reviews.fetch_reviews()

        submitted_text = request.form['textbox']
        answer = get_response(reviews, submitted_text)
        history.append((submitted_text, answer))

    return render_template("home.html", message=history)

@app.route("/app", methods=['GET', 'POST'])
def app_response():
    answer = ""
    submitted_text = request.args.get('text')
    
    if request.method == 'POST' or request.method == 'GET':
        answer = get_response(submitted_text)
        history.append((submitted_text, answer))

    # return render_template("home.html", message=history)
    return answer

def summarize_in_batches(text, llm, q_len, batch_size= 20):
    curr_pos = 0
    prev_pos = 0
    summary = []
    for i in range(batch_size):
        count = 0
        for j, t in enumerate(text[prev_pos:]):
            count += len(t.split())
            if count <= 500:
                curr_pos = j
            else:
                curr_pos += 1 
                break
        revs = ' '.join(text[prev_pos: curr_pos])
        response = llm.create_chat_completion(
            messages = [
                {"role": "system", "content": "You are an assistant who perfectly answers questions based on the reviews provided."},
                {
                    "role": "user",
                    "content": f"Context:\n {revs}\n\n Summarize the reviews preserving important information."
                }
            ]
        )
        prev_pos = curr_pos
        summary.append(response["choices"][0]["message"]["content"])
    
    response = llm.create_chat_completion(
            messages = [
                {"role": "system", "content": "You are an assistant who perfectly answers questions based on the reviews provided."},
                {
                    "role": "user",
                    "content": f"Here's a list of reviews:\n {summary}\n\n Summarize the reviews preserving important information in {512 - q_len} words."
                }
            ]
        )
    
    return response["choices"][0]["message"]["content"]

def get_response(reviews, question):
    q_len = len(question.split())
    sentiment_map = {
    "positive": 1,
    "negative": 0
    }

    # sentiment_llm = AutoModelForSequenceClassification.from_pretrained("gilf/english-yelp-sentiment")
    sentiment_llm = pipeline("text-classification")

    sentiment = sentiment_llm(question)
    question_class = sentiment[0]["label"]
    question_class = question_class.strip().lower()

    llm = Llama.from_pretrained(
        repo_id="unsloth/Llama-3.2-3B-Instruct-GGUF",
	    filename="Llama-3.2-3B-Instruct-Q4_K_M.gguf",
        n_ctx = 4096,
        n_gpu_layers=30
    )


    # sentiment = llm.create_chat_completion(
    #     messages = [
    #         {"role": "system", "content": "You are an assistant who perfectly classifies the sentiment of the question between postive and negative. The answer should be only one word: either positive or negative."},
    #         {
    #             "role": "user",
    #             "content": f"What is the sentiment of the following question: '{question}'"
    #         }
    #     ]
    # )

    # question_class = sentiment["choices"][0]["message"]["content"]
    # question_class = question_class.strip().lower()

    ratings = np.array(reviews.rating)
    if sentiment_map[question_class]: 
        indices = np.where(ratings > 4.0)[0]
    else:
        indices = np.where(ratings < 2.0)[0]

    # Insert your environment key 
    text = reviews.text

    text = [t for i, t in enumerate(text) if i in indices]
    # TODO: Make review fetch adaptive to windows size and question asked
    # text = text[:7]
    if os.path.exists(f"summary_reviews_{question_class}.pkl"):
        summary = load_pickle(f"summary_reviews_{question_class}.pkl")
    else:
        summary = summarize_in_batches(text, llm, q_len)
        save_pickle(summary, f"summary_reviews_{question_class}.pkl")

    response = llm.create_chat_completion(
        messages = [
            {"role": "system", "content": "You are an assistant who perfectly answers questions based on the reviews provided."},
            {
                "role": "user",
                "content": f"Here's a summary of reviews:\n {summary} \n\n Based on the summary above, answer the following question, \n{question}"
            }
        ]
    )

    processed = response["choices"][0]["message"]["content"]
    return processed


if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=5000)