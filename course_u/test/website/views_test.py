from django.test import SimpleTestCase

class TestViews(SimpleTestCase):
    
    def test_views_is_resolved(self):
        assert 1 == 1

# from django.test import TestCase
# from utilities.model_utils import get_all_models, extract_field_types

# # import a model for testing
# from website.models import Field

# class TestUtils(TestCase):
#     def test_get_all_models(self):
#         all_models = get_all_models()
#         self.assertTrue(len(all_models) > 0)  # Ensure there are models
#         print(all_models)

#     def test_extract_field_types(self):
#         field_types = extract_field_types(Field)
#         self.assertTrue(len(field_types) > 0)  # Ensure there are field types
#         self.assertIsInstance(field_types, dict)  # Ensure field_types is a dictionary
#         print(field_types)
