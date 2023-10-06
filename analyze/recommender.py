import numpy as np
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

from analyze.models import Company


class Recommender:
    tfidf_vectorizer = None
    companies_tfidf_matrix = None
    companies_ids = None

    @classmethod
    def init_vectorizer(cls):
        corpus = pd.read_csv('analyze/preprocessed-small.csv')
        tfidf_vectorizer = TfidfVectorizer(use_idf=True, max_features=5000)
        cls.tfidf_vectorizer = tfidf_vectorizer.fit(corpus['description'])

    @classmethod
    def build_tfidf_matrix(cls):
        companies = Company.objects.all()
        companies_keywords_list = [' '.join(company.keywords) for company in companies]
        cls.companies_ids = [company.id for company in companies]
        cls.companies_tfidf_matrix = cls.tfidf_vectorizer.transform(companies_keywords_list)

    @classmethod
    def get_similar_companies_id(cls, target_company):
        keyword_list = [' '.join(target_company.keywords)]
        target_company_tfidf_matrix = cls.tfidf_vectorizer.transform(keyword_list)
        cosine_sim = cosine_similarity(target_company_tfidf_matrix, cls.companies_tfidf_matrix)
        target_item_index = 0
        similar_items = cosine_sim[target_item_index].argsort()[::-1][1:4]  # Exclude the target item
        similar_companies_id = [cls.companies_ids[item_index] for item_index in similar_items]
        return similar_companies_id

    @classmethod
    def init_recommender(cls):
        cls.init_vectorizer()
        cls.build_tfidf_matrix()

    @classmethod
    def update_tfidf_matrix(cls):
        cls.build_tfidf_matrix()


Recommender.init_recommender()


def find_similar_companies(target_company):
    similar_companies_id = Recommender.get_similar_companies_id(target_company)
    similar_companies = [Company.objects.get(id=company_id) for company_id in similar_companies_id]
    return similar_companies
