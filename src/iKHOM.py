# iKHOM my Virtual Assistant 

# (motivated from Amazon's Alexa)

# @author: KhomZ 
# code coming soon
# coding started at 18th Nov 2021,
import requests
import speech_recognition as sr  # pip install speech_recognition
import pyttsx3  # pip install pyttsx3
import datetime  # pip install datetime
import webbrowser  # pip install webbrowser module
import wikipedia  # pip install wikipedia
import pyjokes  # pip install pyjokes
import pyautogui  # pip install pyautogui
from plyer import notification  # pip install plyer and import notification
from bs4 import BeautifulSoup  # pip install bs4

engine = pyttsx3.init()
voices = engine.getProperty('voices')
engine.setProperty('voice', voices[1].id)  # 1 is for female voice and 0 is for male voice


# now let's define a function that accepts the user's command
def input_query():
    recognizer = sr.Recognizer()  # to recognize  from an audio source
    with sr.Microphone() as source:  # source of recognition
        print('recognition is on....') 
        recognizer.pause_threshold = 0.7
        voice = recognizer.listen(source)
        # this method in turn will record the input from the audio source
        # as long as there's some voice or someone is speaking
        try:
            # print(x)
            query = recognizer.recognize_google(voice).lower()
            print('This is the query that was made....', query)
            return query
        except Exception as ex:
            print('An exception occurred', ex)


def report_time():
    # datetime.datetime.now()
    current_time = datetime.datetime.now().strftime('%I:%M %p')
    return current_time


# making the virtual assistant speak
def speak_va(transcribed_query):
    engine.say(transcribed_query)
    engine.runAndWait()


def make_request(url):
    response = requests.get(url)
    return response.text


# now create function for action
def activate_va():
    user_query = input_query()
    print('user query ....', user_query)
    if 'time' in user_query:
        current_time = report_time()
        print(f"The current time is {current_time}")
        speak_va(f"The current time is {current_time}")

    # opening a specific website using webbrowser module
    elif 'open website' in user_query:
        speak_va("Please type the name of the website that you want to open(Specify full url)")
        website_name = input()
        print(website_name)  # log the website name to the terminal
        webbrowser.open(website_name)
        speak_va(f"{website_name} opened.")

        # webbrowser.get('C:\Program Files\Google\Chrome\Application\chrome.exe %s').open(website_name)
        # c = webbrowser.get('firefox')
        # c.open(website_name)
        # c.open_new_tab(website_name)
    
    # installing wikipedia package and searching on wikipedia
    elif 'wikipedia' in user_query:
        speak_va("Searching on Wikipedia")
        user_query = user_query.replace('wikipedia', ' ')
        result = wikipedia.summary(user_query, sentences=4)
        print(result)
        speak_va(result)

    # installing pyjokes and generating random jokes
    elif 'joke' in user_query:
        random_joke = pyjokes.get_joke()
        print(random_joke)
        speak_va(random_joke)

    # installing pyautogui package and taking screenshot
    elif 'screenshot' in user_query:
        image = pyautogui.screenshot()
        image.save('screenshot.png')
        speak_va('Screenshot taken.')

    # performing google search
    elif 'search' in user_query:
        speak_va("What do you want me to search for? Please type!")
        search_term = input()
        search_url = f"https://www.google.com/search?q={search_term}"
        webbrowser.open(search_url)
        speak_va(f"Here are the results for the search term: {search_term}")

    # installing plyer for notifications, bs4 for web-scraping and requests for api calls
    elif 'covid-19 stats' in user_query:
        html_data = make_request('https://www.worldometers.info/coronavirus/')
        # print(html_data)  # loads the html so we need html parser to get the data
        soup = BeautifulSoup(html_data, 'html.parser')
        total_global_row = soup.find_all('tr', {'class': 'total_row'})[-1]  # looking for all the tr's of the total row
        # and [-1] represents the first row of the end of the table
        total_cases = total_global_row.find_all('td')[2].get_text()
        new_cases = total_global_row.find_all('td')[3].get_text()  # index [3] for column 4
        total_recovered = total_global_row.find_all('td')[6].get_text()

        print('total cases: ', total_cases)
        print('new cases: ', new_cases[1:])  # start from index [1] and omit + sign
        print('total recovered: ', total_recovered)

        notification_message = f"Total cases: {total_cases}\n New Cases: {new_cases[1:]}" \
                               f"\n Total Recovered: {total_recovered}"
        # {} this symbol is for interpolation
        # notification pop up
        notification.notify(
            title="COVID-19 Statistics",
            # message="pending...",
            message=notification_message,
            timeout=10
        )
        speak_va("here are the stats for COVID-19")
        speak_va(f'total cases: {total_cases}')
        speak_va(f'new case: {new_cases[1:]}')
        speak_va(f'total recovered: {total_recovered}')

#         here we need to perform web scrapping for a particular website
#         for that we need the packages
#         pip install bs4 for beautiful soup and
#         pip install requests for api calls to a remote url


while True:
    activate_va()
