"""
Firebase Service
Firestore CRUD operations for Lingua-AI
"""

import streamlit as st
from datetime import datetime, timedelta
from typing import Optional, Dict, Any, List
import json

# Firebase Admin SDK
try:
    import firebase_admin
    from firebase_admin import credentials, firestore
    FIREBASE_AVAILABLE = True
except ImportError:
    FIREBASE_AVAILABLE = False


@st.cache_resource
def get_firebase_client():
    """
    Firebase bağlantısını başlat ve cache'le
    """
    if not FIREBASE_AVAILABLE:
        st.error("Firebase Admin SDK yüklü değil. `pip install firebase-admin` komutunu çalıştırın.")
        return None
    
    try:
        # Secrets'dan Firebase config al
        firebase_config = dict(st.secrets["firebase"])
        
        # Eğer app zaten başlatılmışsa, mevcut olanı kullan
        try:
            app = firebase_admin.get_app()
        except ValueError:
            # App başlatılmamış, yeni başlat
            cred = credentials.Certificate(firebase_config)
            app = firebase_admin.initialize_app(cred)
        
        return firestore.client()
    except Exception as e:
        st.error(f"Firebase bağlantı hatası: {str(e)}")
        return None


def get_db():
    """Firestore client'ı döndür"""
    return get_firebase_client()


# ==================== USER OPERATIONS ====================

def get_user(user_id: str) -> Optional[Dict[str, Any]]:
    """Kullanıcı bilgilerini getir"""
    db = get_db()
    if not db:
        return None
    
    try:
        doc = db.collection("users").document(user_id).get()
        if doc.exists:
            data = doc.to_dict()
            data["id"] = doc.id
            return data
        return None
    except Exception as e:
        st.error(f"Kullanıcı getirme hatası: {str(e)}")
        return None


def signup_user(email: str, password: str, display_name: str) -> Dict[str, Any]:
    """
    Yeni kullanıcı kaydı oluştur
    
    Returns:
        {"success": True, "user_id": "..."} veya {"success": False, "error": "..."}
    """
    import hashlib
    
    db = get_db()
    if not db:
        return {"success": False, "error": "Veritabanı bağlantısı kurulamadı"}
    
    email = email.strip().lower()
    
    try:
        # Email zaten kayıtlı mı kontrol et
        existing = db.collection("users").where("email", "==", email).limit(1).stream()
        if any(True for _ in existing):
            return {"success": False, "error": "Bu e-posta adresi zaten kayıtlı"}
        
        # Kullanıcı ID oluştur
        user_id = hashlib.md5(email.encode()).hexdigest()[:20]
        
        # Şifreyi hashle
        password_hash = hashlib.sha256(password.encode()).hexdigest()
        
        # Kullanıcı verisi
        user_data = {
            "email": email,
            "passwordHash": password_hash,
            "displayName": display_name,
            "photoURL": f"https://ui-avatars.com/api/?name={display_name.replace(' ', '+')}&background=667eea&color=fff&size=128",
            "role": "user",
            "points": 0,
            "badges": [],
            "wordsLearned": 0,
            "wordsContributed": 0,
            "quizzesTaken": 0,
            "highScoreQuizzes": 0,
            "currentStreak": 0,
            "longestStreak": 0,
            "lastActiveDate": None,
            "createdAt": firestore.SERVER_TIMESTAMP,
            "updatedAt": firestore.SERVER_TIMESTAMP
        }
        
        # Firestore'a kaydet
        db.collection("users").document(user_id).set(user_data)
        
        return {"success": True, "user_id": user_id}
        
    except Exception as e:
        return {"success": False, "error": str(e)}


def authenticate_user(email: str, password: str) -> Dict[str, Any]:
    """
    Kullanıcı girişini doğrula
    
    Returns:
        {"success": True, "user": {...}} veya {"success": False, "error": "..."}
    """
    import hashlib
    
    db = get_db()
    if not db:
        return {"success": False, "error": "Veritabanı bağlantısı kurulamadı"}
    
    email = email.strip().lower()
    
    try:
        # Kullanıcıyı email ile bul
        users = db.collection("users").where("email", "==", email).limit(1).stream()
        user_doc = None
        for doc in users:
            user_doc = doc
            break
        
        if not user_doc:
            return {"success": False, "error": "Kullanıcı bulunamadı"}
        
        user_data = user_doc.to_dict()
        user_data["id"] = user_doc.id
        
        # Şifre kontrolü
        password_hash = hashlib.sha256(password.encode()).hexdigest()
        stored_hash = user_data.get("passwordHash", "")
        
        if password_hash != stored_hash:
            return {"success": False, "error": "Şifre hatalı"}
        
        # Şifre hash'ini dönüşten çıkar
        user_data.pop("passwordHash", None)
        
        return {"success": True, "user": user_data}
        
    except Exception as e:
        return {"success": False, "error": str(e)}


def update_user_name(user_id: str, new_name: str) -> Dict[str, Any]:
    """
    Kullanıcı adını güncelle
    
    Returns:
        {"success": True} veya {"success": False, "error": "..."}
    """
    db = get_db()
    if not db:
        return {"success": False, "error": "Veritabanı bağlantısı kurulamadı"}
    
    try:
        db.collection("users").document(user_id).update({
            "displayName": new_name.strip(),
            "photoURL": f"https://ui-avatars.com/api/?name={new_name.replace(' ', '+')}&background=667eea&color=fff&size=128",
            "updatedAt": firestore.SERVER_TIMESTAMP
        })
        return {"success": True}
    except Exception as e:
        return {"success": False, "error": str(e)}


def change_user_password(user_id: str, new_password: str) -> Dict[str, Any]:
    """
    Kullanıcı şifresini değiştir
    
    Returns:
        {"success": True} veya {"success": False, "error": "..."}
    """
    import hashlib
    
    db = get_db()
    if not db:
        return {"success": False, "error": "Veritabanı bağlantısı kurulamadı"}
    
    try:
        # Yeni şifreyi hashle
        password_hash = hashlib.sha256(new_password.encode()).hexdigest()
        
        db.collection("users").document(user_id).update({
            "passwordHash": password_hash,
            "updatedAt": firestore.SERVER_TIMESTAMP
        })
        return {"success": True}
    except Exception as e:
        return {"success": False, "error": str(e)}


def update_user_role(user_id: str, new_role: str) -> bool:
    """
    Kullanıcı rolünü güncelle (user/admin)
    
    Args:
        user_id: Kullanıcı ID
        new_role: Yeni rol ('user' veya 'admin')
    
    Returns:
        True başarılı, False başarısız
    """
    db = get_db()
    if not db:
        return False
    
    try:
        db.collection("users").document(user_id).update({
            "role": new_role,
            "updatedAt": firestore.SERVER_TIMESTAMP
        })
        return True
    except Exception as e:
        st.error(f"Rol güncelleme hatası: {str(e)}")
        return False


def create_or_update_user(user_id: str, user_data: Dict[str, Any]) -> bool:
    """Kullanıcı oluştur veya güncelle"""
    db = get_db()
    if not db:
        return False
    
    try:
        user_ref = db.collection("users").document(user_id)
        existing = user_ref.get()
        
        if existing.exists:
            # Mevcut kullanıcıyı güncelle
            update_data = {
                "displayName": user_data.get("displayName"),
                "photoURL": user_data.get("photoURL"),
                "updatedAt": firestore.SERVER_TIMESTAMP
            }
            user_ref.update(update_data)
        else:
            # Yeni kullanıcı oluştur
            new_user = {
                "email": user_data.get("email"),
                "displayName": user_data.get("displayName"),
                "photoURL": user_data.get("photoURL"),
                "role": "user",
                "points": 0,
                "badges": [],
                "wordsLearned": 0,
                "wordsContributed": 0,
                "quizzesTaken": 0,
                "highScoreQuizzes": 0,
                "currentStreak": 0,
                "longestStreak": 0,
                "lastActiveDate": None,
                "createdAt": firestore.SERVER_TIMESTAMP,
                "updatedAt": firestore.SERVER_TIMESTAMP
            }
            user_ref.set(new_user)
        
        return True
    except Exception as e:
        st.error(f"Kullanıcı kaydetme hatası: {str(e)}")
        return False


def update_user_stats(user_id: str, updates: Dict[str, Any]) -> bool:
    """Kullanıcı istatistiklerini güncelle"""
    db = get_db()
    if not db:
        return False
    
    try:
        updates["updatedAt"] = firestore.SERVER_TIMESTAMP
        db.collection("users").document(user_id).update(updates)
        return True
    except Exception as e:
        st.error(f"İstatistik güncelleme hatası: {str(e)}")
        return False


def add_badge_to_user(user_id: str, badge_id: str) -> bool:
    """Kullanıcıya rozet ekle"""
    db = get_db()
    if not db:
        return False
    
    try:
        db.collection("users").document(user_id).update({
            "badges": firestore.ArrayUnion([badge_id]),
            "updatedAt": firestore.SERVER_TIMESTAMP
        })
        return True
    except Exception as e:
        st.error(f"Rozet ekleme hatası: {str(e)}")
        return False


def get_leaderboard(period: str = "all_time", limit: int = 10) -> List[Dict[str, Any]]:
    """Liderlik tablosunu getir"""
    db = get_db()
    if not db:
        return []
    
    try:
        query = db.collection("users").order_by("points", direction=firestore.Query.DESCENDING).limit(limit)
        
        # Dönem filtresi (basit implementasyon - gerçek uygulamada daha karmaşık olabilir)
        # Bu örnekte tüm zamanlar için sıralama yapıyoruz
        
        docs = query.stream()
        users = []
        for doc in docs:
            data = doc.to_dict()
            data["id"] = doc.id
            users.append(data)
        
        return users
    except Exception as e:
        st.error(f"Liderlik tablosu hatası: {str(e)}")
        return []


def is_user_admin(user_email: str) -> bool:
    """Kullanıcının admin olup olmadığını kontrol et"""
    try:
        admin_emails = st.secrets.get("admin", {}).get("emails", [])
        return user_email in admin_emails
    except:
        return False


# ==================== WORD OPERATIONS ====================

@st.cache_data(ttl=120)  # 2 dakika cache
def _get_words_cached(
    status: str = "approved",
    exam_type: str = None,
    difficulty: int = None,
    limit: int = 100
) -> List[Dict[str, Any]]:
    """Kelimeleri getir (cached internal)"""
    db = get_db()
    if not db:
        return []
    
    try:
        query = db.collection("words").where("status", "==", status)
        
        # Sınav türü filtresi
        if exam_type and exam_type != "all":
            query = query.where("examTypes", "array_contains", exam_type)
        
        # Zorluk filtresi
        if difficulty and difficulty != "all":
            query = query.where("difficulty", "==", int(difficulty))
        
        query = query.limit(limit)
        docs = query.stream()
        
        words = []
        for doc in docs:
            data = doc.to_dict()
            data["id"] = doc.id
            words.append(data)
        
        return words
    except Exception as e:
        return []


def get_words(
    status: str = "approved",
    exam_type: Optional[str] = None,
    difficulty: Optional[int] = None,
    limit: int = 100,
    search_query: Optional[str] = None
) -> List[Dict[str, Any]]:
    """Kelimeleri getir (search client-side)"""
    # Cached fonksiyonu çağır
    words = _get_words_cached(status, exam_type, difficulty, limit)
    
    # Arama filtresi (client-side)
    if search_query:
        search_lower = search_query.lower()
        words = [w for w in words if (
            search_lower in w.get("english", "").lower() or 
            search_lower in w.get("turkish", "").lower()
        )]
    
    return words


def get_word(word_id: str) -> Optional[Dict[str, Any]]:
    """Tek bir kelimeyi getir"""
    db = get_db()
    if not db:
        return None
    
    try:
        doc = db.collection("words").document(word_id).get()
        if doc.exists:
            data = doc.to_dict()
            data["id"] = doc.id
            return data
        return None
    except Exception as e:
        st.error(f"Kelime getirme hatası: {str(e)}")
        return None


def add_word(word_data: Dict[str, Any]) -> Optional[str]:
    """Yeni kelime ekle"""
    db = get_db()
    if not db:
        return None
    
    try:
        word_data["createdAt"] = firestore.SERVER_TIMESTAMP
        word_data["updatedAt"] = firestore.SERVER_TIMESTAMP
        word_data["status"] = "pending"
        
        doc_ref = db.collection("words").add(word_data)
        return doc_ref[1].id
    except Exception as e:
        st.error(f"Kelime ekleme hatası: {str(e)}")
        return None


def update_word(word_id: str, updates: Dict[str, Any]) -> bool:
    """Kelimeyi güncelle"""
    db = get_db()
    if not db:
        return False
    
    try:
        updates["updatedAt"] = firestore.SERVER_TIMESTAMP
        db.collection("words").document(word_id).update(updates)
        return True
    except Exception as e:
        st.error(f"Kelime güncelleme hatası: {str(e)}")
        return False


def approve_word(word_id: str, admin_id: str) -> bool:
    """Kelimeyi onayla"""
    return update_word(word_id, {
        "status": "approved",
        "approvedBy": admin_id
    })


def reject_word(word_id: str, admin_id: str, reason: str = "") -> bool:
    """Kelimeyi reddet"""
    return update_word(word_id, {
        "status": "rejected",
        "rejectedBy": admin_id,
        "rejectionReason": reason
    })


def get_pending_words(limit: int = 50) -> List[Dict[str, Any]]:
    """Bekleyen kelimeleri getir"""
    return get_words(status="pending", limit=limit)


def get_random_words(count: int = 4, exclude_ids: List[str] = None) -> List[Dict[str, Any]]:
    """Rastgele kelimeler getir (quiz için)"""
    db = get_db()
    if not db:
        return []
    
    try:
        # Basit implementasyon - tüm onaylı kelimeleri al ve rastgele seç
        words = get_words(status="approved", limit=200)
        
        if exclude_ids:
            words = [w for w in words if w["id"] not in exclude_ids]
        
        import random
        if len(words) >= count:
            return random.sample(words, count)
        return words
    except Exception as e:
        st.error(f"Rastgele kelime hatası: {str(e)}")
        return []


def check_word_exists(english: str) -> bool:
    """Kelimenin zaten var olup olmadığını kontrol et"""
    db = get_db()
    if not db:
        return False
    
    try:
        docs = db.collection("words").where("english", "==", english.lower().strip()).limit(1).stream()
        return any(True for _ in docs)
    except:
        return False


# ==================== TRICK OPERATIONS ====================

def get_tricks(
    status: str = "approved",
    category: Optional[str] = None,
    limit: int = 50
) -> List[Dict[str, Any]]:
    """Trick'leri getir"""
    db = get_db()
    if not db:
        return []
    
    try:
        query = db.collection("tricks").where("status", "==", status)
        
        if category and category != "all":
            query = query.where("category", "==", category)
        
        query = query.limit(limit)
        docs = query.stream()
        
        tricks = []
        for doc in docs:
            data = doc.to_dict()
            data["id"] = doc.id
            tricks.append(data)
        
        return tricks
    except Exception as e:
        st.error(f"Trick getirme hatası: {str(e)}")
        return []


def add_trick(trick_data: Dict[str, Any]) -> Optional[str]:
    """Yeni trick ekle"""
    db = get_db()
    if not db:
        return None
    
    try:
        trick_data["createdAt"] = firestore.SERVER_TIMESTAMP
        trick_data["status"] = "pending"
        trick_data["upvotes"] = 0
        trick_data["downvotes"] = 0
        
        doc_ref = db.collection("tricks").add(trick_data)
        return doc_ref[1].id
    except Exception as e:
        st.error(f"Trick ekleme hatası: {str(e)}")
        return None


def approve_trick(trick_id: str, admin_id: str) -> bool:
    """Trick'i onayla"""
    db = get_db()
    if not db:
        return False
    
    try:
        db.collection("tricks").document(trick_id).update({
            "status": "approved",
            "approvedBy": admin_id,
            "updatedAt": firestore.SERVER_TIMESTAMP
        })
        return True
    except Exception as e:
        st.error(f"Trick onaylama hatası: {str(e)}")
        return False


def get_pending_tricks(limit: int = 50) -> List[Dict[str, Any]]:
    """Bekleyen trick'leri getir"""
    return get_tricks(status="pending", limit=limit)


# ==================== QUIZ OPERATIONS ====================

def save_quiz_result(result_data: Dict[str, Any]) -> Optional[str]:
    """Quiz sonucunu kaydet"""
    db = get_db()
    if not db:
        return None
    
    try:
        result_data["completedAt"] = firestore.SERVER_TIMESTAMP
        doc_ref = db.collection("quiz_results").add(result_data)
        return doc_ref[1].id
    except Exception as e:
        st.error(f"Quiz sonucu kaydetme hatası: {str(e)}")
        return None


def get_user_quiz_results(user_id: str, limit: int = 10) -> List[Dict[str, Any]]:
    """Kullanıcının quiz sonuçlarını getir"""
    db = get_db()
    if not db:
        return []
    
    try:
        docs = db.collection("quiz_results")\
            .where("userId", "==", user_id)\
            .order_by("completedAt", direction=firestore.Query.DESCENDING)\
            .limit(limit)\
            .stream()
        
        results = []
        for doc in docs:
            data = doc.to_dict()
            data["id"] = doc.id
            results.append(data)
        
        return results
    except Exception as e:
        st.error(f"Quiz sonuçları getirme hatası: {str(e)}")
        return []


# ==================== STATISTICS ====================

@st.cache_data(ttl=300)  # 5 dakika cache
def get_app_stats() -> Dict[str, Any]:
    """Uygulama istatistiklerini getir (5 dk cache)"""
    db = get_db()
    if not db:
        return {
            "total_words": 0,
            "total_users": 0,
            "total_quizzes": 0,
            "pending_words": 0
        }
    
    try:
        # Bu basit bir implementasyon - gerçek uygulamada aggregation kullanılabilir
        words = list(db.collection("words").where("status", "==", "approved").stream())
        users = list(db.collection("users").stream())
        quizzes = list(db.collection("quiz_results").stream())
        pending = list(db.collection("words").where("status", "==", "pending").stream())
        
        return {
            "total_words": len(words),
            "total_users": len(users),
            "total_quizzes": len(quizzes),
            "pending_words": len(pending)
        }
    except Exception as e:
        return {
            "total_words": 0,
            "total_users": 0,
            "total_quizzes": 0,
            "pending_words": 0
        }


def initialize_words_from_json(json_path: str) -> int:
    """JSON dosyasından başlangıç kelimelerini yükle"""
    db = get_db()
    if not db:
        return 0
    
    try:
        with open(json_path, 'r', encoding='utf-8') as f:
            words = json.load(f)
        
        count = 0
        for word in words:
            # Kelime zaten var mı kontrol et
            if not check_word_exists(word.get("english", "")):
                word_data = {
                    "english": word.get("english", "").lower().strip(),
                    "turkish": word.get("turkish", ""),
                    "type": word.get("type", "noun"),
                    "synonyms": word.get("synonyms", []),
                    "antonyms": word.get("antonyms", []),
                    "exampleSentence": word.get("exampleSentence", ""),
                    "difficulty": word.get("difficulty", 3),
                    "examTypes": word.get("examTypes", ["genel"]),
                    "status": "approved",
                    "addedBy": "system",
                    "addedByName": "Lingua-AI",
                    "createdAt": firestore.SERVER_TIMESTAMP,
                    "updatedAt": firestore.SERVER_TIMESTAMP
                }
                db.collection("words").add(word_data)
                count += 1
        
        return count
    except Exception as e:
        st.error(f"Kelime yükleme hatası: {str(e)}")
        return 0
