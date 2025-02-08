import pandas as pd
from datetime import datetime

def parse_date(value):
    try:
        # Convert to string and split into day and month
        str_value = str(value).replace(',', '.')
        day, month = map(float, str_value.split('.'))
        day, month = int(day), int(month)  # Convert to integers
        return datetime(datetime.today().year, month, day).date()
    except Exception:
        return None

def find_birthdays_today(file_path, today):
    if today is None:
        today = datetime.today().date()

    # Load the Excel file
    df = pd.read_excel(file_path, header=None, names=["Name", "Date_Raw"])
    
    # Convert the "Date_Raw" column into proper date format
    df["Birthday"] = df["Date_Raw"].apply(parse_date)
    
    # Find names with birthdays today
    birthdays_today = df[df["Birthday"].apply(lambda x: x is not None and x.day == today.day and x.month == today.month)]["Name"]
    
    return birthdays_today.tolist()

