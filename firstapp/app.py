from flask import Flask, request, make_response

app = Flask(__name__)

@app.route('/')
def index():
    return "Hello World"

@app.route('/hello', methods=['GET', 'POST'])
def hello():
    if request.method == 'GET':
        return 'You made a GET request\n'
    elif request.method == 'POST':
        return 'You made a POST request\n'
    else:
        return 'You will never see this message\n'
    
@app.route('/custom_response')
def custom_response():
    response = make_response("This is my response")
    response.status_code = 202
    response.headers['content-type'] = 'text/plain'
    return response

@app.route('/greet/<name>')
def greet(name):
    return f"Hello {name}"

@app.route('/add/<num1>/<num2>')
def add(num1, num2):
    return f'{num1} + {num2} = {num1 + num2}'

@app.route('/handle_url_params')
def handle_params():
    if 'greeting' in request.args.keys() and 'name' in request.args.keys():
        greeting = request.args['greeting']
        name = request.args.get('name')
        return f'{greeting}, {name}'
    else:
        return 'Some parameters are missing'

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5555, debug=True)