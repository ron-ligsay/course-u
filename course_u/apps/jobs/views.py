from django.shortcuts import render
from django.shortcuts import get_object_or_404

from django.utils.safestring import mark_safe
from django.core import serializers
from .models import JobPosting
from apps.website.models import Field

# def job_list(request, field_id=None, job_id=None):
#     # get object of field_id
#     field = None
#     if field_id:
#         field = get_object_or_404(Field, field=field_id)

#     job_postings = None
#     if field_id:
#         job_postings = JobPosting.objects.filter(field_id=field_id)
#     else:
#         job_postings = JobPosting.objects.all()
    
#     # filter to 12 only and random
#     job_postings = job_postings.order_by('?')[:12]
    
#     selected_job = get_object_or_404(JobPosting, pk=1)

#     if job_id:
#         selected_job = get_object_or_404(JobPosting, pk=job_id)

#     selected_job.job_description = mark_safe(selected_job.job_description)

#     return render(request, 'job/job_list.html', {
#         'job_postings': job_postings, 'selected_job': selected_job, 'field': field
#         })

def job_list(request, field_id=None, job_id=None):
    # get object of field_id
    field = None
    if field_id:
        field = get_object_or_404(Field, field=field_id)

    job_postings = None
    if ('job_postings' not in request.session or not request.session['job_postings'] or
        'field_id' not in request.session or request.session['field_id'] != field_id):
        if field_id:
            job_postings = JobPosting.objects.filter(field_id=field_id)
        else:
            job_postings = JobPosting.objects.all()

        # filter to 12 only and random
        job_postings = job_postings.order_by('?')[:12]
        job_postings_json = serializers.serialize('json', job_postings)

        request.session['job_postings'] = job_postings_json
        request.session['field_id'] = field_id
    else:
        job_postings_json = request.session['job_postings']
        job_postings = [obj.object for obj in serializers.deserialize('json', job_postings_json)]

    selected_job = get_object_or_404(JobPosting, pk=1)

    if job_id:
        selected_job = get_object_or_404(JobPosting, pk=job_id)

    selected_job.job_description = mark_safe(selected_job.job_description)

    return render(request, 'job/job_list.html', {
        'job_postings': job_postings, 'selected_job': selected_job, 'field': field
    })