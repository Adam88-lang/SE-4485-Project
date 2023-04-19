from flask import Flask, request, jsonify
from search import search
from filter import Filter
from storage import DBStorage
import html

app = Flask(__name__)

styles = """
<style>
    body {
        background-image: url("https://rare-gallery.com/mocahbig/1363018-Clean-wallpaper.jpg");
    }

    .site, .snippet, .rel-button {
        width: 50%;
        background-color: lightgray;
        padding: 20px;
        box-sizing: border-box;
        margin: 20px 0 20px 20px;
        border-radius: 10px;
        transition: transform 0.3s ease-in-out;
    }

    .site:hover, .snippet:hover, .rel-button:hover {
        transform: translateY(-10px);
    }

    .site {
        font-size: .8rem;
        color: green;
    }

    .snippet {
        font-size: .9rem;
        color: gray;
        margin-bottom: 30px;
    }

    .rel-button {
        cursor: pointer;
        color: blue;
    }

    input[type="text"] {
        padding: 10px;
        border-radius: 5px;
        border: 1px solid gray;
        font-size: 1.2rem;
        width: 50%;
        max-width: 500px;
    }

    input[type="text"]::placeholder {
        font-size: 1.2rem;
    }

    input[type="submit"] {
        padding: 10px;
        border-radius: 5px;
        font-size: 1.2rem;
        background-color: blue;
        color: white;
        border: none;
        cursor: pointer;
    }
</style>
"""

search_template = styles + """
<html>
  <head>
  </head>
  <body>
    <form action="/" method="post">
      <input type="text" name="query" placeholder="Enter Search Here">
      <input type="submit" value="Search">
    </form>
  </body>
</html>
"""

result_template = """
<p class="site">{rank}: {link} <span class="rel-button" onclick='relevant("{query}", "{link}");'>Relevant</span></p>
<a href="{link}">{title}</a>
<p class="snippet">{snippet}</p>
"""


def show_search_form():
    return search_template


def run_search(query):
    results = search(query)
    fi = Filter(results)
    filtered = fi.filter()
    rendered = search_template
    filtered["snippet"] = filtered["snippet"].apply(lambda x: html.escape(x))
    for index, row in filtered.iterrows():
        rendered += result_template.format(**row)
    return rendered


@app.route("/", methods=['GET', 'POST'])
def search_form():
    if request.method == 'POST':
        query = request.form["query"]
        return run_search(query)
    else:
        return show_search_form()


@app.route("/relevant", methods=["POST"])
def mark_relevant():
    data = request.get_json()
    query = data["query"]
    link = data["link"]
    storage = DBStorage()
    storage.update_relevance(query, link, 10)
    return jsonify(success=True)
