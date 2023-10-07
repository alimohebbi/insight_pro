from django.apps import AppConfig



class AnalyzeConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'analyze'

    def ready(self):
        from analyze.recommender import Recommender
        Recommender.init_recommender()
