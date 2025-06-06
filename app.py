#The main code to run the server

# from knowledge import build_prompt 
from flask import Flask, render_template, request, jsonify
from transformers import pipeline

app = Flask(__name__)
# chat_history = []

#document-question-answering
generator = pipeline("text-generation", model="distilgpt2")

@app.route('/')
def home():
    return render_template('index.html')

@app.route("/about")
def about():
    return render_template("about.html")

@app.route('/ask', methods=['POST'])
def	ask():
	user_input = request.json.get('prompt', '')
	if not user_input:
		return jsonify({'error': 'No prompt provided'}), 400

	prompt = f"{user_input}\n"
	res = generator(prompt, max_length=4200, num_return_sequences=1)
	return jsonify({'answer': res[0]['generated_text'].split('A:')[-1].strip()})
	# return domain_knowledge + "\nQ: " + user_input + "\nA:"

@app.route('/login')
def login():
    return render_template('login.html')

@app.route("/history")
def show_history():
    with open(HISTORY_FILE, "r") as f:
        history = json.load(f)
    return render_template("history.html", history=history)

@app.route("/clear-history", methods=["POST"])
def clear_history():
    with open(HISTORY_FILE, "w") as f:
        json.dump([], f)
    return render_template("history.html", history=[])

@app.errorhandler(404)
def not_found(e):
	return render_template("404.html")

# chat_history.append({"q": question, "a": answer})

# return jsonify({"answer": answer})

if __name__ == '__main__':
    app.run(debug=True, port=5000)
