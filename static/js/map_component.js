// Leaflet Interactive Map Component for PetCare India AI

let mapInstance = null;
let markersGroup = null;

function initMap(lat = 17.3850, lng = 78.4867) {
  const mapElement = document.getElementById('map');
  if (!mapElement) return;

  if (!mapInstance) {
    mapInstance = L.map('map').setView([lat, lng], 12);
    L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
      maxZoom: 19,
      attribution: '&copy; OpenStreetMap & Google Places'
    }).addTo(mapInstance);
    markersGroup = L.layerGroup().addTo(mapInstance);
  } else {
    mapInstance.setView([lat, lng], 12);
  }
}

function updateMapMarkers(providers, centerLat = 17.3850, centerLng = 78.4867) {
  if (!mapInstance) initMap(centerLat, centerLng);
  markersGroup.clearLayers();

  // Add User Location Marker
  const userIcon = L.divIcon({
    className: 'user-marker',
    html: '<div style="background: #00f2fe; width: 16px; height: 16px; border-radius: 50%; border: 3px solid white; box-shadow: 0 0 10px #00f2fe;"></div>'
  });
  L.marker([centerLat, centerLng], { icon: userIcon }).addTo(markersGroup).bindPopup('<b>Your Location</b>');

  // Add Provider Markers
  providers.forEach(p => {
    if (p.location && p.location.latitude && p.location.longitude) {
      const isEmergency = p.emergency_available;
      const pinColor = isEmergency ? '#ff4b4b' : (p.provider_category === 'Government Hospital' ? '#4158D0' : '#4facfe');
      
      const providerIcon = L.divIcon({
        className: 'provider-marker',
        html: `<div style="background: ${pinColor}; color: white; padding: 4px 8px; border-radius: 12px; font-weight: bold; font-size: 11px; border: 2px solid white; white-space: nowrap;">🏥 ${p.name.substring(0, 18)}...</div>`
      });

      const popupContent = `
        <div style="font-family: sans-serif; color: #1e293b;">
          <h4 style="margin: 0 0 4px 0;">${p.name}</h4>
          <p style="margin: 0; font-size: 12px; color: #64748b;">${p.address}</p>
          <p style="margin: 4px 0; font-size: 12px;"><b>Distance:</b> ${p.distance_km} km | <b>Phone:</b> ${p.phone}</p>
          <a href="${p.maps_url || '#'}" target="_blank" style="color: #0284c7; text-decoration: none; font-weight: bold; font-size: 12px;">🗺️ Open Directions</a>
        </div>
      `;

      L.marker([p.location.latitude, p.location.longitude], { icon: providerIcon })
        .addTo(markersGroup)
        .bindPopup(popupContent);
    }
  });

  if (providers.length > 0) {
    mapInstance.setView([providers[0].location.latitude, providers[0].location.longitude], 11);
  }
}
