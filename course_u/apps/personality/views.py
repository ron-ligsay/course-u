from django.shortcuts import render, redirect
from django.http import HttpResponse

from django.db.models import Q, Avg
from django.db.models import Max
from django.db import IntegrityError

# App imports
from apps.personality.models import  MBTI, MBTISet, MBTIResponse, Indicator

from apps.recommender.models import UserSkill

from django.db.models import Max

def initialize_mbti_test(request):
    user = request.user
    mbti_set = None  # Initialize the variable

    # get the last mbti_set_id
    #mbti_set_id = MBTISet.objects.all().aggregate(Max('mbti_set_id'))['mbti_set_id__max']    

    try:
        # get mbti_set of the user
        mbti_set = MBTISet.objects.filter(user=user).first()
    except Exception as e:
        print("Exception", e)
        # Handle other exceptions
        # You can take appropriate actions or return an error response
        # For example, you could redirect to an error page
        return HttpResponse("Failed to initialize MBTI test.")

    if mbti_set is None:
        # If it doesn't exist, create a new one
        mbti_set = MBTISet.objects.create(user=user, mbti_set_id=1, identity="AAAA")
        print("Created new mbti_set: ", mbti_set)
        # Create responses for all MBTI questions
        
    else:
        # use the existing user mbti_set_id
        mbti_set_id = mbti_set.mbti_set_id
        # renew mbtiresponses
        MBTIResponse.objects.filter(mbti_set=mbti_set).delete()
        print("Reset the previous mbti_set: ", mbti_set)
        # Create responses for all MBTI questions

    mbti_questions = MBTI.objects.all()
    for question in mbti_questions:
        MBTIResponse.objects.get_or_create(mbti_set=mbti_set, mbti=question)
    
    return redirect('mbti_test', mbti_set_id=mbti_set.pk)


    # if mbti_set_id is None:
    #     mbti_set_id = 1
    # else:
    #     mbti_set_id += 1
    
    print("mbti_set_id: ", mbti_set_id)
   
    # mbti_set = MBTISet.objects.create(user=user, mbti_set_id=mbti_set_id, identity="AAAA")

    # try:
    #     # Attempt to create a new MBTISet without explicitly setting the mbti_set_id
    #     mbti_set = MBTISet.objects.create(user=user, mbti_set_id=mbti_set_id)
        
    # except IntegrityError:
    #     print("IntegrityError", IntegrityError)
    #     # Handle the case where IntegrityError is raised (duplicate entry)
    #     # This means there is an existing set with the same mbti_set_id
    #     # You can handle this situation based on your application's logic
    #     # For example, you could generate a unique ID in a loop or display an error message
        
    #     # use the existing user mbti_set_id
    #     #mbti_set = MBTISet.objects.get(user=user, mbti_set_id=mbti_set_id)

    #     pass
    # except Exception as e:
    #     print("Exception", e)
    #     # Handle other exceptions
    #     # You can take appropriate actions or return an error response
    #     # For example, you could redirect to an error page
    #     return HttpResponse("Failed to initialize MBTI test.")

    if mbti_set is not None:
        # Create responses for all MBTI questions
        mbti_questions = MBTI.objects.all()
        for question in mbti_questions:
            MBTIResponse.objects.get_or_create(mbti_set=mbti_set, mbti=question)

        return redirect('mbti_test', mbti_set_id=mbti_set.pk)
    else:
        # Handle the case where mbti_set is None, e.g., if the IntegrityError was raised
        # You can take appropriate actions or return an error response
        # For example, you could redirect to an error page
        return HttpResponse("Failed to initialize MBTI test.")

    return redirect('mbti_test', mbti_set_id=mbti_set.pk)

def mbti_test(request, mbti_set_id):
    mbti_set = MBTISet.objects.get(pk=mbti_set_id)
    responses = MBTIResponse.objects.filter(mbti_set=mbti_set, is_answered=False)
    
    if request.method == 'POST':
        # Process user responses
        for response in responses:
            option = request.POST.get(f'question_{response.mbti_id}')
            if option:
                response.selected_option = int(option)
                response.is_answered = True
                response.save()
        
        # set id
        print("def mbti_test() mbti_set.id: ", mbti_set.mbti_set_id)
        # All questions answered, calculate personality
        calculate_personality(request.user, mbti_set.mbti_set_id)
        set_personality_skills(request.user, mbti_set.mbti_set_id)
        return redirect('mbti_results', mbti_set_id=mbti_set_id)

    return render(request, 'test/mbti_test.html', {'mbti_set': mbti_set, 'responses': responses})


def calculate_personality(user, mbti_set_id):
    #  # Try to get the user's existing MBTISet instance
    # mbti_set = MBTISet.objects.filter(user=user).first()
     # Get the MBTI set using the provided mbti_set_id
    mbti_set = MBTISet.objects.get(pk=mbti_set_id)
    if not mbti_set:
        # If it doesn't exist, create a new one
        mbti_set = MBTISet.objects.create(user=user, mind=0, energy=0, nature=0, tactics=0)

    print("def calculate_personality() mbti_set: ", mbti_set)
    print("def calculate_personality() mbti_set_id: ", mbti_set.pk)
    # number of objects
    print("MBTI.objects.count(): ", MBTI.objects.count())
    # Calculate mind, energy, nature, and tactics here
    # filter by id, from 1 to 5
    mbti_mind = MBTI.objects.filter(mbti__range=(1, 5))
    mbti_energy = MBTI.objects.filter(mbti__range=(6, 10))
    mbti_nature = MBTI.objects.filter(mbti__range=(11, 15))
    mbti_tactics = MBTI.objects.filter(mbti__range=(16, 20))
    print("mbti_mind: ", mbti_mind, "mbti_energy: ", mbti_energy, "mbti_nature: ", mbti_nature, "mbti_tactics: ", mbti_tactics)

    mind = MBTIResponse.objects.filter(mbti__in=mbti_mind, mbti_set=mbti_set)
    energy = MBTIResponse.objects.filter(mbti__in=mbti_energy, mbti_set=mbti_set)
    nature = MBTIResponse.objects.filter(mbti__in=mbti_nature, mbti_set=mbti_set)
    tactics = MBTIResponse.objects.filter(mbti__in=mbti_tactics, mbti_set=mbti_set)
    print("mind: ", mind, "energy: ", energy, "nature: ", nature, "tactics: ", tactics)

    # get average of selected_option
    mind = mind.aggregate(average_rating=Avg('selected_option'))['average_rating']
    energy = energy.aggregate(average_rating=Avg('selected_option'))['average_rating']
    nature = nature.aggregate(average_rating=Avg('selected_option'))['average_rating']
    tactics = tactics.aggregate(average_rating=Avg('selected_option'))['average_rating']
    print("mind: ", mind, "energy: ", energy, "nature: ", nature, "tactics: ", tactics)
    
    # Update the user's MBTI set instance with the calculated values
    mbti_set.mind = mind
    mbti_set.energy = energy
    mbti_set.nature = nature
    mbti_set.tactics = tactics
    mbti_set.save()

    # Determine the personality type and update the user's MBTI instance
    personality_type = ''
    if mind >= 0:
        personality_type += 'I'
    else:
        personality_type += 'E'
    if energy >= 0:
        personality_type += 'N'
    else:
        personality_type += 'S'
    if nature >= 0:
        personality_type += 'F'
    else:
        personality_type += 'T'
    if tactics >= 0:
        personality_type += 'P'
    else:
        personality_type += 'J'
    print("Personality Type: ", personality_type)
    mbti_set.identity = personality_type

    # get the indicator
    try:
        indicator = Indicator.objects.get(indicator=personality_type)
        print("indicator: ", indicator)
    except Exception as e:
        print("Exception", e)
        # Handle other exceptions
        # You can take appropriate actions or return an error response
        # For example, you could redirect to an error page
        print("Failed to get indicator.")
    
    if indicator is not None:
        mbti_set.indicator = indicator
    else:
       # get the indicator
        try:
            indicator = Indicator.objects.get(indicator=personality_type)
            print("indicator: ", indicator)
        except Exception as e:
            print("Exception", e)
            # Handle other exceptions
            # You can take appropriate actions or return an error response
            # For example, you could redirect to an error page
            print("Failed to get indicator.")

    # marks as completed
    mbti_set.is_completed = True
    mbti_set.save()

def set_personality_skills(request, mbti_set_id):
    # get user_id
    user_id = request.id
    
    # get indicator
    mbti_set = MBTISet.objects.get(pk=mbti_set_id)
    indicator = mbti_set.indicator
    # get indicator skills
    skills = indicator.skills.all()
    # loop through skills
    for skill in skills:
        level = 3
        # get or create UserSkill
        user_skill, created = UserSkill.objects.get_or_create(user_id=user_id, skill_id=skill.id)
        # update level
        if created:
            print('created user skill: ', user_skill)
            user_skill.level = level
        else:
            print('existing user skill: ', user_skill)
            level = user_skill.level
            level += 3
        user_skill.level = level
        user_skill.save()
        print("saved user skill: ", user_skill)
        # add skill source



from apps.personality.mbti_data import mbti_data, mbti_meaning

def mbti_results(request, mbti_set_id):
    mbti_set = MBTISet.objects.get(pk=mbti_set_id)

    # Convert float into percentage
    mbti_set.mind = int((mbti_set.mind + 3)/6 * 100)
    mbti_set.energy = int((mbti_set.energy + 3)/6 * 100)
    mbti_set.nature = int((mbti_set.nature + 3)/6 * 100)
    mbti_set.tactics = int((mbti_set.tactics + 3)/6 * 100)

    # get the reverse percentage
    mind_ = 100 - mbti_set.mind
    energy_ = 100 - mbti_set.energy
    nature_ = 100 - mbti_set.nature
    tactics_ = 100 - mbti_set.tactics

    

    # get the personality type from mbti_set.indicator
    personality_type = mbti_set.indicator.indicator


    #mbti_name = mbti_data[personality_type]['name']
    #mbti_description = mbti_data[personality_type]['description']
    mbti_name = mbti_set.indicator.indicator_name
    mbti_description = mbti_set.indicator.indicator_description

    print("mbti_name: ", mbti_name)
    print("mbti_description: ", mbti_description)

    # get the personality type description
    mbti_energy = mbti_meaning[personality_type[0]]
    mbti_mind = mbti_meaning[personality_type[1]]
    mbti_nature = mbti_meaning[personality_type[2]]
    mbti_tactics = mbti_meaning[personality_type[3]]

     

    return render(request, 'test/mbti_results.html', {
        'mbti_set': mbti_set,
        #'mbti_data': mbti_data,
        #'mbti_meaning': mbti_meaning,
        'mbti_name': mbti_name,
        'mbti_description': mbti_description,
        'mbti_energy': mbti_energy,
        'mbti_mind': mbti_mind,
        'mbti_nature': mbti_nature,
        'mbti_tactics': mbti_tactics,
        'mind_': mind_,
        'energy_': energy_,
        'nature_': nature_,
        'tactics_': tactics_,
        })