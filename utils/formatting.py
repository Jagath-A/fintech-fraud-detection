def format_inr(value, decimals=0):
    """Format numeric values as Indian Rupees with Indian digit grouping."""
    try:
        number = float(value)
    except (TypeError, ValueError):
        number = 0.0

    sign = "-" if number < 0 else ""
    number = abs(number)
    formatted = f"{number:.{decimals}f}"
    whole, _, fraction = formatted.partition(".")

    if len(whole) > 3:
        last_three = whole[-3:]
        remaining = whole[:-3]
        groups = []
        while remaining:
            groups.insert(0, remaining[-2:])
            remaining = remaining[:-2]
        whole = ",".join(groups + [last_three])

    suffix = f".{fraction}" if decimals > 0 else ""
    return f"{sign}₹{whole}{suffix}"

