import time
import requests
from bs4 import BeautifulSoup
import ukr_net_requests_proxies as ip_address
import ukr_net_requests_user_agent as user_agent

topics = ['economics', 'politics', 'russianaggression', 'society', 'technologies', 'science', 'auto']

for i in topics:
    link = f"https://www.ukr.net/news/{i}.html"

    ip = ip_address.get_proxy()
    print(ip['http'])

    agent = user_agent.get_agent()
    print(agent['user-agent'])


    def get_data(url=link, ip=ip, agent=agent):
        print(f"We are starting process of scraping {i} data from {url}.")

        response = requests.get(link, proxies=ip, headers=agent)
        html_response = response.text

        with open(f"{i}_downloaded_data.txt", "w", encoding="utf-8") as f:
            f.write(html_response)

        print(f"We have received target {i} data.")
        return f"{i}_downloaded_data.txt"


    def parse_data():
        html_file = get_data()
        print("And now we are going to parse it.")

        with open(html_file, "r", encoding='utf8') as f:
            soup_for_parse = BeautifulSoup(f, 'html.parser')

        article_titles = soup_for_parse.find_all('div', class_="im-tl")

        for art in article_titles:
            title = art.find('a', class_="im-tl_a").text + '\n'
            with open(f"{i}_clean_data.txt", "a", encoding='utf=8') as f:
                f.write(title)

            link = art.find('a', class_="im-tl_a").get('href') + '\n'
            with open(f"{i}_clean_data.txt", "a", encoding='utf=8') as f:
                f.write(link)
                f.write("\n")

    parse_data()

    print(f"The process of cleaning {i} data is finished.")
    print()

    time.sleep(3)


print("Scraping and parsing are completely finished.")