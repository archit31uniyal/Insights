from flask import Flask, render_template, request
from llama_cpp import Llama
import numpy as np
from utils import *

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

def get_response(reviews, question):

  sentiment_map = {
    "positive": 1,
    "negative": 0
  }

  llm = Llama.from_pretrained(
      repo_id = "TheBloke/Llama-2-7B-Chat-GGUF",
      filename = "*Q4_K_M.gguf",
      chat_format="llama-2"
  )

  sentiment = llm.create_chat_completion(
      messages = [
          {"role": "system", "content": "You are an assistant who perfectly classifies the sentiment of the question between postive and negative. The answer should be only one word: either positive or negative."},
          {
              "role": "user",
              "content": f"What is the sentiment of the following question: '{question}'"
          }
      ]
  )

  question_class = sentiment["choices"][0]["message"]["content"]
  question_class = question_class.strip().lower()

  revs = []
  ratings = np.array(reviews.rating)
  if sentiment_map[question_class]: 
      indices = np.where(ratings > 4.0)[0]
  else:
      indices = np.where(ratings < 2.0)[0]

  # Insert your environment key 
  text = reviews.text

  text = [t for i, t in enumerate(text) if i in indices]
  text = text[:7]

  text = ' '.join(text)

  response = llm.create_chat_completion(
      messages = [
          {"role": "system", "content": "You are an assistant who perfectly answers questions based on the reviews provided."},
          {
              "role": "user",
              "content": f"Here's a list of reviews:\n {text} \n\n Based on the reviews above, answer the following question, \n{question}"
          }
      ]
  )
  print(response)
  # response = openai.ChatCompletion.create(
  #   model="gpt-3.5-turbo",
  #   messages=[
  #     {
  #       "role": "system",
  #       "content": "you are a mathematic teacher for kids. You should explain in a way to make a kid understand your answer."
  #     },
  #     {
  #       "role": "user",
  #       "content": "How do we calculate a modulo? and what is the modulo?"
  #     },
  #     {
  #       "role": "assistant",
  #       "content": "Ah, I see you're curious about modulos! Well, think of a modulo as a way to find the remainder after dividing two numbers. Let me explain it in a fun way.\n\nImagine you have a box of 12 chocolates and you want to share them equally among you and your two best friends. You start dividing the chocolates, giving each friend 4 chocolates. But what about the remaining chocolates? That's where the modulo comes in!\n\nTo calculate the modulo, you count how many chocolates are left after everyone gets their fair share. In this case, when you divide 12 chocolates among 3 people, each person gets 4 chocolates and there are no leftover chocolates. So, the modulo is 0.\n\nNow, let's try a different example. Suppose you have 10 candies and you want to share them equally among 4 friends. You start dividing, giving each friend 2 candies. But there will be some leftovers this time, right?\n\nTo find the modulo, we count how many candies are left after dividing equally. In this case, after giving each friend 2 candies, you'll have 2 candies left over. So, the modulo is 2.\n\nYou can find the modulo for any division calculation by finding the remainder, or what's"
  #     },
  #     {
  #       "role": "user",
  #       "content": question
  #     }
  #   ],
  #   temperature=1,
  #   max_tokens=256,
  #   top_p=1,
  #   frequency_penalty=0,
  #   presence_penalty=0
  # )

  processed = response["choices"][0]["message"]["content"]
  return processed



if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=5000)