from app import create_app

from app.webhook.extensions import COLLECTION_NAME, DATABASE_NAME
app = create_app()





if __name__ == '__main__':
    print("🚀 Starting GitHub Webhook Monitor...")
    print(f"📊 MongoDB: {DATABASE_NAME}.{COLLECTION_NAME}")
    print(f"🌐 Server running on http://localhost:5000")
    app.run(debug=True, host='0.0.0.0', port=5000)
