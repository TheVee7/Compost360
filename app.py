from flask import Flask, render_template, request, redirect, url_for, flash, jsonify
from flask_mail import Mail, Message
from config import Config
import random
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
        if request.method == 'POST':
            name = request.form.get('name')
            email = request.form.get('email')
            message = request.form.get('message')
            
            msg = Message('New Contact Form Submission',
                         sender=app.config['MAIL_USERNAME'],
                         recipients=[app.config['MAIL_USERNAME']])
            msg.body = f"From: {name}\nEmail: {email}\nMessage: {message}"
            mail.send(msg)
            
            flash('Thank you for your message!')
            return redirect(url_for('contact'))
        
        return render_template('contact.html')

    @app.route('/api/dashboard-data')
    def dashboard_data():
        # Check if data exists (in your case, there might be no data in the DB or source)
        entry = None  # No data available currently
        
        if entry is None:
            # If no data, return a response indicating no data is available
            return jsonify({'message': 'No data available'}), 404
        
        # If data exists, return it
        return jsonify(entry)



    return app

if __name__ == '__main__':
    app = create_app()
    app.run(host='0.0.0.0', port=5000, debug=True)