#!/usr/bin/env python3
# -*- coding: UTF-8 -*-
"""
load_birthdays.py - Birthday Retrieval Module for Pi-Box Birthdays Plugin

This module reads an Excel file containing a list of birthdays and identifies birthdays that match the current date.

Functionality:
1. Parses the birthday dates from an Excel file.
2. Converts date formats into a standardized format.
3. Identifies birthdays occurring today.

Dependencies:
- pandas: For reading and processing the Excel file.
- datetime: For working with dates.

Usage:
This module is used by `pibox.birthdays.py` to retrieve a list of people whose birthday is today.
"""

import pandas as pd
from datetime import datetime

def parse_date(value):
    """
    Converts a given date string into a standardized date format.
    
    :param value: Date in string format (e.g., '12.05' for May 12th).
    :return: A datetime.date object or None if conversion fails.
    """
    try:
        str_value = str(value).replace(',', '.')
        day, month = map(float, str_value.split('.'))
        return datetime(datetime.today().year, int(month), int(day)).date()
    except Exception:
        return None

def find_birthdays_today(file_path, today=None):
    """
    Reads an Excel file and finds all names with birthdays matching today's date.
    
    :param file_path: Path to the Excel file containing birthday data.
    :param today: Optional parameter for specifying a date (useful for testing).
    :return: A list of names whose birthday is today.
    """
    if today is None:
        today = datetime.today().date()

    # Load the Excel file
    df = pd.read_excel(file_path, header=None, names=["Name", "Date_Raw"])
    
    # Convert the "Date_Raw" column into proper date format
    df["Birthday"] = df["Date_Raw"].apply(parse_date)
    
    # Find names with birthdays today
    birthdays_today = df[df["Birthday"].apply(lambda x: x is not None and x.day == today.day and x.month == today.month)]["Name"]
    
    return birthdays_today.tolist()
