import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

from analyze.models import Company


def create_vectorizer():
    corpus = pd.read_csv('analyze/preprocessed-small.csv')
    tfidf_vectorizer = TfidfVectorizer(use_idf=True, max_features=5000)
    tfidf_vectorizer.fit(corpus['description'])
    return tfidf_vectorizer


def get_tfidf_matrix_from_db(tfidf_vectorizer):
    companies = Company.objects.all()
    companies_keywords_list = [' '.join(company.keywords) for company in companies]
    companies_ids = [company.id for company in companies]
    companies_tfidf_matrix = tfidf_vectorizer.transform(companies_keywords_list)
    return companies_tfidf_matrix, companies_ids


def get_similar_companies_id(target_company_keyword: list, companies_tfidf_matrix, companies_ids, tfidf_vectorizer):
    target_company_tfidf_matrix = tfidf_vectorizer.transform(target_company_keyword)
    cosine_sim = cosine_similarity(target_company_tfidf_matrix, companies_tfidf_matrix)
    target_item_index = 0
    similar_items = cosine_sim[target_item_index].argsort()[::-1][1:4]  # Exclude the target item
    similar_companies_id = [companies_ids[item_index] for item_index in similar_items]
    return similar_companies_id


def fetch_similar_companies(similar_companies_id):
    # similar_companies = Company.objects.filter(id__in=similar_companies_id)
    similar_companies = [Company.objects.get(id=company_id) for company_id in similar_companies_id]
    return similar_companies


def find_similar_companies(target_company):
    keyword_list = [' '.join(target_company.keywords)]
    tfidf_vectorizer = create_vectorizer()
    companies_tfidf_matrix, companies_ids = get_tfidf_matrix_from_db(tfidf_vectorizer)
    similar_companies_id = get_similar_companies_id(keyword_list, companies_tfidf_matrix, companies_ids,
                                                    tfidf_vectorizer)
    if target_company.id in companies_ids:
        companies_ids.remove(target_company.id)

    return fetch_similar_companies(similar_companies_id)
