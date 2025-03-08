from flask import Flask, render_template, redirect, url_for, request, flash, session, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime
import os
import json  # Added import
import random  # Added import
from transformers import pipeline  # Added import
from collections import Counter
from datetime import timedelta


emotion_pipeline = pipeline("text-classification", model="SamLowe/roberta-base-go_emotions", top_k=2)

def get_dynamic_suggestion(primary_emotion, secondary_emotion, text):
    """Generate a meaningful suggestion with media recommendations from JSON.
    
    Args:
        primary_emotion (str): The main emotion detected
        secondary_emotion (str): The secondary emotion detected
        text (str): The journal text input
    Returns:
        dict: A dictionary containing suggestion text and media links
    """
    # Convert emotions to lowercase for matching
    primary = primary_emotion.lower()
    secondary = secondary_emotion.lower()
    
    # Default suggestion if emotion not found or JSON fails
    default_suggestion = {
        "text": "Take a deep breath and reflect on your feelings.",
        "video_link": "",
        "playlist_link": "",
        "quote": "Every moment is a fresh beginning."
    }
    
    try:
        # Load suggestions from JSON file
        with open("suggestions.json", "r") as file:
            SUGGESTIONS = json.load(file)
        
        # Get suggestions for both emotions or use defaults
        primary_suggestions = SUGGESTIONS.get(primary, [default_suggestion])
        secondary_suggestions = SUGGESTIONS.get(secondary, [default_suggestion])
        
        # Randomly select suggestion objects from each emotion
        primary_suggestion = random.choice(primary_suggestions)
        secondary_suggestion = random.choice(secondary_suggestions)
        
        # Create a personalized touch based on text length
        if len(text) > 100:
            dynamic_part = " Your detailed reflection shows you're processing your emotions well."
        else:
            dynamic_part = " Consider expanding on your thoughts to better understand your feelings."
        
        # Combine the suggestions and media links
        response = {
            "text": f"{primary_suggestion['text']} {secondary_suggestion['text']}{dynamic_part}",
            "quote": primary_suggestion['quote'],  # Use primary emotion's quote
            "video_link": primary_suggestion['video_link'],  # Use primary emotion's video
            "playlist_link": secondary_suggestion['playlist_link']  # Use secondary emotion's playlist
        }
        
        return response
        
    except Exception as e:
        print(f"Error loading suggestions: {e}")
        return default_suggestion  

app = Flask(__name__)

# Setup for the app
basedir = os.path.abspath(os.path.dirname(__file__))
app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{os.path.join(basedir, "instance", "data.db")}'
app.config['SECRET_KEY'] = '1234'  # You can generate a more secure key for production
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Initialize SQLAlchemy and LoginManager
db = SQLAlchemy(app)
login_manager = LoginManager()
login_manager.init_app(app)

# LoginManager Setup
login_manager.login_view = "login"

# User Loader Function for Flask-Login
@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

# Define User Model for the users table in the database
class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(200), nullable=False)
    name = db.Column(db.String(100))
    emotional_score = db.Column(db.Integer, default=50)
    journals = db.relationship('Journal', backref='author', lazy=True)

    # Method to check if the provided password matches the stored one
    def check_password(self, password):
        return check_password_hash(self.password, password)

    # Method to set the password after hashing it
    def set_password(self, password):
        self.password = generate_password_hash(password, method='pbkdf2:sha256')

    def __repr__(self):
        return f'<User {self.email}>'

# Create Journal Model for storing journal entries
class Journal(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    title = db.Column(db.String(200), nullable=False)
    text = db.Column(db.Text, nullable=False)
    reason = db.Column(db.String(100))
    date = db.Column(db.DateTime, default=datetime.utcnow)
    mood = db.Column(db.String(50))
    primary_emotion = db.Column(db.String(50))
    primary_emotion_percentage = db.Column(db.Float)
    secondary_emotion = db.Column(db.String(50))
    secondary_emotion_percentage = db.Column(db.Float)

    def __repr__(self):
        return f'<Journal {self.title}>'

# Define mood values
MOOD_VALUES = {
    "admiration": 5,
    "amusement": 5,
    "anger": -10,
    "annoyance": -5,
    "approval": 5,
    "caring": 5,
    "confusion": -5,
    "curiosity": 5,
    "desire": 5,
    "disappointment": -5,
    "disapproval": -5,
    "disgust": -10,
    "embarrassment": -5,
    "excitement": 10,
    "fear": -10,
    "gratitude": 10,
    "grief": -5,
    "joy": 10,
    "love": 10,
    "nervousness": -5,
    "optimism": 5,
    "pride": 5,
    "realization": 5,
    "relief": 5,
    "remorse": -5,
    "sadness": -10,
    "surprise": 5,
    "neutral": 0
}

# Route for Home Page
@app.route('/')
def home():
    return render_template('home.html')

# Route for Start Page
@app.route('/start')
def start():
    return render_template('login.html')

# Route for Login Page
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        
        # Find user by email
        user = User.query.filter_by(email=email).first()
        
        # If the user exists and the password matches, log the user in
        if user and user.check_password(password):
            login_user(user)  # Log in the user
            session['user_id'] = user.id  # Store user ID in session
            return redirect(url_for('journal'))  # Redirect to journal if login is successful
        else:
            flash('Invalid email or password', 'error')  # Flash an error if login fails
    
    return render_template('login.html')

# Route for Sign Up Page
@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        password = request.form['password']

        # Check if email already exists
        existing_user = User.query.filter_by(email=email).first()
        if existing_user:
            flash('Email already exists! Logging you in.', 'info')
            login_user(existing_user)  # Log the user in if they already exist
            return redirect(url_for('journal'))  # Redirect to journal if user exists

        # Create a new user with hashed password
        new_user = User(name=name, email=email)
        new_user.set_password(password)
        db.session.add(new_user)
        db.session.commit()

        login_user(new_user)  # Log the user in after signing up
        session['user_id'] = new_user.id  # Store user ID in session
        return redirect(url_for('signup_quiz'))  # Redirect to quiz after signup

    return render_template('signup.html')

# Route for Sign Up Quiz
@app.route('/signup_quiz', methods=['GET', 'POST'])
@login_required
def signup_quiz():
    if request.method == 'POST':
        # Process the quiz data here and update the user emotional score
        q1 = request.form.get('q1')
        q2 = request.form.get('q2')
        q3 = request.form.get('q3')
        q4 = request.form.get('q4')
        q5 = request.form.get('q5')
        q6 = request.form.get('q6')
        q7 = request.form.get('q7')
        q8 = request.form.get('q8')
        q9 = request.form.get('q9')
        q10 = request.form.get('q10')

        # Calculate the emotional score based on responses
        emotional_score = 0

        # Scoring logic based on the responses
        if q1 == 'happy':
            emotional_score += 10
        elif q1 == 'neutral':
            emotional_score += 0
        elif q1 == 'sad':
            emotional_score -= 10
        elif q1 == 'angry':
            emotional_score -= 20

        if q2 == 'very_often':
            emotional_score -= 10
        elif q2 == 'sometimes':
            emotional_score += 0
        elif q2 == 'rarely':
            emotional_score += 5
        elif q2 == 'never':
            emotional_score += 10

        if q3 == 'positive':
            emotional_score += 10
        elif q3 == 'neutral':
            emotional_score += 0
        elif q3 == 'negative':
            emotional_score -= 10
        elif q3 == 'avoid':
            emotional_score -= 20

        if q4 == 'positive':
            emotional_score += 10
        elif q4 == 'neutral':
            emotional_score += 0
        elif q4 == 'negative':
            emotional_score -= 10
        elif q4 == 'no_use':
            emotional_score += 5

        if q5 == 'open':
            emotional_score += 10
        elif q5 == 'when_needed':
            emotional_score += 5
        elif q5 == 'rarely':
            emotional_score += 0
        elif q5 == 'hide':
            emotional_score -= 10

        if q6 == 'yes':
            emotional_score += 10
        elif q6 == 'sometimes':
            emotional_score += 5
        elif q6 == 'no':
            emotional_score -= 10

        if q7 == 'relaxed':
            emotional_score += 10
        elif q7 == 'neutral':
            emotional_score += 0
        elif q7 == 'exhausted':
            emotional_score -= 10
        elif q7 == 'frustrated':
            emotional_score -= 20

        if q8 == 'always':
            emotional_score -= 20
        elif q8 == 'often':
            emotional_score -= 10
        elif q8 == 'sometimes':
            emotional_score += 0
        elif q8 == 'rarely':
            emotional_score += 10

        if q9 == 'calm':
            emotional_score += 10
        elif q9 == 'talk':
            emotional_score += 5
        elif q9 == 'suppress':
            emotional_score += 0
        elif q9 == 'lash_out':
            emotional_score -= 10

        if q10 == 'music':
            emotional_score += 10
        elif q10 == 'friends':
            emotional_score += 5
        elif q10 == 'hobby':
            emotional_score += 5
        elif q10 == 'sleep':
            emotional_score += 5

        # Update the user's emotional score in the database
        current_user.emotional_score = emotional_score
        db.session.commit()

        # Check if the user is logged in and redirect to the journal page
        if current_user.is_authenticated:
            return redirect(url_for('journal'))  # Redirect to the journal page after completing the quiz
        else:
            flash('You need to log in to access the journal.', 'error')
            return redirect(url_for('login'))  # Redirect to login if not authenticated

    return render_template('signupquiz.html')

@app.route('/journal', methods=['GET', 'POST'])
@login_required
def journal():
    if request.method == "POST":
        try:
            # Check if it's an AJAX request for analysis
            if request.is_json:
                data = request.get_json()
                text = data.get('journal_text')
                
                # Analyze emotions
                emotion_results = emotion_pipeline(text)[0]
                primary_emotion = emotion_results[0]['label']
                primary_emotion_percentage = emotion_results[0]['score'] * 100
                secondary_emotion = emotion_results[1]['label']
                secondary_emotion_percentage = emotion_results[1]['score'] * 100
                
                # Get suggestions
                suggestion_data = get_dynamic_suggestion(primary_emotion, secondary_emotion, text)
                
                # Return analysis results with emotions
                return jsonify({
                    "success": True,
                    "primary_emotion": primary_emotion,
                    "primary_emotion_percentage": f"{primary_emotion_percentage:.1f}",
                    "secondary_emotion": secondary_emotion,
                    "secondary_emotion_percentage": f"{secondary_emotion_percentage:.1f}",
                    "suggestion": suggestion_data["text"],
                    "quote": suggestion_data["quote"],
                    "video_link": suggestion_data["video_link"],
                    "playlist_link": suggestion_data["playlist_link"]
                })
            else:
                # Regular form submission
                text = request.form.get("journal_text")
                title = request.form.get("title")
                reason = request.form.get("reason")
                
                if not text or not title or not reason:
                    flash("Please fill in all required fields", "error")
                    return redirect(url_for("journal"))
                
                # Analyze emotions
                emotion_results = emotion_pipeline(text)[0]
                primary_emotion = emotion_results[0]['label']
                primary_emotion_percentage = emotion_results[0]['score'] * 100
                secondary_emotion = emotion_results[1]['label']
                secondary_emotion_percentage = emotion_results[1]['score'] * 100
                
                # Create journal entry
                entry = Journal(
                    user_id=current_user.id,
                    title=title,
                    text=text,
                    reason=reason,
                    date=datetime.utcnow(),
                    mood=primary_emotion,
                    primary_emotion=primary_emotion,
                    primary_emotion_percentage=primary_emotion_percentage,
                    secondary_emotion=secondary_emotion,
                    secondary_emotion_percentage=secondary_emotion_percentage
                )
                
                db.session.add(entry)
                db.session.commit()
                
                flash("Journal entry saved successfully!", "success")
                return redirect(url_for("history"))
            
        except Exception as e:
            print(f"Error in journal route: {str(e)}")
            if request.is_json:
                return jsonify({"success": False, "error": str(e)}), 500
            db.session.rollback()
            flash(f"An error occurred: {str(e)}", "error")
            return redirect(url_for("journal"))
    
    return render_template("journal.html")

    
# Route for History Page (View Journal Entries)
@app.route('/history')
@login_required
def history():
    try:
        # Get all entries for current user, newest first
        entries = Journal.query.filter_by(user_id=current_user.id)\
                             .order_by(Journal.date.desc())\
                             .all()
        
        # Format entries for display
        formatted_entries = []
        for entry in entries:
            formatted_entry = {
                'id': entry.id,
                'title': entry.title,
                'text': entry.text,
                'reason': entry.reason,
                'date': entry.date.strftime('%Y-%m-%d %H:%M'),
                'mood': entry.mood,
                'primary_emotion': entry.primary_emotion,
                'primary_emotion_percentage': round(entry.primary_emotion_percentage, 2),
                'secondary_emotion': entry.secondary_emotion,
                'secondary_emotion_percentage': round(entry.secondary_emotion_percentage, 2)
            }
            formatted_entries.append(formatted_entry)
        
        return render_template('history.html', entries=formatted_entries)
    
    except Exception as e:
        flash("Error loading journal entries", "error")
        return render_template('history.html', entries=[])

# Route for Logout
@app.route('/logout')
def logout():
    logout_user()  # Log the user out
    session.pop('user_id', None)  # Remove the user_id from the session
    return redirect(url_for('home'))  # Redirect to home after logging out


@app.route('/analysis')
@login_required
def analysis():
    try:
        # Get user's journal entries
        entries = Journal.query.filter_by(user_id=current_user.id).all()
        
        # Prepare emotion distribution data
        emotions = [entry.primary_emotion for entry in entries]
        emotion_counter = Counter(emotions)
        emotion_colors = {
            'joy': '#FFD700',
            'sadness': '#4169E1',
            'anger': '#FF4500',
            'fear': '#800080',
            'love': '#FF69B4',
            'surprise': '#00FF7F',
            'confusion': '#DDA0DD',
            'excitement': '#FF6347',
            'gratitude': '#98FB98',
            'disappointment': '#CD853F'
        }
        
        emotion_data = {
            'labels': list(emotion_counter.keys()),
            'values': list(emotion_counter.values()),
            'colors': [emotion_colors.get(emotion, '#808080') for emotion in emotion_counter.keys()]
        }
        
        # Prepare emotional score timeline
        score_entries = sorted(entries, key=lambda x: x.date)
        score_data = {
            'dates': [entry.date.strftime('%Y-%m-%d') for entry in score_entries],
            'scores': [current_user.emotional_score for _ in score_entries]
        }
        
        # Prepare reasons distribution
        reasons = [entry.reason for entry in entries]
        reasons_counter = Counter(reasons)
        reason_colors = {
            'work': '#4CAF50',
            'relationship': '#FF69B4',
            'home': '#FFA500',
            'health': '#4169E1',
            'other': '#808080'
        }
        
        reasons_data = {
            'labels': list(reasons_counter.keys()),
            'values': list(reasons_counter.values()),
            'colors': [reason_colors.get(reason, '#808080') for reason in reasons_counter.keys()]
        }
        
        # Prepare top emotions data
        top_emotions = emotion_counter.most_common(5)
        top_emotions_data = {
            'labels': [emotion for emotion, _ in top_emotions],
            'values': [count for _, count in top_emotions]
        }
        
        return render_template('analysis.html',
                             emotion_data=emotion_data,
                             score_data=score_data,
                             reasons_data=reasons_data,
                             top_emotions_data=top_emotions_data)
                             
    except Exception as e:
        flash("Error generating analysis", "error")
        return redirect(url_for("journal"))

if __name__ == '__main__':
    with app.app_context():
        db.create_all()  # Create the database tables if they don't exist
    app.run(debug=True)
