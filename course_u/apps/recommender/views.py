from django.shortcuts import render

from django.contrib.auth.models import User
from .models import UserSkill

from apps.website.models import Skill, Specialization, SpecializationSkills


import pandas as pd
from sklearn.metrics.pairwise import cosine_similarity

from scipy.sparse import csr_matrix

#from .utils import load_ml_model, make_prediction

# get user skills
# calculate similarity
# get top 5 similar users
# save top 5 similar users in a list
# update user profile with top 5 similar users
# user interaction
# save user interaction in a list
# get user interaction list

def get_normalized_skill_levels_df(request):
    """Returns a DataFrame with the index of the specialization name, the columns of the user skills, and the values of the skill levels, where the values are normalized by dividing the sum of the skills of the specialization."""

    # Get a list of all specialization names
    specialization_names = [
        s.title
        for s in Specialization.objects.all()
    ]

    # Get a list of all user skills
    user_skills = UserSkill.objects.filter(user=request.user)
    skill_list = [skill.skill for skill in user_skills]

    # Create a DataFrame to store the skill levels for each specialization
    skill_levels_df = pd.DataFrame(columns=skill_list)

    # Iterate over the specializations
    for specialization in Specialization.objects.all():

        # Create a dictionary to store the skill levels for the specialization
        skill_levels = {}

        # Iterate over the user's skills
        for skill in skill_list:

            # Check if the skill is in the specialization's skill set
            if skill in specialization.specializationskills_set.all():

                # Get the skill level
                skill_level = specialization.specializationskills_set.get(skill=skill).level

            else:

                # Set the skill level to 0
                skill_level = 0

            # Add the skill level to the dictionary
            skill_levels[skill] = skill_level

    # Calculate the sum of the skill levels for each specialization
    sum_of_skill_levels = skill_levels_df.apply(lambda x: x.sum(), axis=1)

    # Normalize the skill levels by dividing the sum of the skill levels for the specialization
    skill_levels_df = skill_levels_df.apply(lambda x: x / sum_of_skill_levels, axis=1)

    return skill_levels_df


def get_top_3_specialization_recommendations(request):
    """Returns the top 3 specializations with the highest cosine similarity to the user's skill levels."""

    # Get the normalized skill levels DataFrame
    skill_levels_df = get_normalized_skill_levels_df(request)

    # Add the User row to the skill levels DataFrame
    skill_levels_df.loc["User"] = UserSkill.objects.filter(user=request.user).values_list("skill", "level")
    
    # Append the user skill levels DataFrame to the skill levels DataFrame
    #skill_levels_df = pd.concat([skill_levels_df, user_skill_levels_df], axis=0)

    # Calculate the cosine similarity between the user's skill levels and the specialization skill levels
    cosine_similarity_matrix = cosine_similarity(skill_levels_df.loc["User"].reshape(1, -1), skill_levels_df.drop("User", axis=0))

    # Get the top 3 specializations with the highest cosine similarity to the user's skill levels
    top_3_specializations = skill_levels_df.drop("User", axis=0).index[cosine_similarity_matrix.argmax(axis=1)].tolist()[:3]

    return top_3_specializations



def recommender(request):

    # Get the top 3 specialization recommendations
    top_3_specialization_recommendations = get_top_3_specialization_recommendations(request)

    # Print the top 3 specialization recommendations
    print("The top 3 specialization recommendations are:")
    for specialization in top_3_specialization_recommendations:
        print(specialization)

    return render(request, 'recommender/recommender.html', {
            #'skill_levels_df': skill_levels_df
        })
