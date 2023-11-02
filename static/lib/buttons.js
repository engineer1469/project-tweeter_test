function handleClick(id) {
  console.log("The button clicked was" + id);
  fetch("/buttons", {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify({ id }),
  });
}

function getWordCloud() {
  console.log("Getting current word cloud...");
  fetch("/generate_wordcloud", {
    method: "GET",
    headers: {
      "Content-Type": "application/json",
    },
  })
    .then((response) => {
      console.log(response);
      if (response.ok) {
        return response.blob();
      } else {
        console.error("Failed to fetch word cloud.");
      }
    })
    .then((blob) => {
      const url = URL.createObjectURL(blob);
      const img = new Image();
      img.src = url;

      const wordcloudDiv = document.getElementById("wordcloud");
      wordcloudDiv.innerHTML = "";
      wordcloudDiv.appendChild(img);
    })
    .catch((error) => {
      console.error("Error:", error);
    });
}

getWordCloud(); 

setInterval(getWordCloud, 5000); // Getting wordcloud every 5 seconds
