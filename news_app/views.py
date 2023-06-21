from django.http import HttpResponse
from django.views.generic import TemplateView, ListView
from django.shortcuts import render, get_object_or_404
from .models import News, Category
from .forms import ContactForm

def news_list(request):
  news_list = News.objects.filter(status=News.Status.Published)
  context = {'news_list':news_list}
  
  return render(request, 'news/news_list.html', context=context)

def news_detail(request, news):
  news = get_object_or_404(News, slug=news, status=News.Status.Published)
  context = {
    'news':news,
  }
  return render(request, 'news/news_detail.html', context)

# ---

def homePageView(request):
  news = News.objects.filter(status=News.Status.Published).order_by('-publish_time')[1:5]
  world_one = News.objects.filter(status=News.Status.Published).filter(category__name="Jahon").order_by("-publish_time")[0]
  world_news = News.objects.filter(status=News.Status.Published).filter(category__name="Jahon").order_by("-publish_time")[:5]
  categories = Category.objects.all()
  context = {
    'news':news,
    'categories':categories,
    'world_one':world_one,
    'world_news':world_news,
  }
  return render(request, 'news/home.html',context)

class HomePageView(ListView):
  model = News
  template_name = "news/home.html"
  context_object_name = 'news'

  def get_context_data(self, **kwargs):
      context = super().get_context_data(**kwargs) # Class which was inherited from ListView is overriding here
      context["categories"] = Category.objects.all()
      context["news"] = News.objects.filter(status=News.Status.Published).order_by('-publish_time')[:5]
      context['world_news'] = News.objects.filter(status=News.Status.Published).filter(category__name="Jahon").order_by("-publish_time")[:5]
      context['sport_news'] = News.objects.filter(status=News.Status.Published).filter(category__name="Sport").order_by("-publish_time")[:5]
      context['tech_news'] = News.objects.filter(status=News.Status.Published).filter(category__name="Fan-texnika").order_by("-publish_time")[:5]
      context['uzb_news'] = News.objects.filter(status=News.Status.Published).filter(category__name="O'zbekiston").order_by("-publish_time")[:5]
      return context
  

def aboutPageView(request):
  return render(request, 'news/about.html')

# 404 Page
def Page404View(request):
  return render(request, 'news/404.html')



# CONTACT

def contactPageView(request):
  form = ContactForm(request.POST or None)
  if request.method == "POST" and form.is_valid():
    form.save()
    return HttpResponse("<h2>Thank you for contacting us!</h2>")
  context = {
    'form':form,
  }
  return render(request, 'news/contact.html', context)

# def ContactPageView(TemplateView):
#   template_name = 'news/contact.html'
#   def get(self, request, *args, **kwargs):
#     form = ContactForm()
#     context = {'form':form}
#     return render(request, 'news/contact.html', context)
#   def post(self, request, *args, **kwargs):
#     form = ContactForm(request.POST)
#     if request.method == "POST" and form.is_valid():
#       form.save()
#       return HttpResponse("<h2>Thank you for contacting us!</h2>")
#     context = {'form':form}
#     return render(request, 'news/contact.html', context)


# Create models for categories in Navbar
class LocalNewsView(ListView):
  model = News
  template_name = 'news/local.html'
  context_object_name = 'local_news'

  def get_queryset(self):
      news = self.model.objects.filter(status=News.Status.Published).filter(category__name = "O'zbekiston")
      return news
  

class GlobalNewsView(ListView):
  model = News
  template_name = 'news/global.html'
  context_object_name = 'global_news'
  
  def get_queryset(self):
      news = self.model.objects.filter(status=News.Status.Published).filter(category__name = "Jahon")
      return news

class SportNewsView(ListView):
  model = News
  template_name = 'news/sport.html'
  context_object_name = 'sport_news'
  
  def get_queryset(self):
      news = self.model.objects.filter(status=News.Status.Published).filter(category__name = "Sport")
      return news

class TechNewsView(ListView):
  model = News
  template_name = 'news/tech.html'
  context_object_name = 'tech_news'
  
  def get_queryset(self):
      news = self.model.objects.filter(status=News.Status.Published).filter(category__name = "Fan-texnika")
      return news