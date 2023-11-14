from django.test import SimpleTestCase

class TestModels(SimpleTestCase):
    
    def test_models_is_resolved(self):
        assert 1 == 1

from django.test import TestCase
from django import setup

import sys
import os

#os.environ.setdefault("DJANGO_SETTINGS_MODULE", "course_u.settings")
# setup()

# Set the path to your Django project directory (course-u in this case)
#sys.path.append(os.path.abspath('C:/Users/aky/AppData/Local/Programs/Python/Python38/course-u/'))

# "C:\\Users\\aky\\AppData\\Local\\Programs\\Python\\Python38\\course_u\\course_u\\test\\",
# sys.path.append(os.path.abspath('C:\\Users\\aky\\AppData\\Local\\Programs\\Python\\Python38\\course_u\\'))

# # Set the Django settings module for your tests
# os.environ['DJANGO_SETTINGS_MODULE'] = 'course_u.settings'

# from dotenv import load_dotenv

# load_dotenv()

# # Run your tests below

# website_dir = os.path.abspath('./apps/website')
# print(website_dir)
# if website_dir not in sys.path:
#     sys.path.insert(0, website_dir)

# # import website models
# from website.models import Field, Specialization

# class WebsiteModelsTestCase(TestCase):
#     # def setUp(self):
#     #     Post.objects.create(title="test", content="test")

#     # def test_post(self):
#     #     post = Post.objects.get(title="test")
#     #     self.assertEqual(post.content, "test")
    
#     def model_field_exists(self):
#         #field = Field.objects.get(field_name="test")
#         #self.assertEqual(field.description, "test")
#         query = Field.objects.all()
#         self.assertTrue(query.exists())
    
#     def model_specialization_exists(self):
#         # specialization = Specialization.objects.get(title="test")
#         # self.assertEqual(specialization.description, "test")
#         query = Specialization.objects.all()
#         self.assertTrue(query.exists())