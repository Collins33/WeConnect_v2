import os

from app import create_app

# first get config name
config_name = os.getenv('APP_SETTINGS')

app = create_app(config_name)

if __name__ == "__main__":
    app.run()