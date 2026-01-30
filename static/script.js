// Configuration
const REFRESH_INTERVAL = 15000; // 15 seconds
let eventCounts = { push: 0, pull_request: 0, merge: 0 };

// Format event message based on action type
function formatEventMessage(event) {
    const author = `<span class="event-author">${event.author}</span>`;
    const fromBranch = event.from_branch ? `<span class="event-branch">${event.from_branch}</span>` : '';
    const toBranch = `<span class="event-branch">${event.to_branch}</span>`;
    const timestamp = `<span class="event-timestamp">${event.timestamp}</span>`;
    
    let message = '';

    
    switch (event.action) {
        case 'PUSH':
            message = `${author} pushed to ${toBranch}`;
            break;
        case 'PULL_REQUEST':
            message = `${author} submitted a pull request from ${fromBranch} to ${toBranch}`;
            break;
        case 'MERGE':
            message = `${author} merged branch ${fromBranch} to ${toBranch}`;
            break;
        default:    
            message = `${author} performed ${event.action}`;
    }
    
    return `
        <div class="event-header">
            <span class="event-type ${event.action.toLowerCase()}">${event.action}</span>
        </div>
        <div class="event-message">${message}</div>
        ${timestamp}
    `;
}

// Fetch and display events
async function fetchEvents() {
    try {
        const response = await fetch('/events');
        const data = await response.json();
        
        if (data.status === 'success') {
            displayEvents(data.events);
            updateStatistics(data.events);
            updateLastUpdateTime();
        } else {
            console.error('Error fetching events:', data.message);
        }
    } catch (error) {
        console.error('Network error:', error);
        showError('Failed to fetch events. Please check your connection.');
    }
}

// Display events in the UI
function displayEvents(events) {
    const container = document.getElementById('events-container');
    
    if (events.length === 0) {
        container.innerHTML = `
            <div class="no-events">
                <p>No events yet. Push some code or create a pull request to see events here!</p>
            </div>
        `;
        return;
    }
    
    container.innerHTML = events.map(event => `
        <div class="event-item ${event.action.toLowerCase()}" data-id="${event.request_id}">
            ${formatEventMessage(event)}
        </div>
    `).join('');
}

// Update statistics
function updateStatistics(events) {
    eventCounts = { push: 0, pull_request: 0, merge: 0 };
    
    events.forEach(event => {
        const action = event.action.toLowerCase();
        if (eventCounts.hasOwnProperty(action)) {
            eventCounts[action]++;
        }
    });
    
    document.getElementById('total-events').textContent = events.length;
    document.getElementById('push-count').textContent = eventCounts.push;
    document.getElementById('pr-count').textContent = eventCounts.pull_request;
    document.getElementById('merge-count').textContent = eventCounts.merge;
}

// Update last update time
function updateLastUpdateTime() {
    const now = new Date();
    const timeString = now.toLocaleTimeString('en-US', { 
        hour: '2-digit', 
        minute: '2-digit', 
        second: '2-digit' 
    });
    document.getElementById('last-update').textContent = `Last updated: ${timeString}`;
}

// Show error message
function showError(message) {
    const container = document.getElementById('events-container');
    container.innerHTML = `
        <div class="no-events">
            <p>${message}</p>
        </div>
    `;
}

// Initialize the application
function init() {
    console.log('GitHub Event Monitor initialized');
    console.log(`Auto-refresh every ${REFRESH_INTERVAL / 1000} seconds`);
    
    // Initial fetch
    fetchEvents();
    
    // Set up periodic refresh
    setInterval(fetchEvents, REFRESH_INTERVAL);
}

// Start the application when DOM is ready
if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', init);
} else {
    init();
}
