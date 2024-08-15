from flask import Flask, render_template, request
import requests
from config import NEWS_API_KEY

app = Flask(__name__)

# Define categories and their queries
CATEGORIES = {
    "latest": "technology",
    "software_development": "Software Development",
    "cloud_computing": "Cloud Computing",
    "cybersecurity": "Cybersecurity",
    "ai_ml": "AI and ML",
    "data_science": "Data Science and Big Data",
    "web_development": "Web Development",
    "devops": "DevOps and Automation",
    "networking": "Networking and Connectivity",
    "blockchain": "Blockchain and Cryptocurrency",
    "tech_trends": "Tech Industry Trends",
}


def filter_tech_articles(articles):
  
    tech_keywords = [
        "Software Development", "Cloud Computing", "Cybersecurity", 
        "AI", "ML", "Data Science", "Big Data", "Web Development", 
        "DevOps", "Automation", "Networking", "Connectivity", 
        "Blockchain", "Cryptocurrency", "Tech Industry Trends"
    ]
    
    tech_articles = [
        article for article in articles
        if any(keyword.lower() in article["title"].lower() or keyword.lower() in article["description"].lower()
               for keyword in tech_keywords)
    ]
    return tech_articles


@app.route("/")
def index():
    query = request.args.get("query", "latest technology")
    
    url = f"https://newsapi.org/v2/everything?q={query}&sortBy=publishedAt&language=en&apiKey={NEWS_API_KEY}"
    
    response = requests.get(url)
    news_data = response.json()
    articles = news_data.get('articles', [])
    
    # Apply the filter to include only relevant tech articles
    tech_articles = filter_tech_articles(articles)[:5]  # Get only the top 5 tech articles
    
    return render_template("index.html", articles=articles, tech_articles=tech_articles, query=query)



@app.route("/<category>")
def category_news(category):
    # Get the query corresponding to the selected category
    query = CATEGORIES.get(category, "technology")
    
    url = f"https://newsapi.org/v2/everything?q={query}&sortBy=publishedAt&language=en&apiKey={NEWS_API_KEY}"
    response = requests.get(url)
    news_data = response.json()
    articles = news_data.get('articles', [])
    
    # Apply the filter to include only relevant tech articles
    tech_articles = filter_tech_articles(articles)
    
    return render_template("index.html", articles=tech_articles, query=query, category=category)


if __name__ == "__main__":
    app.run(debug=True)
