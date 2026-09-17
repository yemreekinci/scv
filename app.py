import streamlit as st
import pandas as pd
import base64
from cv_template import create_cv

st.set_page_config(page_title="SCV - CV Builder", page_icon="📄", layout="wide")

# Dil Seçenekleri Sözlüğü (Dictionary)
translations = {
    "TR": {
        "title": "📄 SCV Evrensel CV Oluşturucu",
        "subtitle": "Dakikalar içinde mesleğinize özel, profesyonel, fotoğraflı ve renk temalı CV'nizi hazırlayın.",
        "tab1": "👤 Kişisel Bilgiler & İletişim",
        "tab2": "💼 Eğitim & Deneyim",
        "tab3": "⭐ Yetenekler & Özel Bölümler",
        "basic_info": "Temel Bilgiler",
        "photo": "Profil Fotoğrafı (Opsiyonel)",
        "theme_color": "CV Ana Tema Rengi",
        "theme_info": "💡 CV'nizin ana başlıkları ve çizgileri bu renkte olacaktır.",
        "name": "Ad Soyad*",
        "job_title": "Meslek Unvanı* (Örn: Yazılım Mühendisi, Aşçı, Akademisyen)",
        "about": "Hakkımda (Özet)",
        "about_help": "Kısa bir kariyer özeti veya hedef yazın.",
        "contact_info": "İletişim Bilgileri",
        "phone": "Telefon",
        "email": "E-posta",
        "location": "Konum Bilgisi (İl/İlçe/Ülke)",
        "social_title": "🔗 Sosyal Medya ve Bağlantılar (Dinamik)",
        "social_caption": "Aşağıdaki tabloya tıklayarak yeni satır ekleyebilirsiniz (Örn: Platform: LinkedIn, Link: linkedin.com/in/adiniz)",
        "exp_title": "💼 Profesyonel Deneyim",
        "exp_info": "💡 Öneri: Deneyimlerinizi maddeler halinde yazmak için cümlenin başına '-' veya '*' koyabilirsiniz.",
        "exp_label": "İş Deneyimleri",
        "exp_ph": "- X Şirketi, Pozisyon (2020 - Günümüz)\n- Başarılar ve sorumluluklar...",
        "edu_title": "🎓 Eğitim Bilgileri",
        "edu_label": "Eğitim Geçmişi",
        "edu_ph": "- X Üniversitesi, Bilgisayar Mühendisliği (2016-2020)\n- Lise Adı, Bölüm...",
        "skills_title": "🛠 Yetenekler",
        "skills_label": "Yetenekler (Maddeler halinde)",
        "skills_ph": "- Python, Java\n- Ekip Yönetimi\n- Müşteri İlişkileri",
        "lang_title": "🌍 Yabancı Diller",
        "lang_label": "Diller ve Seviyeleri",
        "lang_ph": "- İngilizce (İleri)\n- Almanca (Başlangıç)",
        "custom_title": "📌 Mesleğinize Özel Bölümler (Örn: Projeler, Yayınlar, Sertifikalar)",
        "custom_desc": "Her mesleğin dinamiği farklıdır. İhtiyacınız olan başlığı kendiniz belirleyin. (Boş bırakılanlar CV'ye eklenmez.)",
        "c1_label": "1. Özel Başlık",
        "c1_val": "PROJELER",
        "c1_help": "Örn: YAYINLAR, SERGİLER, ÖDÜLLER",
        "c1_detail": "Detayları",
        "c2_label": "2. Özel Başlık",
        "c2_val": "SERTİFİKALAR VE BAŞARILAR",
        "c2_detail": "Detayları",
        "ref_label": "Referanslar",
        "ref_ph": "Talep edildiğinde verilecektir.",
        "submit_btn": "🚀 CV Oluştur ve Önizle",
        "err_mandatory": "Lütfen 'Ad Soyad' ve 'Meslek Unvanı' alanlarını doldurunuz!",
        "creating_pdf": "PDF Oluşturuluyor...",
        "success_msg": "✅ CV Başarıyla Oluşturuldu!",
        "err_msg": "CV oluşturulurken bir hata oluştu:",
        "dl_btn": "📥 PDF Olarak İndir",
        "preview_title": "👁️ CV Önizleme",
        # PDF içi statik metinler
        "pdf_phone": "Telefon:",
        "pdf_loc": "Konum:",
        "pdf_email": "E-posta:",
        "pdf_h_contact": "İLETİŞİM",
        "pdf_h_skills": "YETENEKLER",
        "pdf_h_lang": "DİLLER",
        "pdf_h_ref": "REFERANSLAR",
        "pdf_h_about": "HAKKIMDA",
        "pdf_h_exp": "DENEYİM",
        "pdf_h_edu": "EĞİTİM"
    },
    "EN": {
        "title": "📄 SCV Universal CV Builder",
        "subtitle": "Create your profession-specific, professional, photo-inclusive, and color-themed CV in minutes.",
        "tab1": "👤 Personal Info & Contact",
        "tab2": "💼 Education & Experience",
        "tab3": "⭐ Skills & Custom Sections",
        "basic_info": "Basic Information",
        "photo": "Profile Photo (Optional)",
        "theme_color": "CV Main Theme Color",
        "theme_info": "💡 Main headings and lines in your CV will be this color.",
        "name": "Full Name*",
        "job_title": "Job Title* (e.g., Software Engineer, Chef, Academic)",
        "about": "About Me (Summary)",
        "about_help": "Write a short career summary or objective.",
        "contact_info": "Contact Information",
        "phone": "Phone",
        "email": "Email",
        "location": "Location (City/State/Country)",
        "social_title": "🔗 Social Media & Links (Dynamic)",
        "social_caption": "Click the table below to add a new row (e.g., Platform: LinkedIn, Link: linkedin.com/in/yourname)",
        "exp_title": "💼 Professional Experience",
        "exp_info": "💡 Tip: You can put '-' or '*' at the beginning of a sentence to write your experiences as bullet points.",
        "exp_label": "Work Experience",
        "exp_ph": "- Company X, Position (2020 - Present)\n- Achievements and responsibilities...",
        "edu_title": "🎓 Education Information",
        "edu_label": "Education History",
        "edu_ph": "- University X, Computer Engineering (2016-2020)\n- High School Name, Department...",
        "skills_title": "🛠 Skills",
        "skills_label": "Skills (Bullet points)",
        "skills_ph": "- Python, Java\n- Team Management\n- Customer Relations",
        "lang_title": "🌍 Languages",
        "lang_label": "Languages and Levels",
        "lang_ph": "- English (Advanced)\n- Spanish (Beginner)",
        "custom_title": "📌 Profession-Specific Sections (e.g., Projects, Publications, Certificates)",
        "custom_desc": "Every profession is different. Define the title you need yourself. (Empty fields will not be added to the CV.)",
        "c1_label": "1. Custom Title",
        "c1_val": "PROJECTS",
        "c1_help": "e.g., PUBLICATIONS, EXHIBITIONS, AWARDS",
        "c1_detail": "Details",
        "c2_label": "2. Custom Title",
        "c2_val": "CERTIFICATES AND ACHIEVEMENTS",
        "c2_detail": "Details",
        "ref_label": "References",
        "ref_ph": "Available upon request.",
        "submit_btn": "🚀 Generate and Preview CV",
        "err_mandatory": "Please fill in the 'Full Name' and 'Job Title' fields!",
        "creating_pdf": "Generating PDF...",
        "success_msg": "✅ CV Generated Successfully!",
        "err_msg": "An error occurred while generating CV:",
        "dl_btn": "📥 Download as PDF",
        "preview_title": "👁️ CV Preview",
        # PDF içi statik metinler
        "pdf_phone": "Phone:",
        "pdf_loc": "Location:",
        "pdf_email": "Email:",
        "pdf_h_contact": "CONTACT",
        "pdf_h_skills": "SKILLS",
        "pdf_h_lang": "LANGUAGES",
        "pdf_h_ref": "REFERENCES",
        "pdf_h_about": "ABOUT ME",
        "pdf_h_exp": "EXPERIENCE",
        "pdf_h_edu": "EDUCATION"
    }
}

# Dile özel büyük harf dönüştürücü (İngilizce'de "i" harfi problemi olmaması için)
def to_upper_lang(text, lang_code):
    if not text: return ""
    if lang_code == "TR":
        translation_table = str.maketrans("iığüşöç", "İIĞÜŞÖÇ")
        return text.translate(translation_table).upper()
    return text.upper()

# --- DİL SEÇİMİ ---
col_space, col_lang = st.columns([5, 1])

# Kullanıcı dili değiştirdiğinde eski PDF'i hafızadan silen fonksiyon
def clear_pdf_cache():
    if 'pdf_bytes' in st.session_state:
        del st.session_state['pdf_bytes']

with col_lang:
    selected_lang = st.radio(
        "🌐 Language / Dil", 
        ["TR", "EN"], 
        horizontal=True, 
        key="lang_selector",
        on_change=clear_pdf_cache # Dil değiştiğinde bu fonksiyon çalışır
    )

# Seçilen dile göre metinleri `t` değişkenine ata
t = translations[selected_lang]

st.title(t["title"])
st.markdown(t["subtitle"])

with st.form("cv_form"):
    tab1, tab2, tab3 = st.tabs([t["tab1"], t["tab2"], t["tab3"]])
    
    with tab1:
        st.subheader(t["basic_info"])
        col_img, col_info = st.columns([1, 2])
        
        with col_img:
            photo_file = st.file_uploader(t["photo"], type=["jpg", "jpeg", "png"])
            theme_color = st.color_picker(t["theme_color"], "#2C3E50")
            st.info(t["theme_info"])
            
        with col_info:
            name = to_upper_lang(st.text_input(t["name"]), selected_lang)
            title = to_upper_lang(st.text_input(t["job_title"]), selected_lang)
            about = st.text_area(t["about"], help=t["about_help"])
            
        st.markdown("---")
        st.subheader(t["contact_info"])
        col1, col2, col3 = st.columns(3)
        with col1:
            telephone = st.text_input(t["phone"])
        with col2:
            email = st.text_input(t["email"]).lower()
        with col3:
            address = st.text_input(t["location"])
            
        st.markdown("---")
        st.subheader(t["social_title"])
        st.caption(t["social_caption"])
        
        default_socials = pd.DataFrame([
            {"Platform": "LinkedIn", "Link": ""},
            {"Platform": "GitHub", "Link": ""},
            {"Platform": "Behance", "Link": ""}
        ])
        socials_df = st.data_editor(default_socials, num_rows="dynamic", use_container_width=True, hide_index=True, key="socials_editor")

    with tab2:
        st.subheader(t["exp_title"])
        st.info(t["exp_info"])
        experience = st.text_area(t["exp_label"], height=200, placeholder=t["exp_ph"])
        
        st.markdown("---")
        st.subheader(t["edu_title"])
        education = st.text_area(t["edu_label"], height=150, placeholder=t["edu_ph"])

    with tab3:
        col_sk, col_lang_tab = st.columns(2)
        with col_sk:
            st.subheader(t["skills_title"])
            skills = st.text_area(t["skills_label"], height=150, placeholder=t["skills_ph"])
        with col_lang_tab:
            st.subheader(t["lang_title"])
            languages = st.text_area(t["lang_label"], height=150, placeholder=t["lang_ph"])
            
        st.markdown("---")
        st.subheader(t["custom_title"])
        st.write(t["custom_desc"])
        
        c_col1, c_col2 = st.columns(2)
        with c_col1:
            custom_1_title = to_upper_lang(st.text_input(t["c1_label"], value=t["c1_val"], help=t["c1_help"], key="c1_t"), selected_lang)
            custom_1_text = st.text_area(f"{custom_1_title} {t['c1_detail']}", height=150, key="c1_txt")
            
        with c_col2:
            custom_2_title = to_upper_lang(st.text_input(t["c2_label"], value=t["c2_val"], key="c2_t"), selected_lang)
            custom_2_text = st.text_area(f"{custom_2_title} {t['c2_detail']}", height=150, key="c2_txt")

        st.markdown("---")
        references = st.text_area(t["ref_label"], placeholder=t["ref_ph"])
        
    st.markdown("<br>", unsafe_allow_html=True)
    submitted = st.form_submit_button(t["submit_btn"], use_container_width=True)

if submitted:
    if not name or not title:
        st.error(t["err_mandatory"])
    else:
        socials_list = []
        for index, row in socials_df.iterrows():
            if pd.notna(row['Platform']) and pd.notna(row['Link']) and str(row['Platform']).strip() != "" and str(row['Link']).strip() != "":
                socials_list.append((str(row['Platform']).strip(), str(row['Link']).strip()))

        # PDF şablonuna gönderilecek veriler ve DİL ÇEVİRİLERİ
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
            # PDF Tasarımında kullanılacak çeviriler
            "t_phone": t["pdf_phone"],
            "t_loc": t["pdf_loc"],
            "t_email": t["pdf_email"],
            "h_contact": t["pdf_h_contact"],
            "h_skills": t["pdf_h_skills"],
            "h_lang": t["pdf_h_lang"],
            "h_ref": t["pdf_h_ref"],
            "h_about": t["pdf_h_about"],
            "h_exp": t["pdf_h_exp"],
            "h_edu": t["pdf_h_edu"]
        }

        try:
            with st.spinner(t["creating_pdf"]):
                pdf_bytesio = create_cv(data)
                st.session_state['pdf_bytes'] = pdf_bytesio.getvalue()
                st.session_state['file_name'] = f"{name.replace(' ', '_')}_CV.pdf"
            st.success(t["success_msg"])
        except Exception as e:
            st.error(f"{t['err_msg']} {str(e)}")

if 'pdf_bytes' in st.session_state:
    dl_col, pre_col = st.columns([1, 3])
    with dl_col:
        st.download_button(
            label=t["dl_btn"],
            data=st.session_state['pdf_bytes'],
            file_name=st.session_state['file_name'],
            mime="application/pdf",
            use_container_width=True
        )
    with pre_col:
        st.subheader(t["preview_title"])
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