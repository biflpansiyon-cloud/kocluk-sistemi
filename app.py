import streamlit as st
import pandas as pd
import gspread
from oauth2client.service_account import ServiceAccountCredentials
from datetime import datetime

# --- AYARLAR VE BAĞLANTI ---
st.set_page_config(page_title="AI Koçluk Sistemi", layout="wide")

# Google Sheets Bağlantısı (Cache kullanarak hızlandırıyoruz)
@st.cache_resource
def get_google_sheet_client():
    scope = ['https://spreadsheets.google.com/feeds', 'https://www.googleapis.com/auth/drive']
    creds = ServiceAccountCredentials.from_json_keyfile_dict(st.secrets["gcp_service_account"], scope)
    client = gspread.authorize(creds)
    return client

# Veritabanına Bağlan (Dosya adını buraya tam yazman lazım)
try:
    client = get_google_sheet_client()
    sheet = client.open("Kocluk_Veritabani") # SENİN GOOGLE SHEETS DOSYA ADIN BURAYA!
    worksheet_users = sheet.worksheet("Users")
    worksheet_exams = sheet.worksheet("Exam_Results")
    worksheet_logs = sheet.worksheet("Coach_Logs")
except Exception as e:
    st.error(f"Google Sheets bağlantı hatası: {e}")
    st.stop()

# --- FONKSİYONLAR ---
def check_login(username, password):
    users = worksheet_users.get_all_records()
    df_users = pd.DataFrame(users)
    user = df_users[(df_users['Username'] == username) & (df_users['Password'] == str(password))]
    if not user.empty:
        return user.iloc[0]
    return None

def save_exam_result(data):
    worksheet_exams.append_row(data)

# --- ARAYÜZ (FRONTEND) ---

# Oturum Durumu Kontrolü
if 'user' not in st.session_state:
    st.session_state.user = None

# 1. LOGIN EKRANI
if st.session_state.user is None:
    st.title("🎓 Koçluk Sistemi Giriş")
    with st.form("login_form"):
        username = st.text_input("Kullanıcı Adı")
        password = st.text_input("Şifre", type="password")
        submit = st.form_submit_button("Giriş Yap")
        
        if submit:
            user_info = check_login(username, password)
            if user_info is not None:
                st.session_state.user = user_info
                st.rerun()
            else:
                st.error("Kullanıcı adı veya şifre hatalı!")

# 2. SİSTEM İÇERİSİ
else:
    user = st.session_state.user
    st.sidebar.title(f"Hoşgeldin, {user['AdSoyad']}")
    
    # ÇIKIŞ BUTONU
    if st.sidebar.button("Çıkış Yap"):
        st.session_state.user = None
        st.rerun()

    # --- ÖĞRETMEN PANELİ ---
    if user['Rol'] == 'ogretmen':
        st.header("👨‍🏫 Öğretmen Kontrol Paneli")
        
        tab1, tab2 = st.tabs(["Öğrenci Analizi", "Görüşme Kayıt"])
        
        with tab1:
            st.info("Burada tüm öğrencilerin grafiklerini göreceksin.")
            # Buraya grafik kodları gelecek
            
        with tab2:
            st.write("Yeni görüşme notu ekle...")
            # Buraya form gelecek

    # --- ÖĞRENCİ PANELİ ---
    elif user['Rol'] == 'ogrenci':
        st.header(f"📈 {user['AdSoyad']} - Gelişim Paneli")
        
        tab1, tab2 = st.tabs(["Sonuç Gir", "Durumum"])
        
        with tab1:
            st.subheader("Yeni Deneme Sonucu Ekle")
            with st.form("deneme_form"):
                tarih = st.date_input("Tarih", datetime.now())
                deneme_adi = st.text_input("Deneme Yayını/Adı")
                
                c1, c2, c3, c4 = st.columns(4)
                turkce = c1.number_input("Türkçe Net", step=0.25)
                mat = c2.number_input("Matematik Net", step=0.25)
                sos = c3.number_input("Sosyal Net", step=0.25)
                fen = c4.number_input("Fen Net", step=0.25)
                
                # Çoklu Seçim Hata Analizi
                hatalar = st.multiselect(
                    "Bu sınavda yaşadığın sorunlar:",
                    ["Dikkat Hatası", "Bilgi Eksikliği", "Süre Yetmedi", "Yanlış Okuma", "İşlem Hatası", "Stres/Heyecan"]
                )
                
                notlar = st.text_area("Kendine veya Hocana Notun:")
                
                submit_exam = st.form_submit_button("Sonuçları Kaydet")
                
                if submit_exam:
                    toplam = turkce + mat + sos + fen
                    hata_str = ", ".join(hatalar)
                    # Kayıt sırası: Tarih, OgrenciID, DenemeAdi, T, M, S, F, Toplam, HataAnalizi, OgrenciNotu
                    row_data = [str(tarih), user['Username'], deneme_adi, turkce, mat, sos, fen, toplam, hata_str, notlar]
                    
                    try:
                        save_exam_result(row_data)
                        st.success("Deneme başarıyla kaydedildi! Harikasın 🚀")
                        # Yapay Zeka motivasyon mesajı buraya gelecek
                    except Exception as e:
                        st.error(f"Kayıt hatası: {e}")

        with tab2:
            st.write("Burada kendi gelişim grafiğini göreceksin.")
