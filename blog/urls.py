from django.urls import path
from .views import blog, single_blog

app_name = 'blog'

urlpatterns = [
    path('blog/', blog, name='blog-page'),
    path('single-blog/', single_blog, name='single-blog')
]
