from flask import Flask, render_template, request, redirect, url_for, flash, jsonify
from flask_mail import Mail, Message
from database import db
from models import User, CompostEntry
from config import Config
import random

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    db.init_app(app)
    mail = Mail(app)

    with app.app_context():
        db.create_all()  

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
        quantity = float(request.form.get('quantity'))
        
        entry = CompostEntry(
            user_id=1,  # Replace with actual user ID after authentication
            waste_type=waste_type,
            quantity=quantity,
            temperature=random.uniform(20, 40),
            moisture=random.uniform(40, 70),
            maturation_estimate=random.randint(30, 90)
        )
        
        db.session.add(entry)
        db.session.commit()
        
        return redirect(url_for('dashboard'))

    @app.route('/dashboard')
    def dashboard():
        # Fetch latest compost entry for demo
        entry = CompostEntry.query.order_by(CompostEntry.date_added.desc()).first()
        return render_template('dashboard.html', entry=entry)

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

    @app.route('/api/sensor_data')
    def sensor_data():
        # Simulate sensor data
        return jsonify({
            'temperature': random.uniform(20, 40),
            'moisture': random.uniform(40, 70)
        })

    return app

if __name__ == '__main__':
    app = create_app()
    app.run(host='0.0.0.0', port=5000, debug=True)
    