from typing import List
from xml.etree import ElementTree as ET

import requests

from data_feed.logger import get_logger


logger = get_logger()


def is_success_status_code(status_code: int) -> bool:
    if 200 <= status_code < 300:
        return True
    return False


def send_request(
    url: str,
    query_params: dict = {},
    path_params: dict = {},
) -> requests.Response | None:
    if path_params:
        url = url.format(**path_params)
    try:
        logger.debug(f"Sending request to {url}")
        response = requests.get(url, params=query_params, timeout=10)
        success = is_success_status_code(response.status_code)
        if success:
            logger.debug("SUCCESS: Request returned status code "
                        f"{response.status_code}")
            return response
        logger.error(f"ERROR: Request returned status code "
                     f"{response.status_code}")
        return None
    except requests.exceptions.ConnectionError as e:
        logger.error(f"Connection error when fetching data from {url}: {e}")
        return None
    except requests.exceptions.Timeout as e:
        logger.error(f"Timeout error when fetching data from {url}: {e}")
        return None
    except requests.exceptions.RequestException as e:
        logger.error(f"Request exception when fetching data from {url}: {e}")
        return None
    except Exception as e:
        logger.error(f"Unexpected exception when fetching data from {url}: {e}")
        return None


def parse_response(
    response: requests.Response,
    format: str,
) -> dict | ET.Element:
    if response is None:
        logger.warning("Nothing to parse")
        return None
    logger.debug(f"Parsing response with format {format}")
    match format:
        case "json":
            if "application/json" not in response.headers.get("Content-Type", ""):
                logger.warning("Response is not JSON")
                return None
            return response.json()
        case "xml":
            return ET.fromstring(response.text)
        case "text":
            if "text/plain" not in response.headers.get("Content-Type", ""):
                logger.warning("Response is not text")
                return None
            return response.text.strip().splitlines()
        case _:
            raise ValueError(f"Unsupported format: {format}")
