def analyze_price(current_price, history):

    if not history:

        return {
            "average": current_price,
            "difference": 0,
            "percentage": 0,
            "status": "NEW",
            "message": "This is the first price recorded."
        }


    old_prices = [
        row[1]
        for row in history
    ]

    average_price = sum(old_prices) / len(old_prices)

    difference = current_price - average_price

    percentage = (
        difference / average_price
    ) * 100


    if percentage <= -10:

        status = "GREAT DEAL"

        message = (
            "The current price is significantly "
            "lower than your previous prices."
        )

    elif percentage < 0:

        status = "GOOD PRICE"

        message = (
            "The current price is below "
            "your previous average."
        )

    elif percentage <= 10:

        status = "NORMAL"

        message = (
            "The current price is close "
            "to your usual price."
        )

    else:

        status = "HIGH PRICE"

        message = (
            "The current price is higher "
            "than your previous average."
        )


    return {
        "average": average_price,
        "difference": difference,
        "percentage": percentage,
        "status": status,
        "message": message
    }