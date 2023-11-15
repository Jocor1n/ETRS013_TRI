var map = L.map('map', {
    center: [46.7682, 2.4327],  // Coordinates for Paris
    zoom: 5  // Adjust this number to your desired initial zoom level
});

L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
    attribution: '&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors',
    noWrap: true // Add this option
}).addTo(map);



