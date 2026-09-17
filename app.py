import streamlit as st
import pandas as pd
import base64
from cv_template import create_cv

st.set_page_config(page_title="SCV - Evrensel CV Oluşturucu", page_icon="📄", layout="wide")

st.title("📄 SCV Evrensel CV Oluşturucu")
st.markdown("Dakikalar içinde mesleğinize özel, profesyonel, fotoğraflı ve renk temalı CV'nizi hazırlayın.")

def to_upper_tr(text):
    if not text: return ""
    translation_table = str.maketrans("iığüşöç", "İIĞÜŞÖÇ")
    return text.translate(translation_table).upper()

# Formu genişletilebilir ve düzenli tutmak için st.form kullanıyoruz
with st.form("cv_form"):
    
    # 3 Sekmeli Düzen
    tab1, tab2, tab3 = st.tabs(["👤 Kişisel Bilgiler & İletişim", "💼 Eğitim & Deneyim", "⭐ Yetenekler & Özel Bölümler"])
    
    with tab1:
        st.subheader("Temel Bilgiler")
        col_img, col_info = st.columns([1, 2])
        
        with col_img:
            photo_file = st.file_uploader("Profil Fotoğrafı (Opsiyonel)", type=["jpg", "jpeg", "png"])
            theme_color = st.color_picker("CV Ana Tema Rengi", "#2C3E50")
            st.info("💡 CV'nizin ana başlıkları ve çizgileri bu renkte olacaktır.")
            
        with col_info:
            name = to_upper_tr(st.text_input("Ad Soyad*"))
            title = to_upper_tr(st.text_input("Meslek Unvanı* (Örn: Yazılım Mühendisi, Aşçı, Akademisyen)"))
            about = st.text_area("Hakkımda (Özet)", help="Kısa bir kariyer özeti veya hedef yazın.")
            
        st.markdown("---")
        st.subheader("İletişim Bilgileri")
        col1, col2, col3 = st.columns(3)
        with col1:
            telephone = st.text_input("Telefon")
        with col2:
            email = st.text_input("E-posta").lower()
        with col3:
            address = st.text_input("Konum Bilgisi (İl/İlçe/Ülke)")
            
        st.markdown("---")
        st.subheader("🔗 Sosyal Medya ve Bağlantılar (Dinamik)")
        st.caption("Aşağıdaki tabloya tıklayarak yeni satır ekleyebilirsiniz (Örn: Platform: LinkedIn, Link: linkedin.com/in/adiniz)")
        
        # Dinamik bağlantı tablosu
        default_socials = pd.DataFrame([
            {"Platform": "LinkedIn", "Link": ""},
            {"Platform": "GitHub", "Link": ""},
            {"Platform": "Behance", "Link": ""}
        ])
        # Tablonun verisini kaybetmemesi için key atandı
        socials_df = st.data_editor(default_socials, num_rows="dynamic", use_container_width=True, hide_index=True, key="socials_editor")

    with tab2:
        st.subheader("💼 Profesyonel Deneyim")
        st.info("💡 Öneri: Deneyimlerinizi maddeler halinde yazmak için cümlenin başına '-' veya '*' koyabilirsiniz.")
        experience = st.text_area("İş Deneyimleri", height=200, placeholder="- X Şirketi, Pozisyon (2020 - Günümüz)\n- Başarılar ve sorumluluklar...")
        
        st.markdown("---")
        st.subheader("🎓 Eğitim Bilgileri")
        education = st.text_area("Eğitim Geçmişi", height=150, placeholder="- X Üniversitesi, Bilgisayar Mühendisliği (2016-2020)\n- Lise Adı, Bölüm...")

    with tab3:
        col_sk, col_lang = st.columns(2)
        with col_sk:
            st.subheader("🛠 Yetenekler")
            skills = st.text_area("Yetenekler (Maddeler halinde)", height=150, placeholder="- Python, Java\n- Ekip Yönetimi\n- Müşteri İlişkileri")
        with col_lang:
            st.subheader("🌍 Yabancı Diller")
            languages = st.text_area("Diller ve Seviyeleri", height=150, placeholder="- İngilizce (İleri)\n- Almanca (Başlangıç)")
            
        st.markdown("---")
        st.subheader("📌 Mesleğinize Özel Bölümler (Örn: Projeler, Yayınlar, Sertifikalar)")
        st.write("Her mesleğin dinamiği farklıdır. İhtiyacınız olan başlığı kendiniz belirleyin. (Boş bırakılanlar CV'ye eklenmez.)")
        
        c_col1, c_col2 = st.columns(2)
        with c_col1:
            custom_1_title = to_upper_tr(st.text_input("1. Özel Başlık", value="PROJELER", help="Örn: YAYINLAR, SERGİLER, ÖDÜLLER", key="custom_1_title_input"))
            # DİKKAT: Veri kaybını önleyen en önemli eklenti 'key' parametresidir.
            custom_1_text = st.text_area(f"{custom_1_title} Detayları", height=150, key="custom_1_text_input")
            
        with c_col2:
            custom_2_title = to_upper_tr(st.text_input("2. Özel Başlık", value="SERTİFİKALAR VE BAŞARILAR", key="custom_2_title_input"))
            # DİKKAT: Veri kaybını önleyen en önemli eklenti 'key' parametresidir.
            custom_2_text = st.text_area(f"{custom_2_title} Detayları", height=150, key="custom_2_text_input")

        st.markdown("---")
        references = st.text_area("Referanslar", placeholder="Talep edildiğinde verilecektir.")
        
    st.markdown("<br>", unsafe_allow_html=True)
    submitted = st.form_submit_button("🚀 CV Oluştur ve Önizle", use_container_width=True)

# Form gönderildiğinde verileri işle ve PDF'i Session State'e (belleğe) kaydet
if submitted:
    if not name or not title:
        st.error("Lütfen 'Ad Soyad' ve 'Meslek Unvanı' alanlarını doldurunuz!")
    else:
        # Sosyal medya dataframe'ini liste formatına çevir (Sadece dolu olanları al)
        socials_list = []
        for index, row in socials_df.iterrows():
            if pd.notna(row['Platform']) and pd.notna(row['Link']) and str(row['Platform']).strip() != "" and str(row['Link']).strip() != "":
                socials_list.append((str(row['Platform']).strip(), str(row['Link']).strip()))

        # Veri sözlüğü
        data = {
            "name": name,
            "title": title,
            "theme_color": theme_color,
            "photo": photo_file.read() if photo_file else None,
            "email": email,
            "telephone": telephone,
            "address": address,
            "socials": socials_list,
            "languages": languages,
            "about": about,
            "experience": experience,
            "education": education,
            "skills": skills,
            "references": references,
            "custom_1_title": custom_1_title,
            "custom_1_text": custom_1_text,
            "custom_2_title": custom_2_title,
            "custom_2_text": custom_2_text,
        }

        try:
            with st.spinner("PDF Oluşturuluyor..."):
                pdf_bytesio = create_cv(data)
                # Üretilen PDF'i uygulamanın belleğine kaydediyoruz (Sayfa yenilense de kaybolmaz)
                st.session_state['pdf_bytes'] = pdf_bytesio.getvalue()
                st.session_state['file_name'] = f"{name.replace(' ', '_')}_CV.pdf"
            st.success("✅ CV Başarıyla Oluşturuldu!")
        except Exception as e:
            st.error(f"CV oluşturulurken bir hata oluştu: {str(e)}")

# Eğer bellekte üretilmiş bir PDF varsa, önizleme ve indirme butonunu göster
if 'pdf_bytes' in st.session_state:
    dl_col, pre_col = st.columns([1, 3])
    
    with dl_col:
        # st.download_button sayfayı yeniler, ancak verilerimiz st.session_state'te olduğu için artık kaybolmaz.
        st.download_button(
            label="📥 PDF Olarak İndir",
            data=st.session_state['pdf_bytes'],
            file_name=st.session_state['file_name'],
            mime="application/pdf",
            use_container_width=True
        )
        
    with pre_col:
        st.subheader("👁️ CV Önizleme")
        base64_pdf = base64.b64encode(st.session_state['pdf_bytes']).decode('utf-8')
        pdf_display = f'''
            <iframe 
                src="data:application/pdf;base64,{base64_pdf}#toolbar=0" 
                width="100%" 
                height="900" 
                type="application/pdf"
                style="border: 1px solid #ccc; border-radius: 8px;">
            </iframe>
        '''
        st.markdown(pdf_display, unsafe_allow_html=True)