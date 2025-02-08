# A Comprehensive Data Analysis on a WhatsApp Group Chat

# *Introduction*:

Whatsapp has quickly become the world’s most popular text and voice messaging application. Specializing in cross-platform messaging with over 1.5 billion monthly active users, this makes it the most popular mobile messenger app worldwide.

- But I thought why not do **Data Analysis on a WhatsApp group chat** of *college students* and find out interesting insights about who is most active,Most Busy Day and Month , the most used emoji, the most actives times of the day, Top User interactions, Chat Statistics, Message Timing Patterns, Most Common Words, Monthly Timeline, WordCloud, Weekly Activity Map? 

- These would be some interesting insights for sure, more for me than for you, since the people in this chat are people I know personally.

# *Data Retrieval & Preprocessing*

### Beginning. How do I export my conversations? From Where To Obtain Data?


- The first step is **Data Retrieval & Preprocessing**, that is to **gather the data**. WhatsApp allows you to **export your chats** through a **.txt format**.

<p align="center">
<img src="extras/WhatsApp Image 2025-01-30 at 20.43.05_3533808e.jpg" width=150 align="center">
</p>

- Tap on **options**, click on **More**, and **Export Chat.**
 <p align="center">
<img src="extras/WhatsApp Image 2025-01-30 at 20.43.10_3a6ca252.jpg" width=150 align="center">
</p>

- I will be Exporting **Without Media.**
 <p align="center">
<img src="extras/WhatsApp Image 2025-01-30 at 20.43.10_412109b8.jpg" width=250 align="center">
</p>

#### NOTE:
- Without media: exports about **40k messages **
- While exporting data, *avoid including media files* because if the number of media files is greater than certain figure then not all the media files are exported.
  
### Opening this .txt file up, you get messages in a format that looks like this:

<img src="extras/textfile.png" align="center">



### *Preparation and reading data*

Since WhatsApp texts are multi-line, you cannot just read the file line by line and get each message that you want. Instead, you need a way to identify if a line is a new message or part of an old message. You could do this use regular expressions, but I went forward with a more simple method, which splits the time formats and creates a DataFrame from a Raw .txt file.

While reading each line, I split it based on a comma and take the first item returned from the `split()` function. If the line is a new message, the first item would be a valid date, and it will be appended as a new message to the list of messages. If it’s not, the message is part of the previous message, and hence, will be appended to the end of the previous message as one continuous message.

```bash
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
Install the required dependencies:
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


![Screenshot 2025-01-31 183110](https://github.com/user-attachments/assets/50efad68-10ad-4356-ad7e-c76225149a4f)


![Screenshot 2025-01-31 185213](https://github.com/user-attachments/assets/65d19de9-f6f5-42e4-86b3-61fffefe2862)


![Screenshot 2025-01-31 185049](https://github.com/user-attachments/assets/88124fe6-1cc7-4da4-a1cc-d66daa11a529)



![Screenshot 2025-01-31 185238](https://github.com/user-attachments/assets/322f20b5-e0cb-4236-be5a-8f51be7df4d5)



![Screenshot 2025-01-31 185427](https://github.com/user-attachments/assets/2acf1ca3-315f-49ac-9a9a-9220559361a0)


![Screenshot 2025-01-31 185437](https://github.com/user-attachments/assets/7ee4d9b4-ca74-4068-9207-7bd4f3aa010c)




![Screenshot 2025-01-31 185448](https://github.com/user-attachments/assets/6724b024-358a-4587-81e7-875d252dd31a)



![Screenshot 2025-01-31 200555](https://github.com/user-attachments/assets/2cc82d62-06f3-4ee6-b206-922d30dfee77)


![Screenshot 2025-01-31 185500](https://github.com/user-attachments/assets/417656b8-1f95-4bb4-aced-ce0eb02a3277)


![Screenshot 2025-01-31 185521](https://github.com/user-attachments/assets/4ed95080-ce8b-4b54-a7a7-3b7f632481ad)

![Screenshot 2025-01-31 185536](https://github.com/user-attachments/assets/c2f73e94-1897-4fda-8eee-e8c62036db89)


![Screenshot 2025-01-31 201041](https://github.com/user-attachments/assets/df53effa-96be-453f-9176-e76fa52b1734)



![Screenshot 2025-01-31 185542](https://github.com/user-attachments/assets/122f10f4-cbb3-41ed-a228-dd7132fc04a7)





![Screenshot 2025-01-31 185509](https://github.com/user-attachments/assets/b99202e9-92e7-4142-8bfa-03b65a706527)


