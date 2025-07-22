import gensim
from nltk.tokenize import word_tokenize
import random


class IncorrectAnswerGenerator:
    ''' This class generates incorrect answers given a correct answer '''

    def __init__(self, document):
        # Load Gensim model (GloVe in this case)
        self.model = gensim.downloader.load("glove-wiki-gigaword-100")

        # Tokenize the document into words
        self.all_words = []
        for sent in document.split("\n"):
            self.all_words.extend(word_tokenize(sent))
        self.all_words = list(set(self.all_words))  # Remove duplicates

    def get_all_options_dict(self, answer, num_options):
        ''' Returns a dict of 'num_options' options, one being the correct answer '''
        options_dict = dict()

        try:
            # Fetch similar words to the correct answer from the word embeddings
            similar_words = self.model.similar_by_word(answer, topn=15)[::-1]

            for i in range(1, num_options + 1):
                options_dict[i] = similar_words[i - 1][0]
        except Exception as e:
            # If an error occurs, we fall back to finding similar words from the document
            self.all_sim = []
            for word in self.all_words:
                if word not in answer:
                    try:
                        similarity_score = self.model.similarity(answer, word)
                        self.all_sim.append((similarity_score, word))
                    except Exception:
                        self.all_sim.append((0.0, word))
                else:
                    self.all_sim.append((-1.0, word))

            # Sort by similarity
            self.all_sim.sort(reverse=True)

            # Pick the top options
            for i in range(1, num_options + 1):
                options_dict[i] = self.all_sim[i - 1][1]

        # Randomly replace one of the options with the correct answer
        replacement_idx = random.randint(1, num_options)
        options_dict[replacement_idx] = answer

        return options_dict
