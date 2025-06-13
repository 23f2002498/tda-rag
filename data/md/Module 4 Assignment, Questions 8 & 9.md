# Module 4 Assignment, Questions 8 & 9

**User**: carlton
**URL**: [https://discourse.onlinedegree.iitm.ac.in/t/module-4-assignment-questions-8-9/152414/2](https://discourse.onlinedegree.iitm.ac.in/t/module-4-assignment-questions-8-9/152414/2)

Hi JRV,

You have not shown what you have tried in order access the database. Have you followed the instructions carefully or looked at the [sample notebook](https://colab.research.google.com/drive/1j_5AsWdf0SwVHVgfbEAcg7vYguKUN41o#scrollTo=bEN1ss8Z6FoJ) which was provided in the Week 4 content that accesses the same repository to see how one might access the database?

```
import pandas as pd
import sqlalchemy as sa

engine = sa.create_engine("mysql+pymysql://guest:relational@db.relational-data.org/stats")

```

Note: This code snippet was taken from the same sample notebook provided in Week 4. It will not work if you copy paste it. You have to change it to suit what your question is asking.

IMPORTANT: When debugging your code make sure you are not hitting the *public* endpoint again and again. That’s a sure fire way to get banned from accessing it.

Connect ONCE using the right connection details. Get the required data ONCE and store it either in a variable (or on disk - which is preferred because then even if your code crashes you can retrieve the data locally). Then do the debugging of the rest of your code ad nauseum. Jupyter Notebooks are very useful in this regard for separating out code cells and doing the debugging separately from your data connection/fetch cells.

Regards
