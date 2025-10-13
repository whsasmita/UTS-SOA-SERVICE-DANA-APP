import sys
import os

# Add parent directory to path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from utils.soap import get_soap_client, call_soap_method

# WSDL Topup Service
WSDL_URL = "http://localhost:8002?wsdl"

def handle_topup(account_number, amount):
    """Mengirim permintaan topup ke Topup Service."""
    client = get_soap_client(WSDL_URL)
    if not client:
        print("❌ Koneksi gagal ke Topup Service.")
        return None

    status, result = call_soap_method(
        client,
        "topup",
        account_number=account_number,
        amount=str(amount)
    )

    if status == "success" and str(result).lower().startswith("success"):
        print(f"✅ {result}")
        return result
    else:
        print(f"❌ Topup gagal: {result}")
        return None

if __name__ == "__main__":
    # Quick test manual
    acc = input("Masukkan nomor rekening: ").strip()
    amt = input("Masukkan jumlah topup: ").strip()
    handle_topup(acc, amt)