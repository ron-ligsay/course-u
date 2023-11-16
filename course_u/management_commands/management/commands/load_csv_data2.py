from django.core.management.base import BaseCommand
import csv
import os
import mysql.connector
#from website.models import Specialization, Field  # Import your models
#from assessment.models import Test, QuestionSet, UserResponse
#from personality.models import  MBTI, MBTISet, MBTIResponse
from django.apps import apps

# from decouple import Config, RepositoryEnv
# config = Config(RepositoryEnv('.env'))

class Command(BaseCommand):
    help = 'Import data from CSV files to MySQL database'
    
    def handle(self, *args, **options):
        connection = mysql.connector.connect(
            host='localhost',
            user='root',
            password='sql2023', # 'sql2023' , 'sawadekap', '022002
            database= 'courseu_db', #config('DB_NAME', default = 'courseu_db')#'courseu_db',
        )

        base_dir = os.getcwd()
        csv_table_mapping = {
            base_dir + '\\static\\csv\\website_field.csv': {
                'table_name': 'website_field',
                'model_name' : 'Field',
                'columns' : ['field','field_name','description','explanation'],
                'attributes' : ['INT PRIMARY KEY', 'VARCHAR(150)', 'VARCHAR(1000)', 'VARCHAR(1000)']
            },
            # base_dir + '\\static\\csv\\userdb.csv': {
            #     'table_name': 'userdb',
            #     'model_name' : 'User',
            #     'columns' : ['userid','username','password','email'],
            #     'attributes' : ['INT PRIMARY KEY', 'VARCHAR(25)', 'VARCHAR(25)', 'VARCHAR(100)' ]
            # },
            base_dir + '\\static\\csv\\website_specialization.csv': {
                'table_name': 'website_specialization',
                'model_name': 'Specialization',
                'columns': ['specialization_id', 'title','description','roadmap_id', 'field_id',],
                'attributes': ['INT PRIMARY KEY',  'VARCHAR(150)', 'VARCHAR(1000)', 'INT','INT',]
            },
            base_dir + '\\src\\linkedin_scrapy\\selenium\\jobs_post_2.csv': {
                'table_name': 'jobs_jobposting',
                'model_name': 'JobPosting',
                #jobpost_id,Link,Job_Title,Company_Name,Company_link,Date,Keyword,Keyword_id,Location,Employment_Type,Job_Function,Industries,Seniority_Level,Job_Description
                'columns': ['id','link','job_title',
                            'company_name','company_link','date_posted',
                            'keyword','keyword_id','location',
                            'employment_type','job_function','industries','seniority_level',
                            'job_description'],
                'attributes': ['INT AUTO_INCREMENT PRIMARY KEY','VARCHAR(5000)', 'VARCHAR(100)', 
                                'VARCHAR(100)', 'VARCHAR(5000)', 'DATE', 
                                'VARCHAR(100)','INT','VARCHAR(300)',
                                'VARCHAR(150)','VARCHAR(150)','VARCHAR(150)','VARCHAR(150)',
                                'TEXT'
                                ]
            },
            base_dir + '\\static\\csv\\assessment_test.csv': {
                'table_name': 'assessment_test',
                'model_name': 'Test',
                'columns':  ['question_id', 'question','description','options', 'correct_option','field_id',],
                'attributes': ['INT PRIMARY KEY', 'VARCHAR(1000)', 'VARCHAR(1000)', 'JSON', 'INT', 'INT',]
            },
            base_dir + '\\static\\csv\\assessment_questionset.csv': {
                'table_name': 'assessment_questionset',
                'model_name': 'QuestionSet',
                'columns':  ['set_id','n_questions','is_completed','score','year','user_id',],
                'attributes': ['INT PRIMARY KEY NOT NULL AUTO_INCREMENT',  'INT', 'BOOLEAN', 'INT','INT','INT',]
            },  
            base_dir + '\\static\\csv\\assessment_userresponse.csv': {
                'table_name': 'assessment_userresponse',
                'model_name': 'UserResponse',
                'columns':  ["response","selected_option","is_correct","set_id","question_id","is_answered",],
                # add default values for response and is_answered
                'attributes' : ["INT PRIMARY KEY NOT NULL AUTO_INCREMENT","INT", "BOOLEAN", "INT", "INT","BOOLEAN"]
            },
            base_dir + '\\static\\csv\\personality_mbti.csv': {
                'table_name': 'personality_mbti',
                'model_name': 'MBTI',
                'columns':  ["mbti","mbti_question","option_a","option_b","ans_a","ans_b","acr_a","acr_b"],
                'attributes' : ["INT PRIMARY KEY NOT NULL AUTO_INCREMENT","VARCHAR(1000)", "VARCHAR(1000)", "VARCHAR(1000)", "VARCHAR(15)","VARCHAR(15)","VARCHAR(1)","VARCHAR(1)"]
            },
            base_dir + '\\static\\csv\\personality_indicator.csv': {
                'table_name': 'personality_indicator',
                'model_name': 'Indicator',
                'columns':  ["indicator_id","indicator","indicator_name","indicator_description"],
                'attributes' : ["INT PRIMARY KEY NOT NULL AUTO_INCREMENT","VARCHAR(4)", "VARCHAR(50)", "VARCHAR(1000)"]
            },
            base_dir + '\\static\\csv\\website_skill.csv': {
                'table_name': 'website_skill',
                'model_name': 'Skill',
                'columns':  ["id","skill"],
                'attributes' : ["INT PRIMARY KEY NOT NULL AUTO_INCREMENT", "VARCHAR(300)"]
            },
            base_dir + '\\static\\csv\\website_specialization_skills.csv': {
                'table_name': 'website_specializationskills',
                'model_name': 'SpecializationSkills',
                'columns':  ["id","level","skill_id","specialization_id"],
                'attributes' : ["INT PRIMARY KEY NOT NULL AUTO_INCREMENT", "INT","INT","INT"]
            },
            base_dir + '\\static\\csv\\personality_indicator_skills.csv': {
                'table_name': 'personality_indicator_skills',
                'model_name': 'IndicatorSkills',
                'columns':  ["id","indicator_id","skill_id"],
                'attributes' : ["INT PRIMARY KEY NOT NULL AUTO_INCREMENT","INT", "INT"]
            },
            base_dir + '\\static\\csv\\personality_mbtiset.csv': {
                'table_name': 'personality_mbtiset',
                'model_name': 'MBTISet',
                'columns':  ["mbti_set_id","user_id","is_completed","mind","energy","nature","tactics","identity"],
                'attributes' : ["INT PRIMARY KEY NOT NULL AUTO_INCREMENT","INT", "BOOLEAN", "FLOAT", "FLOAT","FLOAT","FLOAT","VARCHAR(5) NULL"]
            },
            base_dir + '\\static\\csv\\personality_mbtiresponse.csv': {
                'table_name': 'personality_mbtiresponse',
                'model_name': 'MBTIResponse',
                'columns':  ["mbti_response_id","mbti_set_id","mbti_id","is_answered","selected_option"],
                'attributes' : ["INT PRIMARY KEY NOT NULL AUTO_INCREMENT", "INT", "INT","BOOLEAN", "INT NULL"]
            },
            base_dir + '\\static\\csv\\website_userrecommendations.csv': {
                'table_name': 'recommender_userrecommendations',
                'model_name': 'UserRecommendations',
                'columns':  ["recommendation_id","score_1","score_2","score_3","current_year","field_1_id","field_2_id","field_3_id","selected_field_id","user_id",],
                'attributes' : ["INT PRIMARY KEY NOT NULL AUTO_INCREMENT", "FLOAT","FLOAT","FLOAT","INT","INT", "INT","INT","INT","INT" ]
            },
            base_dir + '\\static\\csv\\assessment_test_skills.csv': {
                'table_name': 'assessment_test_skills',
                'model_name': 'TestSkill',
                'columns':  ["id","test_id","skill_id"],
                'attributes' : ["INT PRIMARY KEY NOT NULL AUTO_INCREMENT", "INT","INT"]
            },
            base_dir + '\\static\\csv\\acad_course.csv': {
                'table_name': 'acad_course',
                'model_name': 'Course',
                'columns':  ["id","course_name","number_of_years","description"],
                'attributes' : ["INT PRIMARY KEY NOT NULL AUTO_INCREMENT", "VARCHAR(100)","INT","VARCHAR(1000)"]
            },
            base_dir + '\\static\\csv\\acad_subject.csv': {
                'table_name': 'acad_subject',
                'model_name': 'Subject',
                'columns':  ["id","subject_name","description"],
                'attributes' : ["INT PRIMARY KEY NOT NULL AUTO_INCREMENT", "VARCHAR(100)","VARCHAR(1000)"]
            },
            base_dir + '\\static\\csv\\acad_subject_skills.csv': {
                'table_name': 'acad_subject_skills',
                'model_name': 'SubjectSkills',
                'columns':  ["id","subject_id","skill_id"],
                'attributes' : ["INT PRIMARY KEY NOT NULL AUTO_INCREMENT", "INT","INT"]
            },
            base_dir + '\\static\\csv\\acad_curriculum.csv': {
                'table_name': 'acad_curriculum',
                'model_name': 'Curriculum',
                'columns':  ["id","year","course_id","subject_id"],
                'attributes' : ["INT PRIMARY KEY NOT NULL AUTO_INCREMENT", "INT","INT","INT"]
            },
            base_dir + '\\static\\csv\\acad_studentprofile.csv': {
                'table_name': 'acad_studentprofile',
                'model_name': 'StudentProfile',
                'columns':  ["id","is_student","current_year","enrolled_courses_id","user_id"],
                'attributes' : ["INT PRIMARY KEY NOT NULL AUTO_INCREMENT", "BOOLEAN","INT","INT","VARCHAR(100)"]
            },
            base_dir + '\\static\\csv\\recommender_userskillsource.csv': {
                'table_name': 'recommender_userskillsource',
                'model_name': 'UserSkillSource',
                'columns':  ["id","user_id","skill_id","source"],
                'attributes' : ["INT PRIMARY KEY NOT NULL AUTO_INCREMENT", "INT","INT","VARCHAR(100)"]
            },
            base_dir + '\\static\\csv\\recommender_userskill.csv': {
                'table_name': 'recommender_userskill',
                'model_name': 'UserSkill',
                'columns':  ["id","user_id","skill_id","source","skill_level"],
                'attributes' : ["INT PRIMARY KEY NOT NULL AUTO_INCREMENT", "INT","INT","VARCHAR(100)","INT"]
            },
        }
        
        cursor = connection.cursor()
        
       
        for csv_file_path, table_info in csv_table_mapping.items():
             # Check if the table exists
            
            query = f"SHOW TABLES LIKE '{table_info['table_name']}'"
            cursor.execute(query)
            table_exists = cursor.fetchone() is not None

            if table_exists:
                print(f"Table '{table_info['table_name']}' already exists. Skipping creating table...")
            else:
                print(f"Creating table '{table_info['table_name']}'...")
                print(table_info['attributes'])
                # ... (create the table)
                col_list = table_info['columns']
                attr_list = table_info['attributes']
                #columnns = ', '.join([f"`{col}` {attr}" for col, attr in zip(table_info['columns'], table_info['attributes'])])
                columns = ', '.join([f"{col} {attr}" for col, attr in zip(col_list, attr_list)])
                print("Columns: ",columns)
                query = f"CREATE TABLE IF NOT EXISTS `{table_info['table_name']}` ( {columns} );"
                print("Query: ",query)
                cursor.execute(query)
                connection.commit()
                print("Now loading data to the table...")
            # Load data from CSV
            with open(csv_file_path, 'r') as file:
                csv_reader = csv.DictReader(file)
                # for row in csv_reader:
                #     try:
                #         columns = ', '.join(row.keys())
                #         placeholders = ', '.join(['%s'] * len(row))
                #         query = f"INSERT INTO {table_info['table_name']} ({columns}) VALUES ({placeholders})"
                #         print("query: ", query)
                #         cursor.execute(query, tuple(row.values()))
                #     except mysql.connector.errors.DataError as e:
                #         print(f"Error Importing row {row + 1}: {e}")
                #         print(f"Stack trace: {e.__traceback__}")
                for row_number, row in enumerate(csv_reader):
                    try:
                        columns = ', '.join(row.keys())
                        placeholders = ', '.join(['%s'] * len(row))
                        query = f"INSERT INTO {table_info['table_name']} ({columns}) VALUES ({placeholders})"
                        print("query: ", query)
                        cursor.execute(query, tuple(row.values()))
                    except mysql.connector.errors.DataError as e:
                        print(f"Error Importing row {row_number + 1}: {e}")
                        print(f"Stack trace: {e.__traceback__}")
                        
        connection.commit()
        cursor.close()
        connection.close()

        self.stdout.write(self.style.SUCCESS('Data imported successfully'))


print("Database created successfully")