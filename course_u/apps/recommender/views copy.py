from django.shortcuts import render

from django.contrib.auth.models import User
from .models import UserSkill

from apps.website.models import Skill, Specialization, SpecializationSkills
from collections import defaultdict


import pandas as pd
import numpy as np
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.metrics import pairwise_distances

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



# def get_normalized_skill_levels_df():
#     """Returns a DataFrame with the index of the specialization name, the columns of the specialization skills, and the values of the skill levels, where the values are normalized by dividing the sum of the skills of the specialization."""
#     print('get_normalized_skill_levels_df')
#     # Get a list of all unique skills across all specializations
#     all_skills = Skill.objects.all()
#     unique_skills = [skill.skill for skill in all_skills]

#     # Create a defaultdict to store the skill levels for each specialization
#     skill_levels = defaultdict(lambda: 0)

#     # Iterate over the specializations
#     for specialization in Specialization.objects.all():
#         print(specialization.title)
#         # Iterate over all unique skills
#         for skill_title in unique_skills:
#             print(skill_title)

#             # Assign the skill level from the specialization's skill set, if it exists
#             skill_levels[specialization.title, skill_title] = specialization.specializationskills_set.filter(skill__skill=skill_title).first().level if specialization.specializationskills_set.filter(skill__skill=skill_title).first() is not None else 0

#     # Create the DataFrame from the defaultdict
#     skill_levels_df = pd.DataFrame.from_dict(skill_levels, orient='index', columns=unique_skills)

#     # Normalize the skill levels by dividing the sum of the skill levels for the specialization
#     skill_levels_df = skill_levels_df.replace(0, method='ffill').div(skill_levels_df.sum(axis=1), axis=0)

#     return skill_levels_df



# def get_top_3_specialization_recommendations(request):
#     """Returns a list of the top 3 specializations with the highest cosine similarity to the user's skill levels."""
#     print("get_top_3_specialization_recommendations")
#     # Get the user's skill levels
#     user_skill_levels = UserSkill.objects.filter(user=request.user).values_list("skill", flat=True)

#     # Get the skill levels DataFrame
#     skill_levels_df = get_normalized_skill_levels_df()

#     # Create a defaultdict to store the user's skill levels
#     user_skill_dict = defaultdict(lambda: 0)

#     # Populate the user's skill levels dictionary
#     for skill_title in skill_levels_df.columns:
#         user_skill_dict[skill_title] = UserSkill.objects.filter(user=request.user, skill__title=skill_title).first().level if skill_title in user_skill_levels else 0
#         print(user_skill_dict[skill_title])

#     # Add the user's skill levels to the DataFrame
#     #skill_levels_df = skill_levels_df.append(user_skill_dict, ignore_index=True)
#     # instead of append use concat
#     skill_levels_df = pd.concat([skill_levels_df, pd.DataFrame(user_skill_dict, index=[0])], ignore_index=True)

#     # Filter the skill levels by the user's skills
#     filtered_skill_levels_df = skill_levels_df.filter(skill_levels_df.columns.intersection(user_skill_levels))

#     # Calculate the cosine similarity between the user's skill levels and the specialization skill levels
#     cosine_similarity_matrix = cosine_similarity(skill_levels_df.loc[skill_levels_df['specialization'] == 'User'].values.reshape(1, -1), filtered_skill_levels_df.drop("User", axis=0))

#     # Get the top 3 specializations with the highest cosine similarity to the user's skill levels
#     top_3_specialization_recommendations = filtered_skill_levels_df.drop("User", axis=0).loc[cosine_similarity_matrix.argmax()].tolist()[:3]

#     return top_3_specialization_recommendations


# def recommender(request):
#     print('recommender')
#     #top_3_specialization_recommendations = get_top_3_specialization_recommendations(request)
#     top_3_specialization_recommendations = 0

#     #Print the top 3 specialization recommendations
#     print("The top 3 specialization recommendations are:")
#     for specialization in top_3_specialization_recommendations:
#         print(specialization)

#     return render(request, 'recommender/recommender.html', {
#         'top_3_specialization_recommendations': top_3_specialization_recommendations
#     })


# def load_sparse_data(request):
#     specialization_sparce = pd.read_csv('specialization_sparce.csv')
#     print('specialization_sparce: ', specialization_sparce)
#     # convert the data to django queryset
#     #specialization_sparce_queryset = specialization_sparce.to_queryset()

#     # store the queryset in the Django Views.
#     #request.session['specialization_sparce_queryset'] = specialization_sparce_queryset

#     return specialization_sparce



# def get_user_skills(request):
#     # Get the user's skills from the request.
#     user_skills = request.GET.get('skills', '').split(',')
#     print('user_skills: ', user_skills)
#     # Convert the user's skills to a NumPy array.
#     user_skills_array = np.array(user_skills)
#     print('user_skills_array: ', user_skills_array)
#     # Normalize the user's skills.
#     normalized_user_skills_array = user_skills_array / np.linalg.norm(user_skills_array)
#     print('normalized_user_skills_array: ', normalized_user_skills_array)

#     return normalized_user_skills_array


# def get_top_3_specialization_recommendation(request):
#     specialization_sparce = load_sparse_data(request)
    
#     normalized_user_skills_array = get_user_skills(request)

#     # Calculate the cosine similarity between the user's skills and the specialization skills.
#     cosine_similarities = pairwise_distances(normalized_user_skills_array, specialization_sparse_filtered, metric='cosine')


#     return 

import os
from django.http import HttpResponse

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
        user_skills_level.append(UserSkill.objects.filter(user=request.user, skill__skill=skill).first().level)
    print('user_skills_level: ', user_skills_level)

    # create a dictionary of user skills and levels, 
    user_skills_dict = dict(zip(user_skills_list, user_skills_level))
    
    # convert the dictionary to a dataframe, where the columns are the skills and the values are the levels
    user_skills_df = pd.DataFrame.from_dict(user_skills_dict, orient='index').T


    # fill the missing values with 0
    user_skills_df = user_skills_df.fillna(0)

    # Normalize the user's skills. by getting the sum of the user skills and dividing each skill by the sum. if skill = 0, then = 0
    normalized_user_skills_df = user_skills_df / user_skills_df.sum(axis=1, skipna=True)

    # fill the missing values with 0
    normalized_user_skills_df = normalized_user_skills_df.fillna(0)
    print('normalized_user_skills_df: ', normalized_user_skills_df)
    
    specialization_sparse = load_csv(request)

    # Filter the specialization data frame columns by the user's skills. except the first and second columns
    specialization_sparse_filtered = specialization_sparse[['title','field_id'] + user_skills_list]

    print('specialization_sparse_filtered: ', specialization_sparse_filtered)

    cosine_similarities = cosine_similarity(normalized_user_skills_df[user_skills_list], specialization_sparse_filtered[user_skills_list])
    top_3_indices = cosine_similarities.argsort(axis=1)[:, -3:]
    top_3_specializations = specialization_sparse_filtered.iloc[:, 0].values[top_3_indices]
    print('top_3_specializations: ', top_3_specializations)

    
    
    # Calculate the cosine similarity between the user's skills and the other skills for each field_id
    # grouped_cosine_similarities = specialization_sparse_filtered.groupby('field_id').apply(lambda group: cosine_similarity(
    #     normalized_user_skills_df[user_skills_list],
    #     group[user_skills_list]
    # ))

    normalized_user_skills_array = normalized_user_skills_df[user_skills_list].values
    # Calculate the cosine similarity between the user's skills and the other skills.
    grouped_cosine_similarities = specialization_sparse_filtered.groupby('field_id').apply(lambda group: pairwise_distances(
        normalized_user_skills_array,
        group[user_skills_list].values,
        metric='cosine'
    ))
    print('grouped_cosine_similarities: ', grouped_cosine_similarities)

    # Get the indices of the top 3 recommendations for each field_id
    #top_3_indices = grouped_cosine_similarities.apply(lambda group: np.argsort(group.values)[:, -3:])
    #top_3_indices = grouped_cosine_similarities.apply(lambda group: np.argsort(group['field_id'])[:, -3:])
    top_3_indices = grouped_cosine_similarities.apply(lambda group: np.argsort(group['field_id'].to_numpy())[:, -3:])

    #top_3_indices = grouped_cosine_similarities.apply(lambda group: np.argsort(group[['field_id', 'skill']])[:, -3:])

    top_3_recommendations = grouped_cosine_similarities.apply(lambda group: group.columns[top_3_indices.loc[group.index]].tolist())
    print('top_3_recommendations: ', top_3_recommendations)

    # # Get the corresponding specialization titles for the top 3 recommendations
    # top_3_specializations = grouped_cosine_similarities.apply(lambda group: group.columns[top_3_indices.loc[group.index]].tolist())
        
    # # Calculate the count of each specialization within each field_id
    # specialization_counts = top_3_specializations.apply(lambda group: group.value_counts())

    # # Sort the counts in descending order for each field_id
    # sorted_specializations = specialization_counts.apply(lambda field_counts: field_counts.sort_values(ascending=False), axis=1)

    # # Select the top 3 specializations for each field_id
    # top_3_fields = sorted_specializations.apply(lambda field_counts: field_counts.index[:3].tolist(), axis=1)

    for field_id, top_3_specializations in top_3_recommendations.iteritems():
        print("Field ID: {}".format(field_id))
        print("Top 3 Specializations: {}".format(top_3_specializations))
        print()

    return render(request, 'recommender/recommender.html', {
        'top_3_specialization_recommendations': top_3_specializations
    })



    # Calculate the cosine similarity between the user's skills and the other skills.
    grouped_cosine_similarities = specialization_sparse_filtered.groupby('field_id').apply(lambda group: pairwise_distances(
        normalized_user_skills_array,
        group[user_skills_list].values,
        metric='cosine'
    ))
    print('grouped_cosine_similarities: ', grouped_cosine_similarities)

    # Get the indices of the top 3 recommendations for each field_id
    top_3_indices = grouped_cosine_similarities.apply(lambda group: np.argsort(group.get_group('field_id'))[-3:])

    top_3_recommendations = grouped_cosine_similarities.apply(lambda group: group.columns[top_3_indices.loc[group.index]].tolist())





        grouped_cosine_similarities = specialization_sparse_filtered.groupby('field_id').apply(lambda group: pairwise_distances(
        normalized_user_skills_array,
        group[user_skills_list].values,
        metric='cosine'
    ))

    # Convert the grouped cosine similarities to a Pandas DataFrame.
    grouped_cosine_similarities_df = pd.DataFrame(grouped_cosine_similarities)

    # Get the indices of the top 3 recommendations for each field_id.
    top_3_indices = grouped_cosine_similarities_df.apply(lambda group: np.argsort(group.get_group('field_id'))[-3:])

    # Get the top 3 recommendations for each field_id.
    top_3_recommendations = grouped_cosine_similarities_df.apply(lambda group: group.columns[top_3_indices.loc[group.index]].tolist())
    



     grouped_cosine_similarities = specialization_sparse_filtered.groupby('field_id').apply(lambda group: pairwise_distances(
      normalized_user_skills_array,
      group[user_skills_list].values,
      metric='cosine'
  ))

    # Convert the grouped cosine similarities to a Pandas DataFrame.
    grouped_cosine_similarities_df = pd.DataFrame(grouped_cosine_similarities)

  # Check if the group variable is a Series object or a DataFrame object.
    if isinstance(group, pd.Series):
        group = pd.DataFrame(group)

    # Get the indices of the top 3 recommendations for each field_id.
    top_3_indices = grouped_cosine_similarities_df.apply(lambda group: np.argsort(group['field_id'])[-3:])

    # Get the top 3 recommendations for each field_id.
    top_3_recommendations = grouped_cosine_similarities_df.apply(lambda group: group.columns[top_3_indices.loc[group.index]].tolist())
    
    print('top_3_recommendations: ', top_3_recommendations)


    for field_id, top_3_specializations in top_3_recommendations.iteritems():
        print("Field ID: {}".format(field_id))
        print("Top 3 Specializations: {}".format(top_3_specializations))
        print()

    return render(request, 'recommender/recommender.html', {
        'top_3_specialization_recommendations': top_3_specializations
    })


   normalized_user_skills_array = normalized_user_skills_df[user_skills_list].values
    
    # Define the variable group.
    group = None

    # Calculate the cosine similarities between the user's skills and the other skills.
    cosine_similarities = pairwise_distances(normalized_user_skills_array, specialization_sparse_filtered[user_skills_list])

    # Group the cosine similarities by field_id.
    grouped_cosine_similarities = cosine_similarities.groupby('field_id')

    # For each group, get the top 3 recommendations.
    for field_id, group in grouped_cosine_similarities:
        # Get the indices of the top 3 recommendations.
        top_3_indices = np.argsort(group['field_id'])[-3:]

        # Get the top 3 recommendations.
        top_3_recommendations = group.columns[top_3_indices].tolist()

        # Print the top 3 recommendations.
        print("Field ID: {}".format(field_id))
        print("Top 3 Recommendations: {}".format(top_3_recommendations))
        print()



field_score = {}
    for field_id in field_ids:
        print("Field: ", field_id)
        # filter specialization_sparse_filtered by field_id
        specialization_sparse_filtered_by_field = specialization_sparse_filtered[specialization_sparse_filtered['field_id'] == field_id]
        cosine_similarities = cosine_similarity(normalized_user_skills_df[user_skills_list], specialization_sparse_filtered_by_field[user_skills_list])
        top_3_indices = cosine_similarities.argsort(axis=1)[:, -3:]
        top_3_specializations_field = specialization_sparse_filtered_by_field.iloc[:, 0].values[top_3_indices]
        print('top_3_specializations: ', top_3_specializations_field)
        # get total sum score of each specialization and add to field_score
        field_score[field_id] = cosine_similarities.sum(axis=1).sum()

    # get top 3 fields
    top_3_fields = sorted(field_score, key=field_score.get, reverse=True)[:3]
    # top fields score
    top_3_fields_score = [field_score[field_id] for field_id in top_3_fields]
    

    print('top_3_fields: ', top_3_fields)
    print('top_3_fields_score: ', top_3_fields_score)
    field_names = []
    for field_id in top_3_fields:
        field_name =  Field.objects.get(field=field_id).field_name
        print("field: ", field_name)
        field_names.append(field_name)