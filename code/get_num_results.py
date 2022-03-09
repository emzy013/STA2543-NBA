from bs4 import BeautifulSoup
import requests
import pandas as pd

def get_num_results(player, before=2020):
    # Format search query and create url.
    query = player.strip(" ").replace(" ", "+") + "+before%3A" + str(before)
    url = "https://www.google.com/search?q={}".format(query)

    # Use headers to pretend that we are not scraping.
    headers = {"User-Agent": "Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.149 Safari/537.36"}
    result = requests.get(url, headers=headers)

    # Parse HTML.
    soup = BeautifulSoup(result.content, 'html.parser')

    # Get number of serach results.
    total_results_text = soup.find("div", {"id": "result-stats"}).find(text=True, recursive=False)
    num_results = ''.join([num for num in total_results_text if num.isdigit()])

    return num_results

if __name__ == "__main__":
    num_results = get_num_results("Stephen Curry", before=2005)
    print(num_results)
