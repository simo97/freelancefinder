"""Pages relating to the jobs app."""

from django.db.models import Q
from django.views.generic import ListView
from django.views.generic.detail import DetailView
from django.views.generic.edit import FormMixin

from .forms import PostFilterForm, JobSearchForm
from .models import Job, Post


class FormGetMixin(FormMixin):
    """FormMixin which uses GET request data."""

    def get_form_kwargs(self):
        """Pull field values from GET data."""
        kwargs = {'initial': self.get_initial(), 'data': self.request.GET}
        return kwargs


class JobListView(ListView, FormGetMixin):
    """List all jobs."""

    model = Job
    paginate_by = 20
    form_class = JobSearchForm
    template_name = "jobs/job_list.html"

    def get_queryset(self):
        """Queryset should sort by desc created by default."""
        search = self.request.GET.get('search', None)
        tag = self.request.GET.get('tag', None)
        querys = Job.objects.all()
        if search is not None:
            querys = querys.filter(Q(title__icontains=search) | Q(description__icontains=search))
        if tag is not None:
            querys = querys.filter(tags__name__in=[tag]).distinct()
        return querys.order_by('-created')

    def get_context_data(self, **kwargs):
        """Include search/filter form."""
        context = super(JobListView, self).get_context_data(**kwargs)

        context['form'] = self.get_form()

        return context


class JobDetailView(DetailView):
    """Show a single job."""

    model = Job
    template_name = 'jobs/job_detail.html'


class PostListView(FormMixin, ListView):
    """List all Posts."""

    model = Post
    paginate_by = 20
    form_class = PostFilterForm
    template_name = "jobs/post_list.html"

    def get_form_kwargs(self):
        """Use GET for form info."""
        kwargs = {'initial': self.get_initial(), 'data': self.request.GET}
        return kwargs

    def get_queryset(self):
        """Queryset should sort by desc created by default."""
        title = self.request.GET.get('title', None)
        is_job_posting = self.request.GET.get('is_job_posting', False)
        is_freelance = self.request.GET.get('is_freelance', False)
        querys = Post.objects.all()
        if is_job_posting:
            querys = querys.filter(is_job_posting=True)
        if is_freelance:
            querys = querys.filter(is_freelance=True)
        if title is not None:
            querys = querys.filter(title__icontains=title)
        return querys.order_by('-created')

    def get_context_data(self, **kwargs):
        """Include search/filter form."""
        context = super(PostListView, self).get_context_data(**kwargs)

        context['form'] = self.get_form()

        return context
