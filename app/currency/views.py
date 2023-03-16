from django.contrib.auth import get_user_model
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, DetailView, UpdateView, DeleteView

from currency.models import Rate, ContactUs, Source
from currency.forms import RateForm, ContactUsForm, SourceForm


class RatesListView(ListView):
    queryset = Rate.objects.all()
    template_name = 'list_rates.html'


class RateDetailView(LoginRequiredMixin, DetailView):
    queryset = Rate.objects.all()
    template_name = 'rate_details.html'


class RateCreateView(CreateView):
    form_class = RateForm
    template_name = 'rate_create.html'
    success_url = reverse_lazy('currency:rate-list')


class RateUpdateView(UserPassesTestMixin, UpdateView):
    def test_func(self):
        if self.request.user.is_superuser:
            return True

    form_class = RateForm
    template_name = 'rate_update.html'
    success_url = reverse_lazy('currency:rate-list')
    queryset = Rate.objects.all()


class RateDeleteView(UserPassesTestMixin, DeleteView):
    def test_func(self):
        if self.request.user.is_superuser:
            return True

    queryset = Rate.objects.all()
    template_name = 'rate_delete.html'
    success_url = reverse_lazy('currency:rate-list')


class MessagesListView(ListView):
    queryset = ContactUs.objects.all()
    template_name = 'list_message.html'


class MessageDetailView(DetailView):
    queryset = ContactUs.objects.all()
    template_name = 'message_details.html'


class MessageCreateView(CreateView):
    form_class = ContactUsForm
    template_name = 'message_create.html'
    success_url = reverse_lazy('currency:message-list')

    def _send_mail(self):
        subject = 'User Contact Us'
        recipient = 'support@example.com'
        message = f'''
            Request from: {self.object.name}
            Reply to email: {self.object.email_from}
            Subject: {self.object.subject}
            Body: {self.object.message}
        '''

        from django.core.mail import send_mail
        send_mail(
            subject,
            message,
            recipient,
            [recipient],
            fail_silently=False,
        )

    def form_valid(self, form):
        redirect = super().form_valid(form)
        self._send_mail()
        return redirect


class MessageUpdateView(UpdateView):
    form_class = ContactUsForm
    template_name = 'message_update.html'
    success_url = reverse_lazy('currency:message-list')
    queryset = ContactUs.objects.all()


class MessageDeleteView(DeleteView):
    queryset = ContactUs.objects.all()
    template_name = 'message_delete.html'
    success_url = reverse_lazy('currency:message-list')


class SourcesListView(ListView):
    template_name = 'list_sources.html'
    queryset = Source.objects.all()


class SourceDetailView(DetailView):
    queryset = Source.objects.all()
    template_name = 'source_details.html'


class SourceCreateView(CreateView):
    form_class = SourceForm
    template_name = 'source_create.html'
    success_url = reverse_lazy('currency:source-list')


class SourceUpdateView(UpdateView):
    form_class = SourceForm
    template_name = 'source_update.html'
    success_url = reverse_lazy('currency:source-list')
    queryset = Source.objects.all()


class SourceDeleteView(DeleteView):
    queryset = Source.objects.all()
    template_name = 'source_delete.html'
    success_url = reverse_lazy('currency:source-list')


class ProfileView(LoginRequiredMixin, UpdateView):
    template_name = 'registration/profile.html'
    success_url = reverse_lazy('index')
    queryset = get_user_model().objects.all()
    fields = (
        'first_name',
        'last_name'
    )

    def get_object(self, queryset=None):
        return self.request.user
