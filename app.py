from flask import Flask, render_template, request, jsonify, json
from transformers import AutoModelForCausalLM, AutoTokenizer

app = Flask(__name__)

model_name = "distilgpt2" 
tokenizer = AutoTokenizer.from_pretrained(model_name)
model = AutoModelForCausalLM.from_pretrained(model_name)

with open('knowledge_base.json', 'r', encoding='utf-8') as f:
    knowledge_base = json.load(f)


kb_texts = [f"Q: {item['question']}\nA: {item['answer']}" for item in knowledge_base]

@app.route('/')
def home():
    return render_template('index.html')

def find_best_match(user_input, kb):
    user_input_lower = user_input.lower()
    best_score = 0
    best_answer = None
    for item in kb:
        question = item['question'].lower()
        shared_words = set(user_input_lower.split()) & set(question.split())
        score = len(shared_words) / max(len(question.split()), 1)
        if score > best_score:
            best_score = score
            best_answer = item['answer']
    return best_answer, best_score

@app.route('/ask', methods=['POST'])
def ask():
    user_input = request.json.get('prompt', '')
    if not user_input:
        return jsonify({'error': 'No prompt provided'}), 400
    
    answer, score = find_best_match(user_input, knowledge_base)
    if score > 0.88:
        return jsonify({'answer': answer})
    
    default_context = """..."""  
    
    prompt = f"{default_context}\nQ: {user_input}\nA:"
    
    inputs = tokenizer(prompt, return_tensors="pt")
    outputs = model.generate(
        inputs.input_ids,
        max_length=420,
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