The program is a Flask-based web application designed to facilitate user searches. The application integrates with an external search API and provides the capability to rank and filter search results based on relevance. A core part of the application is its user interface, which incorporates CSS styles and JavaScript functions to offer a dynamic and responsive search experience.

The application works as follows:

When accessed, it displays a search form to users.
Upon submitting a search query, the program caches the search results to improve performance.
Search results are then filtered for relevance.
For each result, the application fetches related keywords using the Wikipedia API.
The results are rendered dynamically, integrating both the primary results and their related keywords.
Additionally, users can mark a search result as relevant. This action updates the result's relevance score in a database storage.
The application's front-end is designed using CSS, and it features a range of visual elements like ellipses and rectangles for an enhanced visual appearance. Moreover, JavaScript functions are embedded for submitting searches and marking search results as relevant.
