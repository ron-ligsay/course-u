from django.db import models
from django.apps import apps

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
