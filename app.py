import streamlit as st
# Modüllerimizi çağırıyoruz
from modules import auth, student_panel, teacher_panel

# Sayfa Ayarı
st.set_page_config(page_title="AI Koçluk", layout="wide")

# Oturum Kontrolü
if 'user' not in st.session_state:
    st.session_state.user = None

# --- ANA AKIŞ ---

if st.session_state.user is None:
    # Kullanıcı yoksa Login sayfasını göster
    auth.show_login_page()

else:
    # Kullanıcı varsa Menü ve Panelleri göster
    user = st.session_state.user
    
    # Üst Bar
    c1, c2 = st.columns([9, 1])
    c1.success(f"Kullanıcı: {user['AdSoyad']}")
    if c2.button("Çıkış"):
        st.session_state.user = None
        st.rerun()
    
    st.divider()
    
    # Role göre yönlendir
    if user['Rol'] == 'ogretmen':
        teacher_panel.show_teacher_panel()
        
    elif user['Rol'] == 'ogrenci':
        student_panel.show_student_panel(user)
    
    else:
        st.error("Tanımsız Rol!")
