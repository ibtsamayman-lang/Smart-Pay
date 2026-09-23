import streamlit as st
import importlib

from query_parser import parse_query
from scraper import search_products


# ==============================
# Location
# ==============================

try:

    streamlit_geolocation = importlib.import_module(
        "streamlit_geolocation"
    ).streamlit_geolocation

except (ImportError, AttributeError):

    def streamlit_geolocation():
        return None


# ==============================
# Page Settings
# ==============================

st.set_page_config(
    page_title="SmartBuy",
    page_icon="🛍️",
    layout="wide"
)


# ==============================
# Header
# ==============================

st.title("🛍️ SmartBuy")

st.markdown(
    "### 🧠 Smart Product Search"
)

st.write(
    "Find real products, prices, images, stores "
    "and direct links in one place."
)


# ==============================
# Search
# ==============================

product_name = st.text_input(
    "🔎 What do you want to buy?",
    placeholder="Example: iPhone 15 / فستان أسود تحت 2000"
)


search_button = st.button(
    "🔍 Search",
    use_container_width=True
)


# ==============================
# Location
# ==============================

with st.expander("📍 Nearby Stores"):

    location = streamlit_geolocation()

    if location:

        latitude = location.get("latitude")
        longitude = location.get("longitude")

        if (
            latitude is not None
            and longitude is not None
        ):

            st.success(
                "📍 Location detected!"
            )

            maps_url = (
                "https://www.google.com/maps/search/"
                + product_name.replace(" ", "+")
                + "/@"
                + str(latitude)
                + ","
                + str(longitude)
                + ",14z"
            )

            st.link_button(
                "🗺️ Find Nearby Stores",
                maps_url
            )

    else:

        st.info(
            "Allow location access to search "
            "for nearby stores."
        )


# ==============================
# Search Products
# ==============================

if search_button:

    if not product_name.strip():

        st.warning(
            "Please enter a product name."
        )

    else:

        # ==============================
        # Smart Query Understanding
        # ==============================

        query_info = parse_query(
            product_name
        )

        st.subheader(
            "🧠 Smart Understanding"
        )

        col1, col2, col3, col4 = st.columns(4)

        with col1:

            st.metric(
                "Category",
                query_info["category"]
                or "Not detected"
            )

        with col2:

            st.metric(
                "Brand",
                query_info["brand"]
                or "Not detected"
            )

        with col3:

            st.metric(
                "Color",
                query_info["color"]
                or "Not detected"
            )

        with col4:

            if query_info["budget"]:

                st.metric(
                    "Budget",
                    f"{query_info['budget']:,.0f} EGP"
                )

            else:

                st.metric(
                    "Budget",
                    "No limit"
                )


        st.divider()


        # ==============================
        # Search
        # ==============================

        with st.spinner(
            "🔎 Finding real products..."
        ):

            results = search_products(
                product_name
            )


        # ==============================
        # No Results
        # ==============================

        if not results:

            st.error(
                "No real product pages were found."
            )

            st.info(
                "Try another product name "
                "in Arabic or English."
            )


        else:

            # ==============================
            # Apply Budget Filter
            # ==============================

            budget = query_info["budget"]

            if budget:

                filtered_results = []

                for product in results:

                    price = product.get(
                        "price"
                    )

                    if price is not None:

                        if price <= budget:

                            filtered_results.append(
                                product
                            )

                # If budget filtering removed
                # everything, keep original results
                # so the user can still see products.

                if filtered_results:

                    results = filtered_results


            # ==============================
            # Results Count
            # ==============================

            st.success(
                f"Found {len(results)} products."
            )

            st.divider()


            # ==============================
            # Product Grid
            # ==============================

            for i in range(
                0,
                len(results),
                3
            ):

                row = results[
                    i:i + 3
                ]

                columns = st.columns(3)


                for col, product in zip(
                    columns,
                    row
                ):

                    with col:

                        # ==============================
                        # Product Image
                        # ==============================

                        image = product.get(
                            "image"
                        )

                        if image:

                            try:

                                st.image(
                                    image,
                                    use_container_width=True
                                )

                            except Exception:

                                st.markdown(
                                    """
                                    <div style="
                                        height:220px;
                                        display:flex;
                                        align-items:center;
                                        justify-content:center;
                                        background:#f3f3f3;
                                        border-radius:15px;
                                        font-size:60px;
                                    ">
                                    🛍️
                                    </div>
                                    """,
                                    unsafe_allow_html=True
                                )

                        else:

                            st.markdown(
                                """
                                <div style="
                                    height:220px;
                                    display:flex;
                                    align-items:center;
                                    justify-content:center;
                                    background:#f3f3f3;
                                    border-radius:15px;
                                    font-size:60px;
                                ">
                                🛍️
                                </div>
                                """,
                                unsafe_allow_html=True
                            )


                        # ==============================
                        # Product Name
                        # ==============================

                        st.subheader(
                            product.get(
                                "title",
                                "Unknown Product"
                            )
                        )


                        # ==============================
                        # Store
                        # ==============================

                        st.write(
                            "🏪 "
                            + product.get(
                                "store",
                                "Unknown Store"
                            )
                        )


                        # ==============================
                        # Price
                        # ==============================

                        price = product.get(
                            "price"
                        )

                        currency = product.get(
                            "currency",
                            "EGP"
                        )


                        if price is not None:

                            st.markdown(
                                f"### 💰 "
                                f"{price:,.2f} "
                                f"{currency}"
                            )

                        else:

                            st.warning(
                                "💰 Price unavailable"
                            )


                        # ==============================
                        # Product Link
                        # ==============================

                        link = product.get(
                            "link"
                        )

                        if link:

                            st.link_button(
                                "🛒 View Product",
                                link,
                                use_container_width=True
                            )


                        st.divider()