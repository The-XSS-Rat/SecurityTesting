import requests
from bs4 import BeautifulSoup
import datetime

# Read the list of cybersecurity resources from an external file
with open("techStream/resources.txt", "r") as f:
    urls = f.read().splitlines()

# Create a new HTML document
html = "<html><head><title>Cybersecurity Articles</title></head><body>"

# Loop through each URL and scrape the latest articles
for url in urls:
    response = requests.get(url)
    soup = BeautifulSoup(response.content, features="xml")
    
    # Extract the title, link, and summary of the latest articles
    articles = soup.find_all("item")[:5]
    for article in articles:
        title = article.find("title").text
        link = article.find("link").text
        summary = article.find("description").text
        
        # Add the title, link, and summary to the HTML document
        html += "<h2><a href='" + link + "'>" + title + "</a></h2>"
        html += "<p>" + summary + "</p>"

# Close the HTML document
html += "</body></html>"

# Save the HTML document to a file
timestamp = datetime.datetime.now().strftime("%Y-%m-%d-%H-%M-%S")
filename = f"techStream/cybersecurity-articles-{timestamp}.html"
with open(filename, "w") as f:
    f.write(html)
print(f"HTML document saved to {filename}")
