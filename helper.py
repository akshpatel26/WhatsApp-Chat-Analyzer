import pandas as pd
import numpy as np
import re
from collections import Counter
from wordcloud import WordCloud
from urlextract import URLExtract
import matplotlib.pyplot as plt
import seaborn as sns

def create_pattern_visualizations(pattern_results, df):
    # Remove NaN values before creating pie chart
    sentiment_data = pattern_results['sentiment_counts'].dropna()
    
    # Only create pie chart if there are non-zero values
    if len(sentiment_data) > 0:
        fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 6))
        
        # Rest of your existing visualization code
        ax2.pie(sentiment_data, labels=sentiment_data.index, autopct='%1.1f%%', colors=c)
    else:
        print("No valid sentiment data to visualize")
        
def fetch_stats(selected_user, df):
    if selected_user != 'Overall':
        df = df[df['user'] == selected_user]

    # Total Messages
    num_messages = df.shape[0]

    # Total Words (excluding media and links)
    words = []
    for msg in df['message'].apply(lambda x: str(x).lower()):
        ms = re.split(r'[`\-=~!@#$%^&*()_+\[\]{};\'\\:"|<,./<>? ]', msg)
        for word in ms:
            if word and word != 'media' and word != 'omitted':
                words.append(word)

    # Media Messages
    media_count = df['message'].str.contains('<media omitted>', case=False).sum()

    # Links
    extractor = URLExtract()
    links = []
    for message in df['message']:
        links.extend(extractor.find_urls(str(message)))

    # Missed Calls
    missed_calls = df['message'].str.contains('missed .* call', case=False, regex=True).sum()

    # Total Members
    total_members = df['user'].nunique()

    # Chat date range
    df_sorted = df.sort_values('date')
    chat_from = df_sorted['date'].iloc[0].strftime('%Y-%m-%d') if not df_sorted.empty else "N/A"
    chat_to = df_sorted['date'].iloc[-1].strftime('%Y-%m-%d') if not df_sorted.empty else "N/A"

    return {
        'num_messages': num_messages,
        'num_words': len(words),
        'num_media': media_count,
        'num_links': len(links),
        'missed_calls': missed_calls,
        'total_members': total_members,
        'chat_from': chat_from,
        'chat_to': chat_to
    }


def get_chat_patterns(df):
    # Group by date to find who starts and ends chats
    date_groups = df.groupby('date')

    chat_started_by = date_groups.first()['user'].value_counts().reset_index()
    chat_started_by.columns = ['Member', 'Count']

    chat_ended_by = date_groups.last()['user'].value_counts().reset_index()
    chat_ended_by.columns = ['Member', 'Count']

    return chat_started_by, chat_ended_by


def monthly_timeline(selected_user, df):
    if selected_user != 'Overall':
        df = df[df['user'] == selected_user]

    timeline = df.groupby(['year', 'month_num', 'month']).count()['message'].reset_index()
    timeline['time'] = timeline['month'] + '-' + timeline['year'].astype(str)
    return timeline


def week_activity_map(selected_user, df):
    if selected_user != 'Overall':
        df = df[df['user'] == selected_user]

    return df['day_name'].value_counts()


def month_activity_map(selected_user, df):
    if selected_user != 'Overall':
        df = df[df['user'] == selected_user]

    return df['month'].value_counts()


def activity_heatmap(selected_user, df):
    if selected_user != 'Overall':
        df = df[df['user'] == selected_user]

    user_heatmap = df.pivot_table(index='day_name', columns='hour', values='message', aggfunc='count').fillna(0)
    return user_heatmap


def most_busy_users(df):
    x = df['user'].value_counts().head()
    new_df = df['user'].value_counts().reset_index()
    new_df.columns = ['user', 'num_messages']
    return x, new_df


def create_wordcloud(selected_user, df):
    if selected_user != 'Overall':
        df = df[df['user'] == selected_user]

    wc = WordCloud(width=500, height=500, min_font_size=10, background_color='white').generate(' '.join(df['message']))
    return wc


def most_common_words(selected_user, df):
    if selected_user != 'Overall':
        df = df[df['user'] == selected_user]

    words = ' '.join(df['message'])
    words = re.findall(r'\w+', words)
    most_common = Counter(words).most_common(10)
    return pd.DataFrame(most_common, columns=['Word', 'Frequency'])


def emoji_helper(selected_user, df):
    if selected_user != 'Overall':
        df = df[df['user'] == selected_user]

    emojis = df['message'].str.findall(
        r'[\U0001F600-\U0001F64F\U0001F300-\U0001F5FF\U0001F680-\U0001F6FF\U0001F700-\U0001F77F\U0001F900-\U0001F9FF\U0001F1E0-\U0001F1FF]+')
    emojis = [item for sublist in emojis for item in sublist]
    emoji_counts = Counter(emojis).most_common(10)
    return pd.DataFrame(emoji_counts, columns=['Emoji', 'Count'])


def get_response_patterns(df):
    """Analyze response patterns between users"""
    # Sort messages by datetime
    df_sorted = df.sort_values('date')

    # Calculate time difference between messages
    df_sorted['time_diff'] = df_sorted['date'].diff()

    # Get response times between users
    response_times = []
    prev_user = None

    for idx, row in df_sorted.iterrows():
        if prev_user and prev_user != row['user']:
            response_times.append({
                'from_user': prev_user,
                'to_user': row['user'],
                'response_time': row['time_diff'].total_seconds() / 60  # Convert to minutes
            })
        prev_user = row['user']

    return pd.DataFrame(response_times)


def get_peak_activity_hours(selected_user, df):
    """Analyze peak activity hours"""
    if selected_user != 'Overall':
        df = df[df['user'] == selected_user]

    hourly_activity = df.groupby('hour')['message'].count()
    peak_hours = hourly_activity.nlargest(3)
    return peak_hours



# Add these functions to helper.py

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.cluster import KMeans
from sklearn.preprocessing import StandardScaler
from textblob import TextBlob
from collections import defaultdict


def analyze_message_patterns(df, selected_user='Overall'):
    """Analyze message patterns including timing, length, and content clusters"""
    if selected_user != 'Overall':
        df = df[df['user'] == selected_user]

    # Message timing patterns
    df['hour_category'] = pd.cut(df['hour'],
                                 bins=[0, 6, 12, 18, 24],
                                 labels=['Night', 'Morning', 'Afternoon', 'Evening'])

    # Message length analysis
    df['message_length'] = df['message'].str.len()
    df['word_count'] = df['message'].str.split().str.len()

    # Basic statistics
    timing_patterns = df['hour_category'].value_counts()
    avg_message_length = df['message_length'].mean()
    avg_words_per_message = df['word_count'].mean()

    # Message content clustering
    vectorizer = TfidfVectorizer(max_features=100, stop_words='english')

    # Filter out media messages and ensure messages are strings
    text_messages = df[~df['message'].str.contains('<media omitted>', case=False, na=False)]['message'].astype(str)

    if len(text_messages) > 10:  # Only cluster if we have enough messages
        tfidf_matrix = vectorizer.fit_transform(text_messages)

    # Sentiment analysis
    def get_sentiment(text):
        try:
            return TextBlob(str(text)).sentiment.polarity
        except:
            return 0

    df['sentiment'] = df['message'].apply(get_sentiment)

    # User interaction patterns
    user_interactions = defaultdict(int)
    prev_user = None
    for user in df['user']:
        if prev_user and user != prev_user:
            user_interactions[f"{prev_user}->{user}"] += 1
        prev_user = user

    # Compile results
    results = {
        'timing_patterns': timing_patterns.to_dict(),
        'avg_message_length': avg_message_length,
        'avg_words_per_message': avg_words_per_message,
        'sentiment_stats': {
            'positive': (df['sentiment'] > 0.2).sum(),
            'neutral': ((df['sentiment'] >= -0.2) & (df['sentiment'] <= 0.2)).sum(),
            'negative': (df['sentiment'] < -0.2).sum()
        },
        'user_interactions': dict(sorted(user_interactions.items(), key=lambda x: x[1], reverse=True)[:5])
    }

    return results


def create_pattern_visualizations(pattern_results, df):
    """Create visualizations for message patterns"""

    # Create figures dictionary
    figs = {}

    # 1. Time of Day Distribution
    fig1, ax1 = plt.subplots(figsize=(10, 6))
    timing_data = pd.Series(pattern_results['timing_patterns'])
    timing_data.plot(kind='bar', ax=ax1)
    ax1.set_title('Message Distribution by Time of Day')
    ax1.set_ylabel('Number of Messages')
    figs['timing'] = fig1

    # 2. Sentiment Distribution
    fig2, ax2 = plt.subplots(figsize=(8, 8))
    c = ["#DAD7CD", "#A3B18A", "#588157"]
    sentiment_data = pd.Series(pattern_results['sentiment_stats'])
    ax2.pie(sentiment_data, labels=sentiment_data.index, autopct='%1.1f%%', colors=c)
    ax2.set_title('Message Sentiment Distribution')
    figs['sentiment'] = fig2

    # 3. User Interactions Heatmap
    interaction_data = pd.Series(pattern_results['user_interactions'])
    if len(interaction_data) > 0:
        fig3, ax3 = plt.subplots(figsize=(10, 6))
        interaction_df = pd.DataFrame(list(interaction_data.items()),
                                      columns=['Interaction', 'Count'])
        sns.barplot(data=interaction_df, x='Count', y='Interaction', ax=ax3, palette="rocket")
        ax3.set_title('Top User Interactions')
        figs['interactions'] = fig3

    return figs