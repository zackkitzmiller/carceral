import json
import logging
import os
import random
import re
import sys

from tornado.log import enable_pretty_logging
import tornado.httpserver
import tornado.ioloop
import tornado.web

logging.basicConfig(stream=sys.stdout, level=logging.DEBUG)
logger = logging.getLogger(__name__)


def slugify(text, separator="-"):
    ret = text
    ret = re.sub("([a-zA-Z])(uml|acute|grave|circ|tilde|cedil)", r"\1", ret)
    ret = re.sub("\W", " ", ret)
    ret = ret.strip()
    ret = re.sub(" +", separator, ret)
    return ret.strip()


fileDir = os.path.dirname(os.path.realpath('__file__'))
filename = os.path.join(fileDir, 'dat/words')
filename = os.path.abspath(os.path.realpath(filename))
LINES = open(filename).read().splitlines()


def get_service_name():
    return random.choice(LINES).lower()


def build_word(word):
    return {
        'name': word,
        'meta': {
            'url': 'https://www.merriam-webster.com/dictionary/{0}'.format(word)
        }
    }


class CarceralHandler(tornado.web.RequestHandler):

    def get(self):
        query = self.get_argument('q', None)
        num_suggestions = int(self.get_argument('n', 3))
        suggestions = {
            'recommended': []
        }

        for n in xrange(0, num_suggestions):
            suggestions['recommended'].append(build_word(get_service_name()))

        if query is not None:
            suggestions['not_recommended'] = []
            suggestions['not_recommended'].append(
                {
                    'name': slugify(query),
                    'meta': {}
                }
            )

        resp = {
            'suggestions': suggestions
        }

        self.set_header("Content-Type", "application/json")
        self.finish(json.dumps(resp))


def main():
    application = tornado.web.Application([
        (r"/", CarceralHandler),
    ], debug=True)
    http_server = tornado.httpserver.HTTPServer(application)
    port = int(os.environ.get("PORT", 5000))
    http_server.listen(port)
    logger.info('this bitch is fired up')
    enable_pretty_logging()
    tornado.ioloop.IOLoop.instance().start()


if __name__ == "__main__":
    main()
