def format_currency(amount):
    return f"₹{amount:,}"

def format_duration(hours):
    if isinstance(hours, str):
        return hours
    return f"{hours} hrs"

def format_percentage(value):
    return f"{value:.1f}%"
