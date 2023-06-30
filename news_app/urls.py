from django.urls import path
from . import views

urlpatterns = [
    path('', views.HomePageView.as_view(), name='home_page'),
    path('contact/', views.contactPageView, name='contact_page'),
    path('about/', views.aboutPageView, name='about_page'),
    path('404/',views.Page404View, name='404_page'),
    path('news/', views.news_list, name='news_list'), 
    path("news/create/", views.NewsCreateView.as_view(), name="news_create"),
    path('news/<str:slug>/edit/', views.NewsUpdateView.as_view(), name='news_update'),
    path("news/<str:slug>/delete/", views.NewsDeleteView.as_view(), name='news_delete'),
    # Categories
    path('local-news/',views.LocalNewsView.as_view(),name='local_news_page'),
    path('global-news/',views.GlobalNewsView.as_view(),name='global_news_page'),
    path('sport-news/',views.SportNewsView.as_view(),name='sport_news_page'),
    path('tech-news/',views.TechNewsView.as_view(), name='tech_news_page'),
    path('search-results/',views.SearchResultsList.as_view(), name='search_results'),

    path('news/<slug:news>/', views.news_detail, name='news_detail'),
    # Custom Admin
    path('adminpage/', views.admin_page_view, name='admin_page'),
]
