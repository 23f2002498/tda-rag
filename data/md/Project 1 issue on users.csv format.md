# Project 1 issue on users.csv format

**User**: carlton
**URL**: [https://discourse.onlinedegree.iitm.ac.in/t/project-1-issue-on-users-csv-format/154172/5](https://discourse.onlinedegree.iitm.ac.in/t/project-1-issue-on-users-csv-format/154172/5)

Please refer to github api documentation.

<https://docs.github.com/en/rest?apiVersion=2022-11-28>

Even in the TA sessions we cover some aspects of APIs and things to consider.

You must follow strict GITHUB API rate limits and also use url encoded parameters to get each page

GITHUB also sends you back headers which tell you how much of your allowance you have used etc.

If you follow their documentation carefully you will be able to make 5000 api calls per hour, 900 per minute, 100 concurrent calls on a single endpoint. But I have also explained clearly in my TA session how you can accidently easily go over the limit even though you have coded everything correctly and how to prevent that from happening.

Kind regards
