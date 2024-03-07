import json
import requests
import csv
import os

# 加载一次性邮件域名列表
def load_disposable_email_domains():
    disposable_domains = set()
    file_path = os.path.join(os.path.dirname(__file__), "disposable_email_domains.csv")
    with open(file_path, "r", encoding="utf-8") as csvfile:
        reader = csv.reader(csvfile)
        for row in reader:
            disposable_domains.add(row[0].strip())
    return disposable_domains

# 加载免费邮件域名列表
def load_free_email_domains():
    free_domains = set()
    file_path = os.path.join(os.path.dirname(__file__), "free_email_domains.csv")
    with open(file_path, "r", encoding="utf-8") as csvfile:
        reader = csv.reader(csvfile)
        for row in reader:
            free_domains.add(row[0].strip())
    return free_domains

# 识别 IP 类型的函数
def identify_ip(ip):
    if ip.startswith("192.168.") or ip.startswith("10.") or ip.startswith("172.16."):
        return "内网IP"
    elif ip.startswith("127."):
        return "回环IP"
    else:
        return "外网IP"

# 分析外网 IP 的地理位置和运营商信息
def analyze_ip(ip, api_key):
    url = f"https://api.ipgeolocation.io/ipgeo?apiKey={api_key}&ip={ip}"
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        return {"地区": data["country_name"], "运营商": data["isp"]}
    else:
        return {}

# 检查邮箱是否为一次性邮箱或免费邮箱
def check_email_type(email, disposable_domains, free_domains):
    domain = email.split("@")[-1]
    if domain in disposable_domains:
        return "一次性邮箱"
    elif domain in free_domains:
        return "免费邮箱"
    else:
        return "未知"

# 分析免费邮箱是否为公司邮箱或 Webmail
def analyze_free_email(email):
    domain = email.split("@")[-1]
    if domain.endswith("qq.com") or domain.endswith("163.com") or domain.endswith("126.com"):
        return "公司邮箱"
    else:
        return "Webmail"

# 读取 JSON 文件并进行分析
def read_and_analyze_json(file_path, api_key):
    disposable_domains = load_disposable_email_domains()
    free_domains = load_free_email_domains()

    with open(file_path, "r", encoding="utf-8") as json_file:
        data = json.load(json_file)
        for entry in data:
            input_data = entry["输入数据"]
            data_type = entry["数据类型"]
            print("输入数据:", input_data)
            print("数据类型:", data_type)
            if data_type == "IP地址":
                ip_type = identify_ip(input_data)
                print("IP类型:", ip_type)
                if ip_type == "外网IP":
                    ip_info = analyze_ip(input_data, api_key)
                    print("地理位置:", ip_info.get("地区", "未知"))
                    print("运营商:", ip_info.get("运营商", "未知"))
            elif data_type == "电子邮件地址":
                print("邮箱类型:", check_email_type(input_data, disposable_domains, free_domains))
                if check_email_type(input_data, disposable_domains, free_domains) == "免费邮箱":
                    print("邮箱性质:", analyze_free_email(input_data))
            print()  # 输出空行进行分隔

# 主函数
def main():
    file_path = input("请输入JSON文件路径: ")
    api_key = "**********"  # 替换为您的ipgeolocation API密钥
    read_and_analyze_json(file_path, api_key)

if __name__ == "__main__":
    main()
