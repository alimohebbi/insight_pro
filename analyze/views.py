# Create your views here.
import json
import subprocess
from urllib.parse import urlparse, urlunparse

from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.shortcuts import render
from django.template import loader

from .forms import WebURLForm
from .models import Insight
from .nlp_tasks import get_highlights, sentiment_score


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


def results(request, website_id):
    insight = Insight.objects.get(id=website_id)
    top3_companies = Insight.objects.order_by('-sentiment_score')[:3]
    top3_companies_names = [(company.website_url, round(company.sentiment_score, 3)) for company in
                            top3_companies]
    company_sentiment_rank = Insight.objects.filter(sentiment_score__gt=insight.sentiment_score).count() + 1
    template = loader.get_template("analyze/results.html")
    context = {
        "insight": insight,
        "top_companies": top3_companies_names,
        'sentiment_rank': company_sentiment_rank
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
            insight_id = get_or_create_insight(target_url)
            response_data = {'message': 'ok', 'insight_id': insight_id}
            return JsonResponse(response_data)
        except json.JSONDecodeError:
            return JsonResponse({'message': 'Invalid JSON data'}, status=400)

    return JsonResponse({'message': 'Invalid request method'}, status=400)


def get_or_create_insight(target_url):
    try:
        insight_obj = Insight.objects.get(website_url=target_url)
    except Insight.DoesNotExist:
        scrap_website(target_url)
        insight = analyze_info()
        insight_obj = Insight(website_url=target_url, sentiment_score=insight['score'],
                              highlights=insight['highlights'])
        insight_obj.save()
    return insight_obj.id


def scrap_website(target_url) -> None:
    result = subprocess.run(
        ["/Users/usiusi/Documents/Repositories/web_insight/venv/bin/python", "analyze/scraper.py", target_url],
        stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True)


def analyze_info() -> dict:
    lines = []
    delimiter = '.\r'
    with open("scrapy_dump.txt", "r") as file:
        for line in file:
            lines.append(line.strip())

    full_text = delimiter.join(lines)

    highlights = get_highlights(text=full_text)
    score = sentiment_score(lines)

    return {'score': score, 'highlights': highlights}



def normalize_url(url):
    parsed_url = urlparse(url)

    if not parsed_url.scheme or parsed_url.scheme not in ('http', 'https'):
        scheme = 'https'
    else:
        scheme = parsed_url.scheme
    normalized_url = urlunparse((scheme, parsed_url.netloc, parsed_url.path,
                                 parsed_url.params, parsed_url.query, parsed_url.fragment))
    return str(normalized_url).replace('www.','')

