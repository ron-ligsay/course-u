import numpy as np
import pandas as pd

IT_subset = pd.read_csv('data/IT_subset.csv')

IT_subset['Skills'] = IT_subset['Key Skills'].apply(lambda x: x.split('|'))
IT_subset['Skills'] = IT_subset['Skills'].apply(lambda x: [item.strip() for item in x])
IT_subset['Skills'] = IT_subset['Skills'].apply(lambda x: list(set([item.lower() for item in x])))
IT_subset.head()


# Flatten the lists in the list_column and convert all strings to lowercase
flat_list = [item.lower() for sublist in IT_subset['Skills'] for item in sublist]

# Create a dictionary to store unique strings and their counts
unique_counts = {}
for item in flat_list:
    if item in unique_counts:
        unique_counts[item] += 1
    else:
        unique_counts[item] = 1

# Create a new DataFrame from the dictionary
df_skill_count = pd.DataFrame({'Unique String': list(unique_counts.keys()), 'Count': list(unique_counts.values())})

print(df_skill_count)


df_skill_count.sort_values(by="Count",ascending=False).tail(5)

skill_list_opt = df_skill_count['Unique String'].tolist()

# Filter out strings not in the filter list for each row
IT_subset['Skills'] = IT_subset['Skills'].apply(lambda lst: [item for item in lst if item in skill_list_opt])

def combine_skills(skills):
    flat_skills = [skill for sublist in skills for skill in sublist]
    return ','.join(flat_skills)

grouped_IT_subset = IT_subset.groupby('role_job')['Skills'].agg(combine_skills).reset_index()

grouped_IT_subset

# not used


# Combine skills for each role
grouped = IT_subset.groupby('role_job')['Skills'].sum()
grouped


# Group by 'Role' and aggregate skills with their frequencies
grouped_df = IT_subset.groupby('role_job')['Skills'].sum().apply(lambda skills: pd.Series(skills).value_counts()).fillna(0).reset_index()

grouped_df.head()

# Group by 'Role' and aggregate skills with their frequencies
grouped_df = IT_subset.groupby('role_job')['Skills'].sum().apply(lambda skills: pd.Series(skills).value_counts()).fillna(0).reset_index()

grouped_df.head()

# diff way of normalizing

# Calculate total skills for each role
grouped_df['TotalSkills'] = grouped_df.drop('role_job', axis=1).sum(axis=1)

# Normalize skill frequencies by dividing by total skills
normalized_df = grouped_df.copy()
normalized_df.iloc[:, 1:-1] = normalized_df.iloc[:, 1:-1].div(normalized_df['TotalSkills'], axis=0)

# Calculate recommendation scores based on normalized skill frequencies
normalized_df['Score'] = normalized_df.iloc[:, 1:-1].sum(axis=1)

normalized_df.tail()



def content_recommender_normalized(input_skills):
    #Create a DataFrame containing only the input skills' columns
    input_skills_df = normalized_df[['role_job'] + input_skills]

    # Calculate the sum of normalized skill frequencies for each role
    role_normalized_sums = input_skills_df[input_skills].sum(axis=1)

    # Set the normalized sums as the input scores
    input_skills_df['InputScore'] = role_normalized_sums
    
    # Calculate percentages based on the input scores
    input_skills_df['Percentage'] = (input_skills_df['InputScore'] / input_skills_df['InputScore'].sum()) * 100
    
    # Get the top recommended roles based on the normalized input scores
    top_roles = input_skills_df.sort_values(by='InputScore', ascending=False).head(5)
    
     # Calculate the sum of the top 5 InputScores
    top_5_input_score_sum = top_roles['InputScore'].sum()

    # Calculate the percentage contribution of each role's InputScore
    top_roles['Top 5 Percentage'] = (top_roles['InputScore'] / top_5_input_score_sum) * 100
    
    # Format the Percentage column to display with two decimal places
    top_roles['Top 5 Percentage'] = top_roles['Top 5 Percentage'].apply(lambda x: '{:.0f}%'.format(x))
    
    return top_roles[['role_job', 'Top 5 Percentage']]#'InputScore','Percentage',


item_set_1 = ['html','css','javascript','design','web','php','web application','bootstrap','ui','json','backend']
item_set_2 = ['python','sql','analytical','data analysis']
item_set_3 = ['java','c++','c']
item_set_4 = ['machine learning','apache','mvc','algorithm','artificial intelligence']#'
item_set_5 = ['github']

my_skills = item_set_4

print("Top 5 Recommended Roles")
content_recommender_normalized(my_skills)


# others

skills = [col for col in normalized_df.columns if col not in ['Role','TotalSkills','Score']]
print("Total Skills: " , len(skills))

def in_skill_list(skill):
    if skill in skills:
        print(skill, "is present in the list.")
    else:
        print(skill, "is not present in the list.")

in_skill_list('web')