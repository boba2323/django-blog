from django import template
from ..models import BlogPost
register = template.Library()

@register.inclusion_tag("blogapp/recently_viewed_posts.html", takes_context=True)
def show_recently_views_posts(context):
    request = context['request']
    recently_viewed_ids = request.session.get('recently_viewed', [])
    recently_viewed_posts = BlogPost.objects.filter(id__in=recently_viewed_ids)
    recently_viewed_posts = sorted(recently_viewed_posts, key=lambda post:recently_viewed_ids.index(post.id))
    print("tag", recently_viewed_posts)
    return {'recently_viewed_posts': recently_viewed_posts}