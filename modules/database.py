import streamlit as st
import pandas as pd
import gspread
from oauth2client.service_account import ServiceAccountCredentials

# Google Sheets Bağlantısını burada yapıyoruz
# Başka hiçbir yerde bağlantı kodu yazmayacağız!

@st.cache_resource
def get_connection():
    scope = ['https://spreadsheets.google.com/feeds', 'https://www.googleapis.com/auth/drive']
    creds = ServiceAccountCredentials.from_json_keyfile_dict(st.secrets["gcp_service_account"], scope)
    client = gspread.authorize(creds)
    
    # Dosya adını buradan değiştirirsin
    sheet = client.open("Kocluk_Veritabani") 
    return sheet

# Veri okuma fonksiyonu
def get_data(sheet_name):
    sh = get_connection()
    worksheet = sh.worksheet(sheet_name)
    data = worksheet.get_all_records()
    df = pd.DataFrame(data)
    return df

# Veri kaydetme fonksiyonu
def save_data(sheet_name, row_data):
    sh = get_connection()
    worksheet = sh.worksheet(sheet_name)
    worksheet.append_row(row_data)
