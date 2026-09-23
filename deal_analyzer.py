from product import Deal


NON_STORE_SOURCES = [
    "Alibaba Guide",
    "Price Comparison",
    "Unknown"
]


def create_deal(store, prices, link):

    if not prices:
        return None

    # Keep valid positive prices
    valid_prices = [
        price
        for price in prices
        if 0 < price <= 1000000
    ]

    if not valid_prices:
        return None

    lowest_price = min(valid_prices)

    if store == "Dubizzle":
        source_type = "Marketplace"
    else:
        source_type = "Store"

    return Deal(
        store,
        lowest_price,
        link,
        source_type
    )