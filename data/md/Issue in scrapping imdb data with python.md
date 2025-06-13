# Issue in scrapping imdb data with python

**User**: carlton
**URL**: [https://discourse.onlinedegree.iitm.ac.in/t/issue-in-scrapping-imdb-data-with-python/134635/2](https://discourse.onlinedegree.iitm.ac.in/t/issue-in-scrapping-imdb-data-with-python/134635/2)

Hi Ramandeep,

This error occurs because when you send a “get” request to imdb using the python requests library there are some headers that are sent with that request, that enables imdb to know where the request came from. Because the interaction is considered a program (i.e. not a human interaction) and it is able to detect that from the request python sends, it refuses to honour that request and sends back a 403 error code which means accessing this resource using a web scraping tool is forbidden.

There are ways to get around it by crafting a request to bypass those scraping protections, but it usually will be in violation of their legal position on scraping (if they have specified that somewhere in the terms and conditions). Many large databases that have valuable datasets want payment for programmatic access to their site via APIs. Having said that, there are many resources online that explain how web requests work (eg. on Mozilla Developer Network [MDN](https://developer.mozilla.org/en-US/)) and from there you can glean technical insight into how to craft for example a header to make the website think that the request is not originating from a python program but an interactive “User-Agent” like a browser etc. There are also other python libraries that have been written that also do this type of “spoofing”, but again be aware of the legalities.

This serves two purposes,

1. the obvious of course is the value of the subscription, both to the company and to you the user, because you get exactly the data you are looking for, but just as significantly,
2. API access reduces the workload on the servers that fetch those results. When you scrape a webpage directly you are downloading hundreds of kilobytes of data, most of which is for the interactivity and elements that are purely thematic or cosmetic or for usability. An API on the other hand is very lightweight to maintain, it only sends the key data you have requested usually in the form of a JSON and thus reduces the cost to them in terms of network bandwidth.

In situations like the IMDB website, Anand has produced a great lecture using JavaScript instead to scrape the information from the site. Please review it because it is very useful in many instances where there are restrictions on getting data through a non browser application.

Hope that helps.
