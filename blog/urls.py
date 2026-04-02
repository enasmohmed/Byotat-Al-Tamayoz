from django.urls import path, re_path

from .views import PostListView, PostDetailView


urlpatterns = [
    path("", PostListView.as_view(), name="posts_list"),
    # Default <slug:> allows only [-a-zA-Z0-9_]+ — breaks Arabic slugs (allow_unicode on the model).
    re_path(r"^(?P<slug>[^/]+)/$", PostDetailView.as_view(), name="post_detail"),
]
