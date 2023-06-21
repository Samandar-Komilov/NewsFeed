from django.urls import path
from . import views

urlpatterns = [
    path('', views.HomePageView.as_view(), name='home_page'),
    path('contact/', views.contactPageView, name='contact_page'),
    path('about/', views.aboutPageView, name='about_page'),
    path('404/',views.Page404View, name='404_page'),
    path('news/', views.news_list, name='news_list'),
    path('news/<slug:news>/', views.news_detail, name='news_detail'),
    path('local-news/',views.LocalNewsView.as_view(),name='local_news_page'),
    path('global-news/',views.GlobalNewsView.as_view(),name='global_news_page'),
    path('sport-news/',views.SportNewsView.as_view(),name='sport_news_page'),
    path('tech-news/',views.TechNewsView.as_view(), name='tech_news_page'),
]
