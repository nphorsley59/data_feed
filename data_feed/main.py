import time

import pandas as pd

from data_feed.fetch_data import (
    get_search_ids_from_pmc,
    get_id_metadata_from_pmc,
    get_article_from_bioc,
    fetch_oa_subset_list,
    extract_oa_pmc_ids,
)
from data_feed.general_utils import (
    build_search_string,
    safe_dict_key_to_value,
    safe_list_index_to_value,
    text_to_header,
)
from data_feed.logger import get_logger


logger = get_logger()


logger.info(text_to_header("Loading PMC IDs for PubMed OA subset"))
data = fetch_oa_subset_list()
oa_pmc_ids = extract_oa_pmc_ids(data)

logger.info(text_to_header("Querying PubMed based on keyword search"))
keywords = ["gdf15"]
search_string = build_search_string(keywords=keywords)
search_ids = get_search_ids_from_pmc(search=search_string, n=100)

logger.info(text_to_header("Parsing query results and fetching articles for OA subset"))
metadata_list = []
articles_list = []
for uid in search_ids:
    pmc_id, metadata = get_id_metadata_from_pmc(id=uid)
    if pmc_id in oa_pmc_ids:
        metadata_list.append(metadata)
        articles_list.append(get_article_from_bioc(id=pmc_id))
    time.sleep(0.5)
logger.info(f"Fetched articles for {len(articles_list)}/{len(search_ids)} PMC IDs")

logger.info(text_to_header("Parsing articles to extract relevant information"))
article_content_list = []
for article in articles_list:
    content = safe_list_index_to_value(article, 0)
    source = safe_dict_key_to_value(content, 'source')
    date = safe_dict_key_to_value(content, 'date')
    article_version = safe_dict_key_to_value(content, 'version')
    docs = safe_list_index_to_value(
        safe_dict_key_to_value(content, 'documents'),
        0,
    )
    passages = safe_dict_key_to_value(docs, 'passages')
    article_text = []
    if passages is not None:
        for passage in passages:
            article_text.append(
                safe_dict_key_to_value(passage, 'text'),
            )
    article_content_list.append({
        "source": source,
        "date": date,
        "article_version": article_version,
        "article_text": article_text,
    })

logger.info(text_to_header("Converting article contents to a table and saving to file"))
df = pd.DataFrame(article_content_list).explode('article_text')

breakpoint()
