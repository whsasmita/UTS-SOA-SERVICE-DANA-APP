import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

from spyne import Application, rpc, ServiceBase, Unicode
from spyne.protocol.soap import Soap11
from spyne.server.wsgi import WsgiApplication
from wsgiref.simple_server import make_server

from services.transaction_service.transaction import transfer_dana
from utils.jwt_helper import validate_jwt_token

class TransactionService(ServiceBase):
    @rpc(Unicode, Unicode, Unicode, Unicode, _returns=Unicode)
    def transfer(ctx, token, sender_account_number, receiver_account_number, amount):
        """Endpoint untuk transfer dengan JWT validation."""
        # Validasi JWT token
        valid, payload = validate_jwt_token(token)
        if not valid:
            return f"error: {payload}"
        
        # Pastikan token sesuai dengan sender account
        if payload['account_number'] != sender_account_number:
            return "error: Unauthorized access - Token tidak sesuai dengan rekening pengirim"
            
        return transfer_dana(sender_account_number, receiver_account_number, amount)

application = Application(
    [TransactionService],
    'dana.soap',
    in_protocol=Soap11(validator='lxml'),
    out_protocol=Soap11()
)

wsgi_app = WsgiApplication(application)

if __name__ == '__main__':
    server = make_server('0.0.0.0', 8003, wsgi_app)
    print("Transaction Service berjalan di http://localhost:8003")
    print("WSDL: http://localhost:8003?wsdl")
    server.serve_forever()