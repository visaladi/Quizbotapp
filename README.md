# Quizbotapp
# PDF Quiz Generator

A simple Flask-based web application that converts PDF or plain text files into interactive multiple-choice quizzes. It extracts text from uploaded documents, generates fill-in-the-blank questions by blanking out key words, and provides selectable answer options.

---

## Features

* Upload PDF (`.pdf`) or plain text (`.txt`) files
* Automatic text extraction using PyPDF2
* Fill-in-the-blank question generation with pure Python (regex)
* Multiple-choice options drawn from sentence keywords
* Interactive web interface built with Flask
* Session-based score calculation and result display

---

## Prerequisites

* Python 3.12 or higher
* `pip` package manager

---

## Installation

1. **Clone the repository**

   ```bash
   git clone https://github.com/yourusername/pdf-quiz-generator.git
   cd pdf-quiz-generator
   ```

2. **Create and activate a virtual environment**

   ```bash
   python -m venv venv
   # On Windows
   venv\Scripts\activate
   # On macOS/Linux
   source venv/bin/activate
   ```

3. **Install dependencies**

   ```bash
   pip install -r requirements.txt
   ```

---

## Dependencies

This project relies on the following Python packages (pinned versions as of July 2025):

```
blinker==1.9.0
click==8.2.1
colorama==0.4.6
Flask==3.1.1
gensim==4.3.3
itsdangerous==2.2.0
Jinja2==3.1.6
joblib==1.5.1
MarkupSafe==3.0.2
nltk==3.9.1
numpy==1.26.4
PyPDF2==3.0.1
regex==2024.11.6
scipy==1.13.1
smart_open==7.3.0.post1
tqdm==4.67.1
Werkzeug==3.1.3
wrapt==1.17.2
```

You can generate or update this file by running:

```bash
pip freeze > requirements.txt
```

---

## Usage

1. **Start the Flask app**

   ```bash
   python app.py
   ```

2. **Open your browser** at `http://127.0.0.1:5000/`

3. **Upload** a PDF or TXT file on the landing page

4. **Generate** and **take** your quiz

5. **View** your score on the results page

---

## Project Structure

```
pdf-quiz-generator/
├── app.py               # Main Flask application (Flask routes & session handling)
├── workers.py           # Text extraction and question generation logic
├── templates/           # HTML templates
│   ├── index.html       # Landing/upload page
│   ├── quiz.html        # Quiz display page
│   └── result.html      # Score results page
├── static/              # Static assets (CSS & JS)
│   ├── styles.css       # Styling rules
│   └── script.js        # Front-end interactivity
├── pdf/                 # Temporary upload directory (created at runtime)
├── requirements.txt     # Project dependencies (pip freeze output)
└── README.md            # Project documentation (this file)
```

---

---

## LLM Integration

This project currently uses simple regex-based question generation and does not include a large language model (LLM). To leverage an LLM (e.g., OpenAI GPT-4) for more sophisticated question generation and distractor creation, you could:

* Install an LLM client library, for example:

  ```bash
  pip install openai
  ```
* Obtain and configure your API key via an environment variable:

  ```bash
  export OPENAI_API_KEY="your_key_here"
  ```
* Update the question generation logic in `workers.py` to call the LLM:

  ```python
  import openai

  def generate_with_llm(prompt: str) -> str:
      response = openai.ChatCompletion.create(
          model="gpt-4",
          messages=[{"role": "user", "content": prompt}]
      )
      return response.choices[0].message.content.strip()
  ```
* Craft prompts that instruct the LLM to produce a question and multiple-choice options, for example:

  ```python
  prompt = (
      f"Create a multiple choice question (4 options) based on the following sentence: '{sentence}'."
  )
  llm_output = generate_with_llm(prompt)
  ```

---

## Contributing

Contributions are welcome! To contribute:

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/YourFeature`)
3. Commit your changes (`git commit -m "Add feature"`)
4. Push to the branch (`git push origin feature/YourFeature`)
5. Open a Pull Request on GitHub

Please follow the existing code style and include tests where appropriate.

---

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.
