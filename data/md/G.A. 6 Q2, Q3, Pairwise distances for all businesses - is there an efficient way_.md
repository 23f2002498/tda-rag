# G.A. 6 Q2, Q3, Pairwise distances for all businesses - is there an efficient way?

**User**: carlton
**URL**: [https://discourse.onlinedegree.iitm.ac.in/t/g-a-6-q2-q3-pairwise-distances-for-all-businesses-is-there-an-efficient-way/142203/2](https://discourse.onlinedegree.iitm.ac.in/t/g-a-6-q2-q3-pairwise-distances-for-all-businesses-is-there-an-efficient-way/142203/2)

The first big optimization you would do is cut the duplicate calculations that your logic would have. You only need to compute the top half of the triangular matrix, the rest would be just duplicate calculations if you visualise the relationships between the sets of businesses as a matrix.

For loops with pandas is one the most inefficient way to deal with pandas dataframes.

### For all you aspiring data scientists, if you want to level up from pottering panda to Kung fu panda, Please read on…

# Efficiently iterating over rows in a Pandas DataFrame

by  
Maxime Labonne  
Ph.D., Staff ML Scientist @ Liquid AI • Author of “Hands-On Graph Neural Networks”

Published in  
Towards Data Science  
Mar 21, 2022

6 min read  

[![](https://europe1.discourse-cdn.com/flex013/uploads/iitm/optimized/3X/6/c/6c0202f3cea65de32a608d56852a555f8d7d825d_2_690x388.jpeg)

1280×720 200 KB](https://europe1.discourse-cdn.com/flex013/uploads/iitm/original/3X/6/c/6c0202f3cea65de32a608d56852a555f8d7d825d.jpeg)

Image by author, emojis by [OpenMoji](https://openmoji.org/) ([CC BY-SA 4.0](https://creativecommons.org/licenses/by-sa/4.0/#)).

When I started machine learning, I followed the guidelines and created my own features by combining multiple columns in my dataset. It’s all well and good, but the way I did it was **horribly inefficient**. I had to wait several minutes to do the most basic operations.

My problem was simple: I didn’t know the fastest way to iterate over rows in Pandas.

I often see people online using the same techniques I used to apply. It’s not elegant but it’s ok if you don’t have much data. However, if you process **more than 10k rows**, it quickly becomes an obvious performance issue.

In this article, I’m gonna give you the **best way to iterate over rows in a Pandas DataFrame**, with no extra code required. It’s not just about performance: it’s also about understanding what’s going on under the hood to become a better data scientist.

Let’s import a dataset in Pandas. In this case, I chose the one I worked on when I started: it’s time to fix my past mistakes! ![:adhesive_bandage:](https://emoji.discourse-cdn.com/google/adhesive_bandage.png?v=12 ":adhesive_bandage:")

You can run the code with the following [Google Colab notebook](https://colab.research.google.com/drive/1v9v4j1MnklaCd9eFcuGnB5x_5FoINmRe?usp=sharing).

import pandas as pd  
import numpy as np

df = pd.read\_csv(‘<https://raw.githubusercontent.com/mlabonne/how-to-data-science/main/data/nslkdd_test.txt>’)

This dataset has 22k rows and 43 columns with a combination of categorical and numerical values. Each row describes a connection between two computers.

Let’s say we want to create a new feature: the **total number of bytes** in the connection. We just have to sum up two existing features: `src_bytes` and `dst_bytes`. Let’s see different methods to calculate this new feature.

# :x::x: 1. Iterrows

According to the [official documentation](https://pandas.pydata.org/docs/reference/api/pandas.DataFrame.iterrows.html), `iterrows()` iterates “over the rows of a Pandas DataFrame as (index, Series) pairs”. It converts each row into a Series object, which causes two problems:

1. It can **change the type** of your data (dtypes);
2. The conversion **greatly degrades performance**.

For these reasons, the ill-named `iterrows()` is the WORST possible method to actually iterate over rows.

```
%%timeit -n 10
# Iterrows
total = []
for index, row in df.iterrows():
total.append(row['src_bytes'] + row['dst_bytes'])

```

> 10 loops, best of 5: **1.07 s** per loop

Now let’s see slightly better techniques…

# :x: 2. For loop with .loc or .iloc (3× faster)

This is what I used to do when I started: a **basic for loop** to select rows by index (with `.loc` or `.iloc`).

Why is it bad? Because DataFrames are not designed for this purpose. As with the previous method, rows are converted into Pandas Series objects, which degrades performance.

Interestingly enough,`.iloc` is faster than `.loc`. It makes sense since Python doesn’t have to check user-defined labels and directly look at where the row is stored in memory.

```
%%timeit -n 10
# For loop with .loc
total = []
for index in range(len(df)):
total.append(df['src_bytes'].loc[index] + df['dst_bytes'].loc[index])

```

> 10 loops, best of 5: **600 ms** per loop

```
%%timeit -n 10
# For loop with .iloc
total = []
for index in range(len(df)):
total.append(df['src_bytes'].iloc[index] + df['dst_bytes'].iloc[index])

```

> 10 loops, best of 5: **377 ms** per loop

Even this basic for loop with `.iloc` is **3 times** faster than the first method!

# :x: 3. Apply (4× faster)

The `apply()` method is another popular choice to iterate over rows. It creates code that is easy to understand but at a cost: performance is nearly as bad as the previous for loop.

This is why I would strongly advise you to **avoid this function** for this specific purpose (it’s fine for other applications).

Note that I convert the DataFrame into a list using the `to_list()` method to obtain identical results.

```
%%timeit -n 10
# Apply
df.apply(lambda row: row['src_bytes'] + row['dst_bytes'], axis=1).to_list()

```

> 10 loops, best of 5: **282 ms** per loop

The `apply()` method is a for loop in disguise, which is why the performance doesn’t improve that much: it’s only **4 times faster** than the first technique.

# :x: 4. Itertuples (10× faster)

If you know about `iterrows()`, you probably know about `itertuples()`. According to the [official documentation](https://pandas.pydata.org/docs/reference/api/pandas.DataFrame.itertuples.html), it iterates “over the rows of a DataFrame as namedtuples of the values”. In practice, it means that **rows are converted into tuples**, which are **much lighter objects** than Pandas Series.

This is why `itertuples()` is a better version of `iterrows()`. This time, we need to access the values with an **attribute** (or an index). If you want to access them with a **string** (e.g., if there’s a space in the string), you can use the `getattr()` function instead.

```
%%timeit -n 10
# Itertuples
total = []
for row in df.itertuples():
total.append(row.src_bytes + row.dst_bytes)

```

> 10 loops, best of 5: **99.3 ms** per loop

This is starting to look better: it is now **10 times faster** than `iterrows()` .

# :x: 5. List comprehensions (200× faster)

List comprehensions are a fancy way to iterate over a list as a one-liner.

For instance, `[print(i) for i in range(10)]` prints numbers from 0 to 9 **without any explicit for loop**. I say “explicit” because Python actually processes it as a for loop if we look at the bytecode.

So why is it faster? Quite simply because we don’t call the `.append()` method in this version.

```
%%timeit -n 100
# List comprehension
[src + dst for src, dst in zip(df['src_bytes'], df['dst_bytes'])]

```

> 100 loops, best of 5: **5.54 ms** per loop

Indeed, this technique is **200 times faster** than the first one! But we can still do better.

# :white_check_mark: 6. Pandas vectorization (1500× faster)

Until now, all the techniques used simply add up single values. Instead of adding single values, why not **group them into vectors** to sum them up? The difference between adding two numbers or two vectors is not [significant for a CPU](https://en.wikipedia.org/wiki/Single_instruction,_multiple_data), which should speed things up.

On top of that, Pandas can **process Series objects in parallel**, using every CPU core available!

The syntax is also the simplest imaginable: this solution is extremely intuitive. Under the hood, Pandas takes care of vectorizing our data with an optimized C code using contiguous memory blocks.

```
%%timeit -n 1000
# Vectorization
(df['src_bytes'] + df['dst_bytes']).to_list()

```

> 1000 loops, best of 5: **734 µs** per loop

This code is **1500 times faster** than `iterrows()` and it is even simpler to write.

# :white_check_mark::white_check_mark: 7. NumPy vectorization (1900× faster)

NumPy is designed to handle scientific computing. It has **less overhead** than Pandas methods since rows and dataframes all become `np.array`. It relies on the same optimizations as Pandas vectorization.

There are **two ways** of converting a Series into a `np.array`: using `.values` or `.to_numpy()`. The former has been deprecated for years, which is why we’re gonna use `.to_numpy()` in this example.

```
%%timeit -n 1000
# Numpy vectorization
(df['src_bytes'].to_numpy() + df['dst_bytes'].to_numpy()).tolist()

```

> 1000 loops, best of 5: **575 µs** per loop

We found our winner with a technique that is **1900 times faster** than our first competitor! Let’s wrap things up.

# :trophy: Conclusion

[![](https://europe1.discourse-cdn.com/flex013/uploads/iitm/optimized/3X/7/e/7e1bf4e0a57705fe2ce4c01c42b66784f409163a_2_690x354.png)

1400×720 136 KB](https://europe1.discourse-cdn.com/flex013/uploads/iitm/original/3X/7/e/7e1bf4e0a57705fe2ce4c01c42b66784f409163a.png)

The number of rows in the dataset can greatly impact the performance of certain techniques (image by author).

Don’t be like me: if you need to iterate over rows in a DataFrame, **vectorization** is the way to go! You can find the code to reproduce the experiments [at this address](https://mlabonne.github.io/blog/). Vectorization is not harder to read, it doesn’t take longer to write, and the performance gain is incredible.

It’s not just about performance: understanding how each method works under the hood helped me to **write better code**. Performance gains are always based on the same techniques: transforming data into vectors and matrices to take advantage of parallel processing. Alas, this is often at the expense of readability. But it doesn’t have to be.

Iterating over rows is **just an example** but it shows that, sometimes, you can have the cake and eat it. ![:birthday:](https://emoji.discourse-cdn.com/google/birthday.png?v=12 ":birthday:")

---

Kind regards,  
From your friendly TDS TA

PS.

> “There is no cake”  
> by the test subject Doug Rattman in the Aperture Science Computer-Aided Enrichment Center before his untimely demise caused by the artificially superintelligent computer GlaDOS.
