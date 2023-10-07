# Create your views here.
import json
import os
import subprocess

from django.conf import settings
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.shortcuts import render
from django.template import loader

from utils import normalize_url, url_to_filename
from .forms import WebURLForm
from .models import Company
from .nlp_tasks import get_highlights, sentiment_score, make_word_cloud, get_keywords_domain, DocumentsPreProcessor, \
    interpret_semantic_score
from .recommender import find_similar_companies, Recommender


def index(request):
    if request.method == 'POST':
        form = WebURLForm(request.POST)
        if form.is_valid():
            target_url = normalize_url(form.cleaned_data['target_url'])
            request.session['target_url'] = target_url
            return HttpResponseRedirect(f'/analyze/progress/')

        else:
            return render(request, 'analyze/index.html', {'form': form})

    form = WebURLForm()
    return render(request, 'analyze/index.html', {'form': form})


def results(request, company_id):
    company = Company.objects.get(id=company_id)
    similar_companies = find_similar_companies(company)
    top_companies_names = [(company.website_url, round(company.sentiment_score, 3), company.id) for company in
                           similar_companies]
    company_sentiment_rank = Company.objects.filter(sentiment_score__gt=company.sentiment_score).count() + 1
    template = loader.get_template("analyze/results.html")
    number_of_companies = Company.objects.count()
    semantic_score_inter = interpret_semantic_score(company.sentiment_score)
    context = {
        "company": company,
        "top_companies": top_companies_names,
        'sentiment_rank': company_sentiment_rank,
        'total_companies': number_of_companies,
        'semantic_score_inter':semantic_score_inter
    }

    return HttpResponse(template.render(context, request))


def leaderboard(request):
    top_companies_names = top_sentiment_companies()
    template = loader.get_template("analyze/leader_board.html")

    context = {
        "top_companies": top_companies_names,
    }

    return HttpResponse(template.render(context, request))




def progress(request):
    target_url = request.session.get('target_url')
    return render(request, 'analyze/progress.html', {'target_url': target_url})


def get_insight(request):
    if request.method == 'POST':
        # Get the JSON data from the request body
        try:
            data = json.loads(request.body)
            target_url = data.get('target_url')
            company_id = get_or_create_company(target_url)
            response_data = {'message': 'ok', 'company_id': company_id}
            return JsonResponse(response_data)
        except json.JSONDecodeError:
            return JsonResponse({'message': 'Invalid JSON data'}, status=400)
        except FileNotFoundError:
            return JsonResponse({'message': 'Cannot scrap the website'}, status=400)

    return JsonResponse({'message': 'Invalid request method'}, status=400)


def get_or_create_company(target_url):
    try:
        company = Company.objects.get(website_url=target_url)
    except Company.DoesNotExist:
        site_dump_path = settings.MEDIA_ROOT + '/documents/' + url_to_filename(target_url) + '.json'
        scrap_website(target_url, site_dump_path)
        insight = analyze_site_dump(target_url, site_dump_path)
        company = create_company(insight, target_url)
    return company.id


def create_company(insight, target_url):
    company = Company()
    company.website_url = target_url
    company.sentiment_score = insight['score']
    company.highlights = insight['highlights']
    company.domains = insight['domains']
    company.keywords = insight['keywords']
    company.word_cloud = insight['word_cloud_path']
    company.scrapped_documents = insight['site_dump_path']
    company.save()
    Recommender.update_tfidf_matrix()
    return company


def top_sentiment_companies():
    top_companies = Company.objects.order_by('-sentiment_score')[:10]
    top_companies_names = [(company.website_url, round(company.sentiment_score, 3), company.id) for company in
                           top_companies]
    return top_companies_names


def scrap_website(target_url, save_to) -> None:
    venv_python = os.path.join(settings.BASE_DIR, 'venv/bin/python')
    result = subprocess.run(
        [venv_python, "analyze/scraper.py", target_url, save_to],
        stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True)
    with open(save_to, 'r') as json_file:
        documents = json.load(json_file)
        if not documents:
            raise FileNotFoundError(f"The file '{save_to}' is empty.")


def analyze_site_dump(target_url, site_dump_path) -> dict:
    with open(site_dump_path, 'r') as json_file:
        documents = json.load(json_file)
    preprocessor = DocumentsPreProcessor(documents)

    score = sentiment_score(preprocessor.sentiment_analysis_input)
    highlights = list(set(get_highlights(text=preprocessor.highlights_input, sentences_count=5)))

    word_cloud = make_word_cloud(preprocessor.word_cloud_input)
    image_path = settings.MEDIA_ROOT + '/word_clouds/' + url_to_filename(target_url) + '.png'
    word_cloud.to_file(image_path)

    domains, keywords = get_keywords_domain(preprocessor.topic_modeling_input)

    image_url = 'word_clouds/' + url_to_filename(target_url) + '.png'
    dump_url = 'documents/' + url_to_filename(target_url) + '.json'
    return {'score': score,
            'highlights': highlights,
            'domains': domains,
            'keywords': keywords,
            'word_cloud_path': image_url,
            'site_dump_path': dump_url}
