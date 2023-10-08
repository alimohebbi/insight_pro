# Insight Pro

Insight Pro (Insight Provider) is a web service that provides information about culture and environment of companies
based
on their
website.
The service receives the web address of a company, then it visits the company's web pages, analyze the text by NLP
techniques,
and returns valuable insights.

## Online Availability

The current version of the service is available at [www.insight-pro.info](https://www.insight-pro.info).

## Overview

This project provides useful information about companies in following groups:

- **Sentiment Analysis:** categorizes information on the website of a company as positive, negative, or
  neutral. Sentiment analysis scores textual information and higher scores are associated with innovation, customer-
  centric attitudes, and high moral attributes. The service gives an interpretation of the score and the rank of the
  company among
  available companies in the database.
- **Highlights:** includes keywords of the company as a word cloud, and the top five most noticeable statements. The
  service selects the statement by a *Statistical Summarization* technique.
- **Domain of Focus:** encompasses technical directions, or higher level
  abstract objectives of the company. The service uses a *Topic Modeling* technique to infer the domains.
- **Similar Companies:** suggests the most similar companies to the target company. Knowing the competitors of a company
  reveals information about the company and its characteristics. The service suggest the similar companies based on a "
  *Item-Based Collaborative* recommender system.
- **Leaderboard:** retrieves ten companies that gained the highest sentiment score.

## Installing

The web service requires a host that includes python3.9. You can run the service by following below steps:

1. Install dependencies:
    ```
   pip install -r requirments
   ```
2. Generate Django secret key using the code below in python. Then, add it
   to [secret_template.py](web_insight/secret_template.py), and rename the file
   to `secret.py`.
    ```
   import secrets
    secret_key = secrets.token_hex(50)
    print(secret_key)
   ```
3. Set the path to python in [settings.py](web_insight/settings.py).
4. Create Django tables.
    ```
    python manage.py makemigrations analyze
    python manage.py migrate analyze
    python manage.py makemigrations
    python manage.py migrate
    ```
5. Collect static files.
   ```
   python manage.py collectstatic
   ```
6. Run the server.
   ```
   python manage.py runserver
   ```
