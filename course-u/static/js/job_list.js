// <!-- Include jQuery library -->
// <script src="https://code.jquery.com/jquery-3.6.0.min.js"></script>
// <!-- Include your custom JavaScript file -->
// <script src="{% static 'js/job_list.js' %}"></script>

// <script>
//     // Initialize when the document is ready
//     $(document).ready(function () {
//         // Handle clicks on job cards with data-job-id attribute
//         $('.job-card[data-job-id]').click(function () {
//             // Get the job ID from the data attribute
//             var jobId = $(this).data('job-id');
//             // Update the URL dynamically
//             window.location.href = `/job_list/${jobId}/`;
//         });
//     });
// </script>
$(document).ready(function () {
    // Handle clicks on job cards with data-job-id attribute
    $('.job-card[data-job-id]').click(function () {
        // Get the job ID from the data attribute
        var jobId = $(this).data('job-id');
        // Update the URL dynamically
        window.location.href = `/job_list/${jobId}/`;
    });
});
