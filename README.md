# 🌙 MoodMirror - AI-Powered Emotional Journal

<div align="center">
  <img src="https://miro.medium.com/v2/resize:fit:1200/0*oWRpwhaPxCJR-tGU.png" alt="MoodMirror Banner" width="600"/>
</div>

## 📖 About

This is our MINIPROJECT for 6th semester.
MoodMirror is an AI-powered journaling application that helps users understand and track their emotions. Using the RoBERTa model for emotion detection, it analyzes journal entries in real-time, providing emotional insights and personalized suggestions including music and video recommendations.

## ✨ Features

- **🤖 AI Emotion Analysis**: Real-time emotion detection using RoBERTa-base-Go-Emotions model
- **📝 Smart Journaling**: Categorized journal entries with emotion tracking
- **💡 Personalized Suggestions**: Get custom recommendations based on detected emotions
- **🎵 Media Integration**: Curated Spotify playlists and YouTube videos for emotional support
- **📊 Emotional Score Tracking**: Initial quiz to establish baseline emotional state
- **🎨 Modern UI**: Responsive design with glassmorphism effects and smooth animations

## 🚀 Getting Started

### Prerequisites

- Python 3.8+
- pip package manager
- SQLite3
- Modern web browser

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
```

## 🔄 Routes

| Method | Route         | Description                         | Authentication Required |
|--------|--------------|-------------------------------------|----------------------|
| GET    | /            | Home page                           | No                   |
| GET    | /start       | Login page                          | No                   |
| POST   | /login       | User login                          | Yes                   |
| POST   | /signup      | User registration                   | Yes                   |
| GET/POST| /signup_quiz | Emotional baseline quiz             | Yes                  |
| GET/POST| /journal     | Journal entry creation              | Yes                  |
| GET    | /history     | View past journal entries           | Yes                  |
| GET    | /logout      | User logout                         | Yes                  |

## 🎨 Features in Detail

### Authentication System
- User registration with email and password
- Secure password hashing using Werkzeug
- Session management with Flask-Login
- Custom signup quiz for emotional baseline

### Journal System
- Rich text entry support
- Category selection (Work, Relationship, Home, Health, Other)
- Real-time emotion analysis
- Personalized suggestions based on emotions
- Media recommendations (Spotify & YouTube)

### Emotion Analysis
- Uses RoBERTa model for accurate emotion detection
- Detects primary and secondary emotions
- Provides emotion confidence percentages
- Generates contextual suggestions

### UI Features
- Responsive design for all devices
- Interactive animations
- Modern glassmorphism effects
- Dynamic form transitions
- Real-time feedback

## 📦 Dependencies

```txt
Flask==2.0.1
Flask-SQLAlchemy==2.5.1
Flask-Login==0.5.0
Werkzeug==2.0.1
transformers==4.11.3
torch==1.9.0
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

- [ ] Export functionality for journal entries
- [ ] Advanced analytics dashboard
- [ ] Mobile application
- [ ] Multiple language support
- [ ] Custom suggestion templates
- [ ] API integration options


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
  Made with ❤️ by
  Yadhu Krishnan V A
  Sidharth P Krishnan
  Sreelakshmi A V
  Dhanalakshmi K B
</div>
