"""
Gamification Service
Points, badges, and streak management
"""

import streamlit as st
from datetime import datetime, date
from typing import Dict, Any, List, Optional

from utils.constants import BADGES, POINTS
from utils.helpers import calculate_streak


def check_and_award_badges(user_data: Dict[str, Any]) -> List[str]:
    """
    Kullanıcının hak ettiği rozetleri kontrol et
    
    Args:
        user_data: Kullanıcı verileri
    
    Returns:
        Yeni kazanılan rozetlerin listesi
    """
    current_badges = user_data.get("badges", [])
    new_badges = []
    
    words_contributed = user_data.get("wordsContributed", 0)
    words_learned = user_data.get("wordsLearned", 0)
    current_streak = user_data.get("currentStreak", 0)
    high_score_quizzes = user_data.get("highScoreQuizzes", 0)
    
    # Katkı rozetleri
    if words_contributed >= 1 and "caylak" not in current_badges:
        new_badges.append("caylak")
    
    if words_contributed >= 10 and "katkici" not in current_badges:
        new_badges.append("katkici")
    
    if words_contributed >= 50 and "uzman" not in current_badges:
        new_badges.append("uzman")
    
    if words_contributed >= 100 and "efsane" not in current_badges:
        new_badges.append("efsane")
    
    # Öğrenme rozeti
    if words_learned >= 100 and "kelime_avcisi" not in current_badges:
        new_badges.append("kelime_avcisi")
    
    # Streak rozetleri
    if current_streak >= 7 and "streak_master" not in current_badges:
        new_badges.append("streak_master")
    
    if current_streak >= 30 and "streak_efsanesi" not in current_badges:
        new_badges.append("streak_efsanesi")
    
    # Quiz rozeti
    if high_score_quizzes >= 10 and "quiz_sampiyonu" not in current_badges:
        new_badges.append("quiz_sampiyonu")
    
    return new_badges


def calculate_points_for_action(action: str, extra: Dict[str, Any] = None) -> int:
    """
    Aksiyona göre puan hesapla
    
    Args:
        action: Aksiyon tipi (word_approved, quiz_complete, vb.)
        extra: Ek parametreler (örn: quiz skoru)
    
    Returns:
        Kazanılan puan
    """
    base_points = POINTS.get(action, 0)
    
    if action == "quiz_complete" and extra:
        percentage = extra.get("percentage", 0)
        if percentage == 100:
            return base_points + POINTS["quiz_perfect"]
        elif percentage >= 90:
            return base_points + POINTS["quiz_high_score"]
        elif percentage >= 70:
            return base_points + 5
        elif percentage < 50:
            return base_points // 2
    
    return base_points


def update_user_after_word_approved(user_id: str) -> Dict[str, Any]:
    """
    Kelime onaylandıktan sonra kullanıcı istatistiklerini güncelle
    
    Returns:
        Güncellenmiş veriler ve yeni rozetler
    """
    from services.firebase_service import get_user, update_user_stats, add_badge_to_user
    
    user = get_user(user_id)
    if not user:
        return {"success": False}
    
    # Puanları güncelle
    new_points = user.get("points", 0) + POINTS["word_approved"]
    new_contributed = user.get("wordsContributed", 0) + 1
    
    updates = {
        "points": new_points,
        "wordsContributed": new_contributed
    }
    
    # Rozetleri kontrol et
    user_with_updates = {**user, **updates}
    new_badges = check_and_award_badges(user_with_updates)
    
    # Güncelle
    success = update_user_stats(user_id, updates)
    
    # Yeni rozetleri ekle
    for badge_id in new_badges:
        add_badge_to_user(user_id, badge_id)
    
    return {
        "success": success,
        "points_earned": POINTS["word_approved"],
        "new_badges": new_badges
    }


def update_user_after_quiz(user_id: str, score: int, total: int) -> Dict[str, Any]:
    """
    Quiz tamamlandıktan sonra kullanıcı istatistiklerini güncelle
    
    Returns:
        Güncellenmiş veriler ve yeni rozetler
    """
    from services.firebase_service import get_user, update_user_stats, add_badge_to_user
    
    user = get_user(user_id)
    if not user:
        return {"success": False}
    
    percentage = (score / total * 100) if total > 0 else 0
    points_earned = calculate_points_for_action("quiz_complete", {"percentage": percentage})
    
    # Güncelleme verileri
    updates = {
        "points": user.get("points", 0) + points_earned,
        "quizzesTaken": user.get("quizzesTaken", 0) + 1
    }
    
    # %90+ ise high score sayısını artır
    if percentage >= 90:
        updates["highScoreQuizzes"] = user.get("highScoreQuizzes", 0) + 1
    
    # Rozetleri kontrol et
    user_with_updates = {**user, **updates}
    new_badges = check_and_award_badges(user_with_updates)
    
    # Güncelle
    success = update_user_stats(user_id, updates)
    
    # Yeni rozetleri ekle
    for badge_id in new_badges:
        add_badge_to_user(user_id, badge_id)
    
    return {
        "success": success,
        "points_earned": points_earned,
        "new_badges": new_badges,
        "percentage": percentage
    }


def update_user_streak(user_id: str) -> Dict[str, Any]:
    """
    Kullanıcı streak'ini güncelle
    
    Returns:
        Güncellenmiş streak bilgisi
    """
    from services.firebase_service import get_user, update_user_stats, add_badge_to_user
    
    user = get_user(user_id)
    if not user:
        return {"success": False}
    
    last_active = user.get("lastActiveDate")
    current_streak = user.get("currentStreak", 0)
    longest_streak = user.get("longestStreak", 0)
    
    new_streak, is_new_day = calculate_streak(last_active, current_streak)
    
    if not is_new_day:
        return {
            "success": True,
            "streak": new_streak,
            "is_new_day": False,
            "points_earned": 0,
            "new_badges": []
        }
    
    # Yeni gün - streak güncelle
    updates = {
        "currentStreak": new_streak,
        "lastActiveDate": datetime.now().isoformat(),
        "points": user.get("points", 0) + POINTS["daily_login"] + (POINTS["streak_bonus"] if new_streak > 1 else 0)
    }
    
    # En uzun streak'i güncelle
    if new_streak > longest_streak:
        updates["longestStreak"] = new_streak
    
    # Rozetleri kontrol et
    user_with_updates = {**user, **updates}
    new_badges = check_and_award_badges(user_with_updates)
    
    success = update_user_stats(user_id, updates)
    
    # Yeni rozetleri ekle
    for badge_id in new_badges:
        add_badge_to_user(user_id, badge_id)
    
    points_earned = POINTS["daily_login"]
    if new_streak > 1:
        points_earned += POINTS["streak_bonus"]
    
    return {
        "success": success,
        "streak": new_streak,
        "is_new_day": True,
        "points_earned": points_earned,
        "new_badges": new_badges
    }


def update_words_learned(user_id: str, count: int = 1) -> bool:
    """Öğrenilen kelime sayısını artır"""
    from services.firebase_service import get_user, update_user_stats, add_badge_to_user
    
    user = get_user(user_id)
    if not user:
        return False
    
    new_count = user.get("wordsLearned", 0) + count
    updates = {
        "wordsLearned": new_count,
        "points": user.get("points", 0) + (POINTS["word_learned"] * count)
    }
    
    success = update_user_stats(user_id, updates)
    
    # Kelime avcısı rozeti kontrolü
    if new_count >= 100:
        user_with_updates = {**user, **updates}
        new_badges = check_and_award_badges(user_with_updates)
        for badge_id in new_badges:
            add_badge_to_user(user_id, badge_id)
    
    return success


def get_badge_info(badge_id: str) -> Optional[Dict[str, Any]]:
    """Rozet bilgisini getir"""
    return BADGES.get(badge_id)


def get_all_badges() -> Dict[str, Dict[str, Any]]:
    """Tüm rozetleri getir"""
    return BADGES


def get_user_badge_progress(user_data: Dict[str, Any]) -> List[Dict[str, Any]]:
    """
    Kullanıcının rozet ilerleme durumunu getir
    
    Returns:
        Her rozet için ilerleme yüzdesi ve durum
    """
    current_badges = user_data.get("badges", [])
    words_contributed = user_data.get("wordsContributed", 0)
    words_learned = user_data.get("wordsLearned", 0)
    current_streak = user_data.get("currentStreak", 0)
    high_score_quizzes = user_data.get("highScoreQuizzes", 0)
    
    progress_list = []
    
    for badge_id, badge in BADGES.items():
        threshold = badge.get("threshold", 1)
        badge_type = badge.get("type", "")
        
        # İlgili değeri al
        if badge_type == "contribution":
            current_value = words_contributed
        elif badge_type == "learning":
            current_value = words_learned
        elif badge_type == "streak":
            current_value = current_streak
        elif badge_type == "quiz":
            current_value = high_score_quizzes
        else:
            current_value = 0
        
        progress = min((current_value / threshold) * 100, 100)
        is_earned = badge_id in current_badges
        
        progress_list.append({
            **badge,
            "progress": progress,
            "current_value": current_value,
            "is_earned": is_earned
        })
    
    return progress_list


def show_badge_earned_notification(badge_id: str):
    """Yeni rozet kazanıldığında bildirim göster"""
    badge = get_badge_info(badge_id)
    if badge:
        st.balloons()
        st.success(f"""
        🎉 **Tebrikler! Yeni Rozet Kazandınız!**
        
        {badge['emoji']} **{badge['name']}**
        
        {badge['description']}
        """)
