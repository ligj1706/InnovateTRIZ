# Vercel entry point
from triz_web_app.backend.app import app

# This is the WSGI application that Vercel will use
application = app

if __name__ == "__main__":
    app.run()