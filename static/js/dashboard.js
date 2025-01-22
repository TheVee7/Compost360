function fetchData() {
    const loader = document.getElementById('loader');
    loader.style.display = 'block'; // Show the loader

    fetch('/api/dashboard-data')
        .then(response => response.json())
        .then(data => {
            console.log('Fetched Data:', data);  // Log the data to the console
            loader.style.display = 'none'; // Hide the loader
            if (data.error || (data.suggestions && data.suggestions.length === 0)) {
                this.showNoDataMessage();
            } else {
                this.updateDashboard(data);
            }
        })
        .catch(error => {
            loader.style.display = 'none'; // Hide the loader on error
            console.error('Error fetching data:', error);
            this.showNoDataMessage();
        });
}
window.onload = function() {
    fetchData();
};


function updateDashboard(data) {
    console.log('Data received:', data); // Log the data

    document.getElementById('temperature').textContent = `${data.temperature.toFixed(1)}°C`;
    document.getElementById('moisture').textContent = `${data.moisture.toFixed(1)}%`;
    document.getElementById('maturation').textContent = `${data.maturation_estimate} days`;

    const suggestionsContent = document.getElementById('suggestions-content');
    suggestionsContent.innerHTML = ''; // Clear existing suggestions

    (data.suggestions || []).forEach(suggestion => {
        suggestionsContent.innerHTML += `<p>${suggestion}</p>`;
    });

    document.getElementById('no-data-message').style.display = 'none';
    document.querySelector('.metrics-grid').style.display = 'block';
    document.querySelector('.suggestions-panel').style.display = 'block';
}

function toggleNav() {
    const navLinks = document.querySelector('.nav-links');
    const toggleButton = document.querySelector('.navbar-toggle');
    const expanded = toggleButton.getAttribute('aria-expanded') === 'true' || false;
    toggleButton.setAttribute('aria-expanded', !expanded);
    navLinks.classList.toggle('open');
}