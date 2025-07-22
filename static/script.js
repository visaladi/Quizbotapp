// For form submission validation and other possible dynamic behaviors

// Check if file is selected before submission
document.querySelector("form").addEventListener("submit", function(event) {
    const fileInput = document.querySelector('input[type="file"]');
    if (!fileInput.files.length) {
        alert("Please upload a PDF or TXT file.");
        event.preventDefault();  // Prevent form submission
    }
});

// Optional: Display a message on answer selection for instant feedback
const answerLabels = document.querySelectorAll(".options label");

answerLabels.forEach(label => {
    label.addEventListener("click", () => {
        label.style.backgroundColor = "#8bc34a"; // Change color to green when clicked (for feedback)
    });
});
