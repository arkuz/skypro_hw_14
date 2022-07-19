import logging
from flask import Flask

from netflix.views import netflix_blueprint

logging.basicConfig(filename="log.log",
                    level=logging.INFO,
                    format='%(asctime)s - [%(levelname)s] - %(name)s -'
                           ' (%(filename)s).%(funcName)s(%(lineno)d) - %(message)s')
logger = logging.getLogger(__name__)

app = Flask(__name__)
app.config['JSON_AS_ASCII'] = False

app.register_blueprint(netflix_blueprint)

if __name__ == '__main__':
    app.run()
