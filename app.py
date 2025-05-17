from flask import Flask, render_template, request, jsonify
from transformers import pipeline

app = Flask(__name__)
#document-question-answering
generator = pipeline("question-answering", model="distilgpt2")

@app.route('/')
def	home():
	return render_template('index.html')

@app.route('/ask', methods=['POST'])
def	ask():
	user_input = request.json.get('prompt', '')
	if not user_input:
		return jsonify({'error': 'No prompt provided'}), 400
	res = generator(user_input, max_length=420, num_return_sequences=1)
	return jsonify(res[0])

@app.route('/login')
def	login():
	return render_template('login.html')

@app.errorhandler(404)
def not_found(e):
	return render_template("404.html")

if __name__ == '__main__':
	app.run(debug=True, port=5000)
