import pandas as pd
import re


def preprocess(data):
    # Split the data into lines
    lines = data.split('\n')

    # Create a list to hold the processed messages
    messages = []

    # Regex patterns for both 12-hour and 24-hour formats
    patterns = {
        # 12-hour formats
        '12h_1': r'\[(\d{2}/\d{2}/\d{2},\s\d{2}:\d{2}:\d{2}\s[APMapm]{2})\]\s(.*?):\s(.*)', # [DD/MM/YY, HH:MM:SS AM/PM]
        '12h_2': r'(\d{2}/\d{2}/\d{4},\s\d{1,2}:\d{2}\s[APMapm]{2})\s-\s(.*?):\s?(.*)',  # DD/MM/YYYY, HH:MM AM/PM
        '12h_3': r'(\d{2}/\d{2}/\d{4},\s\d{1,2}:\d{2}\s[APMapm]{2})\s-\s([\+0-9\s]+)\s(.*)',  # System messages 12h

        # 24-hour formats
        '24h_1': r'\[(\d{2}/\d{2}/\d{2},\s\d{2}:\d{2}:\d{2})\]\s(.*?):\s(.*)',  # [DD/MM/YY, HH:MM:SS]
        '24h_2': r'(\d{2}/\d{2}/\d{4},\s\d{1,2}:\d{2})\s-\s(.*?):\s?(.*)',  # DD/MM/YYYY, HH:MM
        '24h_3': r'(\d{2}/\d{2}/\d{4},\s\d{1,2}:\d{2})\s-\s([\+0-9\s]+)\s(.*)'  # System messages 24h
    }

    for line in lines:
        if not line.strip():
            continue

        matched = False
        # Try all patterns
        for pattern in patterns.values():
            match = re.match(pattern, line)
            if match:
                date_time, user, message = match.groups()
                messages.append([date_time, user.strip(), message.strip()])
                matched = True
                break

        if not matched:
            # Check if this is a continued message from previous line
            if messages and line.strip():
                messages[-1][2] += '\n' + line.strip()

    # Create DataFrame
    df = pd.DataFrame(messages, columns=['date', 'user', 'message'])

    # Convert the 'message' column to string type
    df['message'] = df['message'].astype(str)

    # Try both 12-hour and 24-hour format conversions
    def convert_datetime(date_series):
        # Try 12-hour formats first
        datetime_12h = pd.to_datetime(date_series, format='%d/%m/%Y, %I:%M %p', errors='coerce')
        datetime_12h_sec = pd.to_datetime(date_series, format='%d/%m/%y, %I:%M:%S %p', errors='coerce')

        # Try 24-hour formats
        datetime_24h = pd.to_datetime(date_series, format='%d/%m/%Y, %H:%M', errors='coerce')
        datetime_24h_sec = pd.to_datetime(date_series, format='%d/%m/%y, %H:%M:%S', errors='coerce')

        # Combine results, taking the first non-NaT value for each row
        result = datetime_12h.combine_first(datetime_12h_sec) \
            .combine_first(datetime_24h) \
            .combine_first(datetime_24h_sec)

        return result

    # Convert dates and handle both formats
    df['date'] = convert_datetime(df['date'].str.strip('[]'))

    # Drop rows where date conversion failed
    df = df.dropna(subset=['date'])

    # Extract additional features
    df['only_date'] = df['date'].dt.date
    df['year'] = df['date'].dt.year
    df['month'] = df['date'].dt.month_name()
    df['month_num'] = df['date'].dt.month
    df['day'] = df['date'].dt.day
    df['day_name'] = df['date'].dt.day_name()
    df['hour'] = df['date'].dt.hour
    df['minute'] = df['date'].dt.minute
    df['second'] = df['date'].dt.second

    print(f"Total messages processed: {len(df)}")

    return df
