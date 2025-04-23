document.addEventListener('DOMContentLoaded', function() {
    // DOM Elements
    const userInput = document.getElementById('userInput');
    const sendBtn = document.getElementById('sendBtn');
    const chatMessages = document.getElementById('chatMessages');
    const historyBtn = document.getElementById('historyBtn');
    const contentBtn = document.getElementById('contentBtn');
    const themeToggleBtn = document.getElementById('themeToggleBtn');
    const sidebar = document.getElementById('sidebar');
    const closeSidebarBtn = document.getElementById('closeSidebarBtn');
    const historyList = document.getElementById('historyList');
    const contentViewer = document.getElementById('contentViewer');
    const closeContentBtn = document.getElementById('closeContentBtn');
    const downloadContentBtn = document.getElementById('downloadContentBtn');
    const contentDisplay = document.getElementById('contentDisplay');
    const newChatBtn = document.getElementById('newChatBtn');
    const newChatIconBtn = document.getElementById('newChatIconBtn');

    // State variables
    let currentUrl = '';
    let waitingForUrl = true;
    let isDarkMode = true; // Default to dark mode since your UI appears dark

    // Initialize theme from localStorage
    if (localStorage.getItem('darkMode') === 'false') {
        document.documentElement.removeAttribute('data-theme');
        themeToggleBtn.textContent = 'Dark Mode';
        isDarkMode = false;
    } else {
        document.documentElement.setAttribute('data-theme', 'dark');
        themeToggleBtn.textContent = 'Light Mode';
    }

    // Event Listeners
    sendBtn.addEventListener('click', handleSendMessage);
    userInput.addEventListener('keypress', function(e) {
        if (e.key === 'Enter') {
            handleSendMessage();
        }
    });

    historyBtn.addEventListener('click', toggleHistorySidebar);
    contentBtn.addEventListener('click', showWebsiteContent);
    themeToggleBtn.addEventListener('click', toggleTheme);
    closeSidebarBtn && closeSidebarBtn.addEventListener('click', toggleHistorySidebar);
    closeContentBtn && closeContentBtn.addEventListener('click', closeContentViewer);
    downloadContentBtn && downloadContentBtn.addEventListener('click', downloadContent);
    
    // New chat buttons event listeners
    newChatBtn && newChatBtn.addEventListener('click', startNewChat);
    newChatIconBtn && newChatIconBtn.addEventListener('click', startNewChat);

    // Functions
    function handleSendMessage() {
        const message = userInput.value.trim();
        if (!message) return;

        // Add user message to chat
        addMessageToChat(message, 'user');
        userInput.value = '';

        if (waitingForUrl) {
            // Handle URL submission
            processUrl(message);
        } else {
            // Handle question
            askQuestion(message);
        }
    }

    function processUrl(url) {
        currentUrl = url;
        addMessageToChat('Processing website...', 'bot');

        fetch('/extract', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ url })
        })
        .then(response => {
            if (!response.ok) {
                throw new Error(`HTTP error! status: ${response.status}`);
            }
            return response.json();
        })
        .then(data => {
            if (data.success) {
                waitingForUrl = false;
                
                // Replace the loading message with success
                const loadingMsg = chatMessages.lastElementChild;
                chatMessages.removeChild(loadingMsg);
                
                addMessageToChat('Content extracted successfully. You can now ask questions about this website.', 'bot');
            } else {
                addMessageToChat(`Error: ${data.error || 'Unknown error'}`, 'error');
            }
        })
        .catch(error => {
            console.error('Error in processUrl:', error);
            addMessageToChat(`Error: ${error.message}`, 'error');
        });
    }

    function askQuestion(question) {
        fetch('/ask', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ 
                question,
                url: currentUrl
            })
        })
        .then(response => {
            if (!response.ok) {
                throw new Error(`HTTP error! status: ${response.status}`);
            }
            return response.json();
        })
        .then(data => {
            if (data.success) {
                addMessageToChat(data.answer, 'bot');
            } else {
                addMessageToChat(`Error: ${data.error || 'Unknown error'}`, 'error');
            }
        })
        .catch(error => {
            console.error('Error in askQuestion:', error);
            addMessageToChat(`Error: ${error.message}`, 'error');
        });
    }

    function addMessageToChat(message, type) {
        const messageDiv = document.createElement('div');
        messageDiv.classList.add('message', type);
        
        const messageText = document.createElement('p');
        messageText.textContent = message;
        messageDiv.appendChild(messageText);
        
        chatMessages.appendChild(messageDiv);
        
        // Scroll to bottom
        chatMessages.scrollTop = chatMessages.scrollHeight;
    }

    function toggleHistorySidebar() {
        if (sidebar) {
            sidebar.classList.toggle('hidden');
            
            if (!sidebar.classList.contains('hidden')) {
                loadHistory();
            }
        }
    }

    function loadHistory() {
        fetch('/history')
            .then(response => {
                if (!response.ok) {
                    throw new Error(`HTTP error! status: ${response.status}`);
                }
                return response.json();
            })
            .then(data => {
                if (data.success && data.history) {
                    displayHistory(data.history);
                } else {
                    historyList.innerHTML = '<div class="history-empty">No history available</div>';
                }
            })
            .catch(error => {
                console.error('Error loading history:', error);
                historyList.innerHTML = `<div class="history-empty">Error loading history: ${error.message}</div>`;
            });
    }

    function displayHistory(history) {
        historyList.innerHTML = '';
        
        if (Object.keys(history).length === 0) {
            const emptyMsg = document.createElement('div');
            emptyMsg.className = 'history-empty';
            emptyMsg.textContent = 'No history yet';
            historyList.appendChild(emptyMsg);
            return;
        }
        
        // Process history object
        for (const url in history) {
            const historyItem = document.createElement('div');
            historyItem.className = 'history-item';
            
            const title = document.createElement('h3');
            title.textContent = url;
            
            historyItem.appendChild(title);
            
            // Add conversation preview if available
            if (history[url].length > 0) {
                const preview = document.createElement('p');
                preview.className = 'history-preview';
                preview.textContent = `${history[url].length} question(s)`;
                historyItem.appendChild(preview);
            }
            
            historyItem.addEventListener('click', () => {
                loadConversation(url, history[url]);
                toggleHistorySidebar();
            });
            
            historyList.appendChild(historyItem);
        }
    }

    function loadConversation(url, conversation) {
        // Clear chat
        chatMessages.innerHTML = '';
        
        // Add initial message
        addMessageToChat('Please enter any website link for asking questions related to it.', 'bot');
        
        // Add URL message
        addMessageToChat(url, 'user');
        
        // Add success message
        addMessageToChat('Content extracted successfully. You can now ask questions about this website.', 'bot');
        
        // Add all conversation messages
        conversation.forEach(msg => {
            addMessageToChat(msg.question, 'user');
            addMessageToChat(msg.answer, 'bot');
        });
        
        // Set current state
        currentUrl = url;
        waitingForUrl = false;
    }

    // Function to start a new chat
    function startNewChat() {
        // Clear chat messages
        chatMessages.innerHTML = '';
        
        // Add welcome message
        addMessageToChat('Please enter any website link for asking questions related to it.', 'bot');
        
        // Reset state
        currentUrl = '';
        waitingForUrl = true;
        
        // Close sidebar if it's open
        if (sidebar && !sidebar.classList.contains('hidden')) {
            sidebar.classList.add('hidden');
        }
        
        // Focus on input
        userInput.focus();
    }

    function showWebsiteContent() {
        fetch('/content')
            .then(response => {
                if (!response.ok) {
                    throw new Error(`HTTP error! status: ${response.status}`);
                }
                return response.json();
            })
            .then(data => {
                if (data.success) {
                    if (contentDisplay) {
                        contentDisplay.textContent = data.content;
                        contentViewer.classList.remove('hidden');
                    } else {
                        addMessageToChat("Content retrieved but display element not found.", 'error');
                    }
                } else {
                    addMessageToChat(`Error: ${data.error || 'Could not retrieve content'}`, 'error');
                }
            })
            .catch(error => {
                console.error('Error in showWebsiteContent:', error);
                addMessageToChat(`Error retrieving content: ${error.message}`, 'error');
            });
    }

    function closeContentViewer() {
        if (contentViewer) {
            contentViewer.classList.add('hidden');
        }
    }

    function downloadContent() {
        window.location.href = '/download';
    }

    function toggleTheme() {
        isDarkMode = !isDarkMode;
        if (isDarkMode) {
            document.documentElement.setAttribute('data-theme', 'dark');
            themeToggleBtn.textContent = 'Light Mode';
        } else {
            document.documentElement.removeAttribute('data-theme');
            themeToggleBtn.textContent = 'Dark Mode';
        }
        localStorage.setItem('darkMode', isDarkMode);
    }
});