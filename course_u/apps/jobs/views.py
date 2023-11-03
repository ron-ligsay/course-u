from django.shortcuts import render
from django.shortcuts import get_object_or_404

from django.utils.safestring import mark_safe

from .models import JobPosting


def job_list(request, job_id=None):
    job_postings = JobPosting.objects.all()
    selected_job = get_object_or_404(JobPosting, pk=1)

    if job_id:
        selected_job = get_object_or_404(JobPosting, pk=job_id)

    selected_job.job_description = mark_safe(selected_job.job_description)

    return render(request, 'job/job_list.html', {'job_postings': job_postings, 'selected_job': selected_job})
