document.addEventListener("DOMContentLoaded", function() {
  function performSearch(keyword) {
    console.log(keyword);
    socket.emit('search', keyword);
  }

  const searchButton = document.getElementById("searchButton");
  const searchInput = document.getElementById("searchInput");

  if (searchButton && searchInput) {
    searchButton.addEventListener("click", function() {
      const keyword = searchInput.value;
      performSearch(keyword);
    });

    searchInput.addEventListener('keydown', function(event) {
      if (event.keyCode === 13) {
        performSearch(searchInput.value);
      }
    });
  } else {
    console.error('Search input or button not found!');
  }
});