# encoding=utf-8
import os.path
import tornado.httpserver
import tornado.ioloop
import tornado.web
import tornado.gen
import tornado.options
from tornado.options import define, options

from models import ApnProxyConfig

define('address', default='127.0.0.1', help='bind on specific address', type=str)
define('debug', default=False, help='run in debug mode', type=bool)
define('port', default=8000, help='run on the given port', type=int)


class BaseHandler(tornado.web.RequestHandler):
    pass


class IndexHandler(BaseHandler):
    def get(self, *args, **kwargs):
        self.render('index.html')


class ApnHandler(BaseHandler):
    def get(self, *args, **kwargs):
        self.redirect('/')

    def post(self, *args, **kwargs):
        proxy_ip = self.get_body_argument('proxy_ip')
        port = self.get_body_argument('port')
        name = self.get_body_argument('name', default='Apn Proxy Config')
        username = self.get_body_argument('username', default=None)
        password = self.get_body_argument('password', default=None)
        apn = ApnProxyConfig(proxy_ip, port, name=name, username=username, password=password)
        self.set_header('Content-Disposition', 'attachment; filename="CustomProxy.mobileconfig"')
        self.set_header('Content-Type', 'application/x-apple-aspen-config')
        self.render('mobileconfig/apn_config.plist', apn=apn)


class Application(tornado.web.Application):
    def __init__(self, debug=True):
        handlers = [
            ('/', IndexHandler),
            ('/apn', ApnHandler),
        ]
        settings = {
            'template_path': os.path.join(os.path.dirname(__file__), 'templates'),
            'static_path': os.path.join(os.path.dirname(__file__), 'static'),
            'debug': debug
        }
        super(Application, self).__init__(handlers, **settings)


def main():
    tornado.options.parse_command_line()
    http_server = tornado.httpserver.HTTPServer(Application(debug=options.debug))
    http_server.listen(options.port, address=options.address)
    tornado.ioloop.IOLoop.instance().start()


if __name__ == '__main__':
    main()