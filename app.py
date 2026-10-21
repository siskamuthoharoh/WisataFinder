
from pathlib import Path

import pandas as pd
import streamlit as st
import requests
import re
from urllib.parse import quote
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity


# =====================================================
# CONFIGURATION
# =====================================================
st.set_page_config(
    page_title="WisataFinder | Explore Indonesia",
    page_icon="🌿",
    layout="wide",
    initial_sidebar_state="collapsed",
)

BASE_DIR = Path(__file__).resolve().parent
DATA_PATH = BASE_DIR / "data" / "processed" / "destinations_clean.csv"


# =====================================================
# CUSTOM DESIGN
# =====================================================
st.markdown(
    """
    <style>
    @import url('https://fonts.googleapis.com/css2?family=DM+Sans:wght@400;500;600;700&family=Playfair+Display:wght@500;600;700&display=swap');

    :root {
        --forest: #214E3D;
        --forest-dark: #17372C;
        --cream: #F7F6F0;
        --paper: #FFFFFF;
        --muted: #6F7D73;
        --terracotta: #B96F4C;
        --border: #E4E7DF;
    }

    .stApp {
        background: var(--cream);
        font-family: 'DM Sans', sans-serif;
    }

    [data-testid="stHeader"] {
        background: rgba(247,246,240,0.92);
    }

    .block-container {
        max-width: 1180px;
        padding-top: 1.5rem;
        padding-bottom: 3rem;
    }

    #MainMenu, footer {
        visibility: hidden;
    }

    [data-testid="stToolbar"] {
        visibility: hidden;
    }

    .brand {
        display: flex;
        align-items: center;
        gap: 12px;
        margin-bottom: 1.5rem;
    }

    .brand-icon {
        background: var(--forest);
        color: white;
        width: 46px;
        height: 46px;
        display: flex;
        justify-content: center;
        align-items: center;
        border-radius: 14px;
        font-size: 24px;
    }

    .brand-name {
        font-size: 1.45rem;
        font-weight: 700;
        color: var(--forest);
        letter-spacing: -0.7px;
    }

    .brand-caption {
        color: var(--muted);
        font-size: 0.68rem;
        letter-spacing: 2px;
    }

    .hero {
        background:
            linear-gradient(90deg,
                rgba(19, 47, 36, 0.92) 0%,
                rgba(19, 47, 36, 0.75) 48%,
                rgba(19, 47, 36, 0.10) 100%),
            url('https://images.unsplash.com/photo-1516690561799-46d8f74f9abf?auto=format&fit=crop&w=1800&q=85');
        background-position: center;
        background-size: cover;
        border-radius: 24px;
        padding: 4rem 3rem;
        min-height: 330px;
        display: flex;
        flex-direction: column;
        justify-content: center;
        margin-bottom: 1.4rem;
    }

    .hero-eyebrow {
        color: #E8C8A7;
        font-size: 0.73rem;
        letter-spacing: 2.5px;
        font-weight: 700;
        margin-bottom: 1rem;
    }

    .hero h1 {
        font-family: 'Playfair Display', Georgia, serif;
        font-size: clamp(2.4rem, 5vw, 4rem);
        line-height: 1.12;
        font-weight: 600;
        color: white;
        max-width: 650px;
        margin: 0 0 1rem 0;
    }

    .hero p {
        color: #F0F2EC;
        font-size: 1rem;
        line-height: 1.8;
        max-width: 520px;
        margin: 0;
    }

    .search-panel {
        background: white;
        border: 1px solid var(--border);
        border-radius: 18px;
        padding: 1.5rem;
        margin-bottom: 1.5rem;
        box-shadow: 0 10px 30px rgba(33,78,61,0.045);
    }

    .section-eyebrow {
        color: var(--terracotta);
        font-size: 0.70rem;
        letter-spacing: 2px;
        font-weight: 700;
        margin-bottom: 0.5rem;
    }

    .section-title {
        font-family: 'Playfair Display', Georgia, serif;
        color: var(--forest);
        font-size: 2rem;
        font-weight: 600;
        line-height: 1.3;
        margin: 0 0 0.4rem 0;
    }

    .section-subtitle {
        color: var(--muted);
        font-size: 0.92rem;
        line-height: 1.7;
        margin-bottom: 1.4rem;
    }

    [data-testid="stTextInput"] input,
    [data-testid="stSelectbox"] div[data-baseweb="select"] > div {
        border-radius: 11px;
        border-color: var(--border);
        background: #FFFFFF;
        min-height: 44px;
    }

    [data-testid="stTextInput"] label,
    [data-testid="stSelectbox"] label {
        color: var(--forest);
        font-weight: 600;
    }

    .stButton > button,
    [data-testid="stFormSubmitButton"] button {
        background: var(--forest);
        color: white;
        border: 1px solid var(--forest);
        border-radius: 11px;
        min-height: 46px;
        font-weight: 600;
        transition: all 0.2s ease;
    }

    .stButton > button:hover,
    [data-testid="stFormSubmitButton"] button:hover {
        background: var(--forest-dark);
        color: white;
        border-color: var(--forest-dark);
        transform: translateY(-1px);
    }

    [data-testid="stMetric"] {
        background: white;
        border: 1px solid var(--border);
        padding: 1.15rem;
        border-radius: 15px;
    }

    [data-testid="stMetricLabel"] {
        color: var(--muted);
    }

    [data-testid="stMetricValue"] {
        color: var(--forest);
    }

    .result-card {
        background: white;
        border: 1px solid var(--border);
        border-radius: 16px;
        padding: 1.25rem;
        margin-bottom: 0.85rem;
        transition: border-color 0.2s ease;
    }

    .result-card:hover {
        border-color: #A8BCAF;
    }

    .result-number {
        color: var(--terracotta);
        font-size: 0.72rem;
        font-weight: 700;
        letter-spacing: 1.4px;
        margin-bottom: 0.4rem;
    }

    .result-title {
        color: var(--forest);
        font-size: 1.22rem;
        font-weight: 700;
        margin-bottom: 0.5rem;
        line-height: 1.4;
    }

    .result-meta {
        color: var(--muted);
        font-size: 0.82rem;
        margin-bottom: 0.75rem;
    }

    .result-description {
        color: #536158;
        font-size: 0.91rem;
        line-height: 1.75;
    }

    .score {
        display: inline-block;
        color: var(--forest);
        background: #EDF3ED;
        border-radius: 8px;
        padding: 6px 10px;
        font-size: 0.78rem;
        font-weight: 700;
        margin-top: 0.6rem;
    }

    .inspiration-card {
        background: white;
        border: 1px solid var(--border);
        border-radius: 15px;
        padding: 1.2rem;
        height: 100%;
    }

    .inspiration-icon {
        font-size: 1.8rem;
        margin-bottom: 0.6rem;
    }

    .inspiration-card h3 {
        color: var(--forest);
        font-size: 1.05rem;
        margin: 0 0 0.4rem 0;
    }

    .inspiration-card p {
        color: var(--muted);
        font-size: 0.86rem;
        line-height: 1.7;
        margin: 0;
    }

    .footer {
        text-align: center;
        color: var(--muted);
        font-size: 0.8rem;
        border-top: 1px solid var(--border);
        margin-top: 3rem;
        padding-top: 1.5rem;
        line-height: 1.8;
    }

    @media (max-width: 700px) {
        .block-container {
            padding-left: 1rem;
            padding-right: 1rem;
        }

        .hero {
            padding: 2.2rem 1.4rem;
            min-height: 280px;
            border-radius: 18px;
        }

        .hero h1 {
            font-size: 2.45rem;
        }

        .section-title {
            font-size: 1.65rem;
        }
    }
    
/* Fix: hero text visibility */
.hero {
    position: relative;
    isolation: isolate;
    overflow: hidden;
    background-color: #214E3D;
}

.hero::before {
    content: "";
    position: absolute;
    inset: 0;
    z-index: -1;
    background: linear-gradient(
        90deg,
        rgba(19, 47, 36, 0.97) 0%,
        rgba(19, 47, 36, 0.88) 60%,
        rgba(19, 47, 36, 0.45) 100%
    );
    border-radius: inherit;
}

.hero h1 {
    color: #FFFFFF !important;
    position: relative;
    z-index: 1;
    text-shadow: 0 2px 8px rgba(0, 0, 0, 0.25);
}

.hero p {
    color: #F5F7F2 !important;
    position: relative;
    z-index: 1;
}

.hero-eyebrow {
    color: #F2C9A9 !important;
    position: relative;
    z-index: 1;
}

/* Fix: search labels and input text */
[data-testid="stTextInput"] label,
[data-testid="stSelectbox"] label {
    color: #214E3D !important;
    font-size: 0.95rem !important;
    font-weight: 700 !important;
    opacity: 1 !important;
}

[data-testid="stTextInput"] input {
    color: #214E3D !important;
    background: #FFFFFF !important;
    -webkit-text-fill-color: #214E3D !important;
    border: 1px solid #C9D5CC !important;
}

[data-testid="stTextInput"] input::placeholder {
    color: #77847B !important;
    -webkit-text-fill-color: #77847B !important;
    opacity: 1 !important;
}

[data-testid="stSelectbox"] div[data-baseweb="select"] {
    color: #214E3D !important;
    background: #FFFFFF !important;
}

/* Keep search area readable */
[data-testid="stForm"] {
    background: #FFFFFF;
    border: 1px solid #E4E7DF;
    border-radius: 16px;
    padding: 1.25rem;
}

[data-testid="stForm"] label {
    color: #214E3D !important;
    opacity: 1 !important;
}

/* Fix brand header visibility */
.brand {
    position: relative;
    z-index: 10;
    display: flex;
    align-items: center;
    gap: 14px;
    padding: 12px 16px;
    margin-bottom: 1.5rem;
    background: #FFFFFF;
    border: 1px solid #E4E7DF;
    border-radius: 16px;
    box-shadow: 0 4px 16px rgba(33, 78, 61, 0.06);
}

.brand-icon {
    flex-shrink: 0;
    background: #214E3D !important;
    color: #FFFFFF !important;
    width: 48px;
    height: 48px;
    display: flex;
    justify-content: center;
    align-items: center;
    border-radius: 14px;
    font-size: 26px;
}

.brand-name {
    color: #214E3D !important;
    font-size: 1.45rem;
    line-height: 1.4;
    font-weight: 700;
    letter-spacing: -0.5px;
    opacity: 1 !important;
    visibility: visible !important;
}

.brand-caption {
    color: #64756A !important;
    font-size: 0.68rem;
    line-height: 1.5;
    letter-spacing: 2px;
    font-weight: 600;
    opacity: 1 !important;
    visibility: visible !important;
}

/* ===== SEARCH: HIGH CONTRAST & READABILITY ===== */

/* Label kata kunci, kota, dan kategori */
[data-testid="stForm"] [data-testid="stTextInput"] label,
[data-testid="stForm"] [data-testid="stSelectbox"] label {
    color: #17372C !important;
    font-size: 1rem !important;
    font-weight: 700 !important;
    opacity: 1 !important;
}

/* Kolom untuk mengetik kata kunci */
[data-testid="stForm"] [data-testid="stTextInput"] input {
    color: #17372C !important;
    -webkit-text-fill-color: #17372C !important;
    background-color: #FFFFFF !important;
    border: 1.5px solid #A8BCAF !important;
    border-radius: 11px !important;
    min-height: 48px !important;
    font-size: 1rem !important;
    font-weight: 500 !important;
    opacity: 1 !important;
}

/* Placeholder, misalnya "wisata alam di Semarang" */
[data-testid="stForm"] input::placeholder {
    color: #68776D !important;
    -webkit-text-fill-color: #68776D !important;
    opacity: 1 !important;
}

/* Fokus ketika kolom diklik */
[data-testid="stForm"] [data-testid="stTextInput"] input:focus {
    border-color: #214E3D !important;
    box-shadow: 0 0 0 2px rgba(33, 78, 61, 0.15) !important;
}

/* Teks kota dan kategori yang terpilih */
[data-testid="stForm"] [data-testid="stSelectbox"] div[data-baseweb="select"] > div {
    background-color: #FFFFFF !important;
    border-color: #A8BCAF !important;
}

[data-testid="stForm"] [data-testid="stSelectbox"] input,
[data-testid="stForm"] [data-testid="stSelectbox"] div[role="combobox"],
[data-testid="stForm"] [data-testid="stSelectbox"] div[data-baseweb="select"] span {
    color: #17372C !important;
    -webkit-text-fill-color: #17372C !important;
    opacity: 1 !important;
}

/* Hasil pencarian dan teks pendukung */
[data-testid="stForm"] p,
[data-testid="stForm"] label {
    opacity: 1 !important;
}

/* Tombol pencarian */
[data-testid="stForm"] [data-testid="stFormSubmitButton"] button {
    background-color: #214E3D !important;
    color: #FFFFFF !important;
    font-size: 1rem !important;
    font-weight: 700 !important;
    min-height: 48px !important;
    border-radius: 11px !important;
}

/* ===== FINAL FIX: SEARCH INPUT & DROPDOWN COLORS ===== */

/* Semua teks di area pencarian */
[data-testid="stForm"] label,
[data-testid="stForm"] [data-testid="stWidgetLabel"] p {
    color: #17372C !important;
    opacity: 1 !important;
}

/* Kolom kata kunci: kondisi normal dan saat diklik */
[data-testid="stForm"] [data-testid="stTextInput"] input,
[data-testid="stForm"] [data-testid="stTextInput"] input:focus,
[data-testid="stForm"] [data-testid="stTextInput"] input:active {
    color: #17372C !important;
    -webkit-text-fill-color: #17372C !important;
    caret-color: #214E3D !important;
    background-color: #FFFFFF !important;
    border: 1.5px solid #A8BCAF !important;
    opacity: 1 !important;
    box-shadow: none;
}

/* Placeholder sebelum pengguna mengetik */
[data-testid="stForm"] [data-testid="stTextInput"] input::placeholder {
    color: #68776D !important;
    -webkit-text-fill-color: #68776D !important;
    opacity: 1 !important;
}

/* Kotak pilihan kota dan kategori */
[data-testid="stForm"] [data-testid="stSelectbox"] [data-baseweb="select"] > div {
    background-color: #FFFFFF !important;
    border-color: #A8BCAF !important;
    opacity: 1 !important;
}

/* Teks pilihan yang sedang ditampilkan */
[data-testid="stForm"] [data-testid="stSelectbox"] [data-baseweb="select"] div,
[data-testid="stForm"] [data-testid="stSelectbox"] [data-baseweb="select"] span {
    color: #17372C !important;
    -webkit-text-fill-color: #17372C !important;
}

/* Panah dropdown */
[data-testid="stForm"] [data-testid="stSelectbox"] svg {
    fill: #214E3D !important;
    color: #214E3D !important;
}

/* Daftar pilihan yang terbuka */
[data-baseweb="popover"],
[data-baseweb="popover"] ul,
[data-baseweb="menu"],
[data-baseweb="menu"] ul {
    background-color: #FFFFFF !important;
}

[data-baseweb="popover"] li,
[data-baseweb="menu"] li,
[data-baseweb="option"] {
    color: #17372C !important;
    -webkit-text-fill-color: #17372C !important;
    background-color: #FFFFFF !important;
    opacity: 1 !important;
}

/* Pilihan saat diarahkan atau dipilih */
[data-baseweb="option"]:hover {
    background-color: #EDF3ED !important;
    color: #17372C !important;
    -webkit-text-fill-color: #17372C !important;
}

/* Garis batas tetap terlihat */
[data-testid="stForm"] [data-testid="stSelectbox"] [data-baseweb="select"] > div:focus-within {
    border-color: #214E3D !important;
    box-shadow: 0 0 0 2px rgba(33, 78, 61, 0.15) !important;
}

/* FIX VISIBILITAS TEKS FORM WISATAFINDER */
[data-testid="stForm"] input,
[data-testid="stForm"] input:focus,
[data-testid="stForm"] input:active {
    color: #17372C !important;
    -webkit-text-fill-color: #17372C !important;
    background: #FFFFFF !important;
    opacity: 1 !important;
}

[data-testid="stForm"] [data-baseweb="select"] > div {
    background-color: #FFFFFF !important;
    opacity: 1 !important;
}

[data-testid="stForm"] [data-baseweb="select"] input,
[data-testid="stForm"] [data-baseweb="select"] span,
[data-testid="stForm"] [data-baseweb="select"] div[role="combobox"] {
    color: #17372C !important;
    -webkit-text-fill-color: #17372C !important;
    opacity: 1 !important;
}

[data-baseweb="popover"],
[data-baseweb="popover"] ul,
[data-baseweb="menu"] {
    background-color: #FFFFFF !important;
}

[data-baseweb="popover"] li,
[data-baseweb="option"],
[data-baseweb="menu"] li {
    color: #17372C !important;
    -webkit-text-fill-color: #17372C !important;
    background-color: #FFFFFF !important;
    opacity: 1 !important;
}

[data-baseweb="option"]:hover {
    background-color: #E8F0E9 !important;
}

[data-testid="stForm"] label,
[data-testid="stWidgetLabel"] p {
    color: #17372C !important;
    opacity: 1 !important;
}




    </style>
    """,
    unsafe_allow_html=True,
)


# =====================================================
# DATA AND SEARCH INDEX
# =====================================================
@st.cache_data
def load_data():
    if not DATA_PATH.exists():
        raise FileNotFoundError(
            f"Dataset tidak ditemukan: {DATA_PATH}"
        )

    data = pd.read_csv(DATA_PATH)
    data.columns = data.columns.str.strip()

    required = ["Place_Name", "Category", "City", "Description"]
    missing = [col for col in required if col not in data.columns]

    if missing:
        raise ValueError(
            f"Kolom berikut belum tersedia: {missing}. "
            f"Kolom dataset: {data.columns.tolist()}"
        )

    for col in required:
        data[col] = data[col].fillna("").astype(str).str.strip()

    for col in ["Price", "Rating"]:
        if col in data.columns:
            data[col] = pd.to_numeric(data[col], errors="coerce")

    data["search_text"] = (
        data["Place_Name"] + " "
        + data["Category"] + " "
        + data["Description"]
    ).str.lower()

    return data


@st.cache_resource
def build_index(texts):
    vectorizer = TfidfVectorizer(
        lowercase=True,
        ngram_range=(1, 2),
        sublinear_tf=True,
        max_features=20000,
    )
    matrix = vectorizer.fit_transform(texts)
    return vectorizer, matrix


try:
    df = load_data()
    vectorizer, tfidf_matrix = build_index(
        tuple(df["search_text"].tolist())
    )
except Exception as exc:
    st.error(f"Aplikasi belum bisa memuat data: {exc}")
    st.stop()





@st.cache_data(ttl=86400, show_spinner=False)
def find_destination_image(place_name, city):
    """
    Mencari foto destinasi.
    Dua klenteng memakai foto Wikimedia Commons yang sudah
    diidentifikasi secara khusus. Destinasi lain memakai
    pencarian otomatis dengan validasi nama yang lebih ketat.
    """
    import re
    from urllib.parse import quote

    place_name = str(place_name).strip()
    city = str(city).strip()

    if not place_name:
        return None

    def normalize(text):
        return " ".join(
            re.findall(
                r"[a-z0-9]+",
                str(text).casefold().replace("_", " ")
            )
        )

    normalized_place = normalize(place_name)

    # Foto manual untuk destinasi yang sudah diverifikasi.
    # Special:FilePath mengarah ke berkas di Wikimedia Commons.
    verified_images = {
        "klenteng sanggar agung": {
            "image_url": (
                "https://commons.wikimedia.org/wiki/Special:FilePath/"
                "The_front_side_of_Sanggar_Agung_Temple%2C_"
                "Surabaya-Indonesia%2C_which_is_facing_the_sea.jpg"
            ),
            "page_url": (
                "https://commons.wikimedia.org/wiki/File:"
                "The_front_side_of_Sanggar_Agung_Temple,_"
                "Surabaya-Indonesia,_which_is_facing_the_sea.jpg"
            ),
            "page_title": "Sanggar Agung Temple, Surabaya",
        },
        "klenteng jin de yuan": {
            "image_url": (
                "https://commons.wikimedia.org/wiki/Special:FilePath/"
                "Klenteng_Jin_De_Yuan%2C_Glodok%2C_Jakarta.jpg"
            ),
            "page_url": (
                "https://commons.wikimedia.org/wiki/File:"
                "Klenteng_Jin_De_Yuan,_Glodok,_Jakarta.jpg"
            ),
            "page_title": "Klenteng Jin De Yuan, Jakarta",
        },
    }

    
    # Samakan variasi penulisan nama dengan foto yang sudah diverifikasi.
    verified_aliases = {
        "klenteng sanggar agung": "klenteng sanggar agung",
        "kelenteng sanggar agung": "klenteng sanggar agung",
        "klenteng hong san tang": "klenteng sanggar agung",
        "kelenteng hong san tang": "klenteng sanggar agung",
        "klenteng jin de yuan": "klenteng jin de yuan",
        "kelenteng jin de yuan": "klenteng jin de yuan",
        "klenteng kim tek le": "klenteng jin de yuan",
        "kelenteng kim tek le": "klenteng jin de yuan",
    }

    verified_key = verified_aliases.get(
        normalized_place,
        normalized_place,
    )

    if verified_key in verified_images:
        return verified_images[verified_key]


    target_words = set(normalized_place.split())

    if not target_words:
        return None

    headers = {
        "User-Agent": (
            "WisataFinder/1.0 "
            "(educational tourism search project)"
        )
    }

    def match_score(title):
        title_normalized = normalize(title)
        title_words = set(title_normalized.split())

        if not title_words:
            return 0.0

        # Abaikan judul yang tidak memuat cukup banyak kata
        # penting dari nama destinasi.
        overlap = len(target_words & title_words) / len(target_words)

        # Kecocokan nama lengkap mendapat nilai tertinggi.
        if normalized_place in title_normalized:
            return 1.0

        return overlap

    # Untuk foto otomatis, gunakan judul berkas Wikimedia Commons.
    # Tidak memakai thumbnail Wikipedia secara langsung karena
    # gambar thumbnail halaman belum tentu menggambarkan destinasi.
    endpoint = "https://commons.wikimedia.org/w/api.php"

    queries = list(dict.fromkeys([
        f'"{place_name}" "{city}"' if city else f'"{place_name}"',
        f'"{place_name}"',
        place_name,
    ]))

    for search_query in queries:
        try:
            response = requests.get(
                endpoint,
                params={
                    "action": "query",
                    "format": "json",
                    "formatversion": 2,
                    "generator": "search",
                    "gsrsearch": search_query,
                    "gsrnamespace": 6,
                    "gsrlimit": 20,
                    "prop": "imageinfo",
                    "iiprop": "url",
                    "iiurlwidth": 640,
                },
                headers=headers,
                timeout=5,
            )
            response.raise_for_status()

            pages = response.json().get(
                "query", {}
            ).get("pages", [])

            candidates = []

            for page in pages:
                title = page.get("title", "")
                image_info = page.get("imageinfo", [])

                if not image_info:
                    continue

                score = match_score(title)

                # Ambang ketat: perlu kecocokan nama yang kuat.
                if score >= 0.75:
                    candidates.append((score, page))

            if candidates:
                candidates.sort(
                    key=lambda item: item[0],
                    reverse=True,
                )

                _, page = candidates[0]
                image_info = page["imageinfo"][0]

                return {
                    "image_url": image_info.get(
                        "thumburl", image_info.get("url")
                    ),
                    "page_url": (
                        "https://commons.wikimedia.org/wiki/"
                        + quote(page["title"].replace(" ", "_"), safe="_:")
                    ),
                    "page_title": page.get("title", place_name),
                }

        except (
            requests.RequestException,
            ValueError,
            KeyError,
            TypeError,
        ):
            continue

    # Lebih baik menampilkan placeholder daripada foto yang meragukan.
    return None


# =====================================================
# BRAND HEADER
# =====================================================
st.markdown(
    """
    <div class="brand">
        <div class="brand-icon">⌖</div>
        <div>
            <div class="brand-name">WisataFinder</div>
            <div class="brand-caption">EXPLORE INDONESIA</div>
        </div>
    </div>
    """,
    unsafe_allow_html=True,
)


# =====================================================
# HERO
# =====================================================
st.markdown(
    """
    <div class="hero">
        <div class="hero-eyebrow">TEMUKAN PETUALANGANMU</div>
        <h1>Tempat indah,<br>cerita baru.</h1>
        <p>
            Dari keindahan alam hingga kekayaan budaya.
            Temukan destinasi yang sesuai dengan perjalanan
            yang ingin kamu ciptakan.
        </p>
    </div>
    """,
    unsafe_allow_html=True,
)


# =====================================================
# STATISTICS
# =====================================================
m1, m2, m3 = st.columns(3)

with m1:
    st.metric("Destinasi tersedia", f"{len(df):,}")

with m2:
    city_count = df.loc[df["City"] != "", "City"].nunique()
    st.metric("Kota tujuan", city_count)

with m3:
    category_count = df.loc[df["Category"] != "", "Category"].nunique()
    st.metric("Kategori wisata", category_count)


st.write("")


# =====================================================
# SEARCH PANEL
# =====================================================
st.markdown(
    """
    <div class="section-eyebrow">MULAI MENJELAJAH</div>
    <div class="section-title">Ke mana perjalananmu?</div>
    <div class="section-subtitle">
        Masukkan kata kunci untuk menemukan destinasi
        berdasarkan kemiripan informasi.
    </div>
    """,
    unsafe_allow_html=True,
)


with st.form("search_form"):
    query = st.text_input(
        "Kata kunci",
        placeholder="Contoh: wisata alam di Semarang",
    )

    f1, f2 = st.columns(2)

    if "Location_Label" in df.columns:
        location_column = "Location_Label"
    else:
        location_column = "City"

    city_options = sorted(
        df[location_column].dropna().unique()
    )

    category_options = sorted(
        category
        for category in df["Category"].dropna().unique()
        if category
    )

    with f1:
        selected_city = st.selectbox(
            "Pilih kota",
            ["Semua kota"] + city_options,
        )

    with f2:
        selected_category = st.selectbox(
            "Pilih kategori",
            ["Semua kategori"] + category_options,
        )

    submitted = st.form_submit_button(
        "⌕  Temukan Destinasi",
        use_container_width=True,
    )

# =====================================================
# FILTER MAKSUD PENCARIAN TEMPAT IBADAH
# =====================================================
def filter_worship_results(results, query):
    q = query.casefold().strip()

    # Kueri spesifik klenteng/kelenteng:
    # identitas destinasi harus cocok melalui nama
    # atau kategori, bukan hanya penyebutan di deskripsi.
    if re.search(r"\b(klenteng|kelenteng)\b", q):
        place_name = (
            results["Place_Name"]
            .fillna("")
            .astype(str)
            .str.casefold()
        )

        category = (
            results["Category"]
            .fillna("")
            .astype(str)
            .str.casefold()
        )

        identity = place_name + " " + category

        return results[
            identity.str.contains(
                r"\b(klenteng|kelenteng)\b",
                regex=True,
                na=False,
            )
        ]

    worship_types = {
        "islam": [
            "muslim", "islam", "islami", "masjid",
            "musala", "mushola", "langgar", "surau"
        ],
        "kristen": [
            "gereja", "kristen", "katolik", "katedral",
            "kapel", "basilika"
        ],
        "hindu": ["hindu", "pura"],
        "buddha": [
            "buddha", "buddhis", "vihara", "wihara",
            "tridharma"
        ],
    }

    detected_type = None

    for religion, keywords in worship_types.items():
        if any(word in q for word in keywords):
            detected_type = religion
            break

    # Kueri umum tidak memerlukan filter agama.
    if detected_type is None:
        return results

    place_name = (
        results["Place_Name"]
        .fillna("")
        .astype(str)
        .str.casefold()
    )

    category = (
        results["Category"]
        .fillna("")
        .astype(str)
        .str.casefold()
    )

    description = (
        results["Description"]
        .fillna("")
        .astype(str)
        .str.casefold()
    )

    identity = place_name + " " + category
    all_text = identity + " " + description

    if detected_type == "islam":
        include = (
            r"\b(masjid|musala|mushola|langgar|surau)\b"
        )
        exclude = (
            r"\b(gereja|katedral|kapel|basilika|"
            r"pura|vihara|wihara|klenteng|kelenteng)\b"
        )

    elif detected_type == "kristen":
        include = (
            r"\b(gereja|katedral|kapel|basilika)\b"
        )
        exclude = (
            r"\b(masjid|musala|mushola|langgar|surau|"
            r"pura|vihara|wihara|klenteng|kelenteng)\b"
        )

    elif detected_type == "hindu":
        include = r"\b(pura)\b"
        exclude = (
            r"\b(masjid|musala|mushola|langgar|surau|"
            r"gereja|katedral|kapel|vihara|wihara|"
            r"klenteng|kelenteng)\b"
        )

    else:
        include = (
            r"\b(vihara|wihara|kuil|tridharma)\b"
        )
        exclude = (
            r"\b(masjid|musala|mushola|langgar|surau|"
            r"gereja|katedral|kapel|basilika|pura)\b"
        )

    relevant_type = all_text.str.contains(
        include, regex=True, na=False
    )

    other_type = identity.str.contains(
        exclude, regex=True, na=False
    )

    return results[relevant_type & ~other_type]

# =====================================================
# RESULTS
# =====================================================
if submitted:
    if not query.strip():
        st.warning("Masukkan kata kunci terlebih dahulu.")
    else:
        
        # Deteksi nama kota yang disebutkan dalam kata kunci
        query_lower = query.casefold()
        detected_city = None

        for city_name in city_options:
            if city_name.casefold() in query_lower:
                detected_city = city_name
                break

        # Kota dalam kata kunci diprioritaskan.
        # Jika tidak ada, gunakan pilihan kota pada dropdown.
        effective_city = (
            detected_city
            if detected_city is not None
            else selected_city
        )
                # Beri peringatan jika destinasi bermasalah dicari
        # dengan filter kota yang tidak sesuai.
        if (
            effective_city != "Semua kota"
            and "Location_Verification" in df.columns
        ):
            excluded_place = df[
                df["Place_Name"].str.contains(
                    query.strip(),
                    case=False,
                    na=False,
                    regex=False,
                )
                & df["Location_Verification"]
                .fillna("")
                .str.startswith("Perlu verifikasi")
            ]

            if not excluded_place.empty:
                st.warning(
                    "Benteng Pendem ditemukan, tetapi tidak ditampilkan "
                    "karena metadata lokasinya perlu diverifikasi. "
                    "Pilih 'Semua kota' untuk mencari tanpa filter kota."
                )
                st.stop()

        # Hapus frasa lokasi dari query agar pencarian
        # kemiripan berfokus pada jenis destinasi.
        search_query = query

        if detected_city:
            import re

            search_query = re.sub(
                rf"\bdi\s+{re.escape(detected_city)}\b",
                "",
                search_query,
                flags=re.IGNORECASE
            ).strip()

        if not search_query:
            search_query = query

        # Hitung TF-IDF dan cosine similarity
        query_vector = vectorizer.transform([search_query])

        scores = cosine_similarity(
            query_vector,
            tfidf_matrix
        ).flatten()

        results = df.copy()
        results["similarity_score"] = scores

       
        
        # Terapkan filter berdasarkan label lokasi
        if effective_city != "Semua kota":
            results = results[
                results[location_column]
                .fillna("")
                .str.casefold()
                == effective_city.casefold()
            ]

            # Jangan tampilkan destinasi yang lokasinya belum terverifikasi
            if "Location_Verification" in results.columns:
                results = results[
                    ~results["Location_Verification"]
                    .fillna("")
                    .str.startswith("Perlu verifikasi")
                ]




        # Filter berdasarkan kategori
        if selected_category != "Semua kategori":
            results = results[
                results["Category"] == selected_category
            ]

        # Tangani destinasi yang dikecualikan karena masalah lokasi.
        if (
            effective_city != "Semua kota"
            and "Location_Verification" in df.columns
        ):
            excluded_place = df[
                df["Place_Name"].str.contains(
                    query.strip(),
                    case=False,
                    na=False,
                    regex=False,
                )
                & df["Location_Verification"]
                .fillna("")
                .str.startswith("Perlu verifikasi")
            ]

            if not excluded_place.empty:
                st.markdown(
    """
    <p style="color: black; font-size: 16px;">
        <b>Lokasi destinasi belum terverifikasi</b><br>
        Benteng Pendem ditemukan, tetapi tidak ditampilkan karena
        metadata lokasinya perlu diverifikasi. Pilih
        <b>Semua kota</b> untuk mencari tanpa filter kota.
    </p>
    """,
    unsafe_allow_html=True,
)
                st.stop()
        # Hanya tampilkan hasil dengan skor kemiripan > 0
        results = results[
            results["similarity_score"] > 0
        ].copy()

        

        
        
        # Prioritaskan kecocokan nama destinasi untuk kueri jenis tempat.
        # TF-IDF + Cosine Similarity tetap menjadi metode utama.

        query_lower = query.casefold()

        # Pertahankan filter khusus tempat ibadah yang sudah ada.
        results = filter_worship_results(results, query)

       
        # Pola nama untuk beberapa jenis destinasi.
        # Pola ini hanya menjadi sinyal tambahan untuk pengurutan.
        query_rules = [
            {
                "trigger": r"\b(monumen|monument)\b",
                "name_pattern": r"\b(monumen|monument|tugu)\b",
            },
            {
                "trigger": r"\b(gunung|mountain)\b",
                "name_pattern": r"\b(gunung|mountain)",
            },
            {
                "trigger": r"\b(klenteng|kelenteng)\b",
                "name_pattern": r"\b(klenteng|kelenteng)\b",
            },
            {
                "trigger": r"\b(kebun binatang|zoo|bonbin)\b",
                "name_pattern": r"\b(kebun binatang|zoo|bonbin)\b",
            },
            {
                "trigger": r"\b(pusat perbelanjaan|shopping center)\b",
                "name_pattern": (
                    r"\b(mall|mal|plaza|pasar|"
                    r"pusat perbelanjaan|shopping center)\b"
                ),
            },
        ]

        active_rule = next(
            (
                rule
                for rule in query_rules
                if re.search(rule["trigger"], query_lower)
            ),
            None,
        )

        if active_rule is not None:
            results["_name_match"] = (
                results["Place_Name"]
                .fillna("")
                .astype(str)
                .str.contains(
                    active_rule["name_pattern"],
                    case=False,
                    regex=True,
                    na=False,
                )
                .astype(int)
            )

            if re.search(
                r"\b(pusat perbelanjaan|shopping center)\b",
                query_lower,
            ):
                results["_category_match"] = (
                    results["Category"]
                    .fillna("")
                    .astype(str)
                    .str.casefold()
                    .eq("pusat perbelanjaan")
                    .astype(int)
                )
            else:
                results["_category_match"] = 0

            results = results.sort_values(
                by=[
                    "_name_match",
                    "_category_match",
                    "similarity_score",
                ],
                ascending=[False, False, False],
                kind="stable",
            )

            results = results.drop(
                columns=["_name_match", "_category_match"]
            )

       
        else:
            # Untuk kueri wisata murah, prioritaskan harga
            # di antara destinasi yang sudah cocok dengan kueri.
            if re.search(
                r"\b(murah|termurah|hemat|terjangkau)\b",
                query_lower,
            ):
                # Harga Rp0 dianggap belum terverifikasi,
                # bukan otomatis berarti gratis.
                results["_price_unknown"] = (
                    results["Price"].isna()
                    | results["Price"].le(0)
                ).astype(int)

                results = results.sort_values(
                    by=[
                        "_price_unknown",
                        "Price",
                        "similarity_score",
                    ],
                    ascending=[True, True, False],
                    kind="stable",
                )

                results = results.drop(
                    columns=["_price_unknown"]
                )
            else:
                # Kueri biasa tetap mengutamakan kemiripan teks.
                results = results.sort_values(
                    by="similarity_score",
                    ascending=False,
                    kind="stable",
                )



        st.write("")

        st.markdown(
            '<div class="section-eyebrow">HASIL PENCARIAN</div>',
            unsafe_allow_html=True
        )

        st.markdown(
            '<div class="section-title">Destinasi untukmu</div>',
            unsafe_allow_html=True
        )

        if results.empty:
            st.info(
                "Belum ditemukan destinasi yang cocok. "
                "Coba kata kunci lain atau ubah filter kota dan kategori."
            )
        else:
            st.success(
                f"Ditemukan {len(results)} destinasi yang relevan."
            )

            top_results = results.head(20)

            for rank, (_, item) in enumerate(
                top_results.iterrows(),
                start=1
            ):
                name = item["Place_Name"]
                city = item[location_column]
                category = item["Category"]
                description = item["Description"]
                if pd.notna(description):
                                    description = item["Description"]

                if pd.notna(description):
                    description = str(description)
                    description = description.replace("\\n", " ")
                    description = description.replace("\r\n", " ")
                    description = description.replace("\n", " ")
                    description = " ".join(description.split())
                else:
                    description = ""

                
                score = item["similarity_score"]

                image_col, content_col = st.columns(
                    [1, 2.5]
                )

                # Cari gambar hanya untuk 3 hasil teratas
                if rank <= 3:
                    image_info = find_destination_image(
                        name,
                        city
                    )
                else:
                    image_info = None

                with image_col:
                    if image_info and image_info.get("image_url"):
                        st.image(
                            image_info["image_url"],
                            use_container_width=True
                        )

                        if image_info.get("page_url"):
                            st.caption(
                                f"[Sumber foto]({image_info['page_url']})"
                            )
                    else:
                        st.markdown(
                            """
                            <div style="
                                background:#EDF3ED;
                                border-radius:12px;
                                padding:35px 10px;
                                text-align:center;
                                color:#214E3D;
                            ">
                                🌿<br>
                                <b>Wisata Indonesia</b><br>
                                <small>Foto belum tersedia</small>
                            </div>
                            """,
                            unsafe_allow_html=True
                        )

                with content_col:
                    st.markdown(
                        f"""
                        <div class="result-card">
                            <div class="result-number">
                                HASIL {rank:02d}
                            </div>
                            <div class="result-title">
                                {name}
                            </div>
                            <div class="result-meta">
                                📍 {city} &nbsp; · &nbsp; 🏷️ {category}
                            </div>
                            <div class="result-description">
                                {description if description else
                                "Belum ada deskripsi destinasi."}
                            </div>
                            <div class="score">
                                Skor kemiripan: {score:.4f}
                            </div>
                        </div>
                        """,
                        unsafe_allow_html=True
                    )

                    details = []

                    if "Price" in item.index and pd.notna(item["Price"]):
                        details.append(
                            f"**Harga:** Rp{item['Price']:,.0f}"
                        )

                    if "Rating" in item.index and pd.notna(item["Rating"]):
                        details.append(
                            f"**Rating:** {item['Rating']}"
                        )

                    if details:
                        st.markdown(" · ".join(details))

            # Unduh hasil pencarian
            csv_data = top_results.to_csv(
                index=False
            ).encode("utf-8-sig")

            st.download_button(
                label="Unduh hasil pencarian (CSV)",
                data=csv_data,
                file_name="hasil_pencarian_wisatfinder.csv",
                mime="text/csv"
            )
# =====================================================
# INSPIRATION SECTION
# =====================================================
else:
    st.write("")
    st.markdown(
        """
        <div class="section-eyebrow">INSPIRASI PERJALANAN</div>
        <div class="section-title">Mulai dari yang kamu suka.</div>
        <div class="section-subtitle">
            Pilih ide perjalanan, lalu gunakan kata kunci tersebut
            untuk memulai pencarian.
        </div>
        """,
        unsafe_allow_html=True,
    )

    c1, c2, c3 = st.columns(3)

    with c1:
        st.markdown(
            """
            <div class="inspiration-card">
                <div class="inspiration-icon">🌿</div>
                <h3>Menjelajah alam</h3>
                <p>
                    Temukan taman, kawasan alam, dan destinasi
                    dengan pemandangan yang menenangkan.
                </p>
            </div>
            """,
            unsafe_allow_html=True,
        )
        if st.button("Cari wisata alam", key="nature"):
            st.session_state["suggested_query"] = "wisata alam"

    with c2:
        st.markdown(
            """
            <div class="inspiration-card">
                <div class="inspiration-icon">🏛️</div>
                <h3>Mengenal budaya</h3>
                <p>
                    Jelajahi tempat bersejarah, warisan budaya,
                    dan destinasi yang menyimpan cerita.
                </p>
            </div>
            """,
            unsafe_allow_html=True,
        )
        if st.button("Cari wisata budaya", key="culture"):
            st.session_state["suggested_query"] = "wisata budaya"

    with c3:
        st.markdown(
            """
            <div class="inspiration-card">
                <div class="inspiration-icon">🎡</div>
                <h3>Waktu bersama</h3>
                <p>
                    Cari taman hiburan dan tempat rekreasi
                    untuk mengisi waktu bersama keluarga.
                </p>
            </div>
            """,
            unsafe_allow_html=True,
        )
        if st.button("Cari rekreasi", key="recreation"):
            st.session_state["suggested_query"] = "tempat rekreasi keluarga"

    if "suggested_query" in st.session_state:
        st.info(
            f"Kata kunci pilihanmu: {st.session_state['suggested_query']}. "
            "Masukkan kata kunci ini pada kolom pencarian di atas."
        )


# =====================================================
# FOOTER
# =====================================================
st.markdown(
    """
    <div class="footer">
        <strong>WisataFinder</strong><br>
        Sistem Temu Kembali Informasi Destinasi Wisata<br>
        TF-IDF · Cosine Similarity · Streamlit
    </div>
    """,
    unsafe_allow_html=True,
)
