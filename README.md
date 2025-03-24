
# 🌙 MoodMirror - AI-Powered Emotional Journal

<div align="center">
  <img src="/static/logo1.png" alt="MoodMirror Banner" width="600"/>
</div>

## 📖 About

This is our MINIPROJECT for 6th semester.
MoodMirror is an AI-powered journaling application that helps users understand and track their emotions. Using the RoBERTa model for emotion detection and Mistral AI for chatbot interactions, it provides comprehensive emotional analysis and support.

## ✨ Features

- **🤖 AI Emotion Analysis**: Real-time emotion detection using RoBERTa-base-Go-Emotions model
- **📝 Smart Journaling**: Categorized journal entries with emotion tracking
- **💡 Personalized Suggestions**: Dynamic suggestions based on primary and secondary emotions
- **🎵 Media Integration**: Curated playlists and videos based on emotional state
- **📊 Visual Analytics**: Comprehensive charts showing emotion distribution and patterns
- **🤖 AI Therapist**: Mistral AI-powered chatbot for emotional support
- **📈 Score Tracking**: Dynamic emotional score system based on journal entries
- **🎨 Modern UI**: Responsive design with fixed navigation and full-screen sections

## 🚀 Getting Started

### Prerequisites

- Python 3.8+
- pip package manager
- SQLite3
- Mistral AI API key

### Installation

1. **Clone the repository**
```bash
git clone https://github.com/yadhu7050/mood-mirror.git
cd MoodMirror
```

2. **Create and activate virtual environment**
```bash
python -m venv venv
# On Windows
venv\Scripts\activate
```

3. **Install dependencies**
```bash
pip install -r requirements.txt
```

4. **Set up environment variables**
Create a `.env` file in the root directory and add:
```
MISTRAL_API_KEY=your_api_key_here
```

5. **Initialize the database**
```python
from app import app, db
with app.app_context():
    db.create_all()
```

6. **Run the application**
```bash
python app.py
```

## 💾 Database Schema

### User Model
```python
class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(200), nullable=False)
    name = db.Column(db.String(100))
    date_of_birth = db.Column(db.String(10))
    emotional_score = db.Column(db.Integer, default=50)
    journals = db.relationship('Journal', backref='author', lazy=True)
```

### Journal Model
```python
class Journal(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    title = db.Column(db.String(200), nullable=False)
    text = db.Column(db.Text, nullable=False)
    reason = db.Column(db.String(100))
    date = db.Column(db.DateTime, default=datetime.utcnow)
    primary_emotion = db.Column(db.String(50))
    primary_emotion_percentage = db.Column(db.Float)
    secondary_emotion = db.Column(db.String(50))
    secondary_emotion_percentage = db.Column(db.Float)
```

## 📦 Dependencies

```txt
Flask==2.0.1
Flask-SQLAlchemy==2.5.1
Flask-Login==0.5.0
Werkzeug==2.0.1
transformers==4.11.3
requests==2.31.0
python-dotenv==0.19.0
torch==1.9.0
```

## 👥 Authors

- **Yadhu Krishnan V A** - [yadhu7050](https://github.com/yadhu7050)
- **Dhanalakshmi K B** - [Dhanalakshmi-lab-stack](https://github.com/Dhanalakshmi-lab-stack)
- **Sidharth P Krishnan** - [Sidharthpkrishnan](https://github.com/Sidharthpkrishnan)
- **Sreelakshmi A V** - [sreelxmi](https://github.com/sreelxmi)

## 📧 Contact

Yadhu Krishnan - yadhukrishnan7050@gmail.com

Project Link: [https://github.com/yadhu7050/mood-mirror](https://github.com/yadhu7050/mood-mirror)

---

<div align="center">
  Made with ❤️ by<br>
  Yadhu Krishnan V A<br>
  Sidharth P Krishnan<br>
  Sreelakshmi A V<br>
  Dhanalakshmi K B
</div>
