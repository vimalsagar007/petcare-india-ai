// PETCARE INDIA AI - Client Controller App Logic

let currentAction = 'hospital';

document.addEventListener('DOMContentLoaded', () => {
  initMap();
  triggerSearch();
});

function selectAction(action) {
  currentAction = action;
  document.querySelectorAll('.action-btn').forEach(btn => btn.classList.remove('active'));
  event.target.classList.add('active');

  const petsTab = document.getElementById('pets-tab');
  const mapContainer = document.getElementById('map-container');
  const providerCards = document.getElementById('provider-cards');

  if (action === 'my_pets') {
    petsTab.style.display = 'block';
    mapContainer.style.display = 'none';
    providerCards.style.display = 'none';
    loadMyPets();
  } else {
    petsTab.style.display = 'none';
    mapContainer.style.display = 'block';
    providerCards.style.display = 'grid';
    triggerSearch();
  }
}

async function triggerSearch() {
  const animal = document.getElementById('animal-select').value;
  const location = document.getElementById('location-input').value;
  const radius = document.getElementById('radius-select').value;
  const urgency = document.getElementById('urgency-select').value;
  const language = document.getElementById('language-select').value;

  let queryText = `Find ${currentAction} for ${animal} in ${location}`;
  if (urgency === 'Emergency') queryText += ' emergency';

  try {
    const response = await fetch('/api/search', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({
        query: queryText,
        animal: animal,
        location: location,
        radius_km: parseFloat(radius),
        urgency: urgency,
        language: language
      })
    });

    const data = await response.json();
    renderResults(data);
  } catch (err) {
    console.error('Error fetching search results:', err);
  }
}

function renderResults(data) {
  const emergencyBanner = document.getElementById('emergency-banner');
  if (data.is_emergency && data.emergency_warning) {
    emergencyBanner.style.display = 'flex';
    document.getElementById('emergency-banner-text').innerText = data.emergency_warning;
  } else {
    emergencyBanner.style.display = 'none';
  }

  // Update Map
  if (data.providers && data.providers.length > 0) {
    updateMapMarkers(data.providers, data.providers[0].location.latitude, data.providers[0].location.longitude);
  }

  // Render Provider Cards
  const cardsContainer = document.getElementById('provider-cards');
  cardsContainer.innerHTML = '';

  if (!data.providers || data.providers.length === 0) {
    cardsContainer.innerHTML = '<div style="grid-column: 1/-1; padding: 2rem; text-align: center; color: var(--text-sub);">No provider found matching your exact search filters. Try increasing search radius or changing location.</div>';
    return;
  }

  data.providers.forEach(p => {
    const card = document.createElement('div');
    card.className = 'provider-card';
    
    const isGovt = p.provider_category === 'Government Hospital';
    const isOpen = p.open_now;

    card.innerHTML = `
      <div>
        <div style="display: flex; gap: 0.5rem; flex-wrap: wrap;">
          ${isGovt ? '<span class="card-badge badge-govt">🏛️ Government Hospital</span>' : '<span class="card-badge badge-open">🏥 Private Clinic</span>'}
          ${isOpen ? '<span class="card-badge badge-open">🟢 Open Now</span>' : '<span class="card-badge" style="background: rgba(255,255,255,0.1); color: #94a3b8;">🔴 Closed</span>'}
        </div>
        <h3 class="card-title">${p.name}</h3>
        <p class="card-meta">📍 ${p.address}</p>
        <p class="card-meta">📞 ${p.phone}</p>
        <p class="card-meta">📏 <strong>${p.distance_km} km away</strong> | ⭐ ${p.rating ? p.rating + ' (' + p.review_count + ' reviews)' : 'Rating N/A'}</p>
        <p style="font-size: 0.75rem; color: var(--text-sub); margin-top: 0.4rem;">Source: ${p.source}</p>
      </div>

      <div class="card-actions">
        <a href="tel:${p.phone !== 'Not available from current provider data.' ? p.phone : ''}" class="btn-card">📞 Call</a>
        <a href="${p.maps_url || '#'}" target="_blank" class="btn-card primary">🗺️ Directions</a>
      </div>
    `;
    cardsContainer.appendChild(card);
  });
}

async function sendChatMessage() {
  const inputEl = document.getElementById('chat-input');
  const text = inputEl.value.trim();
  if (!text) return;

  const messagesContainer = document.getElementById('chat-messages');

  // Append user bubble
  const userBubble = document.createElement('div');
  userBubble.className = 'message-bubble user';
  userBubble.innerText = text;
  messagesContainer.appendChild(userBubble);

  inputEl.value = '';
  messagesContainer.scrollTop = messagesContainer.scrollHeight;

  const animal = document.getElementById('animal-select').value;
  const language = document.getElementById('language-select').value;

  try {
    const resp = await fetch('/api/chat', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ query: text, animal: animal, language: language })
    });

    const data = await resp.json();

    const botBubble = document.createElement('div');
    botBubble.className = 'message-bubble assistant';
    
    let answerHtml = data.knowledge_answer || "I have retrieved matching provider information for your request.";
    if (data.is_emergency) {
      answerHtml = `<strong>🚨 EMERGENCY ALERT:</strong> ${data.emergency_warning}<br><br>` + answerHtml;
    }

    if (data.citations && data.citations.length > 0) {
      answerHtml += `<div class="citation-box"><strong>📚 Grounded Source References:</strong><br>`;
      data.citations.forEach(c => {
        answerHtml += `• ${c.title} - ${c.organization} (${c.reference})<br>`;
      });
      answerHtml += `</div>`;
    }

    botBubble.innerHTML = answerHtml;
    messagesContainer.appendChild(botBubble);
    messagesContainer.scrollTop = messagesContainer.scrollHeight;
  } catch (err) {
    console.error('Chat error:', err);
  }
}

function handleKeyPress(e) {
  if (e.key === 'Enter') sendChatMessage();
}

function toggleView(view) {
  const mapContainer = document.getElementById('map-container');
  const providerCards = document.getElementById('provider-cards');
  const btnMap = document.getElementById('btn-toggle-map');
  const btnList = document.getElementById('btn-toggle-list');

  if (view === 'map') {
    mapContainer.style.display = 'block';
    providerCards.style.display = 'grid';
    btnMap.classList.add('active');
    btnList.classList.remove('active');
  } else {
    mapContainer.style.display = 'none';
    providerCards.style.display = 'grid';
    btnList.classList.add('active');
    btnMap.classList.remove('active');
  }
}

function useBrowserLocation() {
  if (navigator.geolocation) {
    navigator.geolocation.getCurrentPosition(pos => {
      document.getElementById('location-input').value = `${pos.coords.latitude.toFixed(4)}, ${pos.coords.longitude.toFixed(4)}`;
      triggerSearch();
    }, () => {
      alert("Unable to retrieve browser GPS location. Please enter your city or PIN code manually.");
    });
  }
}

async function loadMyPets() {
  const petsList = document.getElementById('pets-list');
  try {
    const res = await fetch('/api/pets');
    const pets = await res.json();
    petsList.innerHTML = '';
    pets.forEach(p => {
      const item = document.createElement('div');
      item.style.cssText = 'background: var(--bg-card); padding: 1rem; border-radius: 12px; margin-bottom: 0.75rem; border: 1px solid var(--border-color);';
      item.innerHTML = `
        <h4 style="color: var(--accent-teal);">${p.name} (${p.animal_type})</h4>
        <p style="font-size: 0.85rem; color: var(--text-sub); margin-top: 0.2rem;">Breed: ${p.breed} | Age: ${p.age} | Sex: ${p.sex}</p>
        <p style="font-size: 0.85rem; color: var(--text-main); margin-top: 0.4rem;"><strong>Vaccination:</strong> ${p.vaccination_status}</p>
        <p style="font-size: 0.8rem; color: var(--text-sub); margin-top: 0.2rem;">Note: ${p.notes}</p>
      `;
      petsList.appendChild(item);
    });
  } catch (e) {
    console.error('Error loading pets:', e);
  }
}

function onLanguageChange() {
  triggerSearch();
}
