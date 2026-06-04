document.addEventListener('DOMContentLoaded', () => {
    const priceDisplay = document.getElementById('price-display');
    const walletDisplay = document.getElementById('wallet-display');
    const marginDisplay = document.getElementById('margin-display');
    const pnlDisplay = document.getElementById('pnl-display');
    const lastUpdateDisplay = document.getElementById('last-update');
    
    // !!! ВАЖНО: Замени 'ТВОЙ_ВНЕШНИЙ_IP' на реальный External IP твоей VM из панели Google Cloud !!!
    // Пример: const BACKEND_URL = 'http://34.123.45.67:8000';
    const BACKEND_URL = 'http://35.229.167.204:8000';

    async function fetchData() {
        try {
            // Проверка на заглушку IP
            if (BACKEND_URL.includes('ТВОЙ_ВНЕШНИЙ_IP')) {
                console.error('Ошибка: BACKEND_URL не настроен! Замените "ТВОЙ_ВНЕШНИЙ_IP" на реальный IP вашей VM.');
                throw new Error('BACKEND_URL не настроен');
            }

            const response = await fetch(`${BACKEND_URL}/api/v1/status`);
            if (!response.ok) throw new Error('Network response was not ok');
            const data = await response.json();
            
            priceDisplay.textContent = `$ ${data.price}`;
            walletDisplay.textContent = `${data.wallet} ${data.currency}`;
            marginDisplay.textContent = `${data.equity} ${data.currency}`;
            lastUpdateDisplay.textContent = data.last_update || '---';
            
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