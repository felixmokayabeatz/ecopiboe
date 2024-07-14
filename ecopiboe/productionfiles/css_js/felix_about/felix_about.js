var images = document.querySelectorAll('.image-container img');
var index = 0;
images[index].classList.add('active');
setInterval(scrollImages, 5000);

function scrollImages() {
    images.forEach(function(image) {
        image.classList.remove('active');
    });
    index = (index + 1) % images.length;
    images[index].classList.add('active');
}
