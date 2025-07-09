import time

from data_feed.fetch_data import (
    get_search_ids_from_pmc,
    get_id_metadata_from_pmc,
    get_article_from_bioc,
    download_oa_subset_list,
    extract_pmc_ids,
)
from data_feed.general_utils import build_search_string
from data_feed.logger import get_logger


logger = get_logger()


data = download_oa_subset_list()
oa_pmc_ids = extract_pmc_ids(data)

keywords = ["gdf15"]
search_string = build_search_string(keywords=keywords)
ids = get_search_ids_from_pmc(search=search_string, n=1000)

metadata_list = []
articles_list = []
for uid in ids:
    pmc_id, metadata = get_id_metadata_from_pmc(id=uid)
    if pmc_id in oa_pmc_ids:
        metadata_list.append(metadata)
        articles_list.append(get_article_from_bioc(id=pmc_id))
    time.sleep(0.25)
logger.info(f"Fetched articles for {len(articles_list)}/{len(ids)} PMC IDs")
breakpoint()
