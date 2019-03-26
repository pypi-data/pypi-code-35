from django.urls import path
from .feeds import PostListFeed, PostDetailFeed
from .views import PostListView, PostDetailView


urlpatterns = (
    path('', PostListView.as_view(), name='blog_post_list'),
    path('feed/', PostListFeed(), name='blog_post_feed'),
    path('tag/<slug:tag>/', PostListView.as_view(), name='blog_post_list_tagged'),
    path('tag/<slug:tag>/feed/', PostListFeed(), name='blog_post_feed_tagged'),
    path('category/<slug:category>/', PostListView.as_view(), name='blog_post_list_categorised'),
    path('category/<slug:category>/feed/', PostListFeed(), name='blog_post_feed_categorised'),
    path('<int:pk>/', PostDetailView.as_view(), name='blog_post_detail'),
    path('<int:pk>/feed/', PostDetailFeed(), name='blog_post_detail_feed')
)
