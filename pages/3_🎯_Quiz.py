"""
🎯 Quiz Sayfası
Kelime bilgisini test etme
"""

import streamlit as st

# Page config
st.set_page_config(
    page_title="Quiz - Lingua-AI",
    page_icon="🎯",
    layout="wide"
)

# Imports
from components.auth import render_user_sidebar, require_auth, get_current_user
from components.quiz_card import (
    init_quiz_state, 
    render_quiz_setup, 
    render_quiz_question, 
    render_quiz_result,
    reset_quiz
)
from services.firebase_service import get_words, save_quiz_result
from services.gamification_service import update_user_after_quiz
from utils.constants import EXAM_TYPES, QUIZ_TYPES
from utils.helpers import init_session_state, calculate_quiz_score

# Session state başlat
init_session_state()
init_quiz_state()

# Sidebar
render_user_sidebar()

# Ana içerik
st.title("🎯 Quiz")
st.markdown("Kelime bilginizi test edin!")

# Auth kontrolü
if not require_auth("Quiz çözmek için giriş yapmalısınız."):
    st.stop()

user = get_current_user()

st.markdown("---")

# Quiz durumuna göre içerik göster
if st.session_state.quiz_completed:
    # Sonuç ekranı
    render_quiz_result()
    
    # Sonucu kaydet
    if "quiz_result_saved" not in st.session_state or not st.session_state.quiz_result_saved:
        score = st.session_state.quiz_score
        total = len(st.session_state.quiz_questions)
        
        # Firebase'e kaydet
        result_data = {
            "userId": user["id"],
            "score": score,
            "totalQuestions": total,
            "percentage": round((score / total * 100) if total > 0 else 0, 1),
            "wrongAnswers": [w.get("id") for w in st.session_state.quiz_wrong_words if w]
        }
        
        save_quiz_result(result_data)
        
        # Kullanıcı istatistiklerini güncelle
        gamification_result = update_user_after_quiz(user["id"], score, total)
        
        if gamification_result.get("points_earned", 0) > 0:
            st.info(f"🎉 **{gamification_result['points_earned']} puan** kazandınız!")
        
        # Yeni rozetler
        new_badges = gamification_result.get("new_badges", [])
        if new_badges:
            from services.gamification_service import show_badge_earned_notification
            for badge_id in new_badges:
                show_badge_earned_notification(badge_id)
        
        st.session_state.quiz_result_saved = True

elif st.session_state.quiz_active:
    # Quiz devam ediyor
    render_quiz_question()

else:
    # Quiz başlangıç ekranı
    st.markdown("### ⚙️ Quiz Ayarları")
    
    # Filtreler
    col1, col2 = st.columns(2)
    
    with col1:
        exam_filter = st.selectbox(
            "📋 Sınav Türü",
            options=["all"] + list(EXAM_TYPES.keys()),
            format_func=lambda x: "Tümü" if x == "all" else f"{EXAM_TYPES[x]['icon']} {EXAM_TYPES[x]['name']}"
        )
    
    with col2:
        quiz_type = st.selectbox(
            "❓ Soru Türü",
            options=list(QUIZ_TYPES.keys()),
            format_func=lambda x: f"{QUIZ_TYPES[x]['icon']} {QUIZ_TYPES[x]['name']}"
        )
    
    # Kelimeleri getir
    words = get_words(
        status="approved",
        exam_type=exam_filter if exam_filter != "all" else None,
        limit=200
    )
    
    if len(words) < 4:
        st.warning("⚠️ Quiz için en az 4 onaylı kelime gerekli. Lütfen kelime ekleyin veya filtrelerinizi değiştirin.")
    else:
        st.success(f"✅ {len(words)} kelime hazır!")
        
        # Soru sayısı
        max_questions = min(50, len(words))
        question_count = st.slider(
            "📊 Soru Sayısı",
            min_value=5,
            max_value=max_questions,
            value=min(10, max_questions)
        )
        
        st.markdown("---")
        
        # Quiz bilgileri
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.markdown("""
            <div style="background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); padding: 20px; border-radius: 12px; text-align: center;">
                <div style="font-size: 32px;">📝</div>
                <div style="font-size: 24px; font-weight: bold; color: white;">{}</div>
                <div style="font-size: 14px; color: rgba(255,255,255,0.8);">Soru</div>
            </div>
            """.format(question_count), unsafe_allow_html=True)
        
        with col2:
            st.markdown("""
            <div style="background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%); padding: 20px; border-radius: 12px; text-align: center;">
                <div style="font-size: 32px;">⏱️</div>
                <div style="font-size: 24px; font-weight: bold; color: white;">~{} dk</div>
                <div style="font-size: 14px; color: rgba(255,255,255,0.8);">Tahmini Süre</div>
            </div>
            """.format(question_count // 2), unsafe_allow_html=True)
        
        with col3:
            st.markdown("""
            <div style="background: linear-gradient(135deg, #4facfe 0%, #00f2fe 100%); padding: 20px; border-radius: 12px; text-align: center;">
                <div style="font-size: 32px;">🏆</div>
                <div style="font-size: 24px; font-weight: bold; color: white;">+{}</div>
                <div style="font-size: 14px; color: rgba(255,255,255,0.8);">Maks. Puan</div>
            </div>
            """.format(25), unsafe_allow_html=True)
        
        st.markdown("---")
        
        # Başlat butonu
        if st.button("🚀 Quiz'e Başla", type="primary", use_container_width=True):
            from components.quiz_card import generate_quiz_questions, start_quiz
            
            questions = generate_quiz_questions(words, question_count, quiz_type)
            
            if questions:
                st.session_state.quiz_result_saved = False
                start_quiz(questions)
                st.rerun()
            else:
                st.error("Sorular oluşturulamadı. Lütfen tekrar deneyin.")

# İpuçları
st.markdown("---")
with st.expander("💡 Quiz İpuçları"):
    st.markdown("""
    ### Soru Türleri
    - **İngilizce → Türkçe**: Verilen İngilizce kelimenin Türkçe karşılığını bulun
    - **Türkçe → İngilizce**: Verilen Türkçe kelimenin İngilizce karşılığını bulun
    - **Eş Anlam Bulma**: Verilen kelimenin eş anlamlısını bulun
    
    ### Puanlama
    - Her doğru cevap: **Puan**
    - %90+ başarı: **Bonus puan**
    - %100 başarı: **Ekstra bonus**
    
    ### Öneriler
    - Yanlış cevapladığınız kelimeleri tekrar çalışın
    - Düzenli quiz çözerek streak'inizi koruyun
    - Farklı soru türlerini deneyin
    """)
