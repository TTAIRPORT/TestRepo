from flask import Flask, render_template
import pandas as pd
from smbprotocol.connection import SMBConnection

app = Flask(__name__)

server_name = "10.1.24.24"
share_name = "tahakkuk"
directory_path = "2024 TAHAKKUK AIR"
file_name = "AYLIK YOLCU VE UÇAK VERİ TABLOSU 2023-2024.xlsx"
user_name = "kurulum"
password = "!!tt132132"
client_name = "ITSANALPC"
domain = "ttairport.local"

def get_excel_data():
    # SMB Bağlantısı kurma ve dosya okuma
    try:
        conn = SMBConnection(user_name, password, client_name, server_name, domain=domain, use_ntlm_v2=True, is_direct_tcp=True)
        connected = conn.connect(server_name, 445)

        if connected:
            print("Bağlantı başarılı")

            file_path = r"\\10.1.24.24\tahakkuk\2024 TAHAKKUK AIR\2024 TİCARİ İŞLER MÜDÜRLÜĞÜ GELİR TAHAKKUKLARINA GÖRE GERÇEKLEŞEN GELİRLER.xlsx"
            file_path2 =r"\\10.1.24.24\ticari isler\Ticari İşler\GÜNCEL TAKİP\TAHAKKUK TAKİP DATASI 2013-2024\2024 TAHAKKUK EDİLEN GELİRLER.xlsx"

            # Excel'den gelen verilerin sayıya dönüştürülmesi ve virgül ile formatlanması
            def format_number(number):
                try:
                    # Sayıyı float türüne dönüştürüp virgüllü formatta döndürme
                    return "{:,.2f}".format(float(number))
                except ValueError:
                    # Hata durumunda sayıyı olduğu gibi döndür
                    return number

            # TAHAKKUK GELİRLERİ OKUMA
            df3 = pd.read_excel(file_path2, sheet_name="2024 EURO KİRA GELİRİ", header=0)
            

            # Verileri okuma ve formatlama
            toplam_kira_geliri = format_number(df3.iat[7, 3])
            ofis_kira_geliri = format_number(df3.iat[9, 3])
            arazi_kira_geliri = format_number(df3.iat[24, 3])
            ticari_alan_kira_geliri = format_number(df3.iat[39, 3])
            atm_kira_geliri = format_number(df3.iat[64, 3])
            antenbaz_kira_geliri = format_number(df3.iat[77, 3])
            dutyfree_kira_geliri = format_number(df3.iat[82, 3])
            f_b_kira_geliri = format_number(df3.iat[87, 3])
            reklam_kira_geliri = format_number(df3.iat[92, 3])
            cip_lounge_kira_geliri = format_number(df3.iat[96, 3])
            stand_film_çekimi_egitim_odasi_kira_geliri = format_number(df3.iat[100, 3])
            karsilama_banko_ozelarac_kira_geliri = format_number(df3.iat[119, 3])
            karsilama_banko_kira_geliri = format_number(df3.iat[126, 3])
            iletisim_sistemleri_gelirleri = format_number(df3.iat[141, 3])
            chekin_kios_gelirleri = format_number(df3.iat[153, 3])
            ucus_bilgi_sistemleri_gelirleri = format_number(df3.iat[159, 3])
            GGKP_gelirleri = format_number(df3.iat[167, 3])
            iklimlerdirme_gelirleri = format_number(df3.iat[180, 3])
            otopark_gelirleri = format_number(df3.iat[221, 3])

            df4 =pd.read_excel(file_path2, sheet_name="ELEKTRİK & SU EURO ", header=0)

            elektirik_su_geliri = format_number(df4.iat[1, 2])

            # KAPAK sayfasını okuma
            df = pd.read_excel(file_path, sheet_name="KAPAK", header=0)

            # Verileri çekme ve formatlama
            b14_value = format_number(df.iat[12, 1])
            c14_value = format_number(df.iat[12, 2])
            b15_value = format_number(df.iat[13, 1])
            c15_value = format_number(df.iat[13, 2])
            b16_value = format_number(df.iat[14, 1])
            c16_value = format_number(df.iat[14, 2])
            b17_value = format_number(df.iat[15, 1])
            c17_value = format_number(df.iat[15, 2])
            b18_value = format_number(df.iat[16, 1])
            c18_value = format_number(df.iat[16, 2])
            b19_value = format_number(df.iat[17, 1])
            c19_value = format_number(df.iat[17, 2])
            b21_value = format_number(df.iat[19, 1])
            c21_value = format_number(df.iat[19, 2])

            # KONSOLİDE sayfasını okuma
            df2 = pd.read_excel(file_path, sheet_name="KONSOLİDE", header=0)
            m62_value = df2.iat[60, 12] # Gelen yolcu sayısı
            m78_value = df2.iat[76, 12] # giden yolcu sayısı
            z62_value = df2.iat[60, 25] #gelen uçak sayısı
            z78_value = df2.iat[76, 25] #giden uçak sayısı

            gelen_yolcu_yuzde = (m62_value / m78_value + m62_value) *100 

            toplam_deger_duzensiz= float(c21_value.replace(",", "")) + float(toplam_kira_geliri.replace(",", ""))
            toplam_deger = format_number(toplam_deger_duzensiz)
            c21_value_yuzde_duzensiz = (float(c21_value.replace(",", "")) / toplam_deger_duzensiz) * 100
            toplam_kira_geliri_yuzde_duzensiz = (float(toplam_kira_geliri.replace(",", "")) / toplam_deger_duzensiz) * 100
            c21_value_yuzde = "{:.2f}".format(c21_value_yuzde_duzensiz)
            toplam_kira_geliri_yuzde = "{:.2f}".format(toplam_kira_geliri_yuzde_duzensiz)

            
            

            # Verileri bir sözlük olarak döndürüyoruz
            return {
                "b14_value": b14_value,
                "c14_value": c14_value,
                "b15_value": b15_value,
                "c15_value": c15_value,
                "b16_value": b16_value,
                "c16_value": c16_value,
                "b17_value": b17_value,
                "c17_value": c17_value,
                "b18_value": b18_value,
                "c18_value": c18_value,
                "b19_value": b19_value,
                "c19_value": c19_value,
                "b21_value": b21_value,
                "c21_value": c21_value,
                "m62_value": m62_value,
                "m78_value": m78_value,
                "z62_value": z62_value,
                "z78_value": z78_value,
                "toplam_kira_geliri": toplam_kira_geliri,
                "ofis_kira_geliri": ofis_kira_geliri,
                "arazi_kira_geliri": arazi_kira_geliri,
                "ticari_alan_kira_geliri": ticari_alan_kira_geliri,
                "atm_kira_geliri": atm_kira_geliri,
                "antenbaz_kira_geliri": antenbaz_kira_geliri,
                "dutyfree_kira_geliri": dutyfree_kira_geliri,
                "f_b_kira_geliri": f_b_kira_geliri,
                "reklam_kira_geliri": reklam_kira_geliri,
                "cip_lounge_kira_geliri": cip_lounge_kira_geliri,
                "stand_film_çekimi_egitim_odasi_kira_geliri": stand_film_çekimi_egitim_odasi_kira_geliri,
                "karsilama_banko_ozelarac_kira_geliri": karsilama_banko_ozelarac_kira_geliri,
                "karsilama_banko_kira_geliri": karsilama_banko_kira_geliri,
                "iletisim_sistemleri_gelirleri": iletisim_sistemleri_gelirleri,
                "chekin_kios_gelirleri": chekin_kios_gelirleri,
                "ucus_bilgi_sistemleri_gelirleri": ucus_bilgi_sistemleri_gelirleri,
                "GGKP_gelirleri": GGKP_gelirleri,
                "iklimlerdirme_gelirleri": iklimlerdirme_gelirleri,
                "otopark_gelirleri": otopark_gelirleri,
                "elektirik_su_geliri": elektirik_su_geliri,
                "toplam_deger": toplam_deger,
                "c21_value_yuzde": c21_value_yuzde,
                "toplam_kira_geliri_yuzde": toplam_kira_geliri_yuzde,
                "gelen_yolcu_yuzde": gelen_yolcu_yuzde
                
            }


    except Exception as e:
        print(f"Bağlantı veya dosya okuma hatası: {e}")
        return None
    
@app.route('/')
def index():
    data = get_excel_data()

    if data:
        # Web sayfasında gösterilecek verileri gönderiyoruz
        return render_template('index.html', data=data)
    else:
        return "Veri okunamadı"



if __name__ == '__main__':
    app.run(debug=True)
