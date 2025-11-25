import streamlit as st
import pandas as pd
import altair as alt
from modules.database import get_data

def show_teacher_panel():
    st.header("👨‍🏫 Öğretmen Kontrol Merkezi")
    
    df = get_data("Exam_Results")
    
    if not df.empty:
        # Sayısal dönüşümler
        cols = ['ToplamNet', 'TurkceNet', 'MatNet', 'FenNet', 'SosNet']
        for c in cols:
            if c in df.columns:
                df[c] = pd.to_numeric(df[c], errors='coerce')
    
    tab1, tab2 = st.tabs(["Genel Bakış", "Öğrenci Detay"])
    
    with tab1:
        if not df.empty:
            st.subheader("Sınıf Geneli")
            chart = alt.Chart(df).mark_line(point=True).encode(
                x='Tarih', y='ToplamNet', color='OgrenciID', tooltip=['AdSoyad', 'ToplamNet']
            ).interactive()
            st.altair_chart(chart, use_container_width=True)
            
    with tab2:
        st.write("Öğrenci detayları buraya gelecek (Modüler sistem sayesinde burayı sonra geliştirebiliriz!)")
