import json
import csv
import os
from ip_geolocation_api import IPGeolocationAPI

# Load Disposable Mailing Domain List
def load_disposable_email_domains():
    disposable_domains = set()
    file_path = os.path.join(os.path.dirname(__file__), "disposable_email_domains.csv")
    with open(file_path, "r", encoding="utf-8") as csvfile:
        reader = csv.reader(csvfile)
        for row in reader:
            disposable_domains.add(row[0].strip())
    return disposable_domains

# Load Free Email Domain List
def load_free_email_domains():
    free_domains = set()
    file_path = os.path.join(os.path.dirname(__file__), "free_email_domains.csv")
    with open(file_path, "r", encoding="utf-8") as csvfile:
        reader = csv.reader(csvfile)
        for row in reader:
            free_domains.add(row[0].strip())
    return free_domains

# Function to recognize IP types
def is_private_ip(ip):
    return ipaddress.ip_address(ip).is_private

# Analyze the geographic location and carrier information of the extranet IPs
def analyze_ip(ip, api_key):
    api = IPGeolocationAPI(api_key)
    ip_info = api.get_bulk_ip_geolocation([ip])
    if ip_info and ip_info[ip]:
        return {"Location": ip_info[ip]['country_name'], "operator": ip_info[ip]['isp']}
    else:
        return {}

# Check if the mailbox is a disposable or free mailbox
def check_email_type(email, disposable_domains, free_domains):
    domain = email.split("@")[-1]
    if domain in disposable_domains:
        return "Disposable mailboxes"
    elif domain in free_domains:
        return "Free Email"
    else:
        return "unknown"

# Analyze whether the free email is a company email or webmail
def analyze_free_email(email):
    domain = email.split("@")[-1]
    if domain.endswith("qq.com") or domain.endswith("163.com") or domain.endswith("126.com"):
        return "Company Email"
    else:
        return "Webmail"

# Read and analyze JSON files
def read_and_analyze_json(file_path, api_key):
    disposable_domains = load_disposable_email_domains()
    free_domains = load_free_email_domains()

    with open(file_path, "r", encoding="utf-8") as json_file:
        data = json.load(json_file)
        for entry in data:
            input_data = entry["input data"]
            data_type = entry["data type"]
            print("input data:", input_data)
            print("data type:", data_type)
            if data_type == "IP address":
                ip_type = is_private_ip(input_data)
                print("IP address:", ip_type)
                if ip_type == "Extranet IP":
                    ip_info = analyze_ip(input_data, api_key)
                    print("country_name:", ip_info.get("country_name", "unknown"))
                    print("operator:", ip_info.get("operator", "unknown"))
            elif data_type == "e-mail":
                print("email-type:", check_email_type(input_data, disposable_domains, free_domains))
                if check_email_type(input_data, disposable_domains, free_domains) == "Free Email":
                    print("Nature of mailbox:", analyze_free_email(input_data))
            print()  # Output blank lines for separation

# main function
def main():
    file_path = input("Please enter the path to the JSON file: ")
    api_key = "your_api_key_here"  # Replace with your ipgeolocation API key
    read_and_analyze_json(file_path, api_key)

if __name__ == "__main__":
    main()
