import os
import re
from typing import List

from data_feed.api_utils import send_request, parse_response
from data_feed.config import Directory
from data_feed.general_utils import format_number_with_commas
from data_feed.logger import get_logger


logger = get_logger()


OA_FILE_LIST_URL = "https://ftp.ncbi.nlm.nih.gov/pub/pmc/oa_file_list.txt"
BIOC_FILE_LIST_URL = "https://www.ncbi.nlm.nih.gov/research/bionlp/RESTful/pmcoa.cgi/BioC_json_file_list"
PMC_SEARCH_URL = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esearch.fcgi"
PMC_SUMMARY_URL = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esummary.fcgi"
PMC_BIOC_URL = "https://www.ncbi.nlm.nih.gov/research/bionlp/RESTful/pmcoa.cgi/BioC_{format}/{id}/{encoding}"


def download_oa_subset_list():
    oa_list_fpath = os.path.join(
        Directory.CACHE.value, 
        "oa_file_list.txt",
    )
    if os.path.exists(oa_list_fpath):
        logger.info(f"OA file list already exists in cache")
        with open(oa_list_fpath, "r") as f:
            data = f.readlines()
        return data
    logger.info(f"Downloading master list of OA articles")
    response = send_request(url=OA_FILE_LIST_URL)
    data = parse_response(response=response, format="text")
    logger.info(f"Received {format_number_with_commas(len(data))} OA records")
    with open(oa_list_fpath, "w") as f:
        f.write("\n".join(data))
    logger.info(f"OA file list saved to cache")
    return data


def download_bioc_subset_list():
    bioc_list_fpath = os.path.join(
        Directory.CACHE.value, 
        "bioc_file_list.txt",
    )
    if os.path.exists(bioc_list_fpath):
        logger.info(f"Bioc file list already exists in cache")
        with open(bioc_list_fpath, "r") as f:
            data = f.readlines()
        return data
    logger.info(f"Downloading master list of BioC articles")
    response = send_request(url=BI)
    data = parse_response(response=response, format="text")
    logger.info(f"Received {format_number_with_commas(len(data))} Bioc records")
    with open(bioc_list_fpath, "w") as f:
        f.write("\n".join(data))
    logger.info(f"BioC file list saved to cache")
    return data


def extract_pmc_ids(lines):
    pmc_ids = set()
    for line in lines:
        line = line.strip()
        if not line:
            logger.info(f"PMC ID could not be extracted; empty line")
            continue
        for field in re.split(r"/|\t", line):
            if re.fullmatch(r"PMC\d+", field):
                pmc_ids.add(field)
                break
        else:
            logger.info(f"PMC ID could not be extracted; no substring "
                        f"match found: {line}")
    logger.info(f"Extracted {format_number_with_commas(len(pmc_ids))} "
                "PMC IDs")
    return pmc_ids


def get_search_ids_from_pmc(
    search: str,
    n: int = 1000,
):
    response_format = "json"
    query_params = {
        "db": "pmc",
        "term": search,
        "retmode": response_format,
        "retmax": n,
    }
    logger.info(f"Searching for '{search}' in PMC")
    logger.info(f"Limiting response to top {n} results")
    logger.info(f"Requesting response in {response_format} format")
    response = send_request(url=PMC_SEARCH_URL, query_params=query_params)
    data = parse_response(response=response, format=response_format)
    ids = data["esearchresult"]["idlist"]
    logger.info(f"Search yielded {len(ids)}/{n} IDs")
    return ids


def get_id_metadata_from_pmc(id: str) -> tuple[str, dict]:
    response_format = "json"
    query_params = {
        "db": "pmc",
        "id": id,
        "retmode": response_format,
    }
    logger.info(f"Fetching metadata for {id} from PMC")
    logger.info(f"Requesting response in {response_format} format")
    response = send_request(url=PMC_SUMMARY_URL, query_params=query_params)
    data = parse_response(response=response, format=response_format)
    logger.info(f"Metadata received for {id}")
    metadata = data["result"][id]
    for aid in metadata["articleids"]:
        if aid.get("idtype") == "pmcid":
            pmc_id = aid.get("value")
    logger.info(f"{pmc_id} found in {id} metadata")
    return pmc_id, metadata


def get_article_from_bioc(id: str):
    response_format = "json"
    response_encoding = "unicode"
    path_params = {
        "format": response_format,
        "id": id,
        "encoding": response_encoding,
    }
    response = send_request(url=PMC_BIOC_URL, path_params=path_params)
    data = parse_response(response=response, format=response_format)
    return data
