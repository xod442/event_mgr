from flask import Flask
from flask.ext.mongoengine import MongoEngine

db = MongoEngine()

def create_app(**config_overrides):
    app = Flask(__name__)
    app.config.from_pyfile('settings.py')
    
    app.config.update(config_overrides)
    
    db.init_app(app)
    
    from user.views import user_app
    app.register_blueprint(user_app)
    
    from relationship.views import relationship_app
    app.register_blueprint(relationship_app)
    
    from feed.views import feed_app
    app.register_blueprint(feed_app)
    
    from home.views import home_app
    app.register_blueprint(home_app)
    
    return app