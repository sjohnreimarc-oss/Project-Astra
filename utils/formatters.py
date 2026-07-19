def convert_seconds(seconds):
    """Convert seconds to a more readable format (days, hours, minutes, seconds)."""
    days = seconds // 86400
    hours = (seconds % 86400) // 3600
    minutes = (seconds % 3600) // 60
    seconds = seconds % 60
    seconds = round(seconds, 3)  # Round to 3 decimal places
    time_string = ""
    if days > 0:
        time_string += f"{int(days)} d, "
    if hours > 0:
        time_string += f"{int(hours)} h, "
    if minutes > 0:
        time_string += f"{int(minutes)} min, "
    time_string += f"{seconds}"
    return time_string
