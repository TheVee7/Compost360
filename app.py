from flask import Flask, render_template, request, redirect, url_for, flash, jsonify
from flask_mail import Mail, Message
from config import Config
from Calculation import CompostMonitor, fetch_data_from_thingspeak

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    mail = Mail(app)

    @app.route('/')
    def index():
        return render_template('index.html')

    @app.route('/purpose', methods=['POST'])
    def handle_purpose():
        purpose = request.form.get('purpose')
        if purpose is None:
            flash('Purpose is required.')
            return redirect(url_for('index'))
        elif purpose == 'individual':
            return redirect(url_for('individual'))
        return redirect(url_for('contact'))

    @app.route('/individual')
    def individual():
        return render_template('individual.html')

    @app.route('/submit_waste', methods=['POST'])
    def submit_waste():
        waste_type = request.form.get('waste_type')
        
        return redirect(url_for('dashboard'))

    @app.route('/dashboard')
    def dashboard():
        # Simulate fetching latest compost entry for demo
        return render_template('dashboard.html')

    @app.route('/about')
    def about():
        return render_template('about.html')

    @app.route('/contact', methods=['GET', 'POST'])
    def contact(): 
        return render_template('contact.html')
    
    
    @app.route('/api/dashboard-data')
    def dashboard_data():
        monitor = CompostMonitor()
        
        CHANNEL_ID = '2509864'
        API_KEY = 'BL366XG71WDZVE3L'
        
        # Fetch the latest data from ThingSpeak
        latest_data = fetch_data_from_thingspeak(CHANNEL_ID, API_KEY)
        
        if latest_data:
            day = int(latest_data['entry_id'])
            temperature = float(latest_data['field2'])  # Assuming temperature is in field2
            moisture = float(latest_data['field1'])     # Assuming moisture is in field1
        
            # Get the analysis and recommendations
            analysis_report = monitor.add_measurement(day, temperature, moisture)
        
            # Check if there are any recommendations in the report
            if "Recommendations:" in analysis_report:
                suggestions = analysis_report.split("\nRecommendations:")[1].strip().split("\n")
            else:
                suggestions = []  # No recommendations if not present
        
            # Optionally, you can calculate maturation_estimate dynamically based on your composting model
            maturation_estimate = 30  # Replace with dynamic calculation if required

            return jsonify({
                "temperature": temperature,
                "moisture": moisture,
                "maturation_estimate": maturation_estimate,
                "suggestions": suggestions
            })
        else:
            return jsonify({"error": "No data available from ThingSpeak."}), 404

    @app.route('/data_graphs')
    def data_graphs():
        return render_template('Data_graphs.html')
    
    return app
if __name__ == '__main__':
    app = create_app()
    app.run(host='0.0.0.0', port=5000, debug=True)