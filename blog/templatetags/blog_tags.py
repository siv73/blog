from blog.models import Post
from django import template
register = template.Library()



@register.simple_tag
def total_posts():
    # print('This loaded')
    return Post.objects.count()

# total_posts()

@register.inclusion_tag('blog/latest.html')
def show_latest_posts():
    # print('latest')
    latest_posts = Post.objects.all().order_by('-publish')[:3]
    print(len(latest_posts))
    return {'latest_posts':latest_posts}

from django.db.models import Count

@register.inclusion_tag('blog/latest.html')
def most_commented():
    return {'most':Post.objects.annotate(total_comments=Count('comments')).order_by('-total_comments')[:2]}

for p in most_commented():
    print(p.title)

 