
 console.log("hello from js") ;
 document.addEventListener("DOMContentLoaded", function() {
    fetch('/get_playlists', {method:"POST",
        headers:{
            'content-type':'application/json',
    
        },
        body:JSON.stringify({response: value})} )     
       .then(response => response.json())
       .then(data => {         
        console.log(data)
            const playlistsContainer = document.getElementById('playlists-container');
            Object.entries(data).forEach(([name, url]) => {
                const playlistElement = document.createElement('div');
                playlistElement.innerHTML = `<h3>${name}</h3><p>${url}</p>`;
                playlistsContainer.appendChild(playlistElement);
            });       
          })       
             .catch(error => console.error('Error fetching playlists:', error)); });
