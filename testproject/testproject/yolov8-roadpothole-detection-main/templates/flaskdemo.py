from flask import Flask, render_template, flash, redirect, url_for
import os

app = Flask(__name__)
app.secret_key = 'your_secret_key'

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/run_pothole_detection', methods=['POST'])
def run_pothole_detection():
    try:
        flash('Pothole detection process started!')
        # Add code to run pothole detection here
        os.system("python pothole_detection.py")  # Replace "pothole_detection.py" with your pothole detection script
    except Exception as e:
        flash(f'Error: {str(e)}')
    return redirect(url_for('index'))

@app.route('/run_zebra_detection', methods=['POST'])
def run_zebra_detection():
    try:
        flash('Zebra detection process started!')
        # Add code to run zebra detection here
        os.system("python zebra_detection.py")  # Replace "zebra_detection.py" with your zebra detection script
    except Exception as e:
        flash(f'Error: {str(e)}')
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)
