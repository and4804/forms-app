// API base URL - will be replaced with ngrok URL when deployed
const API_BASE_URL = window.location.origin;


// Check server status on load
checkServerStatus();

// Form submission handler
document.getElementById('userForm').addEventListener('submit', async (e) => {
    e.preventDefault();
    
    const formData = {
        name: document.getElementById('name').value,
        phone: document.getElementById('phone').value,
        age: document.getElementById('age').value,
        email: document.getElementById('email').value
    };
    
    try {
        const response = await fetch(`${API_BASE_URL}/api/submit`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(formData)
        });
        
        const result = await response.json();
        
        if (result.success) {
            showMessage('success', result.message);
            document.getElementById('userForm').reset();
            loadSubmissions();
        } else {
            showMessage('error', result.error);
        }
    } catch (error) {
        showMessage('error', 'Failed to submit form. Is the server running?');
        console.error('Error:', error);
    }
});

// Refresh button handler
document.getElementById('refreshBtn').addEventListener('click', () => {
    loadSubmissions();
    checkServerStatus();
});

// Check server status
async function checkServerStatus() {
    try {
        const response = await fetch(`${API_BASE_URL}/api/health`);
        const data = await response.json();
        
        const statusBadge = document.getElementById('serverStatus');
        statusBadge.textContent = `✅ Server Online (${data.total_submissions} submissions)`;
        statusBadge.className = 'status-badge online';
    } catch (error) {
        const statusBadge = document.getElementById('serverStatus');
        statusBadge.textContent = '❌ Server Offline';
        statusBadge.className = 'status-badge offline';
    }
}

// Load submissions
async function loadSubmissions() {
    try {
        const response = await fetch(`${API_BASE_URL}/api/submissions`);
        const result = await response.json();
        
        const listContainer = document.getElementById('submissionsList');
        
        if (result.success && result.data.length > 0) {
            listContainer.innerHTML = result.data.map(submission => `
                <div class="submission-card">
                    <div class="name">${escapeHtml(submission.name)}</div>
                    <div class="details">
                        📞 ${escapeHtml(submission.phone)}<br>
                        🎂 Age: ${submission.age}<br>
                        ${submission.email ? `📧 ${escapeHtml(submission.email)}` : ''}
                    </div>
                    <div class="timestamp">Submitted: ${formatDate(submission.timestamp)}</div>
                </div>
            `).join('');
        } else {
            listContainer.innerHTML = '<div class="empty-state">No submissions yet</div>';
        }
    } catch (error) {
        console.error('Error loading submissions:', error);
    }
}

// Show message
function showMessage(type, text) {
    const messageDiv = document.getElementById('message');
    messageDiv.textContent = text;
    messageDiv.className = `message ${type}`;
    
    setTimeout(() => {
        messageDiv.style.display = 'none';
    }, 5000);
}

// Helper function to escape HTML
function escapeHtml(text) {
    const div = document.createElement('div');
    div.textContent = text;
    return div.innerHTML;
}

// Format date
function formatDate(dateString) {
    const date = new Date(dateString);
    return date.toLocaleString();
}

// Load submissions on page load
loadSubmissions();

// Auto-refresh every 30 seconds
setInterval(() => {
    loadSubmissions();
    checkServerStatus();
}, 30000);
