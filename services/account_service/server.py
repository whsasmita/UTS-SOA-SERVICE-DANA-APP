import sys
import os

# Tambahkan root project ke sys.path
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

from spyne import Application, rpc, ServiceBase, Unicode
from spyne.protocol.soap import Soap11
from spyne.server.wsgi import WsgiApplication
from wsgiref.simple_server import make_server

from services.account_service.account import register, login, get_account_info

class AccountService(ServiceBase):
    @rpc(Unicode, Unicode, _returns=Unicode)
    def login_user(ctx, username, password):
        return login(username, password)

    @rpc(Unicode, Unicode, _returns=Unicode)
    def register_user(ctx, username, password):
        return register(username, password)

    @rpc(Unicode, _returns=Unicode)
    def get_account_info(ctx, account_number):
        return get_account_info(account_number)

application = Application(
    [AccountService],
    'dana.soap',
    in_protocol=Soap11(validator='lxml'),
    out_protocol=Soap11()
)

wsgi_app = WsgiApplication(application)

if __name__ == '__main__':
    server = make_server('0.0.0.0', 8001, wsgi_app)
    print("Account Service berjalan di http://localhost:8001")
    print("WSDL: http://localhost:8001?wsdl")
    server.serve_forever()