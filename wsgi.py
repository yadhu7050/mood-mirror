from app import app,init_database

if __name__ == "__main__":
    init_database()
    app.run(host="0.0.0.0", port=5000)
