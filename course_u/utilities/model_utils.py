from django.db import models
from django.apps import apps
import os

BASE_DIR = os.getcwd()

def get_all_models():
    """
    Get all models in the project.

    Returns:
        list: A list of all models in the project.
    """
    #return [model for model in models.get_models()]
    return apps.get_models()


def extract_field_types(model):
    """
    Extract field types from a Django model.

    Args:
        model (models.Model): The model from which to extract field types.

    Returns:
        dict: A dictionary mapping field names to field types.
    """
    model_fields = model._meta.get_fields()
    field_types = {}

    for field in model_fields:
        field_name = field.name
        field_type = field.get_internal_type()
        field_types[field_name] = field_type

    return field_types

def get_model_table_name(model):
    """
    Get the table name of a Django model.

    Args:
        model (models.Model): The model from which to extract the table name.

    Returns:
        str: The table name of the model.
    """
    return model._meta.db_table

# List of CSV files for each model
# Path: course_u/utilities/model_utils.py
from django.conf import settings
from django.apps import apps
from django.core.management import call_command

def get_csv_files():
    """
    Get the CSV files for each model in the project.

    Returns:
        list: A list of CSV files for each model in the project.
    """

    base_dir = settings.BASE_DIR

    csv_files = []

    for model in apps.get_models():
        #csv_file = model.__name__ + '.csv'
        csv_file = base_dir + '\\static\\csv\\' + model.__name__ + '.csv'
        csv_files.append(csv_file)
        print(model,", located on ", csv_file)

    return csv_files

def select_csv_file(csv_files, table_name):
    """
    Select the CSV file for a given table name.

    Args:
        csv_files (list): A list of CSV files.
        table_name (str): The table name for which to select the CSV file.

    Returns:
        str: The CSV file for the given table name.
    """
    for csv_file in csv_files:
        if table_name in csv_file:
            print("Selected CSV file: ", csv_file)
            return csv_file
    
    return None


def get_csv_table_mapping(this_only_list = [], skip_list = []):
    """
    Get the mapping of CSV files to table names.

    Returns:
        dict: A dictionary mapping CSV files to table names.
    """
    csv_files = get_csv_files()
    csv_table_mapping = {}


    for model in apps.get_models():
        
        # if this model is in the skip list, skip it
        if model._meta.db_table in skip_list:
            print("Skipping ", model._meta.db_table, " because it is in the skip_list")
            continue
        
        # if this only list is empty dont skip anything
        if len(this_only_list) > 0:
            if model._meta.db_table not in this_only_list:
                print("Skipping ", model._meta.db_table, " because it is not in the this_only_list")
                continue

        csv_file = select_csv_file(csv_files, model._meta.db_table)
        csv_table_mapping[csv_file] = model._meta.db_table
        
        # columns
        column = []
        for field in model._meta.get_fields():
            column.append(field.name)
        
        # attributes
        attribute = []
        for field in model._meta.get_fields():
            attribute.append(field.get_internal_type())

        csv_table_mapping[csv_file] = {
            'table_name': model._meta.db_table,
            'model_name': model.__name__,
            'columns': column,
            'attributes' : attribute
        }

    return csv_table_mapping



def static_csv_table_mapping():
    csv_table_mapping = {
        BASE_DIR + '\\static\\csv\\field.csv': {
            'table_name': 'website_field',
            'model_name' : 'Field',
            'columns' : ['field','field_name','description'],
            'attributes' : ['INT PRIMARY KEY', 'VARCHAR(150)', 'VARCHAR(1000)']
        },
        BASE_DIR + '\\static\\csv\\userdb.csv': {
            'table_name': 'userdb',
            'model_name' : 'User',
            'columns' : ['userid','username','password','email'],
            'attributes' : ['INT PRIMARY KEY', 'VARCHAR(25)', 'VARCHAR(25)', 'VARCHAR(100)' ]
        },
        BASE_DIR + '\\static\\csv\\specialization1.csv': {
            'table_name': 'website_specialization',
            'model_name': 'Specialization',
            'columns': ['specialization_id', 'field_id', 'title','description','roadmap_id'],
            'attributes': ['INT PRIMARY KEY', 'INT', 'VARCHAR(100)', 'VARCHAR(1000)', 'INT',]
        },
        BASE_DIR + '\\src\\linkedin_scrapy\\selenium\\jobs_post_2.csv': {
            'table_name': 'jobs_jobposting',
            'model_name': 'JobPosting',
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
        BASE_DIR + '\\static\\csv\\test.csv': {
            'table_name': 'assessment_test',
            'model_name': 'Test',
            'columns':  ['question_id', 'field_id','question','description','options', 'correct_option',],
            'attributes': ['INT PRIMARY KEY', 'INT', 'VARCHAR(1000)', 'VARCHAR(1000)', 'JSON', 'INT',]
        },
        BASE_DIR + '\\static\\csv\\questionset.csv': {
            'table_name': 'assessment_questionset',
            'model_name': 'QuestionSet',
            'columns':  ['set_id','user_id','n_questions','is_completed','score',],
            'attributes': ['INT PRIMARY KEY NOT NULL AUTO_INCREMENT', 'INT', 'INT', 'BOOLEAN', 'INT',]
        },  
        BASE_DIR + '\\static\\csv\\userresponse.csv': {
            'table_name': 'assessment_userresponse',
            'model_name': 'UserResponse',
            'columns':  ["response","selected_option","is_correct","set_id","question_id","is_answered",],
            'attributes' : ["INT PRIMARY KEY NOT NULL AUTO_INCREMENT","INT", "BOOLEAN", "INT", "INT","BOOLEAN"]
        },
        BASE_DIR + '\\static\\csv\\mbti.csv': {
            'table_name': 'personality_mbti',
            'model_name': 'MBTI',
            'columns':  ["mbti","mbti_question","option_a","option_b","ans_a","ans_b","acr_a","acr_b"],
            'attributes' : ["INT PRIMARY KEY NOT NULL AUTO_INCREMENT","VARCHAR(1000)", "VARCHAR(1000)", "VARCHAR(1000)", "VARCHAR(15)","VARCHAR(15)","VARCHAR(1)","VARCHAR(1)"]
        },
        BASE_DIR + '\\static\\csv\\mbti_set.csv': {
            'table_name': 'personality_mbtiset',
            'model_name': 'MBTISet',
            'columns':  ["mbti_set_id","user_id","is_completed","mind","energy","nature","tactics","identity"],
            'attributes' : ["INT PRIMARY KEY NOT NULL AUTO_INCREMENT","INT", "BOOLEAN", "FLOAT", "FLOAT","FLOAT","FLOAT","VARCHAR(5)"]
        },
        BASE_DIR + '\\static\\csv\\user_mbti_response.csv': {
            'table_name': 'personality_mbtiresponse',
            'model_name': 'MBTIResponse',
            'columns':  ["mbti_response_id","mbti_set_id","mbti_id","is_answered","selected_option"],
            'attributes' : ["INT PRIMARY KEY NOT NULL AUTO_INCREMENT", "INT", "INT","BOOLEAN", "INT NULL"]
        },
        BASE_DIR + '\\static\\csv\\user_recommendations.csv': {
            'table_name': 'website_userrecommendations',
            'model_name': 'UserRecommendations',
            'columns':  ["recommendation_id","user_id","field_1_id","field_2_id","field_3_id", "score_1","score_2","score_3"],
            'attributes' : ["INT PRIMARY KEY NOT NULL AUTO_INCREMENT", "INT","INT", "INT","INT", "FLOAT","FLOAT","FLOAT"]
        },
        BASE_DIR + '\\static\\csv\\skill.csv': {
            'table_name': 'website_skill',
            'model_name': 'Skill',
            'columns':  ["id","skill"],
            'attributes' : ["INT PRIMARY KEY NOT NULL AUTO_INCREMENT", "VARCHAR(300)"]
        },
        BASE_DIR + '\\static\\csv\\test_skill.csv': {
            'table_name': 'assessment_test_skills',
            'model_name': 'TestSkill',
            'columns':  ["id","test_id","skill_id"],
            'attributes' : ["INT PRIMARY KEY NOT NULL AUTO_INCREMENT", "INT","INT"]
        },
        BASE_DIR + '\\static\\csv\\courses.csv': {
            'table_name': 'acad_course',
            'model_name': 'Course',
            'columns':  ["id","course_name","number_of_years","description"],
            'attributes' : ["INT PRIMARY KEY NOT NULL AUTO_INCREMENT", "VARCHAR(100)","INT","VARCHAR(1000)"]
        },
        BASE_DIR + '\\static\\csv\\subjects.csv': {
            'table_name': 'acad_subject',
            'model_name': 'Subject',
            'columns':  ["id","subject_name","description"],
            'attributes' : ["INT PRIMARY KEY NOT NULL AUTO_INCREMENT", "VARCHAR(100)","VARCHAR(1000)"]
        },
        BASE_DIR + '\\static\\csv\\curriculum.csv': {
            'table_name': 'acad_curriculum',
            'model_name': 'Curriculum',
            'columns':  ["id","year","course_id","subject_id"],
            'attributes' : ["INT PRIMARY KEY NOT NULL AUTO_INCREMENT", "INT","INT","INT"]
        },
        BASE_DIR + '\\static\\csv\\studentprofile.csv': {
            'table_name': 'acad_studentprofile',
            'model_name': 'StudentProfile',
            'columns':  ["studentprofile_id","user_id","is_student","enrolled_courses","current_year"],
            'attributes' : ["INT PRIMARY KEY NOT NULL AUTO_INCREMENT", "INT","BOOLEAN","VARCHAR(100)","INT"]
        },
    }