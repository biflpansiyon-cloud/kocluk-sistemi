import streamlit as st
import pandas as pd
import altair as alt
from datetime import datetime
from modules.database import save_data, get_data

def show_student_panel(user):
    st.header(f"📈 {user['AdSoyad']} - Gelişim Paneli")
    
    tab1, tab2 = st.tabs(["➕ Sonuç Gir", "📊 Grafiklerim"])
    
    # --- SEKME 1: VERİ GİRİŞİ ---
    with tab1:
        with st.form("exam_input"):
            c_date, c_name = st.columns(2)
            tarih = c_date.date_input("Tarih", datetime.now())
            deneme_adi = c_name.text_input("Deneme Adı")
            
            c1, c2, c3, c4 = st.columns(4)
            turkce = c1.number_input("Türkçe", step=0.25)
            mat = c2.number_input("Matematik", step=0.25)
            sos = c3.number_input("Sosyal", step=0.25)
            fen = c4.number_input("Fen", step=0.25)
            
            hatalar = st.multiselect("Hatalar:", ["Dikkat", "Bilgi", "Süre", "Boş", "Stres"])
            notlar = st.text_area("Notlar:")
            
            if st.form_submit_button("Kaydet"):
                toplam = turkce + mat + sos + fen
                # Kayıt formatı
                row = [str(tarih), str(user['Username']), deneme_adi, turkce, mat, sos, fen, toplam, ", ".join(hatalar), notlar]
                
                try:
                    save_data("Exam_Results", row)
                    st.success(f"Kaydedildi! Toplam Net: {toplam}")
                except Exception as e:
                    st.error(f"Hata: {e}")

    # --- SEKME 2: GRAFİK ---
    with tab2:
        df = get_data("Exam_Results")
        if not df.empty:
            # Sadece bu öğrencinin verisini al
            # Username sütununu string yaparak filtrele
            df['OgrenciID'] = df['OgrenciID'].astype(str)
            my_data = df[df['OgrenciID'] == str(user['Username'])]
            
            if not my_data.empty:
                my_data['ToplamNet'] = pd.to_numeric(my_data['ToplamNet'], errors='coerce')
                
                chart = alt.Chart(my_data).mark_line(point=True).encode(
                    x='Tarih', y='ToplamNet', tooltip=['DenemeAdi', 'ToplamNet']
                ).interactive()
                st.altair_chart(chart, use_container_width=True)
            else:
                st.info("Henüz veri yok.")
