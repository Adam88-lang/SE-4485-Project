from bs4 import BeautifulSoup
from urllib.parse import urlparse
from settings import *

# Open the "blacklist.txt" file and read its content, creating a set of blacklisted domains
with open("blacklist.txt") as f:
    domains = set(f.read().split("\n"))

# Function to count tracker URLs in a given row (HTML content)
def tracker_urls(row):
    # Parse the HTML content using BeautifulSoup
    soup = BeautifulSoup(row["html"])
    # Find all script tags with a "src" attribute
    scripts = soup.find_all("script", {"src": True})
    # Extract the "src" attribute from each script tag
    srcs = [s.get("src") for s in scripts]

    # Find all anchor tags with an "href" attribute
    links = soup.find_all("a", {"href": True})
    # Extract the "href" attribute from each anchor tag
    href = [l.get("href") for l in links]

    # Combine the script src and anchor href attributes and parse the domain from each URL
    all_domains = [urlparse(s).hostname for s in srcs + href]
    # Return the count of blacklisted domains found in the given HTML content
    return len([a for a in all_domains if a in domains])

# Function to extract the text content from a given row (HTML content)
def get_page_content(row):
    # Parse the HTML content using BeautifulSoup
    soup = BeautifulSoup(row["html"])
    # Extract the text content from the parsed HTML
    text = soup.get_text()
    # Return the extracted text content
    return text

class Filter():
    # Initialize the Filter class with a given set of results
    def __init__(self, results):
        self.filtered = results.copy()

    # Method to apply the tracker filter on the results
    def tracker_filter(self):
        # Calculate the tracker count for each row in the results using the tracker_urls function
        tracker_count = self.filtered.apply(tracker_urls, axis=1)
        # Set the tracker count to RESULT_COUNT for rows with a tracker count greater than the median tracker count
        tracker_count[tracker_count > tracker_count.median()] = RESULT_COUNT
        # Update the rank of each row based on the tracker count (higher tracker count leads to a lower rank)
        self.filtered["rank"] += tracker_count * 2

    # Method to apply the content filter on the results
    def content_filter(self):
        # Extract the page content for each row in the results using the get_page_content function
        page_content = self.filtered.apply(get_page_content, axis=1)
        # Calculate the word count for each page content
        word_count = page_content.apply(lambda x: len(x.split(" ")))

        # Normalize the word count by dividing it by the median word count
        word_count /= word_count.median()
        # Set the word count to RESULT_COUNT for rows with a normalized word count less than or equal to 0.5
        word_count[word_count <= .5] = RESULT_COUNT
        # Set the word count to 0 for all other rows
        word_count[word_count != RESULT_COUNT] = 0
        # Update the rank of each row based on the word count (lower word count leads to a lower rank)
        self.filtered["rank"] += word_count

    # Method to apply all filters on the results
    def filter(self):
        # Apply the tracker filter
        self.tracker_filter()
        # Apply the content filter
        self.content_filter()
        # Sort the results based on the rank in ascending order
        self.filtered = self.filtered.sort_values("rank", ascending=True)
        # Assign a new rank to each row based on their sorted position
        self.filtered["rank"] = range(1, self.filtered.shape[0] + 1)
        # Return the filtered results
        return self.filtered
