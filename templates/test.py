import requests

def get_public_ip():
    try:
        response = requests.get("https://httpbin.org/ip")
        data = response.json()
        public_ip = data["origin"]
        return public_ip
    except Exception as e:
        print("获取公共 IP 地址时发生错误：", e)
        return None

public_ip = get_public_ip()
print("公共 IP 地址是:", public_ip)
