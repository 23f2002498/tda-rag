# SSL error using urllib

**User**: carlton
**URL**: [https://discourse.onlinedegree.iitm.ac.in/t/ssl-error-using-urllib/134786/2](https://discourse.onlinedegree.iitm.ac.in/t/ssl-error-using-urllib/134786/2)

Hi Dhairy,

Thats because the python certificates are out of date on your local machine. You will need to update them for it to work on your local machine. The nice thing about working on Google Colab is that they always have all the dependencies required. When you work in the local environment you will have to do all that setup manually.

Please refer to the documentation for how to solve the certificate error. One tip is to just copy paste the error verbatim into Chat GPT or in google search and find the answer. My suggestion is once you find the answer, post your resolution here, so that others who are facing the same issue can also benefit.

IMPORTANT:  
Another thing to note is that one of the error messages on your terminal seemed to indicate that max retries have been exceeded. While it may or may not be related to the expired certificate,

`Always try and run the request code only once in a jupyter notebook cell or as few times as possible.`

> result = requests.post (location\_url)

This line should be run ideally only once and thats why juypter notebooks are highly recommended when it comes to scraping. The above line should be in its own cell block.

When you run code in a .py file, everytime you do a debug, *(and that may happen dozens of times or hundreds of times,)* you run the risk of your ip being banned. Because everytime you py file executes you are also unnecessarily refetching the data from the site.

Instead keep the rest of your code in a separate code block for debugging and do the request only once.

Hope that makes sense. We will cover this aspect in the TA session as its an important aspect.

Thanks.
