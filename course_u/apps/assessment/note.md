Creating a flowchart in text format can be challenging, but I can provide you with a step-by-step outline of the flow:

1. User accesses the "start_test" view.
2. Session variables are cleared.
3. The system checks if the user has an incomplete test (an incomplete question set).
4. If an incomplete test exists:
   a. The user is informed of the incomplete test.
   b. The system retrieves the incomplete test and its details.
   c. If the incomplete test has the expected number of questions:
      i. The user is informed that they have completed the test.
      ii. The user is redirected to the "test_overview" view.
   d. If the incomplete test does not have the expected number of questions:
      i. The system identifies the test fields with missing questions.
      ii. For each field with missing questions:
          - The system calculates how many questions are missing.
          - The system generates UserResponse objects for the missing questions, marking them as not answered.
      iii. The system updates the session variables to track the progress.
      iv. The system starts the test.
5. If no incomplete test exists:
   a. The system determines the new set ID for the user.
   b. A new QuestionSet is created with the new set ID, assigned to the user, and marked as not completed.
   c. The system retrieves a set of test questions (e.g., 2 questions per field) for the new question set.
   d. UserResponse objects are created for the new questions, marked as not answered.
   e. Session variables are updated to track the progress.
   f. The system starts the test.

Please note that this outline follows the code structure provided earlier and may require more details for specific error handling and user messaging. It's advisable to create a visual flowchart using a flowcharting tool or diagram software for a more comprehensive representation of the flow.