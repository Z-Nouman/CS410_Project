import math
import requests
from bs4 import BeautifulSoup
from pathlib import Path

# For links, remove prefix so that it matches the form: /wiki/<article>
start_link = "/wiki/Information_retrieval"
target_link = "/wiki/Central_processing_unit"

# Adjust to your preference
max_depth = 3  # Set to math.inf for no limit
max_articles = 100  # Set to math.inf for no limit
save_articles = False  # Set to True to scrape Wikipedia HTML for ML applications


def find_path(
    start_link,
    target_link,
    max_depth=math.inf,
    max_articles=math.inf,
    save_articles=False,
):
    SPLIT_TOKEN = "<SPLIT>"
    NULL_TOKEN = "<NULL>"

    frontier = [start_link, NULL_TOKEN]
    explored = set()
    to_be_explored = {start_link}
    depth_explored = 0
    num_articles_explored = 0

    while (
        (len(frontier) > 0)
        and (depth_explored <= max_depth)
        and (num_articles_explored < max_articles)
    ):
        full_path = frontier.pop(0)
        link = full_path.split(SPLIT_TOKEN)[-1]

        if full_path == NULL_TOKEN:
            depth_explored += 1
            print(
                f"Fully explored depth: {depth_explored - 1}, moving onto next depth..."
            )
            if len(frontier) > 0:
                frontier.append(NULL_TOKEN)
            continue

        to_be_explored.remove(link)
        explored.add(link)
        url = f"https://en.wikipedia.org{link}"
        response = requests.get(url)
        if response.status_code == 200:
            soup = BeautifulSoup(response.content, "html.parser")
        else:
            print(f"Failed to retrieve the page. Status code: {response.status_code}")
            break

        new_links = soup.find_all("a", href=True)
        for new_link in new_links:
            href = new_link.get("href", "")
            if "#" in href:
                href = href[: href.index("#")]
            if (
                ("wiki/" not in href)
                or (":" in href)
                or (href in explored)
                or (href in to_be_explored)
            ):
                continue
            if href == target_link:
                return full_path.split(SPLIT_TOKEN) + [href]
            to_be_explored.add(href)
            frontier.append(full_path + SPLIT_TOKEN + href)
        explored.add(link)
        num_articles_explored += 1

        if save_articles:
            title = link.split("/")[-1]
            with open(
                f"wikipedia_articles/{title}.html", "w", encoding="utf-8"
            ) as file:
                file.write(str(soup))

        if num_articles_explored % 100 == 0:
            print(f"Num explored articles: {num_articles_explored}")
            print("Num articles before end of next depth:", frontier.index(NULL_TOKEN))
            print("--------------------------------------------------")


if __name__ == "__main__":

    if save_articles:
        Path("wikipedia_articles").mkdir(parents=True, exist_ok=True)

    response = find_path(
        start_link=start_link,
        target_link=target_link,
        max_depth=max_depth,
        max_articles=max_articles,
        save_articles=save_articles,
    )
    if response:
        print("Link path from start to target:")
        for link in response:
            print(f"https://en.wikipedia.org{link}")
    else:
        print("Unable to find path provided the max_depth and max_articles.")
