# encoding=utf-8
import os.path
import tornado.httpserver
import tornado.ioloop
import tornado.web
import tornado.gen
import tornado.options
from tornado.options import define, options

from models import ApnProxyConfig
from db import RedisDB

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
        try:
            print self.application.db.save_profile(apn)
        except Exception, e:
            raise e
        self.set_header('Content-Disposition', 'attachment; filename="ApnProxy.mobileconfig"')
        self.set_header('Content-Type', 'application/x-apple-aspen-config')
        self.render('mobileconfig/apn_profile.plist', apn=apn)


class ShareHandler(BaseHandler):
    def set_default_headers(self):
        self.set_header('Content-Disposition', 'attachment; filename="ApnProxy.mobileconfig"')
        self.set_header('Content-Type', 'application/x-apple-aspen-config')

    def match_profile(self, code):
        apn = self.application.db.get_profile(code)
        return apn

    def post(self, *args, **kwargs):
        code = self.get_body_argument('code')
        apn = self.match_profile(code)
        self.render('mobileconfig/apn_profile.plist', apn=apn)

    def get(self, code):
        if code == '':
            self.redirect('/')
        apn = self.match_profile(code)
        self.render('mobileconfig/apn_profile.plist', apn=apn)


class Application(tornado.web.Application):
    def __init__(self, debug=True):
        handlers = [
            ('/', IndexHandler),
            ('/apn', ApnHandler),
            ('/share/(.*)', ShareHandler),
        ]
        settings = {
            'template_path': os.path.join(os.path.dirname(__file__), 'templates'),
            'static_path': os.path.join(os.path.dirname(__file__), 'static'),
            'debug': debug
        }
        self.db = RedisDB()
        super(Application, self).__init__(handlers, **settings)


def main():
    tornado.options.parse_command_line()
    http_server = tornado.httpserver.HTTPServer(Application(debug=options.debug))
    http_server.listen(options.port, address=options.address)
    tornado.ioloop.IOLoop.instance().start()


if __name__ == '__main__':
    main()