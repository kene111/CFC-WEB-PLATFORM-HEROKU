// Event listeners for css transitions

window.addEventListener("load", () => {
  document.querySelector("body").classList.add("loaded"); 
});

window.addEventListener("scroll", () => {
  document.querySelector("body").classList.add("scrolled"); 
});


function openForm() {
  document.getElementById("e_Form").style.display = "block";
}

function closeForm() {
  document.getElementById("e_Form").style.display = "none";
}

// ........................................................Javascript function  DISPLAY LOCATION ................................................................
function getMyCurrentLocation() {
    if (navigator.geolocation) {
      navigator.geolocation.getCurrentPosition(showPosition);
    } else {
      alert("Geolocation is not supported by this browser.");
    }
}
  
function showPosition(position) {
    //var myLatlng = new google.maps.LatLng(lati,longi);
    var properties = {
    zoom: 20,
    minZoom:14,
    center:{lat: position.coords.latitude, lng: position.coords.longitude}, // myLatlng,
    draggable:true,
    //mapTypeId: google.maps.MapTypeId.SATELLITE
    };
    map = new google.maps.Map(document.getElementById("map"), properties);

    var marker = new google.maps.Marker({
        position: {lat:position.coords.latitude, lng: position.coords.longitude},
        animation:google.maps.Animation.BOUNCE,
        map:map
    });
        
    //marker.setMap(map);
    // https://www.youtube.com/watch?v=UrrWxyq1Z48
    //https://www.youtube.com/watch?v=Zxf1mnP5zcw
     
}

// ........................................................Javascript function  ROUTES.............................................................................

function getLocation() {
    if (navigator.geolocation) {
      navigator.geolocation.getCurrentPosition(Route);
    } else {
      alert("Geolocation is not supported by this browser.");
    }
}

function Route(position){
    var lat = position.coords.latitude;
    var long = position.coords.longitude;
    var map = new google.maps.Map(document.getElementById('map'), {
        zoom: 16,
        center: {lat: lat, lng:long}
    });
    
    var url = "https://cors-anywhere.herokuapp.com/https://maps.googleapis.com/maps/api/directions/json?"; //https://cors-anywhere.herokuapp.com/
    var destination = document.getElementById('id_destination').value;
    var current_location = lat +','+ long;
    const key = "";    // Using the directions api key

    if (destination == "") {
        alert(" Please type in your destination");
    }else{
        var xhttp = new XMLHttpRequest();
          xhttp.onreadystatechange = function() {
            if (xhttp.readyState == 4 && xhttp.status == 200) {

                let response = JSON.parse(xhttp.responseText);
                if (response.status == 'OK'){
                    let distance =  response.routes[0].legs[0].distance.text;
                    let duration = response.routes[0].legs[0].duration.text;
                    console.log(distance)
                    console.log(duration)
                    console.log(response)
                    let decodedSets = google.maps.geometry.encoding.decodePath(response.routes[0].overview_polyline.points).toString();
                    console.log(decodedSets)
                   var array = decodedSets.replace(/[()]/g, function(d){
                        return {
                            '(' : '[',
                            ')' : ']',
                        }[d];
                    });
                   console.log(array)
 
                    var new_array = '['+array+']'; // this needed to be done for the parser to parse the array.
                    array = JSON.parse(new_array);
                    var coordinates = array.map(function(item){
                          return {
                            lat: item[0],
                            lng: item[1],
                          };
                        });

                    console.log(coordinates)

                    var Path = new google.maps.Polyline({

                        path:  coordinates,//coordinates,
                        geodesic:true,
                        strokeColor: '#228B22',
                        strokeOpacity:1.0,
                        strokeWeight:2
                    })

                    Path.setMap(map); 

                    var first = coordinates.shift();
                    var last = coordinates.pop();  

                    // Marker for starting position
                    var marker = new google.maps.Marker({
                        position: first,
                        map: map
                    });
                    marker.setMap(map);

                    //marker for destination

                    var marker = new google.maps.Marker({
                        position: last,
                        map: map,
                    });
                    marker.setMap(map);

                    var dest_dur = [];
                    dest_dur.push(distance)
                    dest_dur.push(duration)

                    console.log(dest_dur)
                    var i;
                    var parag;
                    var node;  
                    var pop_element;

                    for(i=0; i < dest_dur.length; i++){
                        parag = document.createElement("p");
                        parag.id = i;
                        parag.style.color = "white";
                        parag.style.textAlign='center';
                        node = document.createTextNode(dest_dur[i]);
                        parag.appendChild(node);
                        pop_element = document.getElementById("des_det"); //hold
                        pop_element.appendChild(parag); 
                    }
                    pop_element.style.display = 'block';

                            $(document).mouseup(function (e) { 
                        if ($(e.target).closest(".de_de").length 
                                    === 0) { 
                            $(".de_de").hide(); 
                            document.getElementById("des_det").innerHTML = "";
                        } 
                    });
                }else{
                    alert("I am sorry, I currently cannot find the specified destination.")
                }  
            }
          };
          xhttp.open("GET",url+"origin="+current_location+"&destination="+destination+"&key="+ key, true);
          xhttp.send();        
   }
}

// ........................................................Javascript function  REVERSE GEOCODING.............................................................................

var url = "https://maps.googleapis.com/maps/api/geocode/json?";

window.addEventListener("load", NewsLocation); // call NewsLocation function when the page loads

function NewsLocation() {
    if (navigator.geolocation) {
      navigator.geolocation.getCurrentPosition(News);
    } else {
      alert("Geolocation is not supported by this browser.");
    }
}
// ---------------------------------------------------------------csrf token----------------------------------------------------------------------------------------
function getCookie(name) {
    var cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        var cookies = document.cookie.split(';');
        for (var i = 0; i < cookies.length; i++) {
            var cookie =  cookies[i].trim();
            // Does this cookie string begin with the name we want?
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}

var csrftoken = getCookie('csrftoken');

function csrfSafeMethod(method) {
    // these HTTP methods do not require CSRF protection
    return (/^(GET|HEAD|OPTIONS|TRACE)$/.test(method));
}

// Function to set Request Header with `CSRFTOKEN`
function setRequestHeader(){
    $.ajaxSetup({
        beforeSend: function(xhr, settings) {
            if (!csrfSafeMethod(settings.type) && !this.crossDomain) {
                xhr.setRequestHeader("X-CSRFToken", csrftoken);
            }
        }
    });
}

// ------------------------------------------------------------------------------------------------------------------------------------------------------------------
function News(position){                  // recieve coordinates from NewsLocation,
    var lat = position.coords.latitude;
    var long = position.coords.longitude;
    var location = lat +','+ long;
    const key = ""; // geocoding api key

    var xhttp = new XMLHttpRequest();
      xhttp.onreadystatechange = function() {
        if (xhttp.readyState == 4 && xhttp.status == 200) {

            let response = JSON.parse(xhttp.responseText);
            var country = response.results[0].address_components[6].short_name;
            console.log(1)
            console.log(country)

            setRequestHeader();

         // for the news platform at the backend

            var clink = '/scraper/infomation/';
            $.ajax({
                url : clink,          
                type : 'POST',
                data: {'country':country},
                dataType: 'json',
            }); // for the news platform at the backend
        }
      };
      xhttp.open("GET",  url+"latlng="+location+"&key="+ key, true);
      xhttp.send();


}


// ........................................................Javascript function  PLACES.............................................................................

function hospitalLocation() {
    if (navigator.geolocation) {
      navigator.geolocation.getCurrentPosition(Hospital);
    } else {
      alert("Geolocation is not supported by this browser.");
    }
}


function Hospital(position){ 
    var url = "https://cors-anywhere.herokuapp.com/https://maps.googleapis.com/maps/api/place/nearbysearch/json?";// https://cors-anywhere.herokuapp.com/                
    var lat = position.coords.latitude;
    var long = position.coords.longitude;
    var location = lat +','+ long;
    var radius =3000;
    //var type = 'Hospital';
    var name= 'Hospital';
    const key = "";  /// places api key


     var xhttp = new XMLHttpRequest();
      xhttp.onreadystatechange = function() {
        if (xhttp.readyState == 4 && xhttp.status == 200) {

            let response = JSON.parse(xhttp.responseText);
            console.log(response)
            var element = [];
            var i;
            var hosp_name;
               
            for (i=0; i < response.results.length; i++){
                hosp_name = response.results[i].name;
                element.push(hosp_name);
            }                                    

            console.log(element); //let unique = [ ... new Set(element)];   a way to remove duplicates


            var i;
            var para;
            var parag;
            var node;  
            var pop_element;

            for(i=0; i < element.length; i++){
                para = document.createElement("p");
                para.id = i;
                para.style.color = "white";
                para.style.textAlign='center';
                node = document.createTextNode(element[i]);
                para.appendChild(node);
                pop_element = document.getElementById("hospitalPopUp"); //hold
                pop_element.appendChild(para); 
            }
            pop_element.style.display = 'block';
            //pop_element.classList.toggle("show");

            document.getElementById("hospitalPopUp").addEventListener("click", function() {
                //alert(event.srcElement.innerHTML); // event.srcElement.id // this.innerHTML   hold

                var map = new google.maps.Map(document.getElementById('map'), {
                    zoom: 16,
                    center: {lat: lat, lng:long}
                });

                var url_2 = "https://cors-anywhere.herokuapp.com/https://maps.googleapis.com/maps/api/directions/json?";// https://cors-anywhere.herokuapp.com/
                var destination = event.srcElement.innerHTML;
                var current_location = lat +','+ long;
                const key_2 = "";  // directions api key


                var xhttp = new XMLHttpRequest();
                  xhttp.onreadystatechange = function() {
                    if (xhttp.readyState == 4 && xhttp.status == 200) {

                        let response = JSON.parse(xhttp.responseText);
                        let decodedSets = google.maps.geometry.encoding.decodePath(response.routes[0].overview_polyline.points).toString();
                        var array = decodedSets.replace(/[()]/g, function(d){
                            return {
                                '(' : '[',
                                ')' : ']',
                            }[d];
                        });

                        var new_array = '['+array+']'; // this needs to be done for the parser to parse the array.
                        array = JSON.parse(new_array);
                        var coordinates = array.map(function(item){
                                return {
                                    lat: item[0],
                                    lng: item[1],
                                };
                            });

                        var Path = new google.maps.Polyline({

                            path: coordinates,
                            geodesic:true,
                            strokeColor: '#228B22',
                            strokeOpacity:1.0,
                            strokeWeight:2
                        })

                        Path.setMap(map); 

                        var first = coordinates.shift();
                        var last = coordinates.pop();  

                        // Marker for starting position
                        var marker = new google.maps.Marker({
                            position: first,
                            map: map
                        });
                        marker.setMap(map);

                        //marker for destination

                        var marker = new google.maps.Marker({
                            position: last,
                            map: map
                        });
                        marker.setMap(map);


                        let distance =  response.routes[0].legs[0].distance.text;
                        let duration = response.routes[0].legs[0].duration.text;

                        var dest_dur = [];
                        dest_dur.push(distance)
                        dest_dur.push(duration)


                        for(i=0; i < dest_dur.length; i++){
                            parag = document.createElement("p");
                            parag.id = i;
                            parag.style.color = "white";
                            parag.style.textAlign='center';
                            node = document.createTextNode(dest_dur[i]);
                            parag.appendChild(node);
                            pop_element = document.getElementById("des_det"); //hold
                            pop_element.appendChild(parag); 
                        }
                        pop_element.style.display = 'block';

                                $(document).mouseup(function (e) { 
                            if ($(e.target).closest(".de_de").length 
                                        === 0) { 
                                $(".de_de").hide(); 
                                document.getElementById("des_det").innerHTML = "";
                            } 
                        });
                          
                    }
                  };

                  xhttp.open("GET",  url_2 +"origin="+current_location+"&destination="+destination+"&key="+ key_2, true);
                  xhttp.send();
            });
        }
      };
      xhttp.open("GET",  url+"location="+location+"&radius="+radius+"&name="+name+"&key="+ key, true);
      xhttp.send();


      $(document).mouseup(function (e) { 
            if ($(e.target).closest(".hospitalPop").length 
                        === 0) { 
                $(".hospitalPop").hide(); 
                document.getElementById("hospitalPopUp").innerHTML = "";
            } 
        }); 

    

} //end


/*------------------------------------------------------------SEND LOCATION ---------------------------------------------------------------------------------------- */

var url = "https://maps.googleapis.com/maps/api/geocode/json?";


function Location(){
    if (navigator.geolocation) {
      navigator.geolocation.getCurrentPosition(sendLocation);
    } else {
      alert("Geolocation is not supported by this browser.");
    }
}



function sendLocation(position){                  // recieve coordinates from NewsLocation,
    var lat = position.coords.latitude; // 6.503618;
    var long = position.coords.longitude; //3.345743;
    var location = lat +','+ long;
    const key = ""; // geocoding api key



    var xhttp = new XMLHttpRequest();
      xhttp.onreadystatechange = function() {
        if (xhttp.readyState == 4 && xhttp.status == 200) {

            let response = JSON.parse(xhttp.responseText);
            var address = response.results[0].formatted_address;
            console.log(address)    // for the address at the backend
            console.log(location)  // for the location at the backend

            var link = '/scraper/maps/';

            setRequestHeader();

            $.ajax({
                url : link,          
                type : 'POST',
                data: {'location':location,'address':address},
                dataType : 'json',
                success: function(){

                    alert("Your Location has been sent.");
                    
                },
            });
        }
      };
      xhttp.open("GET",  url+"latlng="+location+"&key="+ key, true);
      xhttp.send();       
}

//------------------------------------------------------- Help Others -----------------------------------------------------------------

//window.addEventListener("load",  HelpO);
//function HelpO() {
//    if (navigator.geolocation) {
//      navigator.geolocation.getCurrentPosition(toTheBack);
//    } else {
//      alert("Geolocation is not supported by this browser.");
//    }
//}


//function toTheBack(position){
//    var lat = position.coords.latitude;
//    var long = position.coords.longitude;
//    var location = lat +','+ long;
    //var place = document.getElementById('id_place').value;
    //var disas_type = document.getElementById('id_disas').value;
    //const key = "AIzaSyApZA2kzNzsYLa2IeGkOIB-XA87l5hz-vw";


//    setRequestHeader();
//    var Hlink = '/chatbot/ndia/';
//    $.ajax({
//        url : Hlink,          
//        type : 'POST',
//        data: {'location':location},
//        dataType: 'json',
//        success: function(data){
//            $(document).reload(true)
//            
//        },
//
//    }); 

   // var xhttp = new XMLHttpRequest();
   //   xhttp.onreadystatechange = function() {
   //     if (xhttp.readyState == 4 && xhttp.status == 200) {

            //let response = JSON.parse(xhttp.responseText);
            //var count = response.results[0].address_components[6].short_name;
            //ar state = response.results[0].address_components[5].short_name;

      //  }
     // };
    //  xhttp.open("GET",  url+"latlng="+location+"&key="+ key, true);
    //  xhttp.send();
//}


// ------------------------------------------------------- For Predictions --------------------------------------------------------------------------------------------------

window.addEventListener("load", predictions);
function predictions() {
    if (navigator.geolocation) {
      navigator.geolocation.getCurrentPosition(forPredict);
    } else {
      alert("Geolocation is not supported by this browser.");
    }
}


function forPredict(position){

    var lat = position.coords.latitude;
    var long = position.coords.longitude;


    setRequestHeader();

    

    var Plink = "/chatbot/prediction/"; //'/chatbot/prediction/' "{% url 'chatbot-prediction' %}" 'chatbot-prediction'
    $.ajax({
        url : Plink,          
        type : 'POST',
        data: {'lat':lat,'long':long},
        dataType: 'html',
        success: function(json){
            $('#collect').html(json)    
        },
    });

}

// reloading the web page every hour
//$(document).ready(function(){
//    setInterval(function(){ reload_page(); },60*60000); // 60*60000 : 1 hr
// });

//function reload_page()
// {
//    window.location.reload(true);
// }

var current = new Date();
var future = new Date();
future.setTime(future.getTime() + 3600000); //3600000 = 1 hour
future.setMinutes(0);
future.setSeconds(0);

var timeout = (future.getTime() - current.getTime());
setTimeout(function() { window.location.reload(true); }, timeout);