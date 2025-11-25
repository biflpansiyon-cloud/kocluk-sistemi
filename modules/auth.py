import streamlit as st
from modules.database import get_data

def check_login(username, password):
    # Veritabanından kullanıcıları çek
    df_users = get_data("Users")
    
    # Veri tiplerini string yap (Hata önleyici)
    df_users['Username'] = df_users['Username'].astype(str)
    df_users['Password'] = df_users['Password'].astype(str)
    
    username = str(username).strip()
    password = str(password).strip()
    
    # Kontrol et
    user = df_users[(df_users['Username'] == username) & (df_users['Password'] == password)]
    
    if not user.empty:
        return user.iloc[0]
    return None

def show_login_page():
    c1, c2, c3 = st.columns([1,2,1])
    with c2:
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
                    st.error("Hatalı kullanıcı adı veya şifre.")
