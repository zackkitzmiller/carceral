import logging
import os
import sys

from tornado.log import enable_pretty_logging
import tornado.httpserver
import tornado.ioloop
import tornado.web
from tornado_swagger import swagger

from carceral.handlers import CarceralHandler

logging.basicConfig(stream=sys.stdout, level=logging.DEBUG)
logger = logging.getLogger(__name__)

swagger.docs()


def run_server():
    enable_pretty_logging()

    application = swagger.Application([
        (r"/", CarceralHandler),
    ], debug=os.environ.get('DEBUG', False))

    http_server = tornado.httpserver.HTTPServer(application)
    port = int(os.environ.get("PORT", 5000))
    http_server.listen(port)

    logger.info("we're up and running on port {0}".format(port))
    tornado.ioloop.IOLoop.instance().start()


if __name__ == "__main__":
    run_server()
