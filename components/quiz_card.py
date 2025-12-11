"""
Quiz Card Component
Quiz question display and interaction
"""

import streamlit as st
from typing import Dict, Any, List, Optional
import random


def get_quiz_styles() -> str:
    """Quiz için CSS stilleri"""
    return """
    <style>
    .quiz-container {
        background: linear-gradient(135deg, #1a1f2e 0%, #2d3748 100%);
        border-radius: 20px;
        padding: 30px;
        margin: 20px 0;
    }
    
    .quiz-progress {
        display: flex;
        justify-content: space-between;
        align-items: center;
        margin-bottom: 20px;
        padding-bottom: 15px;
        border-bottom: 1px solid rgba(255,255,255,0.1);
    }
    
    .quiz-question-number {
        font-size: 14px;
        color: #a0aec0;
    }
    
    .quiz-timer {
        font-size: 14px;
        color: #667eea;
        font-weight: 600;
    }
    
    .quiz-question {
        font-size: 24px;
        font-weight: 600;
        color: #fff;
        margin-bottom: 30px;
        line-height: 1.4;
    }
    
    .quiz-hint {
        font-size: 14px;
        color: #a0aec0;
        margin-bottom: 20px;
        font-style: italic;
    }
    
    .quiz-option {
        background: rgba(102, 126, 234, 0.1);
        border: 2px solid rgba(102, 126, 234, 0.3);
        border-radius: 12px;
        padding: 16px 20px;
        margin: 10px 0;
        cursor: pointer;
        transition: all 0.3s ease;
        color: #fff;
    }
    
    .quiz-option:hover {
        background: rgba(102, 126, 234, 0.2);
        border-color: #667eea;
        transform: translateX(5px);
    }
    
    .quiz-option.selected {
        background: rgba(102, 126, 234, 0.3);
        border-color: #667eea;
    }
    
    .quiz-option.correct {
        background: rgba(39, 174, 96, 0.3);
        border-color: #27ae60;
    }
    
    .quiz-option.wrong {
        background: rgba(231, 76, 60, 0.3);
        border-color: #e74c3c;
    }
    
    .quiz-result {
        text-align: center;
        padding: 40px;
    }
    
    .quiz-score {
        font-size: 72px;
        font-weight: 700;
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
    }
    
    .quiz-grade {
        font-size: 24px;
        margin-top: 10px;
    }
    
    .quiz-stats {
        display: flex;
        justify-content: center;
        gap: 40px;
        margin-top: 30px;
    }
    
    .quiz-stat {
        text-align: center;
    }
    
    .quiz-stat-value {
        font-size: 28px;
        font-weight: 600;
        color: #667eea;
    }
    
    .quiz-stat-label {
        font-size: 12px;
        color: #a0aec0;
        text-transform: uppercase;
        letter-spacing: 1px;
    }
    </style>
    """


def init_quiz_state():
    """Quiz session state'lerini başlat"""
    if "quiz_active" not in st.session_state:
        st.session_state.quiz_active = False
    if "quiz_questions" not in st.session_state:
        st.session_state.quiz_questions = []
    if "quiz_current_index" not in st.session_state:
        st.session_state.quiz_current_index = 0
    if "quiz_answers" not in st.session_state:
        st.session_state.quiz_answers = []
    if "quiz_score" not in st.session_state:
        st.session_state.quiz_score = 0
    if "quiz_wrong_words" not in st.session_state:
        st.session_state.quiz_wrong_words = []
    if "quiz_completed" not in st.session_state:
        st.session_state.quiz_completed = False


def generate_quiz_questions(
    words: List[Dict[str, Any]], 
    question_count: int = 10, 
    quiz_type: str = "en_to_tr"
) -> List[Dict[str, Any]]:
    """
    Quiz soruları oluştur
    
    Args:
        words: Kelime havuzu
        question_count: Soru sayısı
        quiz_type: Soru türü
    
    Returns:
        Soru listesi
    """
    if len(words) < 4:
        return []
    
    # Rastgele kelimeler seç
    question_words = random.sample(words, min(question_count, len(words)))
    questions = []
    
    for word in question_words:
        # Yanlış şıkları belirle
        wrong_options_pool = [w for w in words if w["id"] != word["id"]]
        wrong_options = random.sample(wrong_options_pool, min(3, len(wrong_options_pool)))
        
        if quiz_type == "en_to_tr":
            question = {
                "type": "en_to_tr",
                "question": f"'{word['english']}' kelimesinin Türkçe karşılığı nedir?",
                "correct_answer": word["turkish"],
                "options": [word["turkish"]] + [w["turkish"] for w in wrong_options],
                "word_id": word["id"],
                "word": word
            }
        elif quiz_type == "tr_to_en":
            question = {
                "type": "tr_to_en",
                "question": f"'{word['turkish']}' kelimesinin İngilizce karşılığı nedir?",
                "correct_answer": word["english"],
                "options": [word["english"]] + [w["english"] for w in wrong_options],
                "word_id": word["id"],
                "word": word
            }
        elif quiz_type == "synonym":
            synonyms = word.get("synonyms", [])
            if synonyms:
                correct = random.choice(synonyms)
                question = {
                    "type": "synonym",
                    "question": f"'{word['english']}' kelimesinin eş anlamlısı hangisidir?",
                    "correct_answer": correct,
                    "options": [correct] + [w["english"] for w in wrong_options],
                    "word_id": word["id"],
                    "word": word
                }
            else:
                # Eş anlam yoksa en_to_tr'ye dön
                question = {
                    "type": "en_to_tr",
                    "question": f"'{word['english']}' kelimesinin Türkçe karşılığı nedir?",
                    "correct_answer": word["turkish"],
                    "options": [word["turkish"]] + [w["turkish"] for w in wrong_options],
                    "word_id": word["id"],
                    "word": word
                }
        else:
            # Default: en_to_tr
            question = {
                "type": "en_to_tr",
                "question": f"'{word['english']}' kelimesinin Türkçe karşılığı nedir?",
                "correct_answer": word["turkish"],
                "options": [word["turkish"]] + [w["turkish"] for w in wrong_options],
                "word_id": word["id"],
                "word": word
            }
        
        # Şıkları karıştır
        random.shuffle(question["options"])
        questions.append(question)
    
    return questions


def start_quiz(questions: List[Dict[str, Any]]):
    """Quiz'i başlat"""
    init_quiz_state()
    st.session_state.quiz_active = True
    st.session_state.quiz_questions = questions
    st.session_state.quiz_current_index = 0
    st.session_state.quiz_answers = []
    st.session_state.quiz_score = 0
    st.session_state.quiz_wrong_words = []
    st.session_state.quiz_completed = False


def render_quiz_question():
    """Aktif soruyu render et"""
    init_quiz_state()
    
    if not st.session_state.quiz_active or st.session_state.quiz_completed:
        return
    
    st.markdown(get_quiz_styles(), unsafe_allow_html=True)
    
    questions = st.session_state.quiz_questions
    current_idx = st.session_state.quiz_current_index
    
    if current_idx >= len(questions):
        st.session_state.quiz_completed = True
        return
    
    question = questions[current_idx]
    total = len(questions)
    
    # Progress bar
    progress = (current_idx) / total
    st.progress(progress)
    
    # Soru bilgisi
    st.markdown(f"""
    <div class="quiz-progress">
        <span class="quiz-question-number">Soru {current_idx + 1} / {total}</span>
        <span class="quiz-timer">🎯 Skor: {st.session_state.quiz_score}</span>
    </div>
    """, unsafe_allow_html=True)
    
    # Soru
    st.markdown(f"""
    <div class="quiz-question">{question['question']}</div>
    """, unsafe_allow_html=True)
    
    # Şıklar
    letters = ["A", "B", "C", "D"]
    
    for i, option in enumerate(question["options"]):
        col1, col2 = st.columns([0.1, 0.9])
        
        with col1:
            st.markdown(f"**{letters[i]}**")
        
        with col2:
            if st.button(option, key=f"option_{current_idx}_{i}", use_container_width=True):
                handle_answer(option, question)


def handle_answer(selected_option: str, question: Dict[str, Any]):
    """Cevabı işle"""
    is_correct = selected_option == question["correct_answer"]
    
    st.session_state.quiz_answers.append({
        "question": question["question"],
        "selected": selected_option,
        "correct": question["correct_answer"],
        "is_correct": is_correct,
        "word_id": question.get("word_id")
    })
    
    if is_correct:
        st.session_state.quiz_score += 1
        st.success("✅ Doğru!")
    else:
        st.error(f"❌ Yanlış! Doğru cevap: **{question['correct_answer']}**")
        st.session_state.quiz_wrong_words.append(question.get("word"))
    
    # Sonraki soruya geç
    st.session_state.quiz_current_index += 1
    
    if st.session_state.quiz_current_index >= len(st.session_state.quiz_questions):
        st.session_state.quiz_completed = True
    
    st.rerun()


def render_quiz_result():
    """Quiz sonucunu göster"""
    if not st.session_state.quiz_completed:
        return
    
    score = st.session_state.quiz_score
    total = len(st.session_state.quiz_questions)
    percentage = (score / total * 100) if total > 0 else 0
    
    # Grade belirleme
    if percentage == 100:
        grade = "🏆 Mükemmel!"
        grade_color = "#27ae60"
    elif percentage >= 90:
        grade = "🎯 Harika!"
        grade_color = "#2ecc71"
    elif percentage >= 70:
        grade = "👍 İyi!"
        grade_color = "#f39c12"
    elif percentage >= 50:
        grade = "📚 Fena Değil"
        grade_color = "#e67e22"
    else:
        grade = "💪 Tekrar Çalış"
        grade_color = "#e74c3c"
    
    # Sonuç kartı - Native bileşenler
    st.markdown("---")
    
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        st.markdown(f"<h1 style='text-align: center; font-size: 72px; color: #667eea;'>%{percentage:.0f}</h1>", unsafe_allow_html=True)
        st.markdown(f"<h2 style='text-align: center; color: {grade_color};'>{grade}</h2>", unsafe_allow_html=True)
    
    st.markdown("---")
    
    # İstatistikler - st.metric kullan
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("✅ Doğru", score)
    with col2:
        st.metric("❌ Yanlış", total - score)
    with col3:
        st.metric("📊 Toplam", total)
    
    # Yanlış kelimeler
    wrong_words = st.session_state.quiz_wrong_words
    if wrong_words:
        st.markdown("---")
        st.subheader("📝 Tekrar Çalışılacak Kelimeler")
        
        for word in wrong_words:
            if word:
                st.markdown(f"- **{word.get('english', '')}**: {word.get('turkish', '')}")
    
    # Aksiyonlar
    st.markdown("---")
    col1, col2 = st.columns(2)
    
    with col1:
        if st.button("🔄 Yeni Quiz", use_container_width=True):
            reset_quiz()
            st.rerun()
    
    with col2:
        if st.button("📚 Kelimelere Dön", use_container_width=True):
            reset_quiz()


def reset_quiz():
    """Quiz'i sıfırla"""
    st.session_state.quiz_active = False
    st.session_state.quiz_questions = []
    st.session_state.quiz_current_index = 0
    st.session_state.quiz_answers = []
    st.session_state.quiz_score = 0
    st.session_state.quiz_wrong_words = []
    st.session_state.quiz_completed = False


def render_quiz_setup(words: List[Dict[str, Any]]):
    """Quiz kurulum ekranı"""
    from utils.constants import QUIZ_TYPES, EXAM_TYPES, QUIZ_SETTINGS
    
    st.markdown("### ⚙️ Quiz Ayarları")
    
    col1, col2 = st.columns(2)
    
    with col1:
        quiz_type = st.selectbox(
            "Soru Türü",
            options=list(QUIZ_TYPES.keys()),
            format_func=lambda x: f"{QUIZ_TYPES[x]['icon']} {QUIZ_TYPES[x]['name']}"
        )
    
    with col2:
        question_count = st.slider(
            "Soru Sayısı",
            min_value=QUIZ_SETTINGS["min_questions"],
            max_value=min(QUIZ_SETTINGS["max_questions"], len(words)),
            value=min(QUIZ_SETTINGS["default_question_count"], len(words))
        )
    
    st.markdown("---")
    
    if st.button("🚀 Quiz'e Başla", type="primary", use_container_width=True):
        questions = generate_quiz_questions(words, question_count, quiz_type)
        if questions:
            start_quiz(questions)
            st.rerun()
        else:
            st.error("Yeterli kelime yok. En az 4 kelime gerekli.")
