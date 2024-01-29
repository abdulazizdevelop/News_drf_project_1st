from django.db import models
from api.accounts.models import User

class News(models.Model):
   
    title = models.CharField(max_length = 255,)
    body = models.TextField()
    photo = models.ImageField(upload_to='news_img/', null=True, blank=True)
    author = models.ForeignKey(User,  on_delete = models.SET_NULL,  null = True,blank =True, related_name = 'news_user')
    
    def __str__(self):
        return self.title
