from django.views.generic import TemplateView

class IndexPage(TemplateView):
    template_name = "index.html"

class AboutPage(TemplateView):
    template_name = "about.html"