// Initialize the application
document.addEventListener('DOMContentLoaded', function() {
    // Get references to DOM elements
    const generateBtn = document.getElementById('generate-btn');
    const resultContainer = document.getElementById('result-container');
    const invoiceNumberDiv = document.getElementById('invoice-number');
    const resultTimestamp = document.getElementById('result-timestamp');
    const loadingDiv = document.getElementById('loading');
    const statsDiv = document.getElementById('stats');

    // Attach click handler to the button
    generateBtn.addEventListener('click', generateInvoiceNumber);

    // Load initial stats
    loadStats();

    /**
     * Generate a new invoice number
     */
    function generateInvoiceNumber() {
        // Disable button and show loading
        generateBtn.disabled = true;
        loadingDiv.style.display = 'flex';

        // Make API call to generate number
        fetch('/api/generate', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            }
        })
            .then(response => response.json())
            .then(data => {
                if (data.success) {
                    // Display the generated number
                    invoiceNumberDiv.textContent = data.invoice_number;
                    
                    // Display timestamp
                    const now = new Date();
                    resultTimestamp.textContent = 'Generiert: ' + now.toLocaleString('de-DE');
                    
                    // Show result container with animation
                    resultContainer.style.display = 'block';
                    
                    // Print to console (server also logs)
                    console.log('Invoice Number Generated:', data.invoice_number);
                    
                    // Update stats
                    loadStats();
                    
                    // Show success animation
                    invoiceNumberDiv.style.animation = 'none';
                    setTimeout(() => {
                        invoiceNumberDiv.style.animation = 'pulse 0.5s ease-out';
                    }, 10);
                } else {
                    alert('Fehler bei der Generierung der Rechnungsnummer');
                }
            })
            .catch(error => {
                console.error('Error:', error);
                alert('Fehler bei der Verbindung zum Server');
            })
            .finally(() => {
                // Re-enable button and hide loading
                generateBtn.disabled = false;
                loadingDiv.style.display = 'none';
            });
    }

    /**
     * Load and display statistics
     */
    function loadStats() {
        fetch('/api/stats', {
            method: 'GET'
        })
            .then(response => response.json())
            .then(data => {
                let statsText = `Generierte Nummern in ${data.year}: ${data.codes_generated} / 1000`;
                
                if (data.history_file_exists) {
                    statsText += `<br><span class="history-status">📁 Verlauf geladen von: ${data.history_file}</span>`;
                } else {
                    statsText += `<br><span class="history-status new">✨ Neuer Verlauf wird angelegt</span>`;
                }
                
                statsDiv.innerHTML = statsText;
            })
            .catch(error => {
                console.error('Error loading stats:', error);
            });
    }
});

// Add pulse animation in CSS (can also be added to style.css)
const style = document.createElement('style');
style.textContent = `
    @keyframes pulse {
        0% {
            transform: scale(1);
        }
        50% {
            transform: scale(1.1);
        }
        100% {
            transform: scale(1);
        }
    }
`;
document.head.appendChild(style);
