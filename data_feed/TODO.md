- After that, data standardization will be important. We need to store metadata in a dataframe and article data in a format that can be chunked.
- We'll probably want to set up database and object storage alongside data standardization.

Once this is done ^ we'll have a fairly robust pipeline that:
1. Searches PMC, by search terms
2. Fetches the relevant articles
3. Standardizes and stores metadata and article text

Next steps will be to set up an LLM, chunk the text, and starting tuning models.
