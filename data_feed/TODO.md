- After that, data standardization will be important. We need to store metadata in a dataframe and article data in a format that can be chunked.
-- Create a progress bar and summary stats for fetching articles
-- Create a progress bar and summary stats for parsing text
-- Add PMC_ID to df
-- Remove source from df
-- Convert date to a real datetime in df
-- Remove article_version from df
-- Add info that will give context about what the text is and what it's order is relative to the rest of the article
- Set up a database and start storing the data in that database

Once this is done ^ we'll have a fairly robust pipeline that:
1. Searches PMC, by search terms
2. Fetches the relevant articles
3. Standardizes and stores metadata and article text

Next steps will be to set up an LLM, chunk the text, and starting tuning models.
