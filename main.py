import sys

from scraper import search_products
from price_scraper import extract_product_price
from store_classifier import classify_store
from deal_analyzer import create_deal

sys.stdout.reconfigure(encoding="utf-8")

deals = []
SKIP_SOURCES = [
    "Alibaba Guide",
    "Price Comparison",
    "Unknown"
]

print("=" * 50)
print("          SMART BUY")
print("=" * 50)
product_name = input("\nWhat do you want to buy? ")

print("\nSearching for the best deals...\n")

results = search_products(product_name)

if not results:

    print("No results found.")

else:

    print(f"Found {len(results)} results:\n")

    for i, product in enumerate(results, 1):

       store = classify_store(product["link"])

       print(f"{i}. {product['title']}")
       print(f"Store: {store}")
       print(f"Website: {product['link']}")
       if store in SKIP_SOURCES:
        print("Skipped - not a direct store source.")
        print("-" * 70)
        continue

       price = product["search_price"]
       

       if price:

          print(f"✓ Price found from search: {price:,.2f} EGP")

          deal = create_deal(
            store,
            [price],
            product["link"]
        )

          if deal:
            deals.append(deal)

       else:

           print("No price found in search result.")

       print("-" * 70)

       if store in SKIP_SOURCES:

         print("Skipped - not a direct store source.")
         print("-" * 70)
         continue

       print("Checking price...")

       price, source,confidence = extract_product_price(product["link"],
                                                        product_name )

       if price:

         print(f"✓ Price found: {price}")
         print(f"Source: {source}")
         print(f"Confidence: {confidence}")

         deal = create_deal(
             store,
             [price],
             product["link"]
    )

         if deal:
             print(f"Lowest price: {deal.price:,.2f} EGP")
             print(f"Type: {deal.source_type}")
             deals.append(deal)

         else:
           print("Not suitable for price comparison.")

       else:

        print("✗ Reliable Price not found")

    print("-" * 70)

print("\n")
print("=" * 50)
print("           PRICE COMPARISON")
print("=" * 50)

if deals:

    deals.sort(key=lambda deal: deal.price)

    for i, deal in enumerate(deals, 1):

        print(
            f"{i}. {deal.store} "
            f"- {deal.price:,.2f} EGP "
            f"({deal.source_type})"
        )

        print(deal.link)
        print("-" * 50)

else:

    print("No valid deals found.")