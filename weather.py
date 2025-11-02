import re
import requests
from bs4 import BeautifulSoup



def fetch_tenki_jp():
    url = "https://tenki.jp/forecast/2/10/3630/7202/"
    r = requests.get(url)
    soup = BeautifulSoup(r.text, "html.parser")

    # 天気
    #weather = soup.find('p', class_='weather-telop')
    weather = soup.select_one('.weather-telop').get_text(strip = True)
    
    # 温度
    #temp_max = soup.find('dd', class_='high-temp temp')
    #temp_min = soup.find('dd', class_='low-temp temp')
    temp = soup.select_one('.date-value').get_text(strip = True).replace('[0]', '').split('℃')
    temp_max = re.sub(r'\D+', '', temp[0])
    temp_min = re.sub(r'\D+', '', temp[1])
    # 降水確率
    row = soup.select_one('.rain-probability').get_text(strip = True).replace('降水確率', '').replace('---', '', 3)
    rain_values = row.split('%')
    rain = max(rain_values)

    return {
        'weather': weather,
        'temp_max': temp_max,
        'temp_min': temp_min,
        "rain": rain
    }


def notify_discord(msg):
    requests.post('https://discord.com/api/webhooks/1434390104826187938/W1OFhik2opEo103XL7NNxNkpJ_qTu_Ph-jPWHcDZ678Er3PQzR2flFZir20iqbCiRm-5', json={"content": msg})


def main():
    data = fetch_tenki_jp()
    msg = (
        "⛅ **今日の天気**\n"
        f"天気: {data['weather']}\n"
        f"最高気温: {data['temp_max']}℃\n"
        f"最低気温: {data['temp_min']}℃\n"
        f"降水確率: {data['rain']}%"
    )

    notify_discord(msg)
    #print(data)

if __name__ == '__main__': main()