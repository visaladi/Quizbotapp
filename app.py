import os
from flask import Flask, render_template, redirect, url_for
from flask.globals import request
from werkzeug.utils import secure_filename
from workers import pdf2text, txt2questions

# Constants
UPLOAD_FOLDER = './pdf/'
ALLOWED_EXTENSIONS = {'pdf', 'txt'}
MAX_CONTENT_LENGTH = 16 * 1024 * 1024  # 16 MB

# Initialize Flask app
app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['MAX_CONTENT_LENGTH'] = MAX_CONTENT_LENGTH
app.secret_key = os.urandom(24)
# Helper function to check allowed file extensions
def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/')
def index():
    """ Landing page """
    return render_template('index.html')

@app.route('/quiz', methods=['GET', 'POST'])
def quiz():
    questions = {}
    error = None

    if request.method == 'POST':
        uploaded_file = request.files.get('file', None)
        if not uploaded_file:
            error = "No file part in the request."
        elif uploaded_file.filename == "":
            error = "No file selected."
        elif not allowed_file(uploaded_file.filename):
            error = "Unsupported file type. Please upload a PDF or TXT."
        else:
            # Save file
            filename = secure_filename(uploaded_file.filename)
            file_ext = filename.rsplit('.', 1)[1].lower()
            file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            uploaded_file.save(file_path)

            # Extract text
            content = pdf2text(file_path, file_ext)
            os.remove(file_path)  # clean up immediately

            if not content.strip():
                error = "Could not extract any text from that file."
            else:
                # Generate questions
                questions = txt2questions(content)
                if not questions:
                    error = "No questions could be generated from the document."

    # Render with either questions or an error
    return render_template(
        'quiz.html',
        questions=questions,
        error=error
    )




@app.route('/result', methods=['POST', 'GET'])
def result():
    correct_q = 0
    total_q = len(request.form)  # Assuming one question for each form item

    # Check if the answers are correct (implement your logic here)
    for k, v in request.form.items():
        if v == 'correct_answer':  # Replace with actual answer checking logic
            correct_q += 1

    return render_template('result.html', total=total_q, correct=correct_q)

if __name__ == "__main__":
    app.run(debug=True)
