
$(document).ready(function () {
    // Handle clicks on job cards with data-job-id attribute
    $('.card-link[field_id]').click(function () {
        // Get the job ID from the data attribute
        var specializationID = $(this).data('specialization_id');
        // Update the URL dynamically
        window.location.href = `/home/${specializationID}/`;
    });
});
