import os
import requests
import cloudscraper
from bs4 import BeautifulSoup
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from pystyle import *
import msvcrt
import smtplib
import random
import time


response = requests.get('https://raw.githubusercontent.com/roc4et/leaked/main/version')
print(response.text)
time.sleep(1)
version= "1.0"


def scrape_names():
    directory = "scraped"
    if not os.path.exists(directory):
        os.makedirs(directory)
    api_key = 'E1qWA2fwS-6lQLE3zjxeffKcI6PXuxXU'
    urls = [
        'https://gamerdvr.com/games/fortnite/screenshots',
        'https://gamerdvr.com/games/fortnite/screenshots?page=2',
        'https://gamerdvr.com/games/fortnite/screenshots?page=3',
        'https://gamerdvr.com/games/fortnite/videos?page=1',
        'https://gamerdvr.com/games/fortnite/videos?page=2',
        'https://gamerdvr.com/games/fortnite/videos?page=3'
    ]
    unique_names = set()
    for url in urls:
        scraper = cloudscraper.create_scraper(browser={'browser': 'firefox','platform': 'windows','mobile': False})
        response = scraper.get(url).content
        soup = BeautifulSoup(response, 'html.parser')
        tags = soup.find_all("a")
        excluded_strings = [
            "Gamertag Search",
            "Login",
            "Sign Up",
            "Go Ad Free or Pro",
            "FAQ / Help",
            "About",
            "Advertise",
            "Trending",
            "Videos",
            "Gifs",
            "Screenshots",
            "Playlists",
            "Albums",
            "Challenges",
            "Ad Free / Pro",
            "Swag Shop",
            "More",
            "View game description",
            "Achievements",
            "1",
            "2",
            "3",
            "Next",
            "Home",
            "Become a Pro Supporter",
            "Discord",
            "Games",
            "Fortnite",
            "Top Game Clips",
            "Top Gifs",
            "Top Screenshots",
            "NightSurgeX2",
            "OpRaHs BR OwnS",
            "chaedough",
            "KOBARS GNOMIES",
            "@GamerDVRcom",
            "Xbox Discord",
            "Twitch Discord",
            "Xbox Clips",
            "Privacy Policy",
            "Change Ad Consent"
        ]
        for tag in tags:
            tag_text = tag.text.strip()
            if tag_text not in excluded_strings and all(c.isalnum() or c.isspace() for c in tag_text):
                tag_text = tag_text.replace(' ', '-')
                unique_names.add(tag_text)
    with open('scraped/dvr_names.txt', 'w') as f:
        for value in sorted(unique_names):
            f.write(value + '\n')
    with open('scraped/dvr_names.txt', 'r') as f:
        data = {
            'api_dev_key': api_key,
            'api_option': 'paste',
            'api_paste_code': f.read(),
            'api_paste_name': 'unique_names.txt',
            'api_paste_private': '0',
            'api_paste_expire_date': '1H'
        }
        response = requests.post('https://pastebin.com/api/api_post.php', data=data)
    if response.ok:
        paste_url = response.text
        print(Colorate.Horizontal(Colors.green_to_cyan,f"\n    Successfully scraped names: {paste_url}\n\n"))
    else:
        print(Colorate.Horizontal(Colors.red_to_yellow,f"\n    Failed to upload!\n\n"))
    print(Colorate.Horizontal(Colors.blue_to_purple,f"\n    Press any key to continue!"))
    msvcrt.getch()
    menue()

def iplookup(ip):
    try:
        response = requests.get(f'http://ip-api.com/json/{ip}?fields=status,message,country,countryCode,regionName,city,zip,isp,reverse,query')
        data = response.json()
        city = data['city']
        state = data['regionName']
        zip_code = data['zip']
        isp = data['isp']
        country = data['country']
        country_code = data['countryCode']
        reverse = data['reverse']
        print(Colorate.Horizontal(Colors.green_to_cyan,f"\n    Information about {ip}:"))
        print(Colorate.Horizontal(Colors.green_to_cyan,f"        City: {city}"))
        print(Colorate.Horizontal(Colors.green_to_cyan,f"        State: {state}"))
        print(Colorate.Horizontal(Colors.green_to_cyan,f"        Country: {country}"))
        print(Colorate.Horizontal(Colors.green_to_cyan,f"        Country Code: {country_code}"))
        print(Colorate.Horizontal(Colors.green_to_cyan,f"        Zip Code: {zip_code}"))
        print(Colorate.Horizontal(Colors.green_to_cyan,f"        ISP: {isp}"))
        print(Colorate.Horizontal(Colors.green_to_cyan,f"        Reversed DNS: {reverse}"))
    except:
        print(Colorate.Horizontal(Colors.red_to_yellow,f"\n    Your Request failed! Please try again or check your submitted IP address. \n\n"))
    print(Colorate.Horizontal(Colors.blue_to_purple,f"\n    Press any key to continue!"))
    msvcrt.getch()
    menue()

def stw_receipt(weekday, month, day, year, email):
    try:
        url = "https://raw.githubusercontent.com/roc4et/leaked/main/html/stw.html"
        response = requests.get(url)
        if response.status_code == 200:
            html = response.text
            # Replace the placeholders in the HTML template with the specified values
            html = html.replace("Monday, July 23, 2018", f"{weekday}, {month} {day}, {year}")
            html = html.replace("133", str(random.randint(100, 999)))
            html = html.replace("109", str(random.randint(100, 999)))
            # Set up the email message
            msg = MIMEMultipart()
            msg['From'] = 'Leaked receipt-maker by roc4et#0001'
            msg['To'] = f'{email}'
            msg['Subject'] = 'Your STW receipt is ready:'
            msg.attach(MIMEText(html, 'html'))
            # Connect to the Gmail SMTP server and send the email
            with smtplib.SMTP('smtp.gmail.com', 587) as smtp:
                smtp.starttls()
                smtp.login('epicgames.receipt.roc4et@gmail.com', 'ukbyjlggvlneoskt')
                smtp.send_message(msg)
            print(Colorate.Horizontal(Colors.green_to_cyan, f"\n    Your STW receipt has been successfully sent to {email}."))
        else:
            raise Exception("Failed to fetch the HTML template.")
    except Exception as e:
        print(Colorate.Horizontal(Colors.red_to_yellow, f"\n    Your receipt hasn't been sent, because an error occurred: {str(e)} \n\n"))
    print(Colorate.Horizontal(Colors.blue_to_purple, f"\n    Press any key to continue!"))
    msvcrt.getch()
    menue()

def scrape_friend_list(gamertag):
    directory = "scraped"
    if not os.path.exists(directory):
        os.makedirs(directory)
    headers = {
        "X-Authorization": "f8d6321d-fdad-47aa-a5a4-6c1623769afc"
    }
    url = f"https://xbl.io/api/v2/search/{gamertag}"
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        search_data = response.json()
        people = search_data.get("people", [])  
        if people:
            first_person = people[0]
            xuid = first_person.get("xuid")
        else:
            print(Colorate.Horizontal(Colors.red_to_yellow, "\n    No matching results found for the gamertag. \n\n"))
            return
    else:
        print("Error:", response.status_code)
        return
    url = f"https://xbl.io/api/v2/friends/{xuid}"
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        friends_data = response.json()       
        file_path = os.path.join(directory, "scraped_friends.txt") 
        with open(file_path, "a") as file:
            for friend in friends_data.get("people", []):
                display_name = friend.get("displayName")               
                if display_name:
                    file.write(display_name + "\n")
        print(Colorate.Horizontal(Colors.green_to_cyan, f"\n    Friends for {gamertag} have been saved to 'scraped/scraped_friends.txt'."))
    else:
        print(Colorate.Horizontal(Colors.red_to_yellow, f"\n    Error: {response.status_code} \n\n")) 
    print(Colorate.Horizontal(Colors.blue_to_purple, f"\n    Press any key to continue!"))
    msvcrt.getch()
    menue()

def menue():
    os.system('cls')
    os.system(f'title Leaked.exe ┃ Version: {version} ')
    print(Colorate.Vertical(Colors.red_to_purple,"""\n
    ╔══════════════════════════════════════════════════════════════════════════════════════════════════════════════╗
    ║                                                                                                              ║
    ║                      ██╗     ███████╗ █████╗ ██╗  ██╗███████╗██████╗ ███████╗███╗   ██╗                      ║
    ║                      ██║     ██╔════╝██╔══██╗██║ ██╔╝██╔════╝██╔══██╗██╔════╝████╗  ██║                      ║
    ║                      ██║     █████╗  ███████║█████╔╝ █████╗  ██║  ██║█████╗  ██╔██╗ ██║                      ║
    ║                      ██║     ██╔══╝  ██╔══██║██╔═██╗ ██╔══╝  ██║  ██║██╔══╝  ██║╚██╗██║                      ║                                   
    ║                      ███████╗███████╗██║  ██║██║  ██╗███████╗██████╔╝██║     ██║ ╚████║                      ║                                 
    ║                      ╚══════╝╚══════╝╚═╝  ╚═╝╚═╝  ╚═╝╚══════╝╚═════╝ ╚═╝     ╚═╝  ╚═══╝                      ║
    ║                                                                                   by roc4et#0001             ║
    ╠══════════════════════════════════════════════════════════════════════════════════════════════════════════════╣
    ║                                                                                                              ║
    ║   [1] DVR Scrape                                                                                             ║
    ║   [2] iP Lookup                                                                                              ║
    ║   [3] STW Receipt                                                                                            ║
    ║   [4] Scrape Friends List                                                                                    ║                                   
    ║                                                                                                              ║                                 
    ║                                                                                                              ║
    ║                                                                                                              ║
    ╠══════════════════════════════════════════════════════════════════════════════════════════════════════════════╝
    ║                                                                                                              
    ║                                                                                                              
    ║                                                                                                              """))
    option = input(Colorate.Horizontal(Colors.red_to_purple,"    ╚═══════> \n"))
    if option == '1':
        scrape_names()
    elif option == '2':
        ip=input(Colorate.Horizontal(Colors.red_to_purple,"\n    What iP do you want to Lookup?: "))
        iplookup(ip)
    elif option == '3':
        day=input(Colorate.Horizontal(Colors.red_to_purple,"\n    Day?: "))
        weekday=input(Colorate.Horizontal(Colors.red_to_purple,"    Weekday: "))
        month=input(Colorate.Horizontal(Colors.red_to_purple,"    Month: "))
        year=input(Colorate.Horizontal(Colors.red_to_purple,"    Year: "))
        email=input(Colorate.Horizontal(Colors.red_to_purple,"    Where should the mail be send to: "))
        stw_receipt(weekday,month,day,year,email)
    elif option == '4':
        gamertag=input(Colorate.Horizontal(Colors.red_to_purple,"\n    What gamertag do you want to scrape?: "))
        scrape_friend_list(gamertag)
    else:
        print(Colorate.Horizontal(Colors.red_to_yellow,f"\n    Unknown option! Please try again. \n\n"))
        msvcrt.getch()
        menue()
menue()