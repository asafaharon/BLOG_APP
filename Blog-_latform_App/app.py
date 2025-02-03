from app import app, db  # ייבוא של app ו-db מהמודול app
from app.models import User, Post, Comment

# יצירת הטבלאות בתוך הקשר האפליקציה
with app.app_context():
    db.create_all()
    print("Tables created successfully!")

if __name__ == '__main__':
    app.run(debug=True, port=8080)
