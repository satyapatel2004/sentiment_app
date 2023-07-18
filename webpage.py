from flask import Flask, render_template, request, redirect
from main import * 

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/process', methods=['POST'])
def process():
    input_data = request.form['input_field']

    valid = check_ticker(input_data)
    
    if valid:
        arr = get_stock(input_data)
        polarity = arr[1]
        polarity = round(polarity, 2)
        keywords = arr[0]


    else:
        polarity = None
        keywords = None


    input_data = input_data.upper() 


    return render_template('result.html', valid=valid, input_data=input_data, polarity=polarity, keywords=keywords)

    
if __name__ == '__main__':
    app.run(debug=True)