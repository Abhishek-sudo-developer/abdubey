let currentPersona = 'scout';

function setPersona(persona) {
    currentPersona = persona;
    document.querySelectorAll('.persona-btn').forEach(btn => btn.classList.remove('active'));
    document.getElementById(`${persona}-btn`).classList.add('active');
}

async function generatePlan() {
    const input = document.getElementById('request-input').value;
    if (!input) return alert("Please enter a destination!");

    const loading = document.getElementById('loading');
    const results = document.getElementById('results');
    const logsContainer = document.getElementById('logs-container');
    const itineraryOutput = document.getElementById('itinerary-output');

    loading.style.display = 'block';
    results.style.display = 'none';
    logsContainer.innerHTML = '';
    itineraryOutput.innerHTML = '';

    try {
        const response = await fetch('/api/plan', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({
                user_request: input,
                persona: currentPersona
            })
        });

        const data = await response.json();
        
        loading.style.display = 'none';
        results.style.display = 'block';

        // Render logs (if any)
        if (data.logs && data.logs.length > 0) {
            data.logs.forEach(log => {
                const div = document.createElement('div');
                div.className = 'log-entry';
                div.textContent = `[Step ${log.step}] ${log.content}`;
                logsContainer.appendChild(div);
            });
        } else {
            logsContainer.innerHTML = '<p class="log-entry">Orchestration sequence completed successfully. (Direct reasoning used)</p>';
        }

        // Render final itinerary from JSON
        const itinerary = data.itinerary.itinerary;
        if (itinerary && Array.isArray(itinerary)) {
            itinerary.forEach(item => {
                const itemDiv = document.createElement('div');
                itemDiv.className = 'itinerary-item';
                
                itemDiv.innerHTML = `
                    <div class="score-badge">${item.persona_match_score}% Match</div>
                    <div class="activity-title">${item.activity}</div>
                    <div class="location-meta"><i class="fas fa-map-marker-alt"></i> ${item.location}</div>
                    <div class="reasoning-trace">${item.reasoning_trace}</div>
                    ${item.dynamic_adjustment_reason ? `<div class="reasoning-trace" style="color: #fbbf24;"><i class="fas fa-bolt"></i> PIVOT: ${item.dynamic_adjustment_reason}</div>` : ''}
                `;
                
                itineraryOutput.appendChild(itemDiv);
            });
        } else {
            itineraryOutput.innerHTML = `<p>Error: Could not parse itinerary. Raw output: ${JSON.stringify(data.itinerary)}</p>`;
        }

    } catch (error) {
        loading.style.display = 'none';
        alert("Error generating plan. Check console.");
        console.error(error);
    }
}
