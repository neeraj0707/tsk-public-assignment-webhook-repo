# from flask import Flask

# from app.webhook.routes import webhook


# # Creating our flask app
# def create_app():

#     app = Flask(__name__)
    
#     # registering all the blueprints
#     app.register_blueprint(webhook)
    
#     return app



# from flask import Flask, render_template
# from app.webhook.routes import webhook
# from app.extensions import mongo


# def create_app():
#     app = Flask(__name__)
#     # app.config["MONGO_URI"] = "mongodb://localhost:27017/github_webhook_db"
#     app.config["MONGO_URI"] = "mongodb+srv://neeraj0707:Neeraj%405005@cluster0.pcmvdtq.mongodb.net/github_webhook_db?retryWrites=true&w=majority&appName=Cluster0"

#     mongo.init_app(app)

#     # Register your blueprint
#     app.register_blueprint(webhook)

#     # ✅ Add home route correctly (no indentation error)
#     @app.route("/")
#     def home():
#         print(f"Template folder: {app.template_folder}")
#         # return "Flask Webhook Receiver is Running!"
#         return render_template("index.html")
        

#     return app





from flask import Flask, render_template
from app.webhook.routes import webhook
from app.extensions import mongo
import os

def create_app():
    # Explicitly tell Flask where the templates folder is
    app = Flask(__name__, template_folder=os.path.join(os.getcwd(), 'templates'))
    app.config["MONGO_URI"] = "mongodb+srv://neeraj0707:Neeraj%405005@cluster0.pcmvdtq.mongodb.net/github_webhook_db?retryWrites=true&w=majority&appName=Cluster0"

    mongo.init_app(app)
    app.register_blueprint(webhook)

    @app.route("/")
    def home():
        print(f"Template folder: {app.template_folder}")
        return render_template("index.html")

    return app
