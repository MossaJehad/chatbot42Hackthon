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
	context = """
	About 42 Amman
	- A free, teacher-less, project-based computer programming school in Amman, Jordan.
	- Launched in 2023 as part of the École 42 global network.
	- Open to everyone aged 18+, regardless of background or education.
	- Operates 24/7, completely tuition-free, with high-tech facilities.

	Learning Methodology
	- No teachers, no classes, no lectures.
	- Based on peer-to-peer, project-based, gamified learning.
	- Encourages self-learning, collaboration, and problem-solving.
	- Students gain XP by completing projects, unlocking new ones in a branching tree system.
	- Emphasizes "embrace failure" philosophy—fail fast, learn faster.

	Curriculum Structure
	- Core Curriculum (8~18 months, max 2 years)
	- Includes: Unix, C, Algorithms, Networking, System Admin, Graphics, OOP.
	- All students start from the same level.
	- First Internship (4~6 months)
	- Specialization Phase (up to 3 years)
	- Topics include: Advanced Algorithms & AI, Game Dev, Web/Mobile, Cybersecurity, Advanced Unix & Networking, SEA:ME.
	- Can be completed at any 42 campus worldwide.
	- Second Internship (4~6 months, optional)

	Career Opportunities
	- Strong ties with local and international industry partners.
	- Specialization prepares students to enter the job market as senior-level software engineers.
	- Students are not required to work with partner companies.

	Global Network
	- Part of École 42, founded in 2013 in Paris.
	- More than 54 campuses in 31 countries, with 44,000+ graduates.
	- Students get internationally recognized diplomas, like the French diploma.

	How to Apply
	- Register	# return domain_knowledge + "\nQ: " + user_input + "\nA:"
 online and create a profile.
	- Logic Test (~2 hours, online) to assess cognitive skills.
	- Intro Meeting (online or in-person) to learn more about 42 Amman.
	- Piscine (1-month immersive bootcamp) to test fit and readiness.
	- Welcome Home ~ start the core program if you pass the Piscine.

	Why It’s Free
	- 42 Amman is a non-profit initiative by the Crown Prince Foundation.
	- Supported by: CHAMS Association, French Embassy in Jordan, ZINC, CAVT, Ministry of Planning and International Cooperation.

	Recognition
	- École 42 is ranked:
	- Among Top 10 Innovative Universities
	- #1 in Ethical Value among Top 50 schools
	"""
	prompt = f"{context}\nQ: {user_input}\nA:"
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
