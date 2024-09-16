# app.py
from flask import Flask, render_template, jsonify
import subprocess

app = Flask(__name__)

# Route for the home page
@app.route('/', methods=['GET'])
def index():
    return render_template('websiteFinal.html')

# Route to run the Python script when the button is clicked
@app.route('/run-script', methods=['POST'])
def run_script():
    try:
        # Run the Python script
        result = subprocess.run([r'C:\Users\sahil\PycharmProjects\MineralsPrediction\dist\ARIMAmodelPrediction\ARIMAmodelPrediction.exe'], capture_output=True, text=True)
        return jsonify({"output": result.stdout})
    except Exception as e:
        return jsonify({"error": str(e)})
    
@app.route('/run-genai', methods=['POST'])
def run_genai():
    try:
        # Run the Python script
        result = subprocess.run([r'C:\Users\sahil\PycharmProjects\GenAI\dist\genAI\genAI.exe'], capture_output=True, text=True)
        return jsonify({"output": result.stdout})
    except Exception as e:
        return jsonify({"error": str(e)})

if __name__ == '__main__':
    app.run(debug=True)
