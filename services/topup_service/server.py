import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

from spyne import Application, rpc, ServiceBase, Unicode
from spyne.protocol.soap import Soap11
from spyne.server.wsgi import WsgiApplication
from wsgiref.simple_server import make_server

from services.account_service.account import register, login, get_account_info
from utils.jwt_helper import generate_jwt_token, validate_jwt_token

class AccountService(ServiceBase):
    @rpc(Unicode, Unicode, _returns=Unicode)
    def login_user(ctx, username, password):
        """Login dan return JWT token."""
        result = login(username, password)
        if result.startswith("success:"):
            # Extract account number dari result
            try:
                account_number = result.split("Rekening:")[1].split(",")[0].strip()
                # Generate JWT token
                token = generate_jwt_token(username, account_number)
                return f"success: Login berhasil. Token: {token}"
            except Exception as e:
                return f"error: Gagal generate token. {e}"
        return result

    @rpc(Unicode, Unicode, _returns=Unicode)
    def register_user(ctx, username, password):
        """Register dan return JWT token."""
        result = register(username, password)
        if result.startswith("success:"):
            try:
                account_number = result.split("Nomor rekening:")[1].strip()
                # Generate JWT token
                token = generate_jwt_token(username, account_number)
                return f"success: Registrasi berhasil. Nomor rekening: {account_number}. Token: {token}"
            except Exception as e:
                return f"error: Gagal generate token. {e}"
        return result

    @rpc(Unicode, Unicode, _returns=Unicode)
    def get_account_info(ctx, token, account_number):
        """Get account info dengan JWT validation."""
        valid, payload = validate_jwt_token(token)
        if not valid:
            return f"error: {payload}"
        
        # Pastikan token sesuai dengan account yang diminta
        if payload['account_number'] != account_number:
            return "error: Unauthorized access"
            
        return get_account_info(account_number)

    @rpc(Unicode, _returns=Unicode)
    def validate_token(ctx, token):
        """Endpoint untuk validasi token."""
        valid, result = validate_jwt_token(token)
        if valid:
            return f"success: Token valid. User: {result['username']}, Account: {result['account_number']}"
        return f"error: {result}"

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