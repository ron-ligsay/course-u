from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import Group
from django.contrib.auth.views import LogoutView
from django.contrib.sessions.models import Session
from django.contrib import messages
from django.urls import reverse
from django.http import HttpResponse 
from django.shortcuts import render
from django.contrib.auth.models import User


#from website.utils import *
from website.forms import SignUpForm, StudentScoreForm
from website.models import Specialization, Field
from utilities.decorators import unauthenticated_user, allowed_users, admin_only

from assessment.models import Test, QuestionSet
from jobs.models import JobPosting


# Other Imports
import json
import logging
import plotly.express as px

#logger = logging.getLogger(__name__)
logger = logging.getLogger("django") # name of logger : django


#@login_required(login_url='login_user')
#@allowed_users(allowed_roles=['admin','staff','student','instructor']) # only users on the list can access this page, ie. admin and staff
def home(request):
    logger.debug("User: " + str(request.user) + " is accessing home page")
    specialization_items = Specialization.objects.all()
    field_items = Field.objects.all()

    return render(request, 'home.html', {'specialization_items': specialization_items, 'field_items': field_items})


@allowed_users(allowed_roles=['admin','staff','student','instructor'])
def home_field(request, field_id=None):
    field_items = Field.objects.all()
    selected_field = None

    if field_id is not None:
        selected_field = get_object_or_404(Field, field=field_id)
        specialization_items = Specialization.objects.filter(field=selected_field)
        #messages.success(request, "specialization items is filtered")
    else:
        specialization_items = Specialization.objects.all()
        messages.success(request, "specialization items is not filtered")

    return render(request, 'specialization_list.html', {
        'specialization_items': specialization_items,
        'field_items': field_items,
        'selected_field': selected_field,
    })

#@login_required(login_url='login_user')
#@admin_only # only admin can access this page
def admin_home(request):
    #messages.success(request, 'You are in admin home')
    admin = True

    #TestQuestions = Test.objects.all()
    # get list of unique topic on TestQuestions
    topic_list = Test.objects.values('topic').distinct()
    topic_list = [item['topic'] for item in topic_list]

    # number of test, for each topic
    test_count = []
    for topic in topic_list:
        test_count.append(Test.objects.filter(topic=topic).count())
    
    # makie topic_list and test_count into a dictionary
    topic_list = dict(zip(topic_list, test_count))

    auth_user = User.objects.all()
    JobPosting_count = JobPosting.objects.all().count() 
    Specialization_count = Specialization.objects.all().count()
    QuestionSet_count = QuestionSet.objects.all().count()

    Field_items = Field.objects.all()


    return render(request, 'admin_home.html', {
        'admin': admin, 
        'topic_list' : topic_list, 
        'auth_user' : auth_user,
        'JobPosting_count' : JobPosting_count,
        'Specialization_count' : Specialization_count,
        'QuestionSet_count' : QuestionSet_count,
        'Field_items' : Field_items,
        })


def admin_students(request):
    auth_user = User.objects.all()
    return render(request, 'admin_students.html', {'auth_user': auth_user})


@unauthenticated_user # instead of adding if user.is_authenticated, use this decorator
def login_user(request):
    if request.method == 'POST':
        #email = request.POST['email']
        username=request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            messages.success(request, 'You have successfully logged in')
            return redirect('home')
        else:
            messages.success(request, 'Error logging in')
            return redirect('login_user')
    else:
        return render(request, 'user/login.html')

@unauthenticated_user
def sign_in(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password1')            
            user = authenticate(username=username, password=password)
            group = Group.objects.get(name='student')
            user.groups.add(group)
            login(request,user)
            messages.success(request, 'Student ' + username + ' have successfully created an account')
            return redirect('home')
    else:
        form = SignUpForm()
        return render(request, 'user/sign_in.html', {'form': form})
    
    # After successfully registering the user, trigger the signal
    # user = get_user_model().objects.get(username=new_user_username)
    # user_registered.send(sender=user)


    return render(request, 'user/sign_in.html', {'form': form})


def forgot_password(request):
    return render(request, 'user/forgot_password.html')


def recovery(request):
    return render(request, 'user/recovery.html')

def landing_page(request):
    return render(request, 'landing.html')



#########################################################################
# ------------------------for user module------------------------------ #
#########################################################################

@login_required  # Ensure that the user is logged in to access the profile
def user_profile(request):
    user = request.user
    # Query additional user profile data if using a custom user profile model
    context = {'user': user}
    return render(request, 'user/user_profile.html', context)

@login_required(login_url='login_user')
def edit_profile(request):
    user = request.user
    # Query additional user profile data if using a custom user profile model
    context = {'user': user}
    return render(request, 'user/user_profile.html', context)

@login_required(login_url='login_user')
def terms_and_conditions(request):
    user = request.user
    # Query additional user profile data if using a custom user profile model
    context = {'user': user}
    return render(request, 'user/user_profile.html', context)

@login_required(login_url='login_user')
def settings(request):
    user = request.user
    # Query additional user profile data if using a custom user profile model
    context = {'user': user}
    return render(request, 'user/user_profile.html', context)

class CustomLogoutView(LogoutView):
    template_name = 'user/custom_logout.html'  # Optionally, specify a custom logout template

    def get_next_page(self):
        # Customize the redirection logic if needed
        next_page = super().get_next_page()
        # You can add additional logic here if required
        return next_page


#########################################################################
# -----------------------for specialization---------------------------- #
#########################################################################


def specialization_page(request, item_id):
    # Retrieve the selected specialization item or return a 404 error if it doesn't exist
    specialization_item = get_object_or_404(Specialization, pk=item_id)

    # Render the specialization_page template with the item
    return render(request, 'specialization_page.html', {'specialization_item': specialization_item})



def admin_report(request):
    sets = QuestionSet.objects.all()
    username = request.GET.get('username')
    max_score = request.GET.get('max_score')
    min_score = request.GET.get('min_score')

    if username:
        sets = sets.filter(user__username__icontains=username)
    if max_score:
        sets = sets.filter(score__lte=max_score)
    if min_score:
        sets = sets.filter(score__gte=min_score)

    fig = px.bar(
        x=[set.set_id for set in sets],
        y=[set.score for set in sets],
        text=[set.user.username for set in sets],
        labels=dict(x="Set ID", y="Score", color="Set ID"),  
        title="Student Score",
    )

    fig.update_layout(title={
            'font_size': 22,
            'xanchor': 'center',
            'x': 0.5,
        })
    
    chart = fig.to_html()#full_html=False, include_plotlyjs=False

    context = {'chart': chart, 'form': StudentScoreForm()}
    return render(request, 'admin_report.html', context)