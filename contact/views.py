from django.views.generic import FormView
from .forms import ContactForm
from .models import ContactMessage
from django.urls import reverse_lazy

class ContactFormView(FormView):
    template_name = 'contact/contact_form.html'
    form_class = ContactForm
    success_url = reverse_lazy('contact_form')  # بعد الإرسال يرجع نفس الصفحة

    def form_valid(self, form):
        # حفظ الرسالة
        ContactMessage.objects.create(
            name=form.cleaned_data['name'],
            email=form.cleaned_data['email'],
            subject=form.cleaned_data['subject'],
            message=form.cleaned_data['message']
        )
        return super().form_valid(form)
