from flask import Flask, render_template, request, jsonify
from transformers import AutoModelForCausalLM, AutoTokenizer

app = Flask(__name__)

model_name = "distilgpt2" 
tokenizer = AutoTokenizer.from_pretrained(model_name)
model = AutoModelForCausalLM.from_pretrained(model_name)

knowledge_base = [
	{
		"question": "What is 42 Amman?",
		"answer": "42 Amman is a free, teacher-less, project-based computer programming school in Amman, Jordan. It's part of the École 42 global network and is open to everyone aged 18+, regardless of background or education."
	},
	{
		"question": "When was 42 Amman launched?",
		"answer": "42 Amman was launched in 2023 as part of the École 42 global network."
	},
	{
		"question": "Is 42 Amman really free?",
		"answer": "Yes, 42 Amman is completely tuition-free. It's a non-profit initiative by the Crown Prince Foundation, supported by CHAMS Association, French Embassy in Jordan, ZINC, CAVT, and the Ministry of Planning and International Cooperation."
	},
	{
		"question": "How does learning work at 42 Amman?",
		"answer": "42 Amman uses a peer-to-peer, project-based, gamified learning approach. There are no teachers, classes, or lectures. Students learn by doing projects, collaborating with peers, and solving problems. They gain XP by completing projects, which unlocks new projects in a branching tree system."
	},
	{
		"question": "Are there teachers at 42 Amman?",
		"answer": "No, 42 Amman has no teachers, classes, or lectures. Learning is based on a peer-to-peer, project-based methodology where students teach each other and learn by doing."
	},
	{
		"question": "What's the curriculum at 42 Amman?",
		"answer": "The curriculum at 42 Amman consists of: 1) Core Curriculum (8–18 months, max 2 years) covering Unix, C, Algorithms, Networking, System Admin, Graphics, and OOP. 2) First Internship (4–6 months). 3) Specialization Phase (up to 3 years) covering Advanced Algorithms & AI, Game Dev, Web/Mobile, Cybersecurity, Advanced Unix & Networking, and SEA:ME. 4) Optional Second Internship (4–6 months)."
	},
	{
		"question": "What programming languages do you learn at 42?",
		"answer": "At 42 Amman, students start with C programming in the core curriculum. Later, they learn various languages depending on their specialization path, including C++, Python, JavaScript, and more. The focus is on mastering programming concepts rather than specific languages."
	},

	{
		"question": "How do I apply to 42 Amman?",
		"answer": "To apply to 42 Amman: 1) Register online and create a profile. 2) Take the Logic Test (about 2 hours online) to assess cognitive skills. 3) Attend an Intro Meeting (online or in-person) to learn more about 42 Amman. 4) Complete the Piscine (1-month immersive bootcamp) to test fit and readiness. 5) If you pass the Piscine, you can start the core program."
	},
	{
		"question": "What is the Piscine?",
		"answer": "The Piscine is a 1-month immersive bootcamp that serves as the final selection process for 42 Amman. It's an intensive coding experience designed to test your fit and readiness for the program. During the Piscine, candidates work on programming challenges for 12+ hours daily, including weekends, to see if they're suited for 42's learning model."
	},
	{
		"question": "What are the career opportunities after 42 Amman?",
		"answer": "42 Amman has strong ties with local and international industry partners. The specialization phase prepares students to enter the job market as senior-level software engineers. However, students are not required to work with partner companies and can pursue their own career paths."
	},
	{
		"question": "Is 42 Amman internationally recognized?",
		"answer": "Yes, 42 Amman is part of École 42, which was founded in 2013 in Paris. The network includes more than 54 campuses in 31 countries, with 44,000+ graduates. Students receive internationally recognized diplomas, including the French diploma."
	},
	{
		"question": "What is programming?",
		"answer": "Programming is the process of creating a set of instructions that tell a computer how to perform a task. Programming involves tasks such as analysis, generating algorithms, profiling algorithms' accuracy and resource consumption, and implementation of algorithms."
	},
	{
		"question": "What is C programming?",
		"answer": "C is a general-purpose programming language created in the 1970s. It's very powerful and widely used for system programming, embedded systems, and applications. C is known for its efficiency, control, and direct manipulation of hardware. It's the primary language taught in the core curriculum at 42 Amman."
	}
]


kb_texts = [f"Q: {item['question']}\nA: {item['answer']}" for item in knowledge_base]

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/ask', methods=['POST'])
def ask():
    user_input = request.json.get('prompt', '')
    if not user_input:
        return jsonify({'error': 'No prompt provided'}), 400
    
    query_embedding = embedding_model.encode(user_input)
    
    if similarity_score > 0.6: 
        answer = knowledge_base[top_idx]["answer"]
        return jsonify({'answer': answer})
    
    default_context = """
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
    - Core Curriculum (8–18 months, max 2 years)
    - Includes: Unix, C, Algorithms, Networking, System Admin, Graphics, OOP.
    - All students start from the same level.
    - First Internship (4–6 months)
    - Specialization Phase (up to 3 years)
    - Topics include: Advanced Algorithms & AI, Game Dev, Web/Mobile, Cybersecurity, Advanced Unix & Networking, SEA:ME.
    - Can be completed at any 42 campus worldwide.
    - Second Internship (4–6 months, optional)
    """
    
    prompt = f"{default_context}\nQ: {user_input}\nA:"
    
    inputs = tokenizer(prompt, return_tensors="pt")
    outputs = model.generate(
        inputs.input_ids,
        max_length=300,
        top_p=0.9,
        do_sample=True,
        pad_token_id=tokenizer.eos_token_id
    )
    
    response = tokenizer.decode(outputs[0], skip_special_tokens=True)
    answer = response.split("A:")[-1].strip()
    
    return jsonify({'answer': answer})

@app.errorhandler(404)
def not_found(e):
    return render_template("404.html")

if __name__ == '__main__':
    app.run(debug=True, port=5000)