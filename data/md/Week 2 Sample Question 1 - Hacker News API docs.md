# Week 2 Sample Question 1 - Hacker News API docs

**User**: carlton
**URL**: [https://discourse.onlinedegree.iitm.ac.in/t/week-2-sample-question-1-hacker-news-api-docs/134621/2](https://discourse.onlinedegree.iitm.ac.in/t/week-2-sample-question-1-hacker-news-api-docs/134621/2)

[Note: The typo in the question has now been fixed. This response was prior to the fix being implemented, but has been retained for deeper discussion on working with APIs.]

Hi Naren,

Noted. The id does seem to be incorrect. But a useful question to ask is what is wrong with it? Can we learn something in the documentation that will help us know about how their api works or give us more information other than that there is no post with this id?

If you dig a bit deeper into the documentation of the api, you will notice that you are able to walk the id numbers backwards to get all the posts. So therefore the ids are unique but incremental.

It’s documented on their github page that there is a specifically crafted api call to obtain the id of the max item.  
Try and find it.

Compare that with the ID that was asked in the question on portal.

So what does that tell you about the ID you were asked?

I know its not a solution to the original question but I hope that exercise in studying the documentation and gaining an understanding of api calls was beneficial.

We will try and get the question fixed on the back end.

Thanks.
