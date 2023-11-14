from django.core.management.base import BaseCommand
from django.db import connection

class Command(BaseCommand):
    help = 'Delete all database tables'

    def handle(self, *args, **options):
        # Get a list of table names from the database
        #table_names = connection.introspection.table_names()
        #print(table_names)
        table_names1 = [ # Ordered by dependency
            'acad_curriculum','acad_studentgrades','acad_studentprofile','acad_course','acad_subject', 'acad_subject_skills', 
            'assessment_userresponse','assessment_questionset', 'assessment_test', 'assessment_test_skills',
            
            'personality_mbtiresponse', 'personality_mbti', 'personality_mbtiset', 'personality_indicator_skills','personality_indicator',
            'recommender_userskillsource','recommender_userskill',

            # 'auth_group_permissions','auth_user_groups','auth_group', 'auth_user_user_permissions',
            # 'auth_permission', 'django_admin_log','auth_user', 
            # 'django_content_type', 'django_migrations', 'django_session', 

            'jobs_jobposting',
            'website_specialization', 'website_field','website_userprofile', 'website_skill', 'website_userrecommendations'
            ]

        table_skill = [
            'acad_subject_skills', 'assessment_test_skills', 'personality_indicator_skills','website_specializationskills', 
            'recommender_userskillsource','recommender_userskill',
            'website_skill', 'website_userrecommendations'
        ]
        
        table_names = [
            #'acad_student','acad_course',
            'acad_studentgrades','acad_subject_skills','acad_curriculum','acad_subject',
            #'assessment_userresponse','assessment_questionset', 
            'assessment_test_skills','assessment_test', 
            #'personality_mbtiresponse', 'personality_mbti', 'personality_mbtiset',
            #'jobs_jobposting',
            #'website_specialization', 'website_field','website_userprofile', 
            'website_skill',
        ]

        # for assessment test and test skills
        table_assessment = [
           'assessment_userresponse', 'assessment_questionset','assessment_test_skills','assessment_test'
        ]

        table_names0 = [
            'assessment_userresponse'
        ]

        # Iterate through the table names and delete each table
        with connection.cursor() as cursor:
            for table_name in table_names1:
                cursor.execute(f"DROP TABLE IF EXISTS {table_name};")
                self.stdout.write(self.style.SUCCESS(f'Deleted table: {table_name}'))

        self.stdout.write(self.style.SUCCESS('All database tables deleted'))
