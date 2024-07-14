document.addEventListener('play', function(event){
    var videos = document.getElementsByTagName('video');
    for(var i =0; i < videos.length; i++){
        if(videos[i] != event.target){
            videos[i].pause();
        }
    }
}, true);