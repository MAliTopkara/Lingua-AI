"""
Badges Component
Badge display and progress tracking
"""

import streamlit as st
from typing import Dict, Any, List


def get_badge_styles() -> str:
    """Badge için CSS stilleri"""
    return """
    <style>
    .badges-grid {
        display: grid;
        grid-template-columns: repeat(auto-fill, minmax(150px, 1fr));
        gap: 16px;
        margin: 20px 0;
    }
    
    .badge-card {
        background: linear-gradient(135deg, #1a1f2e 0%, #2d3748 100%);
        border: 2px solid rgba(102, 126, 234, 0.3);
        border-radius: 16px;
        padding: 20px;
        text-align: center;
        transition: all 0.3s ease;
    }
    
    .badge-card:hover {
        border-color: #667eea;
        transform: translateY(-3px);
    }
    
    .badge-card.earned {
        border-color: #667eea;
        background: linear-gradient(135deg, rgba(102, 126, 234, 0.2) 0%, rgba(118, 75, 162, 0.2) 100%);
    }
    
    .badge-card.locked {
        opacity: 0.5;
        filter: grayscale(50%);
    }
    
    .badge-emoji {
        font-size: 48px;
        margin-bottom: 12px;
    }
    
    .badge-name {
        font-size: 16px;
        font-weight: 600;
        color: #fff;
        margin-bottom: 8px;
    }
    
    .badge-description {
        font-size: 12px;
        color: #a0aec0;
        line-height: 1.4;
    }
    
    .badge-progress {
        margin-top: 12px;
        background: rgba(255,255,255,0.1);
        border-radius: 10px;
        height: 6px;
        overflow: hidden;
    }
    
    .badge-progress-bar {
        height: 100%;
        background: linear-gradient(90deg, #667eea, #764ba2);
        border-radius: 10px;
        transition: width 0.5s ease;
    }
    
    .badge-progress-text {
        font-size: 11px;
        color: #667eea;
        margin-top: 6px;
    }
    
    /* Rozet vitrin */
    .badge-showcase {
        display: flex;
        flex-wrap: wrap;
        gap: 8px;
        justify-content: center;
    }
    
    .badge-showcase-item {
        font-size: 32px;
        padding: 8px;
        background: rgba(102, 126, 234, 0.1);
        border-radius: 12px;
        transition: transform 0.2s ease;
    }
    
    .badge-showcase-item:hover {
        transform: scale(1.2);
    }
    
    /* Mini rozet */
    .badge-mini {
        display: inline-flex;
        align-items: center;
        gap: 4px;
        background: rgba(102, 126, 234, 0.2);
        padding: 4px 10px;
        border-radius: 20px;
        font-size: 13px;
    }
    </style>
    """


def render_badge_card(badge: Dict[str, Any], is_earned: bool = False, progress: float = 0, current_value: int = 0):
    """
    Tek rozet kartı render et
    
    Args:
        badge: Rozet bilgisi
        is_earned: Kazanıldı mı
        progress: İlerleme yüzdesi
        current_value: Mevcut değer
    """
    status_class = "earned" if is_earned else "locked"
    
    progress_html = ""
    if not is_earned and progress > 0:
        progress_html = f"""
        <div class="badge-progress">
            <div class="badge-progress-bar" style="width: {progress}%;"></div>
        </div>
        <div class="badge-progress-text">{current_value} / {badge.get('threshold', 0)}</div>
        """
    elif is_earned:
        progress_html = '<div class="badge-progress-text" style="color: #27ae60;">✓ Kazanıldı!</div>'
    
    st.markdown(f"""
    <div class="badge-card {status_class}">
        <div class="badge-emoji">{badge.get('emoji', '🏅')}</div>
        <div class="badge-name">{badge.get('name', '')}</div>
        <div class="badge-description">{badge.get('description', '')}</div>
        {progress_html}
    </div>
    """, unsafe_allow_html=True)


def render_badges_grid(user_data: Dict[str, Any]):
    """
    Tüm rozetleri grid olarak göster
    
    Args:
        user_data: Kullanıcı verileri
    """
    from services.gamification_service import get_user_badge_progress
    
    st.markdown(get_badge_styles(), unsafe_allow_html=True)
    
    badge_progress = get_user_badge_progress(user_data)
    
    # Grid için sütunlar
    cols = st.columns(4)
    
    for i, badge in enumerate(badge_progress):
        with cols[i % 4]:
            render_badge_card(
                badge,
                is_earned=badge.get("is_earned", False),
                progress=badge.get("progress", 0),
                current_value=badge.get("current_value", 0)
            )


def render_badge_showcase(badges: List[str], max_display: int = 8):
    """
    Kazanılan rozetleri vitrin olarak göster
    
    Args:
        badges: Rozet ID listesi
        max_display: Maksimum gösterilecek rozet sayısı
    """
    from utils.constants import BADGES
    
    st.markdown(get_badge_styles(), unsafe_allow_html=True)
    
    if not badges:
        st.info("Henüz rozet kazanılmadı. Kelime ekleyerek ve quiz çözerek rozet kazanabilirsiniz!")
        return
    
    display_badges = badges[:max_display]
    remaining = len(badges) - max_display
    
    badge_html = ""
    for badge_id in display_badges:
        badge = BADGES.get(badge_id, {})
        emoji = badge.get("emoji", "🏅")
        name = badge.get("name", "")
        badge_html += f'<span class="badge-showcase-item" title="{name}">{emoji}</span>'
    
    if remaining > 0:
        badge_html += f'<span class="badge-showcase-item" title="{remaining} rozet daha">+{remaining}</span>'
    
    st.markdown(f"""
    <div class="badge-showcase">
        {badge_html}
    </div>
    """, unsafe_allow_html=True)


def render_badge_mini(badge_id: str):
    """
    Mini rozet gösterimi (profil kartı için)
    
    Args:
        badge_id: Rozet ID
    """
    from utils.constants import BADGES
    
    badge = BADGES.get(badge_id, {})
    
    st.markdown(f"""
    <span class="badge-mini">
        {badge.get('emoji', '🏅')} {badge.get('name', '')}
    </span>
    """, unsafe_allow_html=True)


def render_user_profile_card(user_data: Dict[str, Any]):
    """
    Kullanıcı profil kartı - Streamlit native componentleri kullanarak
    
    Args:
        user_data: Kullanıcı verileri
    """
    from utils.helpers import get_level_from_points
    
    level_info = get_level_from_points(user_data.get("points", 0))
    
    # Profil başlığı - sade HTML
    st.markdown(f'''
    <div style="display: flex; align-items: center; gap: 15px; margin-bottom: 20px;">
        <img src="{user_data.get('photoURL', '')}" style="width: 60px; height: 60px; border-radius: 50%;">
        <div>
            <div style="font-size: 20px; font-weight: 700;">{user_data.get('displayName', 'Kullanıcı')}</div>
            <div style="font-size: 14px; color: #a0aec0;">{level_info['icon']} Seviye {level_info['level']}: {level_info['name']}</div>
        </div>
    </div>
    ''', unsafe_allow_html=True)
    
    # İstatistikler - Streamlit columns
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("⭐ Puan", user_data.get('points', 0))
    with col2:
        st.metric("🔥 Streak", user_data.get('currentStreak', 0))
    with col3:
        st.metric("📚 Öğrenilen", user_data.get('wordsLearned', 0))
    with col4:
        st.metric("✍️ Eklenen", user_data.get('wordsContributed', 0))
    
    # İlerleme çubuğu
    progress = level_info.get('progress', 0) / 100
    st.progress(progress)
    st.caption(f"Sonraki seviye için {level_info.get('points_to_next', 0)} puan gerekli")


def render_leaderboard_row(rank: int, user: Dict[str, Any], is_current_user: bool = False):
    """
    Liderlik tablosu satırı
    
    Args:
        rank: Sıralama
        user: Kullanıcı verileri
        is_current_user: Mevcut kullanıcı mı
    """
    from utils.constants import BADGES
    
    # Sıralama ikonları
    rank_icons = {1: "🥇", 2: "🥈", 3: "🥉"}
    rank_display = rank_icons.get(rank, f"#{rank}")
    
    # Rozetler
    badges = user.get("badges", [])[:3]
    badge_emojis = " ".join([BADGES.get(b, {}).get("emoji", "") for b in badges])
    
    bg_color = "rgba(102, 126, 234, 0.2)" if is_current_user else "transparent"
    
    cols = st.columns([0.5, 0.5, 3, 1.5, 1.5, 1])
    
    with cols[0]:
        st.markdown(f"**{rank_display}**")
    
    with cols[1]:
        st.image(user.get("photoURL", "https://ui-avatars.com/api/?name=U"), width=35)
    
    with cols[2]:
        name = user.get("displayName", "Kullanıcı")
        if is_current_user:
            name += " (Sen)"
        st.markdown(f"**{name}**")
    
    with cols[3]:
        st.markdown(f"⭐ {user.get('points', 0)}")
    
    with cols[4]:
        st.markdown(f"🔥 {user.get('currentStreak', 0)}")
    
    with cols[5]:
        st.markdown(badge_emojis or "-")
