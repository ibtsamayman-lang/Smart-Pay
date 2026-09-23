import requests
import re
import json
from bs4 import BeautifulSoup


MIN_PRODUCT_PRICE = 1
MAX_PRODUCT_PRICE = 100000


def get_page(url):

    headers = {
        "User-Agent": "Mozilla/5.0"
    }

    try:
        response = requests.get(
            url,
            headers=headers,
            timeout=10
        )

        if response.status_code == 200:
            return response.text

    except requests.RequestException as e:

        print(f"Could not access: {url}")
        

    return None


def extract_product_price(url, product_name):

    html = get_page(url)

    if not html:
        return None, "Not found", "Low"

    soup = BeautifulSoup(html, "html.parser")


    # ==========================================
    # 1. JSON-LD
    # ==========================================

    scripts = soup.find_all(
        "script",
        type="application/ld+json"
    )

    for script in scripts:

        try:

            data = json.loads(
                script.string or script.get_text()
            )

            data_list = data if isinstance(data, list) else [data]

            for item in data_list:

                if not isinstance(item, dict):
                    continue


                # Handle @graph
                if "@graph" in item:

                    graph = item["@graph"]

                    if isinstance(graph, list):
                        data_list.extend(graph)


                if item.get("@type") != "Product":
                    continue


                offers = item.get("offers")


                # --------------------------------
                # offers = dictionary
                # --------------------------------

                if isinstance(offers, dict):

                    price = offers.get("price")

                    if price:

                        try:

                            value = float(
                                str(price).replace(",", "")
                            )

                            if MIN_PRODUCT_PRICE <= value <= MAX_PRODUCT_PRICE:

                                return (
                                    value,
                                    "JSON-LD",
                                    "High"
                                )

                        except (ValueError, TypeError):
                            pass


                # --------------------------------
                # offers = list
                # --------------------------------

                elif isinstance(offers, list):

                    for offer in offers:

                        if not isinstance(offer, dict):
                            continue

                        price = offer.get("price")

                        if price:

                            try:

                                value = float(
                                    str(price).replace(",", "")
                                )

                                if MIN_PRODUCT_PRICE <= value <= MAX_PRODUCT_PRICE:

                                    return (
                                        value,
                                        "JSON-LD",
                                        "High"
                                    )

                            except (ValueError, TypeError):
                                continue


        except (
            json.JSONDecodeError,
            ValueError,
            TypeError
        ):
            continue


    # ==========================================
    # 2. Product Context
    # ==========================================

    text = soup.get_text(
        " ",
        strip=True
    )

    lower_text = text.lower()

    keyword = product_name.lower().strip()

    position = lower_text.find(keyword)


    if position != -1:

        start = max(0, position - 100)
        end = position + 500

        nearby_text = text[start:end]


        pattern = r"""
            (?:EGP|جنيه|ج\.م)
            \s*
            ([\d,]+(?:\.\d+)?)

            |

            ([\d,]+(?:\.\d+)?)
            \s*
            (?:EGP|جنيه|ج\.م)
        """


        matches = re.findall(
            pattern,
            nearby_text,
            re.IGNORECASE | re.VERBOSE
        )


        prices = []


        for match in matches:

            value = match[0] or match[1]

            try:

                price = float(
                    value.replace(",", "")
                )

                if MIN_PRODUCT_PRICE <= price <= MAX_PRODUCT_PRICE:

                    prices.append(price)

            except ValueError:
                continue


        # إزالة الأسعار المتكررة
        prices = list(dict.fromkeys(prices))


        # لو لقينا سعر واحد فقط
        if len(prices) == 1:

            return (
                prices[0],
                "Product Context",
                "Medium"
            )


        # لو فيه أكتر من سعر، ناخد أول سعر
        # لأنه الأقرب لسياق المنتج
        if len(prices) > 1:

            return (
                prices[0],
                "Product Context",
                "Low"
            )


    # ==========================================
    # 3. Not Found
    # ==========================================

    return None, "Not found", "Low"