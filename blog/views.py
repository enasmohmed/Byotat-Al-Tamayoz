from django.db.models import Q
from django.views.generic import DetailView, ListView

from core.i18n_utils import interface_language

from .models import BlogListPageSettings, Post, PostCategory


class PostListView(ListView):
    model = Post
    template_name = "blog/posts_list.html"
    context_object_name = "posts"
    paginate_by = 6

    def get_queryset(self):
        lang = interface_language(self.request)
        qs = (
            Post.objects.filter(is_published=True, language=lang)
            .select_related("category")
            .order_by("-created_at")
        )
        if not qs.exists():
            qs = (
                Post.objects.filter(is_published=True)
                .select_related("category")
                .order_by("-created_at")
            )
        category_slug = (self.request.GET.get("category") or "").strip()
        if category_slug:
            qs = qs.filter(category__slug=category_slug)
        q = (self.request.GET.get("q") or "").strip()
        if q:
            qs = qs.filter(
                Q(title__icontains=q)
                | Q(title_ar__icontains=q)
                | Q(title_en__icontains=q)
                | Q(content__icontains=q)
                | Q(content_ar__icontains=q)
                | Q(content_en__icontains=q)
                | Q(slug__icontains=q)
            )
        return qs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["blog_list_page"] = BlogListPageSettings.objects.first()
        context["blog_categories"] = PostCategory.objects.all().order_by("name")
        lang = interface_language(self.request)
        recent_qs = (
            Post.objects.filter(is_published=True, language=lang)
            .select_related("category")
            .order_by("-created_at")[:5]
        )
        if not recent_qs:
            recent_qs = (
                Post.objects.filter(is_published=True)
                .select_related("category")
                .order_by("-created_at")[:5]
            )
        context["sidebar_recent_posts"] = list(recent_qs)
        return context

class PostDetailView(DetailView):
    model = Post
    template_name = 'blog/post_detail.html'
    context_object_name = 'post'
    slug_field = 'slug'
    slug_url_kwarg = 'slug'

    def get_queryset(self):
        return Post.objects.filter(is_published=True).select_related("category")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["article_share_url"] = self.request.build_absolute_uri()
        context["article_share_title"] = context["post"].title
        return context
