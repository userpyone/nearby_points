from flask import Flask, render_template, request

# app = Flask(__name__)
app = Flask(__name__, template_folder='../templates')
# app = Flask(__name__, template_folder='templates')
# app.template_folder = "templates"

@app.route('/')
def index():
    return render_template('main.html')

@app.route('/process_form', methods=['POST'])
def process_form():
    if request.method == 'POST':
        user_input = request.form['user_input']
        # Делай с пользовательским вводом что угодно здесь
        print(user_input)
        return user_input

if __name__ == '__main__':
    app.run(debug=True)
