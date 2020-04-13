from instantApp import create_app
from instantApp.extensions import socketio
from dotenv import load_dotenv

load_dotenv('.flaskenv')

if __name__ == '__main__':
    app = create_app('development')
    # socketio.run(app)
    app.run()
