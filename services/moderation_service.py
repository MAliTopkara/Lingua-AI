"""
Moderation Service
Content moderation using OpenAI Moderation API (FREE)
"""

import streamlit as st
from typing import Dict, Any, Tuple

try:
    from openai import OpenAI
    OPENAI_AVAILABLE = True
except ImportError:
    OPENAI_AVAILABLE = False


@st.cache_resource
def get_openai_client():
    """OpenAI client'ı başlat (sadece moderation için)"""
    if not OPENAI_AVAILABLE:
        return None
    
    try:
        api_key = st.secrets.get("openai", {}).get("api_key")
        if not api_key:
            return None
        return OpenAI(api_key=api_key)
    except Exception as e:
        st.error(f"OpenAI bağlantı hatası: {str(e)}")
        return None


def check_content(text: str) -> Tuple[bool, Dict[str, Any]]:
    """
    İçeriği moderasyon kontrolünden geçir
    
    Args:
        text: Kontrol edilecek metin
    
    Returns:
        Tuple of (is_safe, details)
        - is_safe: İçerik güvenli mi
        - details: Moderasyon detayları
    """
    client = get_openai_client()
    
    # OpenAI yoksa varsayılan olarak izin ver
    if not client:
        return True, {"status": "skipped", "reason": "Moderation API mevcut değil"}
    
    try:
        response = client.moderations.create(input=text)
        
        if not response.results:
            return True, {"status": "no_results"}
        
        result = response.results[0]
        
        # Kategorileri kontrol et
        flagged_categories = []
        category_scores = {}
        
        # Kategorileri döngüyle kontrol et
        categories = result.categories
        scores = result.category_scores
        
        category_mapping = {
            "hate": "Nefret söylemi",
            "hate/threatening": "Tehditkar nefret söylemi",
            "harassment": "Taciz",
            "harassment/threatening": "Tehditkar taciz",
            "self-harm": "Kendine zarar",
            "self-harm/intent": "Kendine zarar niyeti",
            "self-harm/instructions": "Kendine zarar talimatı",
            "sexual": "Cinsel içerik",
            "sexual/minors": "Çocuklara yönelik cinsel içerik",
            "violence": "Şiddet",
            "violence/graphic": "Grafik şiddet"
        }
        
        for category, turkish_name in category_mapping.items():
            # Kategori adını attribute'a çevir (/ -> _ ve - -> _)
            attr_name = category.replace("/", "_").replace("-", "_")
            
            try:
                is_flagged = getattr(categories, attr_name, False)
                score = getattr(scores, attr_name, 0)
                
                category_scores[category] = score
                
                if is_flagged:
                    flagged_categories.append({
                        "category": category,
                        "turkish": turkish_name,
                        "score": score
                    })
            except AttributeError:
                continue
        
        is_safe = not result.flagged
        
        return is_safe, {
            "status": "checked",
            "flagged": result.flagged,
            "flagged_categories": flagged_categories,
            "category_scores": category_scores
        }
    
    except Exception as e:
        # Hata durumunda içeriğe izin ver ama uyar
        return True, {
            "status": "error",
            "error": str(e)
        }


def check_word_submission(english: str, turkish: str, example: str = "") -> Tuple[bool, str]:
    """
    Kelime ekleme isteğini kontrol et
    
    Args:
        english: İngilizce kelime
        turkish: Türkçe karşılık
        example: Örnek cümle
    
    Returns:
        Tuple of (is_safe, message)
    """
    # Tüm içeriği birleştir
    combined_text = f"{english} {turkish} {example}".strip()
    
    if not combined_text:
        return True, ""
    
    is_safe, details = check_content(combined_text)
    
    if not is_safe:
        flagged = details.get("flagged_categories", [])
        if flagged:
            categories = ", ".join([f["turkish"] for f in flagged])
            return False, f"İçerik uygunsuz bulundu: {categories}"
        return False, "İçerik moderasyon kontrolünden geçemedi."
    
    return True, ""


def check_trick_submission(title: str, content: str) -> Tuple[bool, str]:
    """
    Trick ekleme isteğini kontrol et
    
    Args:
        title: Trick başlığı
        content: Trick içeriği
    
    Returns:
        Tuple of (is_safe, message)
    """
    combined_text = f"{title}\n\n{content}".strip()
    
    if not combined_text:
        return True, ""
    
    is_safe, details = check_content(combined_text)
    
    if not is_safe:
        flagged = details.get("flagged_categories", [])
        if flagged:
            categories = ", ".join([f["turkish"] for f in flagged])
            return False, f"İçerik uygunsuz bulundu: {categories}"
        return False, "İçerik moderasyon kontrolünden geçemedi."
    
    return True, ""


def get_content_safety_score(text: str) -> float:
    """
    İçeriğin güvenlik skorunu al (0-1 arası, 1 = tamamen güvenli)
    
    Args:
        text: Kontrol edilecek metin
    
    Returns:
        Güvenlik skoru (0-1)
    """
    is_safe, details = check_content(text)
    
    if details.get("status") == "skipped":
        return 1.0
    
    if not is_safe:
        return 0.0
    
    # En yüksek kategori skorunu bul
    scores = details.get("category_scores", {})
    if scores:
        max_score = max(scores.values())
        return 1.0 - max_score
    
    return 1.0


def check_moderation_availability() -> bool:
    """Moderation API'nin kullanılabilir olup olmadığını kontrol et"""
    if not OPENAI_AVAILABLE:
        return False
    
    client = get_openai_client()
    return client is not None
