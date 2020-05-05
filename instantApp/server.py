from instantApp import create_app
from dotenv import load_dotenv

load_dotenv('.flaskenv')

if __name__ == '__main__':
    app = create_app('development')
    app.run(host='0.0.0.0', port=5000, debug=True)
