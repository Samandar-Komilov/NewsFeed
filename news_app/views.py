from django.db.models.query import QuerySet
from django.db.models import Q
from django.http import HttpResponse
from django.urls import reverse_lazy
from django.views.generic import TemplateView, ListView, CreateView, UpdateView, DeleteView
from django.shortcuts import render, get_object_or_404
from .models import News, Category
from .forms import CommentForm, ContactForm
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import User

from hitcount.utils import get_hitcount_model
from hitcount.views import HitCountMixin

def news_list(request):
  news_list = News.objects.filter(status=News.Status.Published)
  context = {'news_list':news_list}
  
  return render(request, 'news/news_list.html', context=context)



def news_detail(request, news):
  news = get_object_or_404(News, slug=news, status=News.Status.Published)

  # Hitcount section
  context = {}
  hit_count = get_hitcount_model().objects.get_for_object(news)
  hits = hit_count.hits
  hitcontext = context['hitcount']={'pk':hit_count.pk}
  hit_count_response = HitCountMixin.hit_count(request, hit_count)
  if hit_count_response.hit_counted:
    hits = hits + 1
    hitcontext['hit_counted'] = hit_count_response.hit_counted
    hitcontext['hit_message'] = hit_count_response.hit_message
    hitcontext['total_hits'] = hits
  # Dont worry if you didnt understand. This was written by devs for using directly with ClassViews but here we have function hence we wrote on hand

  # Comments section
  comments = news.comments.filter(active = True)
  comment_count = comments.count()
  new_comment = None
  if request.method == "POST":
    comment_form = CommentForm(data=request.POST)
    if comment_form.is_valid():
      # Create new comment object but not save in DB
      new_comment = comment_form.save(commit=False)
      new_comment.news = news # Bu qaysi postning kommenti ekanini bildirib qo'ydik
      new_comment.user = request.user # Bir user boshqasini nomidan yoza olmaydi, demak request egasi ekanini bildirish zarur
      # Save to DB
      new_comment.save()
      comment_form = CommentForm()
  else:
    comment_form = CommentForm()

  context = {
    'news':news,
    'comments':comments,
    'new_comment':new_comment,
    'comment_form':comment_form,
    'comment_count':comment_count,
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
  

# CRUD views
from news_project.custom_permissions import OnlyLoggedSuperUser

class NewsUpdateView(OnlyLoggedSuperUser,UpdateView):
  model = News
  fields = ('title','body','image','category','status', )
  template_name = 'crud/news_edit.html'

class NewsDeleteView(OnlyLoggedSuperUser,DeleteView):
  model = News
  fields = "__all__"
  template_name = 'crud/news_delete.html'
  success_url = reverse_lazy('home_page')  # Delete successful bolganda shu urlga direct qilinadi.

class NewsCreateView(OnlyLoggedSuperUser,CreateView):
  model = News
  fields = ('title', 'body', 'image', 'category', 'status', )
  template_name = 'crud/news_create.html'
  prepopulated_fields = {'slug':('title',)}
  login_url = 'login'

# Custom admin page
@login_required
@user_passes_test(lambda u:u.is_superuser) # Dekorator ichiga funksiya tiqib yuborish
def admin_page_view(request):
  admin_users = User.objects.filter(is_superuser = True)
  context = {
    'admin_users':admin_users,
  }
  return render(request, 'pages/admin_page.html',context)

# Search results View
class SearchResultsList(ListView):
  model = News
  template_name = 'news/search_result.html'
  context_object_name = 'all_news'

  # Q() orqali input nameni querysetdan qidiramiz:
  def get_queryset(self):
    query = self.request.GET.get('q')
    return News.objects.filter(
      Q(title__icontains = query) | Q(body__icontains = query)
    )