import requests
from bs4 import BeautifulSoup
import pandas as pd
import re
import time
import random

def scrape_esavelmat():
    session = requests.Session()
    session.headers.update({
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36'
    })

    data_list = []
    columns = [
        "ID", "Nimi", "Kokoelma", "Yleislaji", "Tyyppi", "Muistiinpanija", 
        "Vuosi", "Sivu", "Tahtilaji", "Sävellaji", "Pitäjä", "Kylä", 
        "Maakunta", "Lääni", "Sanat", "Kirjahuomiot", "Kommentit", 
        "Samanlaisuus", "Intervalli", "Melodian suunta"
    ]
    
    start_num = 1
    end_num = 668

    print(f"Aloitetaan massakeräys: {start_num} - {end_num}")

    for i in range(start_num, end_num + 1):
        num_str = str(i).zfill(4)
        id_str = f"kt1_{num_str}"
        url = f"https://esavelmat.jyu.fi/savelma.php?numero={id_str}&uil="
        
        if i % 10 == 0:
            print(f"Eteneminen: {i}/{end_num}...")
        
        try:
            response = session.get(url, timeout=15)
            response.encoding = 'utf-8'
            soup = BeautifulSoup(response.content, 'html.parser')
            
            # Puhdistetaan teksti ja poistetaan rivinvaihdot
            full_text = soup.get_text(" ", strip=True).replace("\n", " ").replace("\r", " ")

            def get_val(label, next_label_list):
                stop_pattern = "|".join(next_label_list)
                pattern = rf"{label}:(.*?)(?={stop_pattern}|\||$)"
                match = re.search(pattern, full_text, re.IGNORECASE)
                if match:
                    val = match.group(1).strip().rstrip('-').strip()
                    # Poistetaan puolipisteet datan seasta (Excel-turvallisuus)
                    return val.replace(";", ",")
                return ""

            row = {
                "ID": id_str,
                "Nimi": get_val("nimi", ["sivu", "muistiinpanija"]),
                "Kokoelma": get_val("kokoelma", ["yleislaji"]),
                "Yleislaji": get_val("yleislaji", ["tyyppi"]),
                "Tyyppi": get_val("tyyppi", ["nimi", "sivu"]),
                "Muistiinpanija": get_val("muistiinpanija", ["vuosi"]),
                "Vuosi": get_val("vuosi", ["sävellaji", "tahtilaji", "sivu"]),
                "Sivu": get_val("sivu", ["muistiinpanija"]),
                "Sävellaji": get_val("sävellaji", ["tahtilaji"]),
                "Tahtilaji": get_val("tahtilaji", ["pitäjä"]),
                "Pitäjä": get_val("pitäjä", ["kylä", "maakunta"]),
                "Kylä": get_val("kylä", ["maakunta", "lääni"]),
                "Maakunta": get_val("maakunta", ["lääni", "sanat"]),
                "Lääni": get_val("lääni", ["sanat", "kirjahuomiot"]),
                "Sanat": get_val("sanat", ["kirjahuomiot"]),
                "Kirjahuomiot": get_val("kirjahuomiot", ["kommentit"]),
                "Kommentit": get_val("kommentit", ["samanlaisuus"]),
                "Samanlaisuus": get_val("samanlaisuus", ["intervalli"]),
                "Intervalli": get_val("intervalli", ["melodian suunta"]),
                "Melodian suunta": get_val("melodian suunta", ["Sulje"])
            }

            data_list.append(row)
            
            # Kohtelias viive: 0.3 - 0.7 sekuntia per sivu
            time.sleep(random.uniform(0.3, 0.7))

        except Exception as e:
            print(f"\nVirhe ID:n {id_str} kohdalla: {e}")
            time.sleep(2) # Odota hetki jos yhteys pätkii

    # Tallennus
    df = pd.DataFrame(data_list, columns=columns)
    output_name = "esavelmat_kaikki_tiedot.csv"
    df.to_csv(output_name, index=False, sep=';', encoding='utf-8-sig', quoting=1)
    
    print(f"\nValmista! {len(data_list)} kappaletta tallennettu: {output_name}")

if __name__ == "__main__":
    scrape_esavelmat()