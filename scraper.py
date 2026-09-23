from ddgs import DDGS
import requests
from bs4 import BeautifulSoup
import json
import re
from urllib.parse import urlparse


HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
        "AppleWebKit/537.36 "
        "(KHTML, like Gecko) "
        "Chrome/142.0.0.0 Safari/537.36"
    )
}


def get_page(url):
    try:
        response = requests.get(
            url,
            headers=HEADERS,
            timeout=15
        )

        if response.status_code == 200:
            return response.text

    except requests.RequestException:
        pass

    return None


def get_store(url):

    domain = urlparse(url).netloc.lower()

    if "jumia" in domain:
        return "Jumia"

    if "noon" in domain:
        return "Noon"

    if "amazon" in domain:
        return "Amazon Egypt"

    if "zara" in domain:
        return "Zara"

    if "faces" in domain:
        return "Faces"

    if "ramfabeauty" in domain:
        return "Ramfa Beauty"

    if "feel22" in domain:
        return "Feel22"

    return domain


def extract_price(text):

    if not text:
        return None

    patterns = [
        r"(\d[\d,]*(?:\.\d+)?)\s*(?:EGP|egp|جنيه|ج\.م)",
        r"(?:EGP|egp|جنيه|ج\.م)\s*(\d[\d,]*(?:\.\d+)?)"
    ]

    for pattern in patterns:

        match = re.search(
            pattern,
            text
        )

        if match:

            try:
                price = float(
                    match.group(1).replace(",", "")
                )

                if 1 <= price <= 1000000:
                    return price

            except ValueError:
                pass

    return None


def extract_product_data(url):

    html = get_page(url)

    if not html:
        return None

    soup = BeautifulSoup(
        html,
        "html.parser"
    )

    title = None
    image = None
    price = None

    # -------------------------
    # 1. JSON-LD
    # -------------------------

    scripts = soup.find_all(
        "script",
        type="application/ld+json"
    )

    for script in scripts:

        try:

            raw_data = (
                script.string
                or script.get_text()
            )

            data = json.loads(raw_data)

        except (
            json.JSONDecodeError,
            TypeError
        ):
            continue

        items = []

        if isinstance(data, list):
            items.extend(data)

        elif isinstance(data, dict):

            items.append(data)

            if "@graph" in data:

                graph = data["@graph"]

                if isinstance(graph, list):
                    items.extend(graph)

        for item in items:

            if not isinstance(item, dict):
                continue

            product_type = item.get("@type")

            if isinstance(product_type, list):
                is_product = (
                    "Product" in product_type
                )
            else:
                is_product = (
                    product_type == "Product"
                )

            if not is_product:
                continue

            title = item.get("name")

            image = item.get("image")

            if isinstance(image, list):
                image = image[0]

            elif isinstance(image, dict):
                image = image.get("url")

            offers = item.get("offers")

            if isinstance(offers, dict):

                price = offers.get("price")

            elif isinstance(offers, list):

                for offer in offers:

                    if isinstance(
                        offer,
                        dict
                    ):

                        price = offer.get(
                            "price"
                        )

                        if price:
                            break

            if price:

                try:

                    price = float(
                        str(price).replace(
                            ",",
                            ""
                        )
                    )

                except (
                    ValueError,
                    TypeError
                ):
                    price = None

            if title:

                return {
                    "title": title,
                    "price": price,
                    "image": image,
                    "store": get_store(url),
                    "link": url,
                    "currency": "EGP"
                }

    # -------------------------
    # 2. OpenGraph / Meta
    # -------------------------

    meta_title = soup.find(
        "meta",
        property="og:title"
    )

    meta_image = soup.find(
        "meta",
        property="og:image"
    )

    if meta_title:

        title = meta_title.get(
            "content"
        )

    meta_description = soup.find(
        "meta",
        property="og:description"
    )

    description = ""

    if meta_description:

        description = meta_description.get(
            "content",
            ""
        )

    if meta_image:

        image = meta_image.get(
            "content"
        )

    # -------------------------
    # 3. Search page text for price
    # -------------------------

    page_text = soup.get_text(
        " ",
        strip=True
    )

    price = extract_price(
        page_text
    )

    # -------------------------
    # 4. Normal title fallback
    # -------------------------

    if not title:

        if soup.title:

            title = soup.title.get_text(
                strip=True
            )

    # -------------------------
    # 5. Return product
    # -------------------------

    if title:

        return {
            "title": title,
            "price": price,
            "image": image,
            "store": get_store(url),
            "link": url,
            "currency": "EGP"
        }

    return None


def search_products(product_name):

    results = []

    seen_links = set()

    queries = [
        f"{product_name} Egypt",
        f"{product_name} مصر",
        f"{product_name} price Egypt",
        f"{product_name} سعر مصر"
    ]

    try:

        with DDGS() as ddgs:

            for query in queries:

                print(
                    "\nSEARCH:",
                    query
                )

                search_results = ddgs.text(
                    query,
                    max_results=15
                )

                for item in search_results:

                    link = item.get(
                        "href",
                        ""
                    )

                    if not link:
                        continue

                    if link in seen_links:
                        continue

                    seen_links.add(link)

                    print(
                        "TRYING:",
                        link
                    )

                    product = (
                        extract_product_data(
                            link
                        )
                    )

                    if product:

                        print(
                            "FOUND:",
                            product["title"]
                        )

                        results.append(
                            product
                        )

                    else:

                        print(
                            "FAILED:",
                            link
                        )

    except Exception as e:

        print(
            "SEARCH ERROR:",
            e
        )

    return results