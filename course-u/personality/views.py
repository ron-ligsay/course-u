from django.shortcuts import render, redirect

from django.db.models import Q, Avg

# App imports
from personality.models import  MBTI, MBTISet, MBTIResponse

# Create your views here.
################################
#       MBTI TEST VIEWS        #
################################


from django.db.models import Max

def initialize_mbti_test(request):
    user = request.user

    # Check if there is an unfinished MBTISet for the user
    unfinished_set = MBTISet.objects.filter(user=user, is_completed=False).first()

    if unfinished_set:
        # If there is an unfinished set, continue that test
        mbti_set = unfinished_set
    else:
        # If no unfinished set exists, create a new one with a set_id one greater than the maximum set_id
        last_set = MBTISet.objects.aggregate(Max('mbti_set_id'))
        new_set_id = last_set['mbti_set_id__max'] + 1 if last_set['mbti_set_id__max'] else 1
        mbti_set = MBTISet.objects.create(user=user, mbti_set_id=new_set_id)

    # Create responses for all MBTI questions
    mbti_questions = MBTI.objects.all()
    for question in mbti_questions:
        MBTIResponse.objects.get_or_create(mbti_set=mbti_set, mbti=question)

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
    if mind >= 2.5:
        personality_type += 'I'
    else:
        personality_type += 'E'
    if energy >= 2.5:
        personality_type += 'N'
    else:
        personality_type += 'S'
    if nature >= 2.5:
        personality_type += 'F'
    else:
        personality_type += 'T'
    if tactics >= 2.5:
        personality_type += 'P'
    else:
        personality_type += 'J'
    print("Personality Type: ", personality_type)
    mbti_set.identity = personality_type

    # marks as completed
    mbti_set.is_completed = True
    mbti_set.save()


def mbti_results(request, mbti_set_id):
    mbti_set = MBTISet.objects.get(pk=mbti_set_id)

    # Convert float into percentage
    mbti_set.mind = int(mbti_set.mind * 20)
    mbti_set.energy = int(mbti_set.energy * 20)
    mbti_set.nature = int(mbti_set.nature * 20)
    mbti_set.tactics = int(mbti_set.tactics * 20)

    return render(request, 'test/mbti_results.html', {'mbti_set': mbti_set})