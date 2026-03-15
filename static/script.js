const chatHistory = document.getElementById('chat-history');
const userInput = document.getElementById('user-input');
const sendBtn = document.getElementById('send-btn');

let history = [];
let currentTopic = '';

const AVATARS = {
    'philosopher': 'static/philosopher.png',
    'chaos': 'static/chaos.png',
    'scientist': 'static/scientist.png',
    'arbiter': 'static/arbiter.png',
    'user': 'default' 
};

// UI Helper: Add message to chat
function addMessage(text, role, persona = '') {
    const wrapper = document.createElement('div');
    wrapper.className = `message-wrapper ${role}`;
    if (persona === 'arbiter') wrapper.classList.add('arbiter-wrapper');

    const avatar = document.createElement('div');
    avatar.className = 'avatar-mini';
    
    if (persona && AVATARS[persona] !== 'default') {
        avatar.style.backgroundImage = `url('${AVATARS[persona]}')`;
        avatar.innerText = '';
    } else if (role === 'user') {
        avatar.style.background = 'var(--accent-philosopher)';
        avatar.innerText = 'ME';
        avatar.style.color = '#000';
    } else {
        avatar.innerText = persona ? persona[0].toUpperCase() : 'A';
    }

    const msgDiv = document.createElement('div');
    msgDiv.className = `message ${role}`;
    if (persona === 'arbiter') msgDiv.classList.add('arbiter-msg');
    
    msgDiv.innerText = text;
    
    if (persona !== 'arbiter') {
        wrapper.appendChild(avatar);
    }
    wrapper.appendChild(msgDiv);
    
    chatHistory.appendChild(wrapper);
    chatHistory.scrollTop = chatHistory.scrollHeight;
    
    if (role === 'bot' && persona && persona !== 'arbiter') {
        history.push({ role: 'model', text: text });
    } else if (role === 'user') {
        history.push({ role: 'user', text: text });
    }
}

// UI Helper: Highlight active persona card
function highlightPersona(personaId) {
    document.querySelectorAll('.persona-card').forEach(card => card.classList.remove('active'));
    if (personaId) {
        const card = document.getElementById(`p-${personaId}`);
        if (card) card.classList.add('active');
    }
}

// UI Helper: Update energy bars randomly to feel "live"
function updateEnergy() {
    document.querySelectorAll('.energy-bar').forEach(bar => {
        const val = Math.floor(Math.random() * 60) + 40;
        bar.style.width = `${val}%`;
    });
}

// Logical Flow: Execute a full multi-persona turn
async function runDebateCycle(userText) {
    if (!currentTopic) currentTopic = userText;
    
    sendBtn.disabled = true;
    sendBtn.innerText = '토론 중...';
    
    addMessage(userText, 'user');
    userInput.value = '';
    
    // 1. Fact check the user input first
    await factCheck(userText);
    
    // 2. Batch Request to save quota
    try {
        const response = await fetch('/debate_batch', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({
                topic: currentTopic,
                history: history.slice(-6)
            })
        });
        const data = await response.json(); // Expected: {philosopher, chaos, scientist}
        
        const personas = ['philosopher', 'chaos', 'scientist'];
        for (const p of personas) {
            highlightPersona(p);
            updateEnergy();
            
            const text = data[p] || "... (답변 생성이 지연되고 있습니다) ...";
            addMessage(text, 'bot', p);
            
            // Random fact check for AI sometimes
            if (Math.random() > 0.8) {
                await factCheck(text);
            }
            
            await new Promise(r => setTimeout(r, 800));
        }
    } catch (err) {
        console.error("Batch Debate Error:", err);
        addMessage("시스템 할당량 초과 또는 네트워크 오류가 발생했습니다.", "bot", "arbiter");
    }
    
    highlightPersona(null);
    sendBtn.disabled = false;
    sendBtn.innerText = '전송';
}

// Fact Check triggering
async function factCheck(claim) {
    highlightPersona('arbiter');
    const arbiterCard = document.getElementById('p-arbiter');
    arbiterCard.classList.add('glitch');
    
    try {
        const response = await fetch('/factcheck', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ claim: claim.substring(0, 500) })
        });
        const data = await response.json();
        addMessage(`[중재자 팩트체크] ${data.text}`, 'bot', 'arbiter');
    } catch (err) {
        console.error(err);
    } finally {
        setTimeout(() => arbiterCard.classList.remove('glitch'), 500);
    }
}

sendBtn.addEventListener('click', () => {
    const text = userInput.value.trim();
    if (text) runDebateCycle(text);
});

userInput.addEventListener('keypress', (e) => {
    if (e.key === 'Enter') {
        const text = userInput.value.trim();
        if (text) runDebateCycle(text);
    }
});

// Initial energy pulse
setInterval(updateEnergy, 3000);
