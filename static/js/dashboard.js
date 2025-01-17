class Dashboard {
    constructor() {
        this.temperatureElement = document.getElementById('temperature');
        this.moistureElement = document.getElementById('moisture');
        this.suggestionsElement = document.getElementById('suggestions-content');
    }

    fetchData() {
        fetch('/api/dashboard-data')
            .then(response => response.json())
            .then(data => {
                if (data.message === 'No data available') {
                    this.showNoDataMessage(); // Handle "No data" case
                } else {
                    this.updateDashboard(data); // Regular update if data exists
                }
            })
            .catch(error => console.error('Error fetching data:', error));
    }
    
    showNoDataMessage() {
        this.temperatureElement.textContent = "No data available.";
        this.moistureElement.textContent = "No data available.";
        this.suggestionsElement.textContent = "No data available.";
    }
    

    updateDashboard(data) {
        // Update temperature and moisture values
        this.temperatureElement.textContent = data.temperature + "°C";
        this.moistureElement.textContent = data.moisture + "%";
        
        // Update suggestions dynamically
        this.suggestionsElement.innerHTML = '';
        if (data.suggestions && data.suggestions.length > 0) {
            data.suggestions.forEach(suggestion => {
                const suggestionElement = document.createElement('p');
                suggestionElement.textContent = suggestion;
                this.suggestionsElement.appendChild(suggestionElement);
            });
        } else {
            this.suggestionsElement.innerHTML = "<p>No suggestions available.</p>";
        }
    }

    init() {
        this.fetchData();
    }
}

document.addEventListener('DOMContentLoaded', () => {
    const dashboard = new Dashboard();
    dashboard.init();
});
