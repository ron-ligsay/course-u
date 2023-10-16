import os

# Function to find and print .pyc files in a directory and its subdirectories
def find_pyc_files(directory):
    for root, _, files in os.walk(directory):
        for file in files:
            if file.endswith('.pyc'):
                pyc_file_path = os.path.join(root, file)
                print(pyc_file_path)

# Function to find and delete .pyc files in a directory and its subdirectories
def find_and_delete_pyc_files(directory):
    for root, _, files in os.walk(directory):
        for file in files:
            if file.endswith('.pyc'):
                pyc_file_path = os.path.join(root, file)
                print(f"Deleting {pyc_file_path}")
                os.remove(pyc_file_path)

# Function to find .py files under all migrations folders
def find_py_files_in_migrations(root_directory,excluded_files=None):
    py_files = []
    for root, _, files in os.walk(root_directory):
        if 'migrations' in root:
            for file in files:
                if file.endswith('.py') and file not in excluded_files:
                    py_file_path = os.path.join(root, file)
                    py_files.append(py_file_path)
    return py_files

# Function to find and delete .py files in migrations folders
def delete_py_files_in_migrations(root_directory, excluded_files=None):
    #excluded_files = {'0001_auto_20230907_1949.py'}  # Add filenames to exclude here
    deleted_files = []
    
    for root, _, files in os.walk(root_directory):
        if 'migrations' in root:
            for file in files:
                if file.endswith('.py') and file not in excluded_files:
                    py_file_path = os.path.join(root, file)
                    os.remove(py_file_path)
                    deleted_files.append(py_file_path)
    return deleted_files

# Specify the directory you want to search in
directory_to_search = os.getcwd()# + '\\..'  # Replace with your directory path
excluded_files = {'__init__.py','0001_auto_20230907_1949.py'}  # Add filenames to exclude here

def print_migration_files(excluded_files=None):
    

    # Call the function to find .py files under all migrations folders
    py_files_in_migrations = find_py_files_in_migrations(directory_to_search, excluded_files)

    # Print the list of .py files found
    for py_file in py_files_in_migrations:
        print(py_file)

def remove_migration_files(excluded_files=None):

    # Call the function to delete .py files in migrations folders (excluding specified files)
    deleted_files = delete_py_files_in_migrations(directory_to_search,excluded_files)

    # Print the list of deleted files
    for deleted_file in deleted_files:
        print(f"Deleted: {deleted_file}")


# Call the function to find and print .pyc files
#find_pyc_files(directory_to_search)

# Call the function to find and delete .pyc files
#find_and_delete_pyc_files(directory_to_search)

#print_migration_files()

#remove_migration_files()

# Checker
def check():
    find_pyc_files(directory_to_search)
    print_migration_files(excluded_files)

# deleter
def delete():
    find_and_delete_pyc_files(directory_to_search)
    remove_migration_files(excluded_files)

# Use this to verfiy that the files that will be deleted
#check()

# Once verified, you can delete the files
#delete()