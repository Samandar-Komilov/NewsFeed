from django.db import models
from django.urls import reverse
from django.utils import timezone
from django.contrib.auth.models import User

class Category(models.Model):
  name = models.CharField(max_length=50)
  
  def __str__(self):
    return self.name
  


class News(models.Model):
  class Status(models.TextChoices):
    Draft = "DF","Draft"
    Published = "PB","Published"
  
  title = models.CharField(max_length=250)
  slug = models.SlugField(max_length=250)
  body = models.TextField(blank=False)
  image = models.ImageField(upload_to='news/images')
  category = models.ForeignKey(Category, on_delete=models.CASCADE) # CaSCADE vazifasi masalan shu kategoriya ochib ketsa, unga bog'langan postlar ham ochib ketadi
  publish_time = models.DateTimeField(default=timezone.now)
  created_time = models.DateTimeField(auto_now_add=True)
  updated_time = models.DateTimeField(auto_now=True)
  status = models.CharField(max_length=2, 
                            choices=Status.choices,
                            default=Status.Draft)
  # view_count = models.IntegerField(default=0)
  class Meta:
    ordering = ["-publish_time"]  # Teskari tartiblash: - belgisi oxirgi published postni eng yuqorida korsatib turadi. Agar - bolmasa oz tartibida
  def __str__(self):
      return self.title
  
  def get_absolute_url(self):
      return reverse("news_detail", args=[self.slug])
  
  
# Contact
class Contact(models.Model):
  name = models.CharField(max_length=60, blank=False)
  email = models.EmailField(max_length=254)
  message = models.TextField()
  def __str__(self):
      return self.email
  

# Comment model
class Comment(models.Model):
  news = models.ForeignKey(News,
                          on_delete=models.CASCADE,
                          related_name='comments') 
  user = models.ForeignKey(User,
                          on_delete=models.CASCADE,
                          related_name='comments')
  body = models.TextField()
  created_time = models.DateTimeField(auto_now_add=True)
  active = models.BooleanField(default=True)

  class Meta:
    ordering = ['created_time']

  def __str__(self):
     return f"Comment - {self.body} by {self.user}"


"""
>>> related_name => hozir comment > news qilyapmiz, news > comment holatida ham qilish imkonini beradi.
News > related_name > Comment - qanday bolishini tushunamiz:
> news1 = News.objects.get(id=5)
> news1.comments.all()
-----
> user1 = User.objects.get(id=6)
> user1.comments.all()
"""