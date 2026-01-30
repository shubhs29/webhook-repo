from flask import Flask, render_template
import os

def create_app():
    # Point to templates folder at project root
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    template_folder = os.path.join(base_dir, 'templates')
    static_folder = os.path.join(base_dir, 'static')
    
    app = Flask(__name__, 
                template_folder=template_folder,
                static_folder=static_folder)
    
    # Register webhook blueprint
    from app.webhook.routes import webhook
    app.register_blueprint(webhook)
    
    # Main UI route at root
    @app.route('/')
    def index():
        """Serve the UI"""
        return render_template('index.html')
    
    return app