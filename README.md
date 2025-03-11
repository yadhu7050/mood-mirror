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
# On macOS/Linux
source venv/bin/activate
```

3. **Install dependencies**
```bash
pip install flask
pip install flask-sqlalchemy
pip install flask-login
pip install transformers
pip install torch
```

4. **Set up the project structure**
```
MoodMirror/
├── app.py
├── suggestions.json
├── requirements.txt
├── README.md
├── instance/
│   └── data.db
├── static/
│   ├── homestyles.css
│   ├── login.css
│   ├── signup.css
│   ├── styles.css
│   ├── login.js
│   ├── script.js
│   ├── signupquiz.js
│   └── solid-navy-blue-concrete-textured-wall.jpg
└── templates/
    ├── home.html
    ├── login.html
    ├── signup.html
    ├── signupquiz.html
    ├── journal.html
    └── history.html
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

7. **Access the application**
Open your browser and navigate to `http://localhost:5000`

### Environment Variables Required

```bash
MISTRAL_API_KEY=your_api_key_here
```

## 💾 Database Schema

### User Model
```python
class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(200), nullable=False)
    name = db.Column(db.String(100))
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
    mood = db.Column(db.String(50))
    primary_emotion = db.Column(db.String(50))
    primary_emotion_percentage = db.Column(db.Float)
    secondary_emotion = db.Column(db.String(50))
    secondary_emotion_percentage = db.Column(db.Float)
```

## 🔄 Routes

| Method | Route | Description | Authentication Required |
|--------|-------|-------------|----------------------|
| GET/POST | / | Home page | No |
| GET/POST | /login | User login | No |
| GET/POST | /signup | User registration | No |
| GET/POST | /signup_quiz | Initial emotional assessment | Yes |
| GET/POST | /journal | Create and analyze journal entries | Yes |
| GET | /history | View journal history | Yes |
| GET | /analysis | View emotional analytics | Yes |
| GET/POST | /chatbot | AI Therapist interaction | Yes |
| GET | /logout | User logout | Yes |
| POST | /reset-password | Password reset functionality | No |

## 🎨 Features in Detail

### Emotion Analysis System
- Primary and secondary emotion detection
- Percentage-based emotion confidence scores
- Dynamic suggestion generation based on emotional context
- Integration with media recommendations

### AI Chatbot Integration
- Powered by Mistral AI API
- Context-aware responses using journal history
- Focused on emotional support and guidance
- Configurable response parameters

### Analytics Dashboard
- Emotion distribution pie chart
- Emotional score timeline
- Reasons distribution doughnut chart
- Most common emotions bar chart
- Interactive and responsive visualizations

### Security Features
- Secure password hashing
- Session management
- Password reset functionality
- Protected routes with login_required

## 📦 Dependencies

```txt
Flask==2.0.1
Flask-SQLAlchemy==2.5.1
Flask-Login==0.5.0
Flask-Mail==0.9.1
Werkzeug==2.0.1
transformers==4.11.3
requests==2.31.0
itsdangerous==2.0.1
```

## 🤝 Contributing

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## 🐛 Bug Reports

Report bugs by opening a new issue. Include:
- Detailed description of the bug
- Steps to reproduce
- Expected behavior
- Screenshots if applicable

## 🚀 Future Enhancements

- [ ] Enhanced email notification system
- [ ] Multiple language support for emotion analysis
- [ ] Advanced chatbot conversation memory
- [ ] Custom suggestion templates
- [ ] Mobile application
- [ ] User preference settings
- [ ] Journal entry search and filtering
- [ ] Export functionality for analytics

## 👥 Authors

- **Yadhu Krishnan V A** - [yadhu7050](https://github.com/yadhu7050)
- **Dhanalakshmi K B** - [Dhanalakshmi-lab-stack](https://github.com/Dhanalakshmi-lab-stack)
- **Sidharth P Krishnan** - [Sidharthpkrishnan](https://github.com/Sidharthpkrishnan)
- **Sreelakshmi A V** - [sreelxmi](https://github.com/sreelxmi)

## 🙏 Acknowledgments

- RoBERTa model by SamLowe
- Flask framework community
- SQLAlchemy team
- Freepik for the background image
- All contributors and users

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
