import requests
import os
import time
import random

# Asetukset
output_dir = "esavelmat_kjs_midit"
base_url = "https://esavelmat.jyu.fi/mid/kjs_"
start_num = 1
end_num = 280

# Luodaan kansio jos sitä ei ole
if not os.path.exists(output_dir):
    os.makedirs(output_dir)
    print(f"Luotu kansio: {output_dir}")

print(f"Aloitetaan KJS-kokoelman lataus (1-280)...")

session = requests.Session()
session.headers.update({
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36'
})

for i in range(start_num, end_num + 1):
    num_str = str(i).zfill(4)
    file_name = f"kjs_{num_str}.mid"
    url = f"{base_url}{num_str}.mid"
    
    file_path = os.path.join(output_dir, file_name)
    
    # Hypätään yli, jos tiedosto on jo ladattu
    if os.path.exists(file_path):
        continue

    try:
        response = session.get(url, timeout=15)
        
        if response.status_code == 200:
            with open(file_path, 'wb') as f:
                f.write(response.content)
            if i % 10 == 0:
                print(f"Ladattu {i}/280...")
        else:
            print(f"Tiedostoa {file_name} ei löytynyt (Status {response.status_code})")
            
        # Pieni viive palvelimen kuormituksen välttämiseksi
        time.sleep(random.uniform(0.2, 0.5))
        
    except Exception as e:
        print(f"Virhe tiedoston {file_name} kohdalla: {e}")
        time.sleep(2)

print(f"\nValmista! Kaikki löytyneet KJS-midit ladattu kansioon: {output_dir}")