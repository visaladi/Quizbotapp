import random
import nltk
from nltk.tokenize import sent_tokenize
from incorrect_answer_generation import IncorrectAnswerGenerator


class QuestionGeneration:
    ''' This class handles question generation from the document content '''

    def __init__(self, num_questions, num_options):
        self.num_questions = num_questions  # Number of questions to generate
        self.num_options = num_options  # Number of options per question
        self.stop_words = set(nltk.corpus.stopwords.words('english'))
        self.incorrect_answer_generator = None  # Initialize later

    def clean_text(self, text):
        ''' Cleans and prepares the text for question generation '''
        sentences = sent_tokenize(text)
        cleaned_text = ""
        for sentence in sentences:
            # Clean non-alphanumeric characters
            cleaned_sentence = ''.join(e for e in sentence if e.isalnum() or e.isspace())
            cleaned_text += cleaned_sentence + " "
        return cleaned_text

    def generate_questions_dict(self, document):
        ''' Generates a dictionary of questions and their options '''
        # Clean document text
        document = self.clean_text(document)

        # Tokenize the document into words
        words = document.split()

        # Select random words as possible question roots
        question_roots = random.sample(words, self.num_questions)

        questions_dict = {}

        # Create questions and answer options
        for i, root_word in enumerate(question_roots):
            question = f"What is the meaning of {root_word}?"
            # Generate incorrect answers using IncorrectAnswerGenerator
            self.incorrect_answer_generator = IncorrectAnswerGenerator(document)
            options_dict = self.incorrect_answer_generator.get_all_options_dict(root_word, self.num_options)

            questions_dict[i + 1] = {
                "question": question,
                "answer": root_word,
                "options": options_dict
            }

        return questions_dict
