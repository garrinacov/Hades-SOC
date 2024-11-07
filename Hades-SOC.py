import requests
import json

# Membuat tampilan dengan warna dan style
def print_header(text, color_code="35"):
    """ Menampilkan header dengan warna tertentu """
    print(f"\033[1;{color_code}m{text}\033[0m")
    print("=" * len(text))  # Membuat garis bawah yang sama panjangnya dengan teks

# Menampilkan bagian header
print_header("Hades-SOC Tools v1.0", color_code="34")  # Biru untuk header utama

# Meminta pengguna untuk memasukkan IP yang ingin dicek
ip = input("\033[1;34mEnter IP Address: \033[0m")

# AbuseIPDB API setup
abuseipdb_url = 'https://api.abuseipdb.com/api/v2/check'
abuseipdb_key = '<API_KEY_ABUSEIPDB>'
abuseipdb_headers = {
    'Accept': 'application/json',
    'Key': abuseipdb_key
}
abuseipdb_querystring = {
    'ipAddress': ip,
    'maxAgeInDays': '90',
    'verbose': 'true'
}

# CriminalIP API setup
criminalip_url = f"https://api.criminalip.io/v1/asset/ip/summary?ip={ip}"
criminalip_key = "<API_KEY_CRIMINALIP>"
criminalip_headers = {
    "x-api-key": criminalip_key
}

# Request ke AbuseIPDB API
response_abuseipdb = requests.get(abuseipdb_url, headers=abuseipdb_headers, params=abuseipdb_querystring)

# Request ke CriminalIP API
response_criminalip = requests.get(criminalip_url, headers=criminalip_headers)

# Mengecek apakah kedua request berhasil
if response_abuseipdb.status_code == 200 and response_criminalip.status_code == 200:
    # Decode JSON responses
    abuseipdb_data = response_abuseipdb.json()
    criminalip_data = response_criminalip.json()

    # Menampilkan informasi dari AbuseIPDB
    print_header(f"AbuseIPDB Reports for IP {ip}", color_code="36")  # Cyan untuk laporan AbuseIPDB
    if 'reports' in abuseipdb_data['data']:
        for report in abuseipdb_data['data']['reports']:
            reported_at = report.get('reportedAt', 'N/A')
            comment = report.get('comment', 'No comment')
            categories = report.get('categories', [])

            # Pastikan categories adalah list dan konversikan elemen menjadi string
            if not isinstance(categories, list):
                categories = []
            categories = [str(item) for item in categories]  # Pastikan semua item adalah string

            # Menampilkan data kategori, jika ada
            print(f"\033[1;36mReported At:\033[0m \033[1;32m{reported_at}\033[0m")
            print(f"\033[1;36mComment:\033[0m \033[1;32m{comment}\033[0m")
            print(f"\033[1;36mCategories:\033[0m \033[1;32m{', '.join(categories) if categories else 'N/A'}\033[0m")
            print("-" * 40)
    else:
        print("\033[1;32mNo reports found on AbuseIPDB.\033[0m")

    # Menampilkan informasi dari CriminalIP
    print_header(f"CriminalIP Summary for IP {ip}", color_code="33")  # Kuning untuk CriminalIP
    print("\033[1;32m" + json.dumps(criminalip_data, sort_keys=True, indent=4) + "\033[0m")  # Hijau untuk hasil JSON

else:
    if response_abuseipdb.status_code != 200:
        print(f"\033[1;31mError with AbuseIPDB API: {response_abuseipdb.status_code}\033[0m")
        print(f"\033[1;31m{response_abuseipdb.text}\033[0m")
    if response_criminalip.status_code != 200:
        print(f"\033[1;31mError with CriminalIP API: {response_criminalip.status_code}\033[0m")
        print(f"\033[1;31m{response_criminalip.text}\033[0m")
