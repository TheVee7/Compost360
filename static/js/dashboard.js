class Dashboard {
    constructor() {
        this.temperatureElement = document.getElementById('temperature');
        this.moistureElement = document.getElementById('moisture');
        this.suggestionsElement = document.getElementById('suggestions-content');
        
        this.initializeRealTimeUpdates();
    }

    initializeRealTimeUpdates() {
        setInterval(() => {
            this.fetchSensorData();
        }, 5000);
    }

    async fetchSensorData() {
        try {
            const response = await fetch('/api/sensor_data');
            const data = await response.json();
            
            this.updateMetrics(data);
            this.updateSuggestions(data);
        } catch (error) {
            console.error('Error fetching sensor data:', error);
        }
    }

    updateMetrics(data) {
        this.temperatureElement.textContent = `${data.temperature.toFixed(1)}°C`;
        this.moistureElement.textContent = `${data.moisture.toFixed(1)}%`;
    }

    updateSuggestions(data) {
        let suggestions = [];
        
        if (data.temperature > 35) {
            suggestions.push('⚠️ Temperature is high - consider adding brown materials');
        } else if (data.temperature < 25) {
            suggestions.push('⚠️ Temperature is low - add green materials or turn the pile');
        }

        if (data.moisture > 60) {
            suggestions.push('⚠️ Too wet - add dry brown materials');
        } else if (data.moisture < 45) {
            suggestions.push('⚠️ Too dry - add water or green materials');
        }

        this.suggestionsElement.innerHTML = suggestions.map(s => `<p>${s}</p>`).join('');
    }
}