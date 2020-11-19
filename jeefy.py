import os
import click
from app import create_app


config_name = 'mk'
app = create_app(config_name)

if __name__ == '__main__':
    try:
        app.run(host='0.0.0.0', port=80, debug=0)
    except:
        app.run(host='0.0.0.0', port=5000, debug=0)
