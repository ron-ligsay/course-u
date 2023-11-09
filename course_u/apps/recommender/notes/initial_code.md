# Columns
Id, crawl timestamp, Job Title, job salary, job experiece required, key skills, role category
location, functional area, industry, role


# Get Functional Area
where it has 'IT'

IT = nakuri[nakuri['Functional Area'].fillna(0).str.contains("IT", na=False)]
IT = IT[IT['Functional Area'] != "ITES , BPO , KPO , LPO , Customer Service , Operations"]
IT = IT[IT['Functional Area'].map(IT['Functional Area'].value_counts()) > 2]

# Subset
IT_subset = IT[['Job Title','Key Skills','Role Category','Functional Area','Industry', "Role"]]

# Remove missing
IT_subset[IT_subset['Key Skills'].isna()]
IT_subset.dropna(subset=['Key Skills'], inplace=True)

# nunique
IT_subset.nunique()
-
Job Title           8499
Key Skills         10325
Role Category         20
Functional Area       16
Industry              75
Role                  60

# clean key skills
IT_subset['Skills'] = IT_subset['Key Skills'].apply(lambda x: x.split('|'))
IT_subset['Skills'] = IT_subset['Skills'].apply(lambda x: [item.strip() for item in x])
IT_subset['Skills'] = IT_subset['Skills'].apply(lambda x: list(set([item.lower() for item in x])))



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
            Unique String  Count
0       technical support    241
1        test engineering     41
2        web technologies    614
3              test cases    206
4          manual testing    131
...                   ...    ...
6854  network integration      1
6855           metasploit      1
6856              web app      1
6857                 kali      1
6858    burp professional      1


# filter where Count > 45
df_skill_count = df_skill_count[df_skill_count['Count'] > 45]


# Balancing
df_skill_count['Count'] = df_skill_count['Count'].apply(lambda x: 500 if x > 500 else x)

# Representation (Bins)
plt.hist(df_skill_count['Count'], bins=30, edgecolor='black')  # Adjust the number of bins as needed
plt.title('Histogram of Numerical Data')
plt.xlabel('Value')
plt.ylabel('Frequency')
plt.show()


# Combine skills for each role
grouped = IT_subset.groupby('Role')['Skills'].sum()
-
Role
Business Analyst                               [business intelligence, sql, data analysis, ex...
CIO                                                                 [it infrastructure, banking]
CTO/Head/VP-Technology (Telecom/ISP)                             [it infrastructure, networking]
Customer Support Engineer/Technician           [e-commerce, big data, banking, hardware, wind...


# Group by 'Role' and aggregate skills with their frequencies
grouped_df = IT_subset.groupby('Role')['Skills'].sum().apply(lambda skills: pd.Series(skills).value_counts()).fillna(0).reset_index()


# Normalizing
# diff way of normalizing

# Calculate total skills for each role
grouped_df['TotalSkills'] = grouped_df.drop('Role', axis=1).sum(axis=1)

# Normalize skill frequencies by dividing by total skills
normalized_df = grouped_df.copy()
normalized_df.iloc[:, 1:-1] = normalized_df.iloc[:, 1:-1].div(normalized_df['TotalSkills'], axis=0)

# Calculate recommendation scores based on normalized skill frequencies
normalized_df['Score'] = normalized_df.iloc[:, 1:-1].sum(axis=1)

normalized_df.head()


# Recommender code
def content_recommender_normalized(input_skills):
    #Create a DataFrame containing only the input skills' columns
    input_skills_df = normalized_df[['Role'] + input_skills]

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
    
    return top_roles[['Role', 'Top 5 Percentage']]#'InputScore','Percentage',




# using the recommender
content_recommender_normalized(['java','c++','c'])


It appears you've provided a comprehensive analysis of IT job titles and skills, including data cleaning, skill frequency distribution, and recommendation algorithms. The code snippet demonstrates various data manipulation techniques and showcases the ability to extract insights from job postings. The process of identifying relevant skills, filtering based on frequency, and normalizing skill scores to provide recommendations is well-structured.

Here's a breakdown of the key steps involved:

1. **Data Cleaning and Preparation:**
   a. Filter IT-related job postings based on the "Functional Area" column.
   b. Remove missing values from the "Key Skills" column.
   c. Clean and standardize skill names by converting them to lowercase and removing duplicates.

2. **Skill Frequency Analysis:**
   a. Flatten the list of skills from each job posting into a single list.
   b. Create a dictionary to store unique skills and their corresponding frequencies.
   c. Filter the dictionary to include only skills with a frequency greater than 45.

3. **Skill Distribution Representation:**
   a. Create a histogram to visualize the distribution of skill frequencies.
   b. Adjust the number of bins in the histogram to improve the representation of the data.

4. **Role-Based Skill Aggregation:**
   a. Group job postings by "Role" and aggregate their corresponding skills.
   b. Convert the aggregated skills into a pandas DataFrame for further analysis.

5. **Skill Normalization:**
   a. Calculate the total number of skills for each role.
   b. Divide the frequency of each skill by the total skills for that role to obtain normalized frequencies.

6. **Recommendation Algorithm:**
   a. Create a function that takes a list of input skills and returns the top 5 recommended roles.
   b. Calculate the normalized skill frequencies for each role based on the input skills.
   c. Sort the roles based on their normalized input scores and select the top 5.
   d. Calculate the percentage contribution of each role's InputScore to the total.
   e. Format the percentages to display with two decimal places.

Overall, the code demonstrates a well-structured approach to analyzing job postings, identifying relevant skills, and providing recommendations based on normalized skill frequencies. It highlights the importance of data cleaning, skill aggregation, and normalization in developing effective recommendation systems.

Here's a summary of my thoughts on your code.

I think your code is comprehensive and well-structured. You've clearly put a lot of thought into how to clean the data, extract the relevant information, and make recommendations. I'm particularly impressed with your use of histograms to visualize the distribution of skill frequencies and your use of normalized skill frequencies to provide recommendations.

Here are a few recommendations I have for you:

* I think it would be interesting to see how the recommendations change if you use different input skills. For example, what would the recommendations be for someone who is skilled in both Java and Python?
* It would also be interesting to see how the recommendations change if you use different normalization techniques. For example, what would the recommendations be if you used TF-IDF instead of normalized skill frequencies?

I think your code is a great starting point for developing a more sophisticated recommendation system. I would encourage you to continue to experiment with different methods and see how you can improve the accuracy of your recommendations.

Overall, I think you've done a great job with this project. Keep up the good work!



