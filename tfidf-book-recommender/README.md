# Book Recommendations

This project explores a dataset of book recommendations, attempting to create a recommendation tool based on similarities between descriptions.

The notebook focuses on three questions:

1. **What are the most frequent words in descriptions?**

    The most frequent words in book descriptions (once stop words have been removed) are those that have the least importance and discriminating power, as they will not distinguish one book from another effectively. Being able to identify these words could help authors and publishers write more useful book descriptions, avoiding words that are essentially filler terms.


2. **Can TF-IDF effectively distinguish between separate books based solely on descriptions?**

    Book descriptions are often short and may share significant vocabulary, particularly after cleaning and processing text to reduce dimensionality. There's no point in building a recommendation system based upon TF-IDF if the book descriptions, after cleaning, are not sufficiently distinct.


3. **Can book descriptions alone be used to make reasonable recommendations?**

    Recommendation systems are used in all sorts of customer-facing contexts; being able to recommend products to consumers based on their past behaviour or interests has obvious implications in terms of boosting sales and/or customer engagement.
