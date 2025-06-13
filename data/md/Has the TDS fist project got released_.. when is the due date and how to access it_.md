# Has the TDS fist project got released?.. when is the due date and how to access it?

**User**: carlton
**URL**: [https://discourse.onlinedegree.iitm.ac.in/t/has-the-tds-fist-project-got-released-when-is-the-due-date-and-how-to-access-it/137792/8](https://discourse.onlinedegree.iitm.ac.in/t/has-the-tds-fist-project-got-released-when-is-the-due-date-and-how-to-access-it/137792/8)

Hi Abuhashir,

In the TA session on July 4, we covered how to deal with parquet files and missing library errors. The video will be shortly uploaded.

Typically you should be able to read parquet files directly using pandas as long as the pyarrow library has been installed.

Typically this is the workflow on VSCode and it should not be too dissimilar on google colab.

[![Screenshot 2024-07-05 at 15.41.14](https://europe1.discourse-cdn.com/flex013/uploads/iitm/original/3X/4/9/49a20fff9f5903aefe55b37a9fa8f96fcfed2f1e.png)

Screenshot 2024-07-05 at 15.41.14720×510 18 KB](https://europe1.discourse-cdn.com/flex013/uploads/iitm/original/3X/4/9/49a20fff9f5903aefe55b37a9fa8f96fcfed2f1e.png "Screenshot 2024-07-05 at 15.41.14")

As you can see there is no need to specify the engine, just a straight forward pandas read.

Kind regards
