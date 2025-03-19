# alleen nodig als je gunicorn zou draaien.
# en om de pipeline te triggeren...!
from frontend.app import app

if __name__ == "__main__":
    app.run()
# gunicorn --bind 0.0.0.0:5001 wsgi:app
