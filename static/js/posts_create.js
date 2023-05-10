const mapContainer = document.getElementById('map');
const mapOption = {
  center: new daum.maps.LatLng(37.537187, 127.005476),
  level: 3
};

const map = new daum.maps.Map(mapContainer, mapOption);
const geocoder = new daum.maps.services.Geocoder();
const marker = new daum.maps.Marker({
  position: new daum.maps.LatLng(37.537187, 127.005476),
  map: map
});

function search_address_map() {
  new daum.Postcode({
    oncomplete: function(data) {
      const addr = data.address;
      document.getElementById("s_address").value = addr;

      geocoder.addressSearch(data.address, function(results, status) {
        if (status === daum.maps.services.Status.OK) {
          const result = results[0];
          const coords = new daum.maps.LatLng(result.y, result.x);
          mapContainer.style.display = "block";
          map.relayout();
          map.setCenter(coords);
          marker.setPosition(coords);
        }
      });
    }
  }).open();
}

// const addrParts = addr.split(' ');
// const addressPrefix = addrParts[0]; // 주소 앞부분

// document.getElementById("id_city").value = addressPrefix;