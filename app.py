from flask import Flask, jsonify, request, render_template, redirect, url_for
import requests
import csv
app = Flask(__name__)

# 百度地图API密钥
baidu_map_api_key = "mbdkoEaCufPgnzsjWvptjDHl9IiVbmDQ"
hefeng_api_key = "a1db7c4675514e53b0024995347f135a"


@app.route('/')
def index():
    return redirect(url_for('get_weather'))


@app.route('/weather', methods=['GET'])
def get_weather():
    def get_public_ip():
        try:
            response = requests.get("https://httpbin.org/ip")
            data = response.json()
            public_ip = data["origin"]
            return public_ip
        except Exception as e:
            print("获取公共 IP 地址时发生错误：", e)
            return None

    client_ip = get_public_ip()
    print("公共 IP 地址是:", client_ip)
    # client_ip = '27.109.124.6'
    # client_ip = '61.232.224.6'
    # client_ip = '36.32.168.6'
    # client_ip = '14.192.60.6'
    # client_ip = '36.25.128.6'

    # 使用百度地图API获取定位信息
    location_url = f"http://api.map.baidu.com/location/ip?ip={client_ip}&ak={baidu_map_api_key}"
    response = requests.get(location_url)
    location_data = response.json()

    # 打印响应数据结构
    print("Location Data:", location_data)

    # 获取城市信息
    city = location_data["content"]["address_detail"]["city"]
    print(city)

    import csv

    # 直接读取 CSV 文件，查询城市代码
    with open('static/China-City-List-latest.csv', newline='', encoding='utf-8') as csvfile:
        reader = csv.DictReader(csvfile)
        city_name = city  # 你要查询的城市中文名称
        for row in reader:
            if row['Adm2_Name_ZH'] == city_name:
                city_id = row['Location_ID']
                print(f"城市 {city_name} 对应的城市代码为：{city_id}")
                break
        else:
            print(f"未找到城市 {city_name} 的城市代码")

    # 使用百度天气API获取天气详情和空气质量指数
    # 使用和风天气API获取天气详情和空气质量指数
    weather_url = f"https://devapi.qweather.com/v7/weather/now?key={hefeng_api_key}&location={city_id}"
    weather24_url = f"https://devapi.qweather.com/v7/weather/24h?key={hefeng_api_key}&location={city_id}"
    air_url = f"https://devapi.qweather.com/v7/air/now?key={hefeng_api_key}&location={city_id}"


    weather_response = requests.get(weather_url)
    weather24_response = requests.get(weather24_url)
    air_response = requests.get(air_url)
    print(weather_response)
    print(weather24_response)
    print(air_response)
    weather_data = weather_response.json()
    weather24_data = weather24_response.json()
    air_data = air_response.json()
    print(weather_data)
    print(weather24_data)
    print(air_data)
    print(weather24_data['hourly'][0]['temp'])
    # 构建要返回的数据

    temp_list = [
        weather_data['now']['temp'],
        weather24_data['hourly'][0]['temp'],
        weather24_data['hourly'][1]['temp'],
        weather24_data['hourly'][2]['temp'],
        weather24_data['hourly'][3]['temp'],
        weather24_data['hourly'][4]['temp'],
        weather24_data['hourly'][5]['temp'],
        weather24_data['hourly'][6]['temp'],
        weather24_data['hourly'][7]['temp']
    ]
    humidity_list = [
        weather_data['now']['humidity'],
        weather24_data['hourly'][0]['humidity'],
        weather24_data['hourly'][1]['humidity'],
        weather24_data['hourly'][2]['humidity'],
        weather24_data['hourly'][3]['humidity'],
        weather24_data['hourly'][4]['humidity'],
        weather24_data['hourly'][5]['humidity'],
        weather24_data['hourly'][6]['humidity'],
        weather24_data['hourly'][7]['humidity']
    ]
    response_data = {
        "city": city,
        "weather": weather_data['now']['text'],
        "temp": weather_data['now']['temp'],
        "humidity": weather_data['now']['humidity'],
        "t24": temp_list,
        "h24": humidity_list,
        "air_quality": air_data['now']['aqi']
    }
    print(response_data)
    print(response_data['t24'])

    return render_template('index.html', response_data=response_data)
if __name__ == '__main__':
    app.run(debug=True)
