import requests
import os
import time
import random

# Asetukset
output_dir = "esavelmat_midit"
base_url = "https://esavelmat.jyu.fi/mid/kt1_"
start_num = 1
end_num = 668

if not os.path.exists(output_dir):
    os.makedirs(output_dir)

print(f"Aloitetaan lataus kansioon: {output_dir}")

# Käytetään istuntoa (session) tehostamaan yhteyttä
session = requests.Session()
session.headers.update({
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36'
})

for i in range(start_num, end_num + 1):
    # Muotoillaan numero nelinumeroiseksi (esim. 1 -> 0001)
    num_str = str(i).zfill(4)
    file_name = f"kt1_{num_str}.mid"
    url = f"{base_url}{num_str}.mid"
    
    file_path = os.path.join(output_dir, file_name)
    
    # Hypätään yli, jos tiedosto on jo ladattu (kätevä jos yhteys katkeaa)
    if os.path.exists(file_path):
        continue

    try:
        response = session.get(url, timeout=15)
        
        if response.status_code == 200:
            with open(file_path, 'wb') as f:
                f.write(response.content)
            print(f"Ladattu: {file_name}")
        elif response.status_code == 404:
            print(f"Tiedostoa {file_name} ei löydy (404).")
        else:
            print(f"Virhe {file_name}: Status {response.status_code}")
            
        # Pidetään tauko palvelimen säästämiseksi (0.5 - 1.5 sekuntia)
        time.sleep(random.uniform(0.5, 1.5))
        
    except Exception as e:
        print(f"Yhteysvirhe tiedoston {file_name} kohdalla: {e}")
        time.sleep(5) # Odota hetki jos verkko pätkii

print("\nKaikki tiedostot käsitelty!")