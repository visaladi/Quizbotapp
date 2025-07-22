import random
import re


def pdf2text(file_path: str, file_exten: str) -> str:
    """ Converts PDF or TXT to text """
    content = ''

    if file_exten == 'pdf':
        from PyPDF2 import PdfReader
        with open(file_path, 'rb') as pdf_file:
            pdf_reader = PdfReader(pdf_file)
            for page in pdf_reader.pages:
                content += page.extract_text()
        print("PDF extraction successful!")

    elif file_exten == 'txt':
        with open(file_path, 'r') as txt_file:
            content = txt_file.read()
        print("TXT extraction successful!")

    return content


def txt2questions(doc: str, n=5, o=4) -> dict:
    """ Generate up to n fill‑in‑the‑blank questions with o options each """
    sentences = split_into_sentences(doc)
    questions = {}
    for idx, sent in enumerate(sentences[:n], start=1):
        # extract candidate words (longer than 4 letters, alpha only)
        words = re.findall(r'\b[A-Za-z]{5,}\b', sent)
        if not words:
            continue
        answer = random.choice(words)

        # build the question by blanking out the answer
        question_text = sent.replace(answer, '_____')

        # pick wrong options from other words
        wrong_pool = [w for w in set(words) if w != answer]
        wrongs = random.sample(wrong_pool, min(o-1, len(wrong_pool)))

        # assemble options & shuffle
        opts = [answer] + wrongs
        random.shuffle(opts)
        options_dict = {i+1: opt for i, opt in enumerate(opts)}

        questions[idx] = {
            'question': question_text,
            'answer': answer,
            'options': options_dict
        }
    return questions


def split_into_sentences(text):
    """ Split text into sentences using regex (no external libraries) """
    # Basic regex to split text into sentences
    sentence_endings = re.compile(r'(?<!\w\.\w)(?<![A-Z][a-z]\.)(?<=\.|\?)\s')
    sentences = sentence_endings.split(text.strip())
    return [sentence.strip() for sentence in sentences if sentence]


def generate_question_from_sentence(sentence):
    """ Generate a question from a sentence (simple template approach) """
    sentence = sentence.lower()

    # Check if the sentence mentions a time-related phrase
    if "when" in sentence:
        question = "When did this event happen?"
        answer = sentence
    # Check if the sentence mentions a place or location
    elif "where" in sentence:
        question = "Where did this occur?"
        answer = sentence
    # Check if the sentence mentions a person (can be extended with more rules)
    elif "who" in sentence:
        question = "Who is the subject of this statement?"
        answer = sentence
    else:
        # Default question for any other sentence
        question = "What does this sentence describe?"
        answer = sentence

    return question, answer


def generate_options(correct_answer, num_options):
    """ Generate incorrect options along with the correct answer """
    options_dict = {}

    # Add the correct answer randomly
    options_dict[random.randint(1, num_options)] = correct_answer

    # Add some dummy wrong answers for demonstration purposes
    for i in range(1, num_options + 1):
        if i not in options_dict:
            options_dict[i] = f"Option {i} (incorrect)"

    return options_dict
