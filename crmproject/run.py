from app import create_app

app = create_app()

if __name__ == '__main__':
    with app.app_context():
        from app.extensions import db
        db.create_all()  # Create tables if they don't exist
    app.run(debug=True)