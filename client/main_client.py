import sys
import os

# Add parent directory to path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from client.account_client import handle_login, handle_register, handle_get_account_info
from client.topup_client import handle_topup
from client.transaction_client import handle_transfer

# Session user
current_user = {
    'username': None,
    'account_number': None,
    'logged_in': False
}

def display_main_menu():
    """Menu awal sebelum login/register."""
    print("\n===============================")
    print("      DANA SERVICE CLIENT      ")
    print("===============================")
    print("1. Login Akun")
    print("2. Register Akun")
    print("3. Keluar")
    print("===============================")

def display_user_menu():
    """Menu setelah login/register."""
    print(f"\n===============================")
    print(f"   Selamat datang, {current_user['username']}!")
    print(f"   Rekening: {current_user['account_number']}")
    print("===============================")
    print("1. Cek Saldo & Info Rekening")
    print("2. Top Up Saldo")
    print("3. Transfer Dana")
    print("4. Logout")
    print("===============================")

def parse_account_from_register(msg: str):
    """Ambil nomor rekening dari pesan register."""
    try:
        return msg.split("Nomor rekening:")[-1].strip()
    except Exception:
        return None

def parse_account_from_login(msg: str):
    """Ambil nomor rekening dari pesan login."""
    try:
        return msg.split("Rekening:")[-1].split(",")[0].strip()
    except Exception:
        return None

def handle_register_flow():
    print("\n--- REGISTER AKUN ---")
    username = input("Masukkan username: ").strip()
    password = input("Masukkan password: ").strip()

    result = handle_register(username, password)
    if result and str(result).lower().startswith("success"):
        acc = parse_account_from_register(str(result))
        if not acc:
            print("⚠️ Tidak bisa mengambil nomor rekening dari response, silakan cek di menu 'Cek Saldo'.")
        current_user['username'] = username
        current_user['account_number'] = acc
        current_user['logged_in'] = True
        print("✅ Registrasi & login berhasil.")
        return True
    print("❌ Registrasi gagal.")
    return False

def handle_login_flow():
    print("\n--- LOGIN AKUN ---")
    username = input("Masukkan username: ").strip()
    password = input("Masukkan password: ").strip()

    result = handle_login(username, password)
    if result and str(result).lower().startswith("success"):
        acc = parse_account_from_login(str(result))
        if not acc:
            print("⚠️ Tidak bisa mengambil nomor rekening dari response, Anda akan diminta memasukkan rekening.")
            acc = input("Masukkan nomor rekening Anda: ").strip()
        current_user['username'] = username
        current_user['account_number'] = acc
        current_user['logged_in'] = True
        print("✅ Login berhasil.")
        return True
    print("❌ Login gagal.")
    return False

def handle_check_balance():
    """Menampilkan info rekening dari service."""
    print(f"\n--- INFO REKENING ---")
    print(f"👤 Username: {current_user['username']}")
    print(f"📋 Nomor Rekening: {current_user['account_number']}")
    resp = handle_get_account_info(current_user['account_number'])
    if not resp:
        input("\nTekan Enter untuk kembali ke menu...")
        return
    try:
        data_part = str(resp).split("success:")[-1].strip()
        kv = {}
        for part in data_part.split(","):
            if "=" in part:
                k, v = part.strip().split("=", 1)
                kv[k.strip()] = v.strip()
        saldo = float(kv.get('balance', '0'))
        created = kv.get('created_at', '-')
        print(f"💰 Saldo: Rp. {saldo:,.2f}")
        print(f"📅 Tanggal Buat: {created}")
    except Exception:
        print(resp)
    input("\nTekan Enter untuk kembali ke menu...")

def logout():
    current_user['username'] = None
    current_user['account_number'] = None
    current_user['logged_in'] = False
    print("✅ Logout berhasil.")

def main():
    while True:
        if not current_user['logged_in']:
            display_main_menu()
            choice = input("Pilih opsi (1-3): ").strip()
            if choice == '1':
                handle_login_flow()
            elif choice == '2':
                handle_register_flow()
            elif choice == '3':
                print("Terima kasih, sampai jumpa!")
                break
            else:
                print("❌ Pilihan tidak valid. Silakan coba lagi.")
        else:
            display_user_menu()
            choice = input("Pilih opsi (1-4): ").strip()
            if choice == '1':
                handle_check_balance()
            elif choice == '2':
                print("\n--- TOP UP SALDO ---")
                amount = input("Masukkan jumlah top up: ").strip()
                handle_topup(current_user['account_number'], amount)
            elif choice == '3':
                print("\n--- TRANSFER DANA ---")
                receiver_account = input("Nomor rekening penerima: ").strip()
                amount = input("Masukkan jumlah transfer: ").strip()
                handle_transfer(current_user['account_number'], receiver_account, amount)
            elif choice == '4':
                logout()
            else:
                print("❌ Pilihan tidak valid. Silakan coba lagi.")

if __name__ == '__main__':
    os.system('cls' if os.name == 'nt' else 'clear')
    print("🚀 Memulai DANA Service Client...")
    main()