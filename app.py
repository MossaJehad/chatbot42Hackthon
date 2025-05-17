from flask import Flask, render_template
app = Flask(__name__)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/ask')
def student():
    return 'ask endpoint and frontend interface'

@app.route('/login')
def greet():
    return render_template('login.html')

@app.errorhandler(404)
def not_found(e):
	return render_template("404.html")

if __name__ == '__main__':
    app.run(debug=False, port=5000)
