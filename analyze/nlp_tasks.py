from collections import Counter
from itertools import chain

import matplotlib.pyplot as plt
import nltk
from gensim import corpora
from gensim.models import LdaModel
from nltk.corpus import stopwords
from nltk.sentiment.vader import SentimentIntensityAnalyzer
from nltk.tokenize import word_tokenize
from sumy.nlp.stemmers import Stemmer
from sumy.nlp.tokenizers import Tokenizer
from sumy.parsers.plaintext import PlaintextParser
from sumy.summarizers.lsa import LsaSummarizer
from sumy.utils import get_stop_words
from wordcloud import WordCloud

from analyze.preprocessor import clean_text_list

nltk.download('vader_lexicon')
nltk.download('stopwords')
nltk.download('punkt')


def get_highlights(text, sentences_count):
    parser = PlaintextParser.from_string(text, Tokenizer("english"))
    stemmer = Stemmer('english')
    summarizer = LsaSummarizer(stemmer)
    summarizer.stop_words = get_stop_words('english')
    summary = summarizer(parser.document, sentences_count=sentences_count)
    return [str(sentence) for sentence in summary]


def make_word_cloud(text):
    wordcloud = WordCloud(width=800, height=400, background_color='white', min_word_length=4, max_words=70).generate(
        text)
    plt.figure(figsize=(10, 5))
    plt.imshow(wordcloud, interpolation='bilinear')
    plt.axis('off')  # Turn off the axis labels and ticks
    return wordcloud


def sentiment_score(lines):
    scores = []
    for text in lines:
        analyzer = SentimentIntensityAnalyzer()
        sentiment_scores = analyzer.polarity_scores(text)
        scores.append(sentiment_scores['compound'])
    return sum(scores) / len(scores)


def extract_probability_topics(topics):
    cleaned_values = []
    for topic in topics:
        probability = float(topic.split('*')[0])
        name = topic.split('*')[1][1:-1].replace("\"", '')
        cleaned_values.append({'p': probability, 'topic': name})
    return cleaned_values


def get_keywords(topics_prob):
    keyword_prob = []
    for i in topics_prob:
        topics_prob_list = i[1].split('+')

        cleaned_topic_prob = extract_probability_topics(topics_prob_list)
        keyword_prob.extend(cleaned_topic_prob)
    keyword_prob.sort(key=lambda x: x['p'], reverse=True)
    keywords = [item['topic'] for item in keyword_prob]
    return keywords


def get_keywords_domain(documents):
    topics_prob = get_str_topics(documents)
    keywords = get_keywords(topics_prob)
    domains = list(set(keywords[:5]))
    keywords = clean_text_list(keywords)
    return domains, keywords


def get_str_topics(documents):
    # Tokenize and preprocess the documents
    filtered_tokenized_documents = get_tokenize_docs(documents)
    # Create a dictionary and corpus for LDA
    dictionary = corpora.Dictionary(filtered_tokenized_documents)
    corpus = [dictionary.doc2bow(doc) for doc in filtered_tokenized_documents]
    # Train an LDA model
    lda_model = LdaModel(corpus, num_topics=5, id2word=dictionary, passes=50)
    # Print the top three topics
    topics_prob = lda_model.print_topics(num_topics=5, num_words=20)
    return topics_prob


def get_tokenize_docs(documents):
    stop_words = set(stopwords.words('english'))
    tokenized_documents = [
        [word for word in word_tokenize(doc.lower()) if word.isalnum() and word not in stop_words]
        for doc in documents
    ]
    # Calculate word frequencies
    word_frequencies = Counter(word for doc in tokenized_documents for word in doc)
    # Calculate the number of words to remove (top 0.1%)
    num_words_to_remove = int(0.001 * len(word_frequencies))
    # Identify the top 0.1% most frequent words to remove
    words_to_remove = [word for word, _ in word_frequencies.most_common(num_words_to_remove)]
    # Filter out high-frequency words from the tokenized documents
    filtered_tokenized_documents = [
        [word for word in doc if word not in words_to_remove]
        for doc in tokenized_documents
    ]
    return filtered_tokenized_documents


def concat_lines(lines):
    full_text = ''
    for line in lines:
        if len(line) > 1 and line[- 1] != '.':
            line += '.'
        full_text += ' ' + line
    return full_text


class DocumentsPreProcessor:

    def __init__(self, documents):
        flat_lines_documents = list(chain(*documents))
        full_text = concat_lines(flat_lines_documents)
        sentences_for_consideration = int(len(flat_lines_documents) / 2)
        important_lines = list(set(get_highlights(text=full_text, sentences_count=sentences_for_consideration)))
        self.sentiment_analysis_input = important_lines
        self.highlights_input = ' '.join(important_lines)
        self.topic_modeling_input = clean_text_list(important_lines)
        self.word_cloud_input = ' '.join(self.topic_modeling_input)
