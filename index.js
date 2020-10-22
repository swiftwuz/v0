let map;

function IncidentDetails(incident) {
    const content = `
        <div>
            <span>Category: ${incident.category} </span> <br/>
            <span>Description: ${incident.description} </span> <br/>
            <span>Latitude: ${incident.lat} </span> <br/>
            <span>Longitude: ${incident.lng} </span> <br/>
            <img class="details__image" src="${incident.image}"/>
        </div>
    `
    return content
}

function dropPins(allPoints, map){
    var infowindow = new google.maps.InfoWindow(); 
    for (var i = 0; i < allPoints.length; i++){
        let incident = allPoints[i]
      var myLatlng = new google.maps.LatLng(incident.lat, incident.lng);
      var marker = new google.maps.Marker({
          position: myLatlng,
          map: map,
          animation: google.maps.Animation.DROP
      });
      google.maps.event.addListener(marker, 'click', (function(marker, i) {
          return function() {
                document.getElementById("details__body").innerHTML = IncidentDetails(incident)
                // infowindow.setContent("<ul><li>Category " + incident.category + "</li><li>Description " + incident.description + "</li></ul>");
                // infowindow.open(map, marker);
            };
        })(marker, i));  
    }
}

function initMap(incidents, ) {
    map = new google.maps.Map(document.getElementById("map"), {
      center: { lng: -0.2475990969444747,lat: 5.684136332305188},
      zoom: 14,
    });
  
    dropPins(incidents, map)
}


function main() {
    let incidents = [{
        category: "CHAOS1",
        description: "They are fighting",
        image: "https://avatars3.githubusercontent.com/u/24861123?s=460&u=b4a91d2c9ca8df72c871daed1aee8cec0486bb59&v=4",
        lat: 5.684136332305188,
        lng: -0.2475990969444747,
        created_at: "13/01/2020"
    }, {
        category: "CHAOS2",
        description: "They are making noise",
        image: "https://avatars1.githubusercontent.com/u/12677701?s=460&u=b8e803263386261c18d236cc4b73ee8dede30446&v=4",
        lat: 5.683835847589247,
        lng: -0.2397266058667604,
        created_at: "13/01/2020"
    }, {
        category: "CHAOS3",
        description: "They are throwing bullets",
        image: "https://avatars0.githubusercontent.com/u/17879672?s=460&u=9788e938ff3721f02d9d1d80ee6aa49696ef6ee0&v=4",
        lat: 5.677474538991623,
        lng: -0.24460022375167725,
        created_at: "13/01/2020"
    }]

    const config = {
        headers: { Authorization: `Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ0b2tlbl90eXBlIjoiYWNjZXNzIiwiZXhwIjoxNjAzMzI0NDkwLCJqdGkiOiIwMzZlYjg0Zjk0YzQ0MDRmYTI4MTdmZGVmOTQ4ZWNmNSIsInVzZXJfaWQiOjF9.yo07C6-bC0ui9AIlp-bc7fZ7klxqL0kC-NpYnk6de0w` }
    };
    
  
    
    

    axios.get( 
        'https://102cd3196926.ngrok.io/submission/',
        config
      ).then((data) => {
          console.log(data.data.results)
          initMap(data.data.results)

      }).catch(console.log);
    // initMap(incidents)
}



