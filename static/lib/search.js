// Wait for the DOM to be fully loaded
document.addEventListener("DOMContentLoaded", function() {
  // This function will be called when the search button is clicked or Enter is pressed
  function performSearch() {
    const keyword = document.getElementById('searchInput').value;
    console.log(keyword);
    // Use fetch to send the keyword to the server for searching
    fetch("/search", {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify({ keyword }),
    })
    .then(response => response.json())
    .then(data => {
      // Handle the search results here
      // For example, update the UI with the search results
      console.log(data);
    })
    .catch(error => {
      console.error('Error:', error);
    });
  }

  // Get the search input and button elements
  const searchInput = document.getElementById("searchInput");
  const searchButton = document.getElementById("searchButton");

  // Check if both elements exist
  if (searchButton && searchInput) {
    // Attach click event listener to the search button
    searchButton.addEventListener("click", performSearch);

    // Attach keydown event listener to the search input to listen for the Enter key
    searchInput.addEventListener("keydown", function(event) {
      if (event.key === "Enter") {
        performSearch();
      }
    });
  } else {
    // Log an error if the elements are not found
    console.error('Search input or button not found in the DOM');
  }
});
