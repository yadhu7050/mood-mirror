from flask import Flask, request, render_template, jsonify, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from transformers import pipeline
import json
import random
import datetime
import os

app = Flask(__name__)
# Update database URI to use SQLite
basedir = os.path.abspath(os.path.dirname(__file__))
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'instance/data.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Ensure the instance folder exists
os.makedirs(os.path.join(basedir, 'instance'), exist_ok=True)

db = SQLAlchemy(app)

# Define the Journal Entry Model
class JournalEntry(db.Model):
    __tablename__ = 'journal_entry'  # Explicitly set table name
    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.Date, nullable=False)
    title = db.Column(db.String(200), nullable=False)
    reason = db.Column(db.String(50), nullable=False)
    text = db.Column(db.Text, nullable=False)
    primary_emotion = db.Column(db.String(50))
    secondary_emotion = db.Column(db.String(50))
    suggestion = db.Column(db.Text)

    def to_dict(self):
        return {
            'date': self.date.strftime("%Y-%m-%d"),
            'title': self.title,
            'reason': self.reason,
            'text': self.text,
            'primary_emotion': self.primary_emotion,
            'secondary_emotion': self.secondary_emotion,
            'suggestion': self.suggestion
        }

# Load Emotion Detection Model (RoBERTa-base-Go-Emotions)
emotion_pipeline = pipeline("text-classification", model="SamLowe/roberta-base-go_emotions", top_k=2)

# Load Curated Suggestions
with open("suggestions.json", "r") as file:
    SUGGESTIONS = json.load(file)

def get_dynamic_suggestion(primary_emotion, secondary_emotion, text):
    """Generate a meaningful suggestion from JSON with a dynamic touch."""
    primary = primary_emotion.lower()
    secondary = secondary_emotion.lower()

    # Fetch relevant suggestions or use a fallback message
    primary_suggestions = SUGGESTIONS.get(primary, [{"text": "Take a deep breath and reflect."}])
    secondary_suggestions = SUGGESTIONS.get(secondary, [{"text": "Stay mindful of your emotions."}])

    # Pick random suggestion from both emotions
    chosen_primary = random.choice(primary_suggestions)["text"]
    chosen_secondary = random.choice(secondary_suggestions)["text"]

    # Add shorter customization based on user input
    # Truncate the text if it's too long
    preview_text = text[:30] + "..." if len(text) > 30 else text
    dynamic_part = f" Consider how this relates to your current feelings."

    return f"{chosen_primary} {chosen_secondary}{dynamic_part}"

@app.route('/', methods=["GET", "POST"])
def home():
    if request.method == "POST":
        text = request.form["journal_text"]
        title = request.form["title"]
        reason = request.form["reason"]
        date = datetime.date.today()
        
        # Analyze emotions for the journal entry
        emotion_results = emotion_pipeline(text)[0]
        primary_emotion = emotion_results[0]['label']
        secondary_emotion = emotion_results[1]['label']
        suggestion = get_dynamic_suggestion(primary_emotion, secondary_emotion, text)
        
        # Create and save new journal entry
        entry = JournalEntry(
            date=date,
            title=title,
            reason=reason,
            text=text,
            primary_emotion=primary_emotion,
            secondary_emotion=secondary_emotion,
            suggestion=suggestion
        )
        db.session.add(entry)
        db.session.commit()
        
        # Return JSON response for AJAX requests
        if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
            return jsonify({
                "primary_emotion": primary_emotion,
                "secondary_emotion": secondary_emotion,
                "suggestion": suggestion
            })
            
        return redirect(url_for("calendar"))
        
    return render_template("index.html")

@app.route('/calendar')
def calendar():
    entries = JournalEntry.query.order_by(JournalEntry.date.desc()).all()
    return render_template("calendar.html", entries=entries)

@app.route('/analyze', methods=['POST'])
def analyze_sentiment():
    data = request.get_json()
    text = data.get("text", "")

    if not text:
        return jsonify({"error": "No text provided"}), 400

    try:
        # Detect emotions
        emotion_results = emotion_pipeline(text)[0]  # Get first item since pipeline returns list of dicts
        print("🚀 Raw Emotion Results:", emotion_results)  # Debugging Output

        # Extract top 2 emotions from the results
        primary_emotion = emotion_results[0]['label']
        secondary_emotion = emotion_results[1]['label']

        # Get dynamic suggestion
        suggestion = get_dynamic_suggestion(primary_emotion, secondary_emotion, text)

        return jsonify({
            "text": text,
            "primary_emotion": primary_emotion,
            "secondary_emotion": secondary_emotion,
            "suggestion": suggestion
        })
    
    except Exception as e:
        print("❌ Error:", str(e))  # Debugging Output
        return jsonify({"error": str(e)}), 500

def init_db():
    with app.app_context():
        # Create all tables
        db.create_all()
        print("Database initialized successfully!")

if __name__ == '__main__':
    init_db()  # Initialize database before running the app
    app.run(debug=True)
