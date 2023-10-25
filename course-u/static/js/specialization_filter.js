console.log("specialization_filter.js loaded");

document.addEventListener("DOMContentLoaded", function () {
    const fieldLinks = document.querySelectorAll(".field-link");
    const specializationContainer = document.getElementById("specialization-container");

    // Add click event listeners to field links
    fieldLinks.forEach((link) => {
      link.addEventListener("click", function (event) {
        event.preventDefault();
        const fieldId = this.getAttribute("data-field-id");
        console.log(`Field ID: ${fieldId}`)
        
        if (fieldId) { // Check if fieldId is defined and not empty
          // Remove the "card-selected" class from all field links
          fieldLinks.forEach((fieldLink) => {
            fieldLink.querySelector(".card").classList.remove("card-selected");
          });

          // Add the "card-selected" class to the clicked field link
          this.querySelector(".card").classList.add("card-selected");

          // Fetch and update the specialization content based on the selected field
          fetch(`/field/${fieldId}/`)
            .then((response) => response.text())
            .then((data) => {
              specializationContainer.innerHTML = data;
            })
            .catch((error) => {
              console.error("Error fetching data:", error);
            });
        }
      });
    });
});
