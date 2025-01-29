# A Comprehensive Data Analysis on a WhatsApp Group Chat

# *Introduction*:

Whatsapp has quickly become the world’s most popular text and voice messaging application. Specializing in cross-platform messaging with over 1.5 billion monthly active users, this makes it the most popular mobile messenger app worldwide.

- But I thought why not do **Data Analysis on a WhatsApp group chat** of *college students* and find out interesting insights about who is most active,Most Busy Day and Month , the most used emoji, the most actives times of the day, Top User interactions, Chat Statistics, Message Timing Patterns, Most Common Words, Monthly Timeline, WordCloud, Weekly Activity Map? 

- These would be some interesting insights for sure, more for me than for you, since the people in this chat are people I know personally.

# *Data Retrieval & Preprocessing*

### Beginning. How do I export my conversations? From Where To Obtain Data?


- The first step is **Data Retrieval & Preprocessing**, that is to **gather the data**. WhatsApp allows you to **export your chats** through a **.txt format**.
  
- Tap on **options**, click on **More**, and **Export Chat.**

- I will be Exporting **Without Media.**


#### NOTE:
- Without media: exports about **40k messages **
- While exporting data, *avoid including media files* because if the number of media files is greater than certain figure then not all the media files are exported.



### *Preparation and reading data*

Since WhatsApp texts are multi-line, you cannot just read the file line by line and get each message that you want. Instead, you need a way to identify if a line is a new message or part of an old message. You could do this use regular expressions, but I went forward with a more simple method, which splits the time formats and creates a DataFrame from a Raw .txt file.

While reading each line, I split it based on a comma and take the first item returned from the `split()` function. If the line is a new message, the first item would be a valid date, and it will be appended as a new message to the list of messages. If it’s not, the message is part of the previous message, and hence, will be appended to the end of the previous message as one continuous message.

```bash

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
   
```


# *Pre-Processing*

Firstly, let’s load our .txt into a DataFrame.
```bash
df = pd.DataFrame(messages, columns=['date', 'user', 'message'])
```

The dataset now contains 3 columns - DateTime String, User, and Message sent and their respective entries in rows.

**Let’s create some helper columns for better analysis!**

```bash
    df['only_date'] = df['date'].dt.date
    df['year'] = df['date'].dt.year
    df['month'] = df['date'].dt.month_name()
    df['month_num'] = df['date'].dt.month
    df['day'] = df['date'].dt.day
    df['day_name'] = df['date'].dt.day_name()
    df['hour'] = df['date'].dt.hour
    df['minute'] = df['date'].dt.minute
    df['second'] = df['date'].dt.second
```

Now that we have a clean DataFrame to work with, it’s time to perform analysis on it. **Let’s start Visualizing!**


# *Run locally*
Create new project in pycharm and add above files. After that open terminal and run the following command. This will install all the modules needed to run this app.
```bash
pip install -r requirements.txt
```
To run the app, type following command in terminal.
```bash
streamlit run app.py
```

# *Live Demo*

https://whatsapp-chat-analyzer-by-aksh-patel.streamlit.app/


#  *Limitation of Project*

- Maximum file size to be uploaded is 200MB.
- Supports only txt extension.
- Only supports English languages.


# *Exploratory Data Analysis*



![Screenshot 2025-01-29 204644](https://github.com/user-attachments/assets/9b29b8b4-84b9-42c3-8a60-ba85530134ef)


![Screenshot 2025-01-29 204832](https://github.com/user-attachments/assets/ca71c05d-4df4-4ecd-be03-85ed19e0d7c6)



![Screenshot 2025-01-29 210635](https://github.com/user-attachments/assets/d2694db1-f051-4da7-8e49-0ec0d8c64714)


![Screen![Screenshot 2025-01-29 210635](https://github.com/user-attachments/assets/2133e667-cdc9-4134-98a9-d774c2ebfaec)
shot 2025-01-29 210104](https://github.com/user-attachments/assets/bcd07ca1-b0ec-4e12-a458-355e842d29ba)


![Screenshot 2025-01-29 204917](https://github.com/user-attachments/assets/004749d1-fde6-414c-94f0-23a09f822f1f)



![Screenshot 2025-01-29 204952](https://github.com/user-attachments/assets/3fcfd7e7-fa39-4a4b-bbda-c805fb368c7e)





![Screenshot 2025-01-29 210649](https://github.com/user-attachments/assets/29909083-f75f-4028-a414-95bbc9a05ce8)



![Screenshot 2025-01-29 210720](https://github.com/user-attachments/assets/29eafdd5-2ce3-4ab1-8f42-cd9b1165858a)

![Screenshot 2025-01-29 210422](https://github.com/user-attachments/assets/de37b88c-25fc-49cd-8dab-9798a53a2b32)


![Screenshot 2025-01-29 210449](https://github.com/user-attachments/assets/485463d6-2767-44d7-8d26-f7ebe21561f3)

![Screenshot 20![Screenshot 2025-01-29 210501](https://github.com/user-attachments/assets/ad04f186-815d-43ab-9a36-bd51aabdb485)
25-01-29 210720](https://github.com/user-attachments/assets/f485852c-8310-429f-9806-4acd1ed2f066)


![Screenshot 2025-01-29 210408](https://github.com/user-attachments/assets/2735c8dd-52e0-47dd-994e-d8440e1ee4fe)



![Screenshot 2025-01-29 210501](https://github.com/user-attachments/assets/728d5277-6a26-4883-b578-43b2751b90c6)
