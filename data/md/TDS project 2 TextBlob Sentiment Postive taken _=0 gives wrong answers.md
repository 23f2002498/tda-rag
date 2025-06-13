# TDS project 2 TextBlob Sentiment Postive taken >=0 gives wrong answers

**User**: carlton
**URL**: [https://discourse.onlinedegree.iitm.ac.in/t/tds-project-2-textblob-sentiment-postive-taken-0-gives-wrong-answers/125034/10](https://discourse.onlinedegree.iitm.ac.in/t/tds-project-2-textblob-sentiment-postive-taken-0-gives-wrong-answers/125034/10)

Sorry I was not clear and did not word my sentence correctly, I did not mean that 0 means both positive and negative sentiment at the same time. I was saying that 0 sentiment has an *equally valid meaning* (so yes its the absence of positivity/negativity). However, what I was trying to say and obviously failed to communicate clearly,

**Absence of data is NOT 0.**

When you change a null to 0, you have fundamentally introduced bias into the data (not always as there are some cases where it might be a safe assumption).

> If you have 0 rupees, it doesn’t mean you simultaneously have and owe money. It means that you neither have nor owe money.

I totally agree. No argument from me there.

I apologise if I did not make that clear in my previous statement. I never stated that 0 and null are the same. They are fundamentally NOT the same, is what I was saying. I hope the context I gave clarified that. Also banks and financial institutions do not make nulls into 0s (I do not know about Indian institutions, so I cant comment about them) because that would be supremely dangerous.

The reason for my post was in response to this part of your previous post.

> The question is incomplete, *as **it’s a perfectly reasonable assumption** on our part that **empty titles should be marked 0 for sentiment.***

> Let’s look at an example. Let’s say you’re a book seller that wants to make sure that books with a negative title/original\_title should not be sold at your store. Marking the nulls are 0 positivity is perfectly fine in this case because the outcome will be as expected.

Marking nulls as 0s would still fail the book sellers requirement of not selling positive or negative titled books. Here is a simple counter example. The fact that the book exists in the database but is missing the title in the current dataset because of some human/machine error means that the book is still potentially on sale at the bookstore. So when the cashier scans it, it still scans and sells without any trouble. It still is indexed in the database.

However the book is titled, “Carlton is an idiot.” and selling this book means some nut out there is outrageously offended because its a personal attack on everyone named Carlton. Lets assume now we follow the algorithm that says mark it 0 (neutral sentiment) because the book entry was missing its title in the dataset, thus according to the seller’s flawed logic, this book will still be available for sale! . Cue: Big lawsuit book seller blames you the data scientist. Makes national news and bandhs and burning effigies follow.

I hope that illustrated the danger in changing nulls to 0 and then including them in the analysis. It is better to drop nulls from the analysis altogether or to produce a separate report to list them so that it can be handled by a human to correct the deficiencies of that data.

I hope that did not confuse anyone. And even if a business required you to make null’s as 0s, you would as a responsible data scientist still have to validate that assumption based on a good sound reasoning and challenge that assertion if necessary and explain why it could or should not be done.

Just my 2 paisa,  
God bless
