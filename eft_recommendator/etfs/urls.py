from django.urls import path, include
from . import views

app_name = "etfs"

urlpatterns = [
    path("update/", views.UpdateView.as_view(), name="update"),
    path("update/sucess", views.UpdateSuccessView.as_view(), name="update_success"),
    path("", views.StartView.as_view(), name="start"),
    path("user/creation", views.BasicUserCreateView.as_view(), name="create_user"),
    path("user/update/<int:pk>", views.BasicUserUpdateView.as_view(), name="update_user"),
    path("user/recommendations/<int:pk>", views.BasicUserDetailView.as_view(), name="user_detail"),
    path("summary/", views.EtfSummaryView.as_view(), name="etfs_summary"),
    path("search/", views.SearchView.as_view(), name="etf_search"),
    path("<ticker>/", views.EtfDetailView.as_view(), name="etf_detail")
]