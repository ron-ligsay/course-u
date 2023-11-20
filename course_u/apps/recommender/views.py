from django.shortcuts import render
from django.http import HttpResponse

from django.contrib.auth.models import User

from .models import UserSkill, UserSkillSource, UserRecommendations

from apps.website.models import Skill, Specialization, SpecializationSkills, Field
from apps.acad.models import StudentProfile

import pandas as pd
from sklearn.metrics.pairwise import cosine_similarity

import os
import plotly.express as px
import plotly.io as pio

def load_csv(request):
    # Assuming your CSV file is in the same folder as your views
    #csv_file_name = 'specialization_sparse.csv'
    #csv_file_name = 'normalized_field_skills.csv'
    csv_file_name = 'field_skills_tfidf.csv'
    csv_file_path = os.path.join(os.path.dirname(__file__), csv_file_name)

    try:
        # Read the CSV file into a DataFrame
        specialization_sparse = pd.read_csv(csv_file_path)

        # Process the DataFrame as needed (e.g., save to the database, perform operations)
        # ...
        #print("specialization_sparse: ", specialization_sparse)
        return specialization_sparse
    except Exception as e:
        #print("Error processing file: {}".format(e))
        # empty DataFrame with the same columns and dtypes as your original DataFrame
        
        specialization_sparse = pd.DataFrame()

        return specialization_sparse

# import minmaxscaler
from sklearn.preprocessing import MinMaxScaler

# import tfidf
from sklearn.feature_extraction.text import TfidfTransformer

def recommender(request):
    # Get the user's skills from the request.
    user_skills = UserSkill.objects.filter(user=request.user)
    user_skills_list = [skill.skill.skill for skill in user_skills]
    user_skills_list = list(set(user_skills_list))
    user_skills_list = list(user_skills_list)
    

    normalized_field_skills = load_csv(request)

    normalized_user_skills_df_columns = user_skills_list
    
    normalized_field_skills_columns = normalized_field_skills.columns
    # convert to list
    normalized_field_skills_columns = list(normalized_field_skills_columns)

    # get the intersection of the two dataframes
    #intersection_columns = normalized_user_skills_df_columns.intersection(normalized_field_skills_columns)
    intersection_columns = set(normalized_user_skills_df_columns).intersection(set(normalized_field_skills_columns))


    # to list for filtering
    intersection_columns = list(intersection_columns)

    #print('intersection_columns: ', intersection_columns)


    # get level of each skill
    user_skills_level = []
    for skill in intersection_columns:
        userskill_level = UserSkill.objects.get(user=request.user, skill__skill=skill).level
        user_skills_level.append(userskill_level)


    user_skills_dict = dict(zip(intersection_columns, user_skills_level))
    
    user_skills_df = pd.DataFrame.from_dict(user_skills_dict, orient='index').T

        
    # use minmaxscaler
    #scaler = MinMaxScaler()
    #normalized_user_skills_df = pd.DataFrame(scaler.fit_transform(user_skills_df), columns=user_skills_df.columns, index=user_skills_df.index)

    # use tfidf
    tfidf = TfidfTransformer()
    normalized_user_skills_df = pd.DataFrame(tfidf.fit_transform(user_skills_df).toarray(), columns=user_skills_df.columns, index=user_skills_df.index)

    # fill the missing values with 0
    #user_skills_df = user_skills_df.fillna(0) - not used

    # Normalize the user's skills. by getting the sum of the user skills and dividing each skill by the sum. if skill = 0, then = 0
    #skill_sum = user_skills_df.sum(axis=1)
    #normalized_user_skills_df = user_skills_df.div(skill_sum, axis=0)


    # Filter the specialization data frame columns by the user's skills. except the first and second columns
    normalized_field_skills_filtered = normalized_field_skills[['field_id'] + intersection_columns]
    # remove rows with all 0
    normalized_field_skills_filtered = normalized_field_skills_filtered[(normalized_field_skills_filtered[intersection_columns] != 0).any(axis=1)]


    cosine_similarities = cosine_similarity(normalized_user_skills_df[intersection_columns], normalized_field_skills_filtered[intersection_columns])
    print('cosine_similarities: ', cosine_similarities)
    top_3_indices = cosine_similarities.argsort(axis=1)[:, -3:]
    top_3_field = normalized_field_skills_filtered.iloc[:, 0].values[top_3_indices]
    all_fields = normalized_field_skills_filtered.iloc[:, 0].values
    #print('top_3_field: ', top_3_field)

    print('all_fields: ', all_fields)

    # get unique field_id
    field_ids = normalized_field_skills_filtered['field_id'].unique()
    print('field_ids: ', field_ids)
    # Create a dictionary to store the field names and the sum of the cosine similarity scores
    fields_score = {}
    for field_id in all_fields:
        # filter specialization_sparse_filtered by field_id
        normalized_field_skills_filtered_by_field = normalized_field_skills_filtered[normalized_field_skills_filtered['field_id'] == field_id]
        # Calculate the sum of the cosine similarity scores for each skill in each field.
        fields_score[field_id] = normalized_field_skills_filtered_by_field.iloc[:, 1:].sum(axis=1).sum()
    
    # get field names
    fields_name = []
    for field_id in all_fields:
        field_name = Field.objects.get(field=field_id).field_name
        fields_name.append(field_name)

    field_dict = {
        'Software Development': 1,
        'Data and Analytics': 2,
        'Design and UX/UI': 3,
        'Product Management': 4,
        'Testing and Quality Assurance': 5,
        'Security': 6
    }
    field_dict = {v: k for k, v in field_dict.items()}


    # Calculate the field with the highest matching for each skill
    user_skills_field = []
    field_id_list = []
    for skill in intersection_columns:
        # Assuming normalized_user_skills_df has a column for each field and a row for each skill
        #field = normalized_field_skills_filtered[skill].idxmax()
        # Assuming field_id is a column in normalized_field_skills_filtered
        field_id = normalized_field_skills_filtered.loc[normalized_field_skills_filtered[skill].idxmax(), 'field_id']
        field_id_list.append(field_id)
        field = Field.objects.get(field=field_id).field_name
        user_skills_field.append(field)
    
    # Create a DataFrame
    user_skills_df = pd.DataFrame({
        'skill': intersection_columns,
        'level': user_skills_level,
        'field': user_skills_field,
        'field_id': field_id_list,
    })


    # Create a bar plot using Plotly Express
    #fig = px.bar(user_skills_df, title='User Skills Levels', labels={'index': 'Skills', 'value': 'Skill Level'})
    
    # Create a dictionary where the keys are the elements in all_fields and the values are their indices
    order_dict = {field_id: index for index, field_id in enumerate(all_fields)}

    print('fields_score:', fields_score)
    # Create a new column 'order' in user_skills_df that represents the index of each field_id in all_fields
    user_skills_df['fields_score'] = user_skills_df['field_id'].map(fields_score)

    # Sort user_skills_df by the 'order' column
    user_skills_df = user_skills_df.sort_values('fields_score', ascending=False)

    print('user_skills_df: ', user_skills_df)

    # Drop the 'order' column as it's no longer needed
    user_skills_df = user_skills_df.drop('fields_score', axis=1)

    fig = px.bar(
        x=user_skills_df['skill'],
        y=user_skills_df['level'],
        color=user_skills_df['field'],
        #facet_col=user_skills_df['field'],
        title='User Skills Levels',
        labels={'index': 'Skills', 'value': 'Skill Level'},
        #color_continuous_scale=px.colors.sequential.Plasma,
    )
    
    # x and y title
    fig.update_xaxes(title_text='Skills')
    fig.update_yaxes(title_text='Skill Level')

    skill_plot = pio.to_html(fig, full_html=False)


    # Create a DataFrame with Field_ID, Field_Name, and Score
    fields_df = pd.DataFrame(list(zip(field_ids, fields_name, fields_score.values())), columns=['Field_ID', 'Field_Name', 'Score'])

    # Create a pie chart using Plotly Express
    fig = px.pie(fields_df, values='Score', names='Field_Name', title='Top Field Recommendation Score')

    # set title
    fig.update_layout(title_text='Top Field Recommendation Score', title_x=0.5)

    # remove white background
    fig.update_layout(plot_bgcolor='rgba(0,0,0,0)')

    # Convert the figure to HTML
    field_plot = pio.to_html(fig, full_html=False)
    
    
    # make a copy of normamlied_field
    normalized_copy = normalized_field_skills_filtered.copy()

    # label field id of normalized_field_skills_filtered with field_dict
    normalized_copy['field_name'] = normalized_copy['field_id'].map(field_dict)

    print('normalized_field_skills_filtered: ', normalized_copy)

    # melt normalized_field_skills_filtered
    normalized_copy = normalized_copy.melt(id_vars=['field_id', 'field_name'], var_name='skill', value_name='level')
    print('normalized_field_skills_filtered: ', normalized_copy)

    # use fields_score mapping for field_id into field_order
    normalized_copy['field_order'] = normalized_copy['field_id'].map(fields_score)
    # sort by field_order
    normalized_copy = normalized_copy.sort_values('field_order', ascending=False)
    # remove field_order
    normalized_copy = normalized_copy.drop('field_order', axis=1)


    # plotting using plotly express
    stacked_skills = px.bar(
        normalized_copy, 
        x='level', 
        y='skill', 
        color='field_name', 
        title='Skills Levels',
        orientation='h',
        labels={'level': 'Relevance Score', 'field_name': 'Field Name'},
        color_continuous_scale=px.colors.sequential.Plasma,
        height=500,
        width=800,
    )

    # convert to html
    stacked_skills = pio.to_html(stacked_skills, full_html=False)

    # create the radar chart
    radar_skills = px.line_polar(
        normalized_copy, 
        r='level', 
        theta='skill', 
        color='field_name', 
        line_close=True,
        title='Skills Levels',
        labels={'level': 'Relevance Score', 'field_name': 'Field Name'},
        #color_continuous_scale=px.colors.sequential.Plasma,
        height=500,
        width=800,
    )

    # convert to html
    radar_skills = pio.to_html(radar_skills, full_html=False)








    # Sort the fields by the sum of the cosine similarity scores, in descending order.
    top_3_fields = sorted(fields_score, key=fields_score.get, reverse=True)[:3]
    # top fields score
    top_3_fields_score = [fields_score[field_id] for field_id in top_3_fields]
    #print('top_3_fields: ', top_3_fields)
    #print('top_3_fields_score: ', top_3_fields_score)
    # Get the field names for the top 3 fields.
    

    field_names = []
    for field_id in top_3_fields:
        field_name = Field.objects.get(field=field_id).field_name
        field_names.append(field_name)

    field_name_1 = field_names[0]
    field_name_2 = field_names[1]
    field_name_3 = field_names[2]

    # get StudentProfile year
    student_year = StudentProfile.objects.get(user=request.user).current_year

    #UserRecommendations get or create
    user_recommendations = UserRecommendations.objects.get_or_create(user=request.user, current_year=student_year)[0]

    user_recommendations.field_1 = Field.objects.get(field=top_3_fields[0])
    user_recommendations.field_2 = Field.objects.get(field=top_3_fields[1])
    user_recommendations.field_3 = Field.objects.get(field=top_3_fields[2])
    user_recommendations.score_1 = float(top_3_fields_score[0])
    user_recommendations.score_2 = float(top_3_fields_score[1])
    user_recommendations.score_3 = float(top_3_fields_score[2])


    user_recommendations.save()


    return render(request, 'recommender/recommender.html', {
        'top_3_field_recommendations': top_3_field,
        'field_name_1': field_name_1,
        'field_name_2': field_name_2,
        'field_name_3': field_name_3,
        'skill_plot': skill_plot,
        'field_plot': field_plot,
        'stacked_skills': stacked_skills,
        'radar_skills': radar_skills,
        'field_1': Field.objects.get(field=top_3_fields[0]),
        'field_2': Field.objects.get(field=top_3_fields[1]),
        'field_3': Field.objects.get(field=top_3_fields[2]),
    })



def recommendation_field(request, field_id):

    field_object = Field.objects.get(field=field_id)
    
    # skills
    user_skills = UserSkill.objects.filter(user=request.user)
    user_skills_list = [skill.skill.skill for skill in user_skills]
    user_skills_list = list(set(user_skills_list))
    user_skills_set = set(user_skills_list)

    # #print('user_skills_list: ', user_skills_list)

    # specialization_skills = SpecializationSkills.objects.filter(specialization__field=field_id)
    # specialization_skills = specialization_skills.filter(skill__skill__in=user_skills_set)

    # # Create a set to store unique skills
    # unique_skills_set = set()

    # # Create a list to store the final unique specialization skills
    # specialization_skills_list = []

    # # Iterate through the specialization skills and filter duplicates
    # for skill in specialization_skills:
    #     skill_name = skill.skill.skill
    #     level = skill.level
    #     # Check if the skill is not in the set to add it
    #     if skill_name not in unique_skills_set:
    #         unique_skills_set.add(skill_name)
    #         specialization_skills_list.append((skill_name, level))

    # # Sort the list by level
    # specialization_skills_list = sorted(specialization_skills_list, key=lambda x: x[1], reverse=True)


    # # filter to 10 only
    # specialization_skills_list = specialization_skills_list[:10]
    # #print('')
    # #print('!!!!specialization_skills: ', specialization_skills_list)
    # # specialization, jobs, roadmap

    normalized_field_skills = load_csv(request)

    #normalized_field_skills_row = normalized_field_skills[normalized_field_skills['field_id'] == field_id]
    # for each skill column get the highest value and only on the field_id = field_id
    # iterate through the columns
    column_list = []
    column_list_2 = []
    # exclude field_id
    for col in normalized_field_skills.columns[1:]:
        # get field id of the highest value
        row_field_id = normalized_field_skills[col].idxmax()
        # if row_field_id is equal to field_id, get column name
        if row_field_id == field_id:
            column_list.append(col)
        else:
            # if its the second highest value, get the column name
            # get the second highest values field id
            second_highest_field = normalized_field_skills[col].nlargest(2).index[1]
            # if the second highest value's field_id is equal to field_id, get the column name
            if second_highest_field == field_id:
                column_list_2.append(col)

    # filter normalized_field_skills by column_list
    normalized_field_skills_row = normalized_field_skills[['field_id'] + column_list]
    normalized_field_skills_row_2 = normalized_field_skills[['field_id'] + column_list_2]
    # get only row with field_id = field_id
    normalized_field_skills_row = normalized_field_skills_row[normalized_field_skills_row['field_id'] == field_id]
    normalized_field_skills_row_2 = normalized_field_skills_row_2[normalized_field_skills_row_2['field_id'] == field_id]

    # convert to series
    normalized_field_skills_row = normalized_field_skills_row.iloc[:, 1:].sum(axis=0).sort_values(ascending=False)
    normalized_field_skills_row_2 = normalized_field_skills_row_2.iloc[:, 1:].sum(axis=0).sort_values(ascending=False)

    # filter by user skills
    top_user_skills = normalized_field_skills_row[normalized_field_skills_row.index.isin(user_skills_set)]
    top_user_skills = top_user_skills.nlargest(7)
    top_user_skills_2 = normalized_field_skills_row_2[normalized_field_skills_row_2.index.isin(user_skills_set)]
    top_user_skills_2 = top_user_skills_2.nlargest(7)


    # not in user skills
    not_in_user_skills = normalized_field_skills_row[~normalized_field_skills_row.index.isin(user_skills_set)]
    not_in_user_skills = not_in_user_skills.nlargest(7)
    not_in_user_skills_2 = normalized_field_skills_row_2[~normalized_field_skills_row_2.index.isin(user_skills_set)]
    not_in_user_skills_2 = not_in_user_skills_2.nlargest(7)

    # remove 0
    top_user_skills = top_user_skills[top_user_skills != 0]
    top_user_skills_2 = top_user_skills_2[top_user_skills_2 != 0]
    not_in_user_skills = not_in_user_skills[not_in_user_skills != 0]
    not_in_user_skills_2 = not_in_user_skills_2[not_in_user_skills_2 != 0]

    # Get the column names (skills) as a list
    top_user_skills = top_user_skills.index.tolist()
    not_in_user_skills = not_in_user_skills.index.tolist()
    top_user_skills_2 = top_user_skills_2.index.tolist()
    not_in_user_skills_2 = not_in_user_skills_2.index.tolist()

    

    return render(request, 'recommender/recommendation_field.html', {
        'field_object': field_object,
        #'specialization_skills': top_10_skills,
        'top_user_skills': top_user_skills,
        'not_in_user_skills': not_in_user_skills,
        'top_user_skills_2': top_user_skills_2,
        'not_in_user_skills_2': not_in_user_skills_2,
    })


def recommendation_specialization(request, field_id):

    field = Field.objects.get(field=field_id)

    # get specialization
    specialization = Specialization.objects.filter(field=field_id)

    # get specialization skills
    specialization_skills = SpecializationSkills.objects.filter(specialization__field=field_id)

    # get user skills
    user_skills = UserSkill.objects.filter(user=request.user)
    user_skills_list = [skill.skill.skill for skill in user_skills]
    user_skills_list = list(set(user_skills_list))
    user_skills_set = set(user_skills_list)

    # Create a set to store unique skills
    unique_skills_set = set()

    # Create a list to store the final unique specialization skills
    specialization_skills_list = []

    # Iterate through the specialization skills and filter duplicates
    for skill in specialization_skills:
        skill_name = skill.skill.skill
        level = skill.level
        # Check if the skill is not in the set to add it
        if skill_name not in unique_skills_set:
            unique_skills_set.add(skill_name)
            specialization_skills_list.append((skill_name, level))

    # Sort the list by level, get column name
    specialization_skills_list = sorted(specialization_skills_list, key=lambda x: x[1], reverse=True)

    # filter to 10 only
    specialization_skills_list = specialization_skills_list[:10]

    # get specialization jobs
    #specialization_jobs = specialization[0].jobs.all()

    # get specialization roadmap
    #specialization_roadmap = specialization[0].roadmap

    return render(request, 'recommender/recommendation_specialization.html', {
        'field': field,
        'specializations': specialization,
        'specialization': specialization[0],
        'specialization_skills': specialization_skills_list,
        #'specialization_jobs': specialization_jobs,
        #'specialization_roadmap': specialization_roadmap,
    })


def recommendation_course(request, field_id):
    field = Field.objects.get(field=field_id)
    #specialization = Specialization.objects.get(id=specialization_id)
    #roadmap = specialization.roadmap

    return render(request, 'recommender/recommendation_course.html', {
        'field': field,
        #'specialization': specialization,
        #'roadmap': roadmap,
    })

from apps.jobs.models import JobPosting

def recommendation_jobs(request, field_id):
    field = Field.objects.get(field=field_id)
    #specialization = Specialization.objects.get(id=specialization_id)
    #jobs = specialization.jobs.all()

    jobs = JobPosting.objects.all()

    return render(request, 'recommender/recommendation_jobs.html', {
        'field': field,
        #'specialization': specialization,
        'jobs': jobs,
    })