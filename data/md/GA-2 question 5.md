# GA-2 question 5

**User**: carlton
**URL**: [https://discourse.onlinedegree.iitm.ac.in/t/ga-2-question-5/151678/2](https://discourse.onlinedegree.iitm.ac.in/t/ga-2-question-5/151678/2)

Hi Tarika,

You have not changed the user\_agent. If you read the documentation carefully, it would have been mentioned about the need to change the user\_agent.

The first clue comes from the HTTP response code. 403  
Have a look to see what that means,

![](https://europe1.discourse-cdn.com/flex013/uploads/iitm/original/3X/7/5/75528fd0cfe7d407679c5c585848c69857f9571e.png)
[MDN Web Docs](https://developer.mozilla.org/en-US/docs/Web/HTTP/Status#client_error_responses)

![](https://europe1.discourse-cdn.com/flex013/uploads/iitm/optimized/3X/f/4/f43c65b3b818a2ea578c6a20ce48f67e84ba4d29_2_690x388.png)

### [HTTP response status codes - HTTP | MDN](https://developer.mozilla.org/en-US/docs/Web/HTTP/Status#client_error_responses)

HTTP response status codes indicate whether a specific HTTP request has been successfully completed.
Responses are grouped in five classes:

Try and change the user\_agent to something that is personalised to your application and give it a try.

Kind regards
