def classify_store(url):

    url = url.lower()

    stores = {
        "Jumia": "jumia.com.eg",
        "Noon": "noon.com",
        "Amazon Egypt": "amazon.eg",
        "Faces": "faces.eg",
        "Ramfa Beauty": "ramfabeauty.com",
        "Feel22": "feel22.com",
        "Vodafone": "vodafone.com.eg",
        "Orange": "orange.eg",
        "Prime Tech": "primetecheg.com",
        "Dubizzle": "dubizzle.com.eg",
        "Phones7": "phones7.com",
    }

    non_store_sources = {
        "Pricena": "pricena.com",
        "Price Comparison": "egprices.com",
        "Alibaba Guide": "alibaba.com"
    }

    for store, domain in stores.items():

        if domain in url:
            return store

    for source, domain in non_store_sources.items():

        if domain in url:
            return source

    return "Unknown"