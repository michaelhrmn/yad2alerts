import requests
import os
import psycopg2
import sys

def telegram_bot_sendtext(bot_message):
    bot_token = os.environ.get('bot_token')
    bot_chatID = os.environ.get('bot_chatID')
    send_text = 'https://api.telegram.org/bot' + bot_token + '/sendMessage?chat_id=' + bot_chatID + '&parse_mode=Markdown&text=' + bot_message
    response = requests.get(send_text)

    return response.json()

try:
    DATABASE_URL = os.environ['DATABASE_URL']
    conn = psycopg2.connect(DATABASE_URL, sslmode='require')
    cursor = conn.cursor()
    cursor.execute("SELECT id from apts;")
    viewedapts = cursor.fetchall()

except (Exception, psycopg2.Error) as error:
    print ("Error while fetching data from PostgreSQL", error)
    print(telegram_bot_sendtext("Failed to fetch data from DB"))
    sys.exit("Error while fetching data from PostgreSQL")

print("Connected to DB")

apts = []
for row in viewedapts:
    apts.append(row[0])

print("list retrieved: ")
print(apts)

URL = os.environ.get('search_url')
try:
    r = requests.get(url = URL, headers={"USER-AGENT":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.103 Safari/537.36"})
except
    sys.exit("Error getting data from yad2")

data = r.json()

for apt in data["feed"]["feed_items"]:
    if 'row_1' in apt and apt["id"] not in apts:
        print(apt["row_1"]+": "+apt["id"])
        try:
            print("Sending msg via bot")
            print(telegram_bot_sendtext(apt["row_1"]+"\n"+apt["row_2"]+"\n"+apt["price"]+"\n"+"https://www.yad2.co.il/item/"+apt["id"]))
        except:
            print("Failed to send message with description, sending link only")
            print(telegram_bot_sendtext("https://www.yad2.co.il/item/" + apt["id"]))

        cursor.execute("INSERT INTO apts (id) VALUES ('"+apt["id"]+"');")
        conn.commit()
