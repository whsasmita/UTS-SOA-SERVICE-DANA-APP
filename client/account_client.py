import sys
import os

# Add parent directory to path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from utils.soap import get_soap_client, call_soap_method

# URL WSDL dari Account Service
WSDL_URL = "http://localhost:8001?wsdl"

def handle_login(username, password):
    """Mengirim permintaan login ke Account Service."""
    client = get_soap_client(WSDL_URL)
    if not client:
        print("❌ Koneksi gagal ke Account Service.")
        return None
        
    status, result = call_soap_method(client, "login_user", username=username, password=password)
    if status == "success" and str(result).lower().startswith("success"):
        print(f"✅ {result}")
        return result
    else:
        print(f"❌ Login gagal: {result}")
        return None

def handle_register(username, password):
    """Mengirim permintaan registrasi ke Account Service (rekening auto-generate di server)."""
    client = get_soap_client(WSDL_URL)
    if not client:
        print("❌ Koneksi gagal ke Account Service.")
        return None
    
    status, result = call_soap_method(client, "register_user", username=username, password=password)
    if status == "success" and str(result).lower().startswith("success"):
        print(f"✅ {result}")
        return result
    else:
        print(f"❌ Registrasi gagal: {result}")
        return None

def handle_get_account_info(account_number):
    """Ambil info rekening dari Account Service."""
    client = get_soap_client(WSDL_URL)
    if not client:
        print("❌ Koneksi gagal ke Account Service.")
        return None
    status, result = call_soap_method(client, "get_account_info", account_number=account_number)
    if status == "success" and str(result).lower().startswith("success"):
        print(f"✅ {result}")
        return result
    else:
        print(f"❌ Gagal mengambil info rekening: {result}")
        return None

if __name__ == "__main__":
    # Quick test manual
    print("Testing Account Client...")
    r = handle_register("tester_cli", "pass123")
    r = handle_login("tester_cli", "pass123")
    if r:
        # coba parse rekening dari hasil login
        try:
            acc = str(r).split("Rekening:")[-1].split(",")[0].strip()
            handle_get_account_info(acc)
        except Exception:
            pass