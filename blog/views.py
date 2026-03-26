from django.views.generic import ListView, DetailView
from core.i18n_utils import interface_language
from .models import Post

# الـ slug يُنشأ تلقائياً من العنوان في Post.save() إذا تُرك فارغاً — لا يلزم منطق إضافي في العروض.


class PostListView(ListView):
    model = Post
    template_name = 'blog/posts_list.html'
    context_object_name = 'posts'

    def get_queryset(self):
        lang = interface_language(self.request)
        qs = Post.objects.filter(is_published=True, language=lang).order_by('-created_at')
        if not qs.exists():
            return Post.objects.filter(is_published=True).order_by('-created_at')
        return qs

class PostDetailView(DetailView):
    model = Post
    template_name = 'blog/post_detail.html'
    context_object_name = 'post'
    slug_field = 'slug'
    slug_url_kwarg = 'slug'

    def get_queryset(self):
        return Post.objects.filter(is_published=True)
