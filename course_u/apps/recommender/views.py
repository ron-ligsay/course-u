from django.shortcuts import render
from django.http import HttpResponse

from django.contrib.auth.models import User

from .models import UserSkill
from apps.website.models import Skill, Specialization, SpecializationSkills, Field

import pandas as pd
from sklearn.metrics.pairwise import cosine_similarity

import os


def load_csv(request):
    # Assuming your CSV file is in the same folder as your views
    csv_file_name = 'specialization_sparse.csv'
    csv_file_path = os.path.join(os.path.dirname(__file__), csv_file_name)

    try:
        # Read the CSV file into a DataFrame
        specialization_sparse = pd.read_csv(csv_file_path)

        # Process the DataFrame as needed (e.g., save to the database, perform operations)
        # ...
        print("specialization_sparse: ", specialization_sparse)
        return specialization_sparse
    except Exception as e:
        print("Error processing file: {}".format(e))
        # empty DataFrame with the same columns and dtypes as your original DataFrame
        
        specialization_sparse = pd.DataFrame()

        return specialization_sparse



def recommender(request):
    # Get the user's skills from the request.
    user_skills = UserSkill.objects.filter(user=request.user)

    # Get a list of user skill titles
    user_skills_list = [skill.skill.skill for skill in user_skills]

    # unique user skills
    user_skills_list = list(set(user_skills_list))
    print('user_skills_list: ', user_skills_list)

    # convert to list
    user_skills_list = list(user_skills_list)
    print("type: ", type(user_skills_list))

    # get level of each skill
    user_skills_level = []
    for skill in user_skills_list:
        userskill_level = UserSkill.objects.get(user=request.user, skill__skill=skill).level
        user_skills_level.append(userskill_level)
        print('skill: ', skill, 'level: ', userskill_level)
        #user_skills_level.append(UserSkill.objects.filter(user=request.user, skill__skill=skill).first().level)

    # create a dictionary of user skills and levels, 
    user_skills_dict = dict(zip(user_skills_list, user_skills_level))
    
    # convert the dictionary to a dataframe, where the columns are the skills and the values are the levels
    user_skills_df = pd.DataFrame.from_dict(user_skills_dict, orient='index').T
    print("user_skills_df: ", user_skills_df)

    # fill the missing values with 0
    #user_skills_df = user_skills_df.fillna(0)

    # Normalize the user's skills. by getting the sum of the user skills and dividing each skill by the sum. if skill = 0, then = 0
    skill_sum = user_skills_df.sum(axis=1)
    print('skill_sum: ', skill_sum)
    normalized_user_skills_df = user_skills_df.div(skill_sum, axis=0)

    # fill the missing values with 0
    #normalized_user_skills_df = normalized_user_skills_df.fillna(0)
    print('normalized_user_skills_df: ', normalized_user_skills_df)
    
    specialization_sparse = load_csv(request)

    # Filter the specialization data frame columns by the user's skills. except the first and second columns
    specialization_sparse_filtered = specialization_sparse[['title','field_id'] + user_skills_list]
    # remove rows with all 0
    specialization_sparse_filtered = specialization_sparse_filtered[(specialization_sparse_filtered[user_skills_list] != 0).any(axis=1)]


    print('specialization_sparse_filtered: ', specialization_sparse_filtered)

    cosine_similarities = cosine_similarity(normalized_user_skills_df[user_skills_list], specialization_sparse_filtered[user_skills_list])
    top_3_indices = cosine_similarities.argsort(axis=1)[:, -3:]
    top_3_specializations = specialization_sparse_filtered.iloc[:, 0].values[top_3_indices]
    print('top_3_specializations: ', top_3_specializations)

    
    # get unique field_id
    field_ids = specialization_sparse_filtered['field_id'].unique()
    
    # Calculate the sum of the cosine similarity scores for each skill in each field.
    fields_score = {}
    for field_id in field_ids:
        # filter specialization_sparse_filtered by field_id
        specialization_sparse_filtered_by_field = specialization_sparse_filtered[specialization_sparse_filtered['field_id'] == field_id]
        cosine_similarities = cosine_similarity(normalized_user_skills_df[user_skills_list], specialization_sparse_filtered_by_field[user_skills_list])
        # get total sum score of each field and add to field_score
        fields_score[field_id] = cosine_similarities.sum(axis=1).sum()

    # Sort the fields by the sum of the cosine similarity scores, in descending order.
    top_3_fields = sorted(fields_score, key=fields_score.get, reverse=True)[:3]
    # top fields score
    top_3_fields_score = [fields_score[field_id] for field_id in top_3_fields]
    print('top_3_fields: ', top_3_fields)
    print('top_3_fields_score: ', top_3_fields_score)
    # Get the field names for the top 3 fields.
    field_names = []
    for field_id in top_3_fields:
        field_name = Field.objects.get(field=field_id).field_name
        field_names.append(field_name)



    return render(request, 'recommender/recommender.html', {
        'top_3_specialization_recommendations': top_3_specializations,
        'field_names': field_names,
    })