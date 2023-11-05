from django.core.management.base import BaseCommand
from django.db import connection

class Command(BaseCommand):
    help = 'Delete all database tables'

    def handle(self, *args, **options):
        # Get a list of table names from the database
        #table_names = connection.introspection.table_names()
        #print(table_names)
        table_names1 = [
            'acad_curriculum','acad_student','acad_course','acad_subject', 'acad_subject_skills',
            'assessment_userresponse','assessment_questionset', 'assessment_test', 'assessment_test_skills',
            'auth_group_permissions','auth_user_groups','auth_group', 'auth_user_user_permissions',
            'auth_permission', 'django_admin_log','auth_user', 
            'django_content_type', 'django_migrations', 'django_session', 
            'personality_mbtiresponse', 'personality_mbti', 'personality_mbtiset',
            'jobs_jobposting',
            'website_specialization', 'website_field','website_userprofile', 
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

        # Iterate through the table names and delete each table
        with connection.cursor() as cursor:
            for table_name in table_names:
                #cursor.execute(f"DROP TABLE {table_name};")
                cursor.execute(f"DROP TABLE IF EXISTS {table_name};")
                self.stdout.write(self.style.SUCCESS(f'Deleted table: {table_name}'))

        self.stdout.write(self.style.SUCCESS('All database tables deleted'))
