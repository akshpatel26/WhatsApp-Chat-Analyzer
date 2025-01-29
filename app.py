import streamlit as st
import preprocessor
import helper
import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd

st.sidebar.title('WhatsApp Chat Analysis')
col1, col2, col3, col4 = st.sidebar.columns([1, 2, 2, 1])
with col2:
    st.image('https://upload.wikimedia.org/wikipedia/commons/thumb/6/6b/WhatsApp.svg/479px-WhatsApp.svg.png', width=90)
with col3:
    st.image('analy.png', width=90)

st.sidebar.caption(
    'This application lets you analyze Whatsapp conversations in a very comprehensive manner, with charts, metrics, '
    'and other forms of analysis.')
st.title('WhatsApp Chat Analyzer')

with st.expander('See!!.. How it works?'):
    st.subheader('Steps to Analyze:')
    st.markdown(
        '1. Export the chat by going to WhatsApp on your phone, opening the chat, clicking on the three dots, '
        'selecting "More," and then choosing "Export Chat" without media. Save the file to your desired location.')
    st.markdown(
        '2. Browse or drag and drop the chat file.')
    st.markdown('3. Select a user or group to analyze, or leave the default setting of "All" to analyze for all users.')
    st.markdown('4. Click the "Show Analysis" button.')
    st.markdown(
        '5. Enable "Wide mode" for a better viewing experience in settings, or close the sidebar on mobile for improved'
        ' view.')
    st.markdown(
        '6. To analyze for a single user, select their name from the dropdown and click "Show Analysis" again.')
    st.markdown(
        '7. Repeat the steps for additional chats.')

uploaded_file = st.sidebar.file_uploader("Choose a WhatsApp chat text file")
if uploaded_file is not None:
    # To read file as bytes:
    bytes_data = uploaded_file.getvalue()
    data = bytes_data.decode("utf-8")
    df = preprocessor.preprocess(data)

    # Fetch unique users
    user_list = df['user'].unique().tolist()
    if 'group_notification' in user_list:
        user_list.remove('group_notification')
    user_list.sort()
    user_list.insert(0, "Overall")

    selected_user = st.sidebar.selectbox("Show analysis wrt", user_list)

    if st.sidebar.button("Show Analysis"):
        # Fetch all statistics
        stats = helper.fetch_stats(selected_user, df)

        # Display Title
        st.title("Chat Statistics")

        # Display date range and total members
        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("Chat From", stats['chat_from'])
        with col2:
            st.metric("Chat To", stats['chat_to'])
        with col3:
            st.metric("Total Members", stats['total_members'])

        # Display message statistics
        col1, col2, col3, col4, col5 = st.columns(5)
        with col1:
            st.metric("Total Messages", stats['num_messages'])
        with col2:
            st.metric("Total Words", stats['num_words'])
        with col3:
            st.metric("Media Shared", stats['num_media'])
        with col4:
            st.metric("Links Shared", stats['num_links'])
        with col5:
            st.metric("Missed Calls", stats['missed_calls'])
            # bar plot of user activity
        with st.expander("Which members are the most active in the chat?...click '+' to see details"):
            st.markdown(
                'The graph shows the activity level of all members in the chat, represented by a bar chart. '
                'The longest bar represents the highest level of contribution in the chat, and the names of '
                'the members are listed on the X-axis. The second graph illustrates the average number of messages '
                'among all members and shows how much a member\'s activity is above or below the average.')

        user_count = df['user'].value_counts()
        st.bar_chart(user_count)

    # with st.expander("Message Pattern Analysis", expanded=False):
    
        # Get pattern analysis results
        pattern_results = helper.analyze_message_patterns(df, selected_user)

        # Display basic statistics
        st.subheader("Message Pattern Statistics")
        col1, col2 = st.columns(2)

        with col1:
            st.metric("Average Message Length",
                      f"{pattern_results['avg_message_length']:.1f} characters")
        with col2:
            st.metric("Average Words per Message",
                      f"{pattern_results['avg_words_per_message']:.1f} words")

        # Display visualizations
        # st.subheader("Pattern Visualizations")
        figs = helper.create_pattern_visualizations(pattern_results, df)

        # Show timing distribution
        if 'timing' in figs:
            st.subheader("Message Timing Patterns")
            st.pyplot(figs['timing'])
        # Monthly timeline
        st.title("Monthly Timeline")
        timeline = helper.monthly_timeline(selected_user, df)
        fig, ax = plt.subplots()
        ax.plot(timeline['time'], timeline['message'], color='green', marker="o")
        plt.xticks(rotation='vertical')
        st.pyplot(fig)

        # Activity map
        st.title('Activity Map')
        col1, col2 = st.columns(2)

        with col1:
            st.header("Most Busy Day")
            busy_day = helper.week_activity_map(selected_user, df)
            fig, ax = plt.subplots()
            ax.bar(busy_day.index, busy_day.values, color='purple')
            plt.xticks(rotation='vertical')
            st.pyplot(fig)

        with col2:
            st.header("Most Busy Month")
            busy_month = helper.month_activity_map(selected_user, df)
            fig, ax = plt.subplots()
            ax.bar(busy_month.index, busy_month.values, color='orange')
            plt.xticks(rotation='vertical')
            st.pyplot(fig)

        # Weekly Activity Map
        st.title("Weekly Activity Map")
        user_heatmap = helper.activity_heatmap(selected_user, df)

        # Check if user_heatmap is empty
        if user_heatmap.empty:
            st.warning("No activity data available for the selected user.")
        else:
            fig, ax = plt.subplots()
            ax = sns.heatmap(user_heatmap, cmap='Blues', annot=True, fmt='.0f')
            plt.title('Activity Heatmap')
            plt.xlabel('Hour of Day')
            plt.ylabel('Day of Week')
            st.pyplot(fig)

        # Finding the busiest users in the group (Group level)
        if selected_user == 'Overall':
            st.title('Most Busy Users')
            x, new_df = helper.most_busy_users(df)

            # Ensure x is a DataFrame or Series
            if isinstance(x, (pd.Series, pd.DataFrame)):
                fig, ax = plt.subplots()
                col1, col2 = st.columns(2)

                with col1:
                    fig, ax = plt.subplots(figsize=(10, 11))  # Set a specific figure size
                    sns.barplot(x=x.index, y=x.values, palette="viridis")  # Seaborn bar plot
                    ax.set(xlabel=None)
                    st.pyplot(fig)
                with col2:
                    st.dataframe(new_df)
            else:
                st.error("Error: Unable to retrieve busy users data.")

        # WordCloud
        st.title("Wordcloud")
        df_wc = helper.create_wordcloud(selected_user, df)  # Ensure this function exists in helper.py
        fig, ax = plt.subplots()
        ax.imshow(df_wc, interpolation='bilinear')  # Use interpolation for better display
        ax.axis('off')  # Hide axes
        st.pyplot(fig)

        # Most common words
        st.title("Most Common Words")
        most_common_df = helper.most_common_words(selected_user, df)
        fig, ax = plt.subplots(figsize=(10, 6))  # Set a specific figure size
        sns.barplot(x='Frequency', y='Word', data=most_common_df, palette="rocket",
                    ax=ax)  # Seaborn horizontal bar plot

        # Display plot in Streamlit
        st.pyplot(fig)

        # Emoji analysis
        emoji_df = helper.emoji_helper(selected_user, df)
        st.title("Emoji Analysis")

        col1, col2 = st.columns(2)

        with col1:
            st.dataframe(emoji_df)
        with col2:
            fig, ax = plt.subplots()
            ax.pie(emoji_df['Count'].head(), labels=emoji_df['Emoji'].head(), autopct="%0.2f")  # Access columns by name
            st.pyplot(fig)

        try:
            # Response Patterns
            response_patterns = helper.get_response_patterns(df)
            if not response_patterns.empty:
                st.subheader("Response Patterns Analysis")
                avg_response_times = response_patterns.groupby(['from_user', 'to_user'])['response_time'].mean()
                st.dataframe(avg_response_times.reset_index())

            # Peak Activity Hours
            peak_hours = helper.get_peak_activity_hours(selected_user, df)
            if not peak_hours.empty:
                st.subheader("Peak Activity Hours")
                fig, ax = plt.subplots()
                peak_hours.plot(kind='bar', ax=ax)
                plt.title('Peak Activity Hours')
                plt.xlabel('Hour of Day')
                plt.ylabel('Number of Messages')
                st.pyplot(fig)
        except Exception as e:
            st.error(f"Error in advanced analytics: {str(e)}")

        # Show sentiment distribution
        if 'sentiment' in figs:
            st.subheader("Message Sentiment Distribution")
            st.pyplot(figs['sentiment'])

        # Show user interactions
        if 'interactions' in figs:
            st.subheader("Top User Interactions")
            st.pyplot(figs['interactions'])



