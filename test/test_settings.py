# from course_u.settings import *

# # Use a different database for testing (e.g., in-memory SQLite)
# DATABASES = {
#     'default': {
#         'ENGINE': 'django.db.backends.sqlite3',
#         'NAME': ':memory:',
#     }
# }

# # Set test-related configurations
# DEBUG = False  # Disable debugging for tests
# TESTING = True  # A custom flag for identifying test environment
# SECRET_KEY = 'your-secret-key'  # Replace with a random value

# # Disable migrations during testing to speed up test setup
# MIGRATION_MODULES = {app: 'your_app_name.test_migrations' for app in INSTALLED_APPS}

# # Add any other test-specific settings or configurations here

# # Use the console email backend for testing (to prevent sending real emails)
# EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'
