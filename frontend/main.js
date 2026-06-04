document.addEventListener('DOMContentLoaded', () => {
    const priceDisplay = document.getElementById('price-display');
    const walletDisplay = document.getElementById('wallet-display');
    const marginDisplay = document.getElementById('margin-display');
    const pnlDisplay = document.getElementById('pnl-display');
    
    const BACKEND_URL = 'http://localhost:8000'; 

    async function fetchData() {
        try {
            const response = await fetch(`${BACKEND_URL}/api/status`);
            if (!response.ok) throw new Error('Network response was not ok');
            const data = await response.json();
            
            priceDisplay.textContent = `$ ${data.price}`;
            walletDisplay.textContent = `${data.wallet} ${data.currency}`;
            marginDisplay.textContent = `${data.equity} ${data.currency}`;
            
            const pnl = parseFloat(data.pnl);
            pnlDisplay.textContent = `${pnl > 0 ? '+' : ''}${data.pnl} ${data.currency}`;
            
            // Dynamic color for PnL
            pnlDisplay.style.color = pnl > 0 ? '#27ae60' : (pnl < 0 ? '#e74c3c' : '#007bff');

        } catch (error) {
            console.error('Fetch error:', error);
            priceDisplay.textContent = 'Offline';
            walletDisplay.textContent = 'Offline';
            marginDisplay.textContent = 'Offline';
            pnlDisplay.textContent = 'Offline';
            pnlDisplay.style.color = '#333';
        }
    }

    fetchData(); // Fetch data on page load
    setInterval(fetchData, 1000); // Refresh every second
});