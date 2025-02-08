import pandas as pd
import re

def preprocess(data):
    # Split the data into lines
    lines = data.split('\n')
    
    # Create a list to hold the processed messages
    messages = []
    
    # Regex patterns for multiple timestamp formats
    patterns = {
        '12h_standard': r'(\d{2}/\d{2}/\d{2},\s\d{1,2}:\d{2}\s[APMapm]{2})\s-\s(.*?):\s?(.*)',
        '12h_bracketed': r'\[(\d{2}/\d{2}/\d{2},\s\d{2}:\d{2}:\d{2}\s[APMapm]{2})\]\s(.*?):\s(.*)',
        '12h_extended': r'(\d{2}/\d{2}/\d{4},\s\d{1,2}:\d{2}\s[APMapm]{2})\s-\s(.*?):\s?(.*)',
        
        # 24-hour formats
        '24h_standard': r'(\d{2}/\d{2}/\d{2},\s\d{1,2}:\d{2})\s-\s(.*?):\s?(.*)',
        '24h_bracketed': r'\[(\d{2}/\d{2}/\d{2},\s\d{2}:\d{2}:\d{2})\]\s(.*?):\s(.*)',
        '24h_extended': r'(\d{2}/\d{2}/\d{4},\s\d{1,2}:\d{2})\s-\s(.*?):\s?(.*)'
    }
    
    for line in lines:
        line = line.strip()
        if not line:
            continue
        
        matched = False
        for pattern in patterns.values():
            match = re.match(pattern, line)
            if match:
                date_time, user, message = match.groups()
                messages.append([date_time, user.strip(), message.strip()])
                matched = True
                break
        
        # Handle continued messages
        if not matched and messages:
            messages[-1][2] += '\n' + line.strip()
    
    # Create DataFrame
    df = pd.DataFrame(messages, columns=['date', 'user', 'message'])
    
    # Convert dates with multiple format attempts
    date_formats = [
        '%d/%m/%y, %I:%M %p',
        '%d/%m/%y, %I:%M:%S %p',
        '%d/%m/%Y, %I:%M %p',
        '%d/%m/%y, %H:%M',
        '%d/%m/%y, %H:%M:%S',
        '%d/%m/%Y, %H:%M'
    ]
    
    # Function to try multiple datetime conversions
    def convert_datetime(date_series):
        for fmt in date_formats:
            try:
                converted = pd.to_datetime(date_series, format=fmt)
                if not converted.empty:
                    return converted
            except:
                continue
        return pd.to_datetime(date_series, errors='coerce')
    
    # Convert dates
    df['date'] = convert_datetime(df['date'])
    
    # Handle potential conversion failures
    df = df.dropna(subset=['date'])
    
    # Extract datetime features safely
    if not df.empty:
        df['only_date'] = df['date'].dt.date
        df['year'] = df['date'].dt.year
        df['month'] = df['date'].dt.month_name()
        df['month_num'] = df['date'].dt.month
        df['day'] = df['date'].dt.day
        df['day_name'] = df['date'].dt.day_name()
        df['hour'] = df['date'].dt.hour
        df['minute'] = df['date'].dt.minute
    
    # Optional: Handle media and system messages
    df['is_media'] = df['message'].str.contains('<Media omitted>', case=False)
    
    print(f"Total messages processed: {len(df)}")
    
    return df