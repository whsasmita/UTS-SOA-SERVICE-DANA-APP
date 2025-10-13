import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from utils.soap import get_soap_client, call_soap_method

# URL WSDL dari Transaction Service
WSDL_URL = "http://localhost:8003?wsdl"

def handle_transfer(sender_account, receiver_account, amount):
    """Mengirim permintaan transfer ke Transaction Service."""
    print(f"Menghubungi Transaction Service di {WSDL_URL}")
    
    client = get_soap_client(WSDL_URL)
    if not client:
        print("❌ Koneksi gagal ke Transaction Service.")
        return
        
    status, result = call_soap_method(client, "transfer", 
                                    sender_account_number=sender_account, 
                                    receiver_account_number=receiver_account, 
                                    amount=amount)
    
    if status == "success":
        print(f"✅ Transfer berhasil: {result}")
    else:
        print(f"❌ Transfer gagal: {result}")

if __name__ == "__main__":
    # Test transfer
    handle_transfer("1001", "1002", "50000")