import requests


class CompostMonitor:
    def __init__(self):
        # Ideal temperature ranges in Celsius
        self.mesophilic_range = (20, 45)
        self.thermophilic_range = (45, 70)
        
        # Ideal moisture range in percentage
        self.moisture_range = (40, 60)
        
        # Temperature history to track changes
        self.temp_history = []
        
    def add_measurement(self, day, temperature, moisture):
        """Add a new measurement to the monitoring system."""
        self.temp_history.append({
            'day': day,
            'temperature': temperature,
            'moisture': moisture
        })
        
        return self.analyze_conditions()
    
    def analyze_conditions(self):
        """Analyze current composting conditions and provide recommendations."""
        if len(self.temp_history) == 0:
            return "No measurements available for analysis."
            
        current = self.temp_history[-1]
        recommendations = []
        
        # Check moisture conditions
        if current['moisture'] < self.moisture_range[0]:
            recommendations.append("Moisture too low. Add water or wet materials.")
        elif current['moisture'] > self.moisture_range[1]:
            recommendations.append("Moisture too high. Add dry brown materials and ensure proper drainage.")
            
        # Temperature analysis
        current_temp = current['temperature']
        
        # Early stage (first 3 days) temperature progression check
        if current['day'] <= 3:
            if len(self.temp_history) >= 2:
                prev_temp = self.temp_history[-2]['temperature']
                if current_temp <= prev_temp:
                    recommendations.append(
                        "Temperature not increasing as expected in early phase. "
                        "Please stir the pile and check carbon-to-nitrogen ratio."
                    )
        
        # Temperature range checks
        if current['day'] <= 3:
            if current_temp < self.mesophilic_range[0]:
                recommendations.append(
                    "Temperature too low for mesophilic phase. "
                    "Add more nitrogen-rich materials and ensure proper pile size."
                )
        else:
            if current_temp < self.thermophilic_range[0]:
                recommendations.append(
                    "Temperature too low for thermophilic phase. "
                    "Stir the pile and check moisture levels."
                )
            elif current_temp > self.thermophilic_range[1]:
                recommendations.append(
                    "Temperature too high! Reduce pile size or add brown materials."
                )
        
        # Generate status report
        status = f"""
Day {current['day']} Status:
Temperature: {current_temp}°C
Moisture: {current['moisture']}%

Analysis:"""
        
        if not recommendations:
            status += "\nAll conditions are optimal! Continue monitoring."
        else:
            status += "\nRecommendations:"
            for i, rec in enumerate(recommendations, 1):
                status += f"\n{i}. {rec}"
                
        return status

def fetch_data_from_thingspeak(channel_id, read_api_key):
    """Fetch the latest data from ThingSpeak."""
    url = f"https://api.thingspeak.com/channels/{channel_id}/feeds.json?api_key={read_api_key}&results=1"
    response = requests.get(url)
    data = response.json()
    if 'feeds' in data and len(data['feeds']) > 0:
        latest_feed = data['feeds'][0]
        return latest_feed
    else:
        return None

