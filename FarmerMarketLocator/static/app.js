// Check URL for market profile for callback to run
$(document).ready(function() {
    if (window.location.href.indexOf("market") > -1) {
      randomImg();
    }
  });
// generate random image to load for market profile
function randomImg() {
    let mktImgs = [
    "/static/images/annie-spratt.jpg",
    "/static/images/dane-deaner.jpg",
    "/static/images/jorge-franganillo.jpg",
    "/static/images/kyle-nieber.jpg",
    "/static/images/peter-wendt.jpg",
    "/static/images/shelley_pauls.jpg",
    "/static/images/thomas-le.jpg"
];
    let rnd = Math.floor(Math.random() * mktImgs.length);
    let img = new Image(200,200);
    img.src = mktImgs[rnd];
    img.alt = `Unsplash photo by ${mktImgs}`
    document.getElementById("market_img").appendChild(img);
};