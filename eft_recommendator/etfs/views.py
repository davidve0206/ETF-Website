from typing import Any
from django.forms.models import BaseModelForm
from django.http import HttpResponse
from django.shortcuts import render, HttpResponseRedirect
from django.urls import reverse
from django.contrib.auth.mixins import UserPassesTestMixin
from django.views.generic import View, CreateView, UpdateView, DetailView, TemplateView
from django.views.generic.edit import FormMixin
from . import models, forms
from .etfutils import etf_prices, risk_rating, etf_graphs

# Create your views here.

# Views for the user journey - first we require an email and then move on accordingly

class StartView(View):
    template_name = "etfs/start.html"
    
    def get(self, request, *args, **kwargs):
        if "user_email" in request.GET:
            input_email = request.GET.get("user_email")
            try:
                user = models.BasicUser.objects.get(email=input_email)
            except:
                request.session["email"] = input_email
                return HttpResponseRedirect(reverse("etfs:create_user"))
            else: 
                return HttpResponseRedirect(reverse("etfs:user_detail", kwargs={"pk": user.pk}))
        else:
            return render(request, self.template_name)

class BasicUserCreateView(CreateView, FormMixin):
    model = models.BasicUser
    template_name = "etfs/user_form.html"
    form_class = forms.BasicUserForm

    def get_initial(self) -> dict[str, Any]:
        initial = super().get_initial()
        initial["email"] = self.request.session["email"]
        return initial
    
    def form_valid(self, form: BaseModelForm) -> HttpResponse:
        self.object = form.save()
        risk_rating.get_recommended_etfs(self.object, models.Etf)
        return super().form_valid(form)

class BasicUserUpdateView(UpdateView):
    model = models.BasicUser
    template_name = "etfs/user_form.html"
    form_class = forms.BasicUserForm
    
    def form_valid(self, form: BaseModelForm) -> HttpResponse:
        self.object = form.save()
        risk_rating.get_recommended_etfs(self.object, models.Etf)
        return super().form_valid(form)

class BasicUserDetailView(DetailView):
    model = models.BasicUser
    template_name = "etfs/user_detail.html"
    context_object_name = "basic_user"
    
# Views for the ETFs

class EtfSummaryView(TemplateView):
    template_name = "etfs/etfs_summary.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["plot_div"] = etf_graphs.get_etf_summary_graph()
        return context

class EtfDetailView(DetailView):
    model = models.Etf
    template_name = "etfs/etf_detail.html"
    pk_url_kwarg = "ticker"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["plot_div"] = etf_graphs.get_etf_history_graph(self.object.ticker)
        return context
    
class SearchView(TemplateView):
    template_name = "etfs/search_results.html"
    
    def get(self, request, *args, **kwargs):
        search_value = request.GET.get("search", "")
        self.results = models.Etf.objects.filter(ticker__icontains=search_value)
        return super().get(self, request, *args, **kwargs)

    def get_context_data(self, **kwargs) -> dict[str, Any]:
        context = super().get_context_data(**kwargs)
        context["search_results"] = self.results
        return context
    

# Views to Update the ETF DB Tables

class UpdateView(UserPassesTestMixin, View):
    template_name = "etfs/update.html"

    def test_func(self):
        return self.request.user.is_superuser
    
    def get(self, request, *args, **kwargs):
        return render(request, self.template_name)

    def post(self, request, *args, **kwargs):
        if "run_script" in request.POST:
            etf_prices.get_etf_prices(models.Etf)
            return HttpResponseRedirect(reverse("etfs:update_success"))

class UpdateSuccessView(TemplateView):
    template_name = "etfs/update_success.html"

