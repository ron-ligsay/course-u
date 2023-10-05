from django.shortcuts import render
from django.shortcuts import get_object_or_404
from .models import JobPosting
from django.utils.safestring import mark_safe
# Create your views here.
#########################################################################
# ----------------------------for job--------------------------------- #
#########################################################################
# def job_list(request):
#     job_postings = JobPosting.objects.all()
#     return render(request, 'job_list.html', {'job_postings': job_postings})

def job_list(request, job_id=None):
    job_postings = JobPosting.objects.all()
    selected_job = None

    if job_id:
        selected_job = get_object_or_404(JobPosting, pk=job_id)

    selected_job.job_description = mark_safe(selected_job.job_description)

    return render(request, 'job/job_list.html', {'job_postings': job_postings, 'selected_job': selected_job})

def job_detail(request, job_id):
    job_posting = JobPosting.objects.get(pk=job_id)
    return render(request, 'job/job_detail.html', {'job_posting': job_posting})