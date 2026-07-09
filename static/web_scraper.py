import requests
from bs4 import BeautifulSoup

def fetch_top_headlines(url="https://news.ycombinator.com/"):
    print(f"[+] Initializing connection vector to: {url}")
    headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"}
    
    try:
        response = requests.get(url, headers=headers, timeout=10)
        if response.status_code == 200:
            soup = BeautifulSoup(response.text, 'html.parser')
            links = soup.find_all('span', class_='titleline')
            
            print(f"\n[✓] Successfully parsed {len(links)} records:\n" + "="*40)
            for index, link in enumerate(links[:5], start=1):
                a_tag = link.find('a')
                if a_tag:
                    print(f"{index}. {a_tag.text}")
        else:
            print(f"[!] Target server communication failure. Status: {response.status_code}")
    except Exception as error:
        print(f"[X] Execution trace error: {error}")

if __name__ == "__main__":
    fetch_top_headlines()