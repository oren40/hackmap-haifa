const map = L.map('map').setView([32.794, 34.989], 12);
L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
  attribution: '&copy; OpenStreetMap contributors'
}).addTo(map);

// שליפת אירועים קיימים
fetch('/api/events')
  .then(r => r.json())
  .then(events => events.forEach(addMarker));

function addMarker(ev) {
  const m = L.marker([ev.latitude, ev.longitude]).addTo(map);
  m.bindPopup(`<b>${ev.title}</b><br>${ev.date}<br>${ev.category}`);
}

// לחיצה על “שמור” ⇒ POST
document.getElementById('save').onclick = () => {
  navigator.geolocation.getCurrentPosition(pos => {
    const body = {
      title: document.getElementById('title').value,
      description: document.getElementById('desc').value,
      category: document.getElementById('cat').value,
      date: document.getElementById('date').value,
      lat: pos.coords.latitude,
      lng: pos.coords.longitude
    };
    fetch('/api/events', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(body)
    })
    .then(r => {
      if (r.ok) {
        addMarker(body);
        document.getElementById('msg').textContent = '✓ נשמר!';
      } else {
        document.getElementById('msg').textContent = 'שגיאה';
      }
    });
  });
};
