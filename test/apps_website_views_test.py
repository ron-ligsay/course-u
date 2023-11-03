from django.test import TestCase
from django import setup
import os
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "course_u.settings")
setup()

# Create your tests here.
from apps.website.models import Field, Specialization

class SpecializationTestCase(TestCase):
    # def setUp(self):
    #     Post.objects.create(title="test", content="test")

    # def test_post(self):
    #     post = Post.objects.get(title="test")
    #     self.assertEqual(post.content, "test")
    
    def test_field_exists(self):
        #field = Field.objects.get(field_name="test")
        #self.assertEqual(field.description, "test")
        query = Field.objects.all()
        self.assertTrue(query.exists())
    
    def test_specialization_exists(self):
        # specialization = Specialization.objects.get(title="test")
        # self.assertEqual(specialization.description, "test")
        query = Specialization.objects.all()
        self.assertTrue(query.exists())