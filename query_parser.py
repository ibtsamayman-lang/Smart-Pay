import re


# ==========================================
# Detect Budget
# ==========================================

def extract_budget(text):

    patterns = [
        r"(?:under|below|less than|max|up to)\s*(\d+(?:,\d+)?)",
        r"(?:تحت|اقل من|أقل من|حد|لحد|بحد أقصى)\s*(\d+(?:,\d+)?)",
        r"(\d+(?:,\d+)?)\s*(?:جنيه|ج\.م|egp)"
    ]

    for pattern in patterns:

        match = re.search(
            pattern,
            text,
            re.IGNORECASE
        )

        if match:

            return float(
                match.group(1).replace(",", "")
            )

    return None


# ==========================================
# Detect Color
# ==========================================

def extract_color(text):

    colors = {
        "black": ["black", "أسود", "اسود"],
        "white": ["white", "أبيض", "ابيض"],
        "red": ["red", "أحمر", "احمر"],
        "blue": ["blue", "أزرق", "ازرق"],
        "green": ["green", "أخضر", "اخضر"],
        "pink": ["pink", "وردي"],
        "yellow": ["yellow", "أصفر", "اصفر"],
        "brown": ["brown", "بني"]
    }

    text_lower = text.lower()

    for color, words in colors.items():

        for word in words:

            if word.lower() in text_lower:
                return color

    return None


# ==========================================
# Detect Brand
# ==========================================

def extract_brand(text):

    brands = [
        "Apple",
        "Samsung",
        "Nike",
        "Adidas",
        "Lenovo",
        "Dell",
        "HP",
        "Huawei",
        "Xiaomi",
        "Oppo",
        "Realme",
        "Zara",
        "H&M"
    ]

    text_lower = text.lower()

    for brand in brands:

        if brand.lower() in text_lower:
            return brand

    return None


# ==========================================
# Detect Category
# ==========================================

def extract_category(text):

    categories = {

        "phone": [
            "phone",
            "mobile",
            "smartphone",
            "موبايل",
            "هاتف",
            "تليفون",
            "تلفون"
        ],

        "clothing": [
            "clothes",
            "clothing",
            "dress",
            "shirt",
            "pants",
            "shoes",
            "ملابس",
            "فستان",
            "قميص",
            "بنطلون",
            "جزمة",
            "حذاء"
        ],

        "laptop": [
            "laptop",
            "notebook",
            "لاب توب",
            "لابتوب"
        ],

        "headphones": [
            "headphones",
            "earphones",
            "سماعة",
            "سماعات"
        ],

        "tv": [
            "tv",
            "television",
            "تلفزيون",
            "تليفزيون"
        ],

        "fridge": [
            "fridge",
            "refrigerator",
            "ثلاجة",
            "تلاجة"
        ]
    }

    text_lower = text.lower()

    for category, words in categories.items():

        for word in words:

            if word.lower() in text_lower:
                return category

    return None


# ==========================================
# Main Parser
# ==========================================

def parse_query(text):

    return {
        "original": text,
        "category": extract_category(text),
        "brand": extract_brand(text),
        "color": extract_color(text),
        "budget": extract_budget(text)
    }