function performSearch() {
  const keyword = document.getElementById('searchInput').value;
  socket.emit('search', keyword);
}

document.addEventListener("DOMContentLoaded", function() {
  const searchButton = document.getElementById("searchButton");
  const searchInput = document.getElementById("searchInput");

  searchButton.addEventListener("click", function() {
    const keyword = searchInput.value;
    // Call your search function here
    console.log(keyword);
    performSearch(keyword);
  });
});

document.getElementById('searchInput').addEventListener('keydown', function(event) {
  if (event.keyCode === 13) {  // 13 is the keyCode for the Enter key
      // Trigger your search function here
      performSearch(keyword);
  }
});