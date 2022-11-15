from flask import Flask
import os

def create_app():
  app = Flask(__name__)
  app.config['SECRET_KEY'] = 'qwerty'
  
  from .views import views
  
  app.register_blueprint(views, url_prefix='/')
  
  ALLOWED_EXTENSIONS = {'pdf'}
  app.config['ALLOWED_EXTENSIONS'] = ALLOWED_EXTENSIONS
  os.makedirs(os.path.join(app.instance_path), exist_ok=True)
  
  return app