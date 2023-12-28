import asyncio
import json
import requests
from logging import Logger
from typing import List
from xml.etree import ElementTree as ET
import aiohttp
from urllib.parse import urljoin

world_conf_url = "https://w1.dwar.ru/images/data/locale/ru/world_conf.xml"


def get_areas_from_world_config(url: str, logger: Logger) -> List[str]:
    """
    Send a GET request to the specified URL, parse the XML response,
    and extract the 'src' values from the 'file' tags.

    Args:
        url (str): The URL to send the GET request to.
        logger (logging.Logger): Logger for logging messages.

    Returns:
        List[str]: A list of 'src' values from the 'file' tags.
    """
    try:
        logger.debug(f"Sending GET request to {url}")
        response = requests.get(url)
        response.raise_for_status()

        logger.debug("Parsing XML response")
        root = ET.fromstring(response.text)

        file_src_values = [file_elem.get("src") for file_elem in root.findall(".//file")]

        logger.info(f"Found {len(file_src_values)} Areas")
        return file_src_values

    except requests.exceptions.RequestException as req_error:
        logger.error(f"Request error: {req_error}")
        raise req_error
    except ET.ParseError as parse_error:
        logger.error(f"XML parsing error: {parse_error}")
        raise parse_error
    except Exception as e:
        logger.error(f"Error: {e}")
        raise e


def parse_area_xml(logger: Logger, xml_content: str) -> List[dict]:
    """
       Parse XML content to extract area and location information.

       Args:
           logger (logging.Logger): Logger for logging messages.
           xml_content (str): The XML content to parse.

       Returns:
           List[dict]: A list of dictionaries containing area and location information.
    """
    try:
        if xml_content:
            root = ET.fromstring(xml_content)

            locations = []
            for area in root.findall(".//area"):
                area_id = area.get("id")
                for location in area.findall(".//location"):
                    loc_id = location.get("id")
                    loc_title = location.find(".//title").text.strip()
                    locations.append({"area_id": area_id, "loc_id": loc_id, "loc_title": loc_title})

            return locations

    except ET.ParseError as e:
        logger.error(f"Error parsing XML: {e}")
        raise ValueError("Error parsing XML") from e
    except Exception as e:
        logger.error(f"An unexpected error occurred: {e}")
        raise


def create_area_tasks(logger: Logger, area_names: List[str], session: aiohttp.ClientSession) -> List[asyncio.Task]:
    """
    Create asynchronous tasks for fetching area data.

    Args:
        logger (logging.Logger): Logger for logging messages.
        area_names (List[str]): List of area names.
        session (aiohttp.ClientSession): Aiohttp session for making asynchronous requests.

    Returns:
        List[asyncio.Task]: A list of asynchronous tasks.
    """
    tasks = []
    base_url = "https://w1.dwar.ru/images/data/locale/ru/xml_map/"
    logger.debug(f"Creating tasks for fetching areas")
    for area_name in area_names:
        task = asyncio.create_task(
            session.get(urljoin(
                base_url, area_name
            ))
        )
        tasks.append(task)
    logger.debug(f"Tasks created successfully")
    return tasks


def save_world_map_to_json(logger: Logger, content: List[dict], filename: str = "world.json") -> None:
    try:
        with open(filename, mode="w", encoding="utf-8") as json_file:
            logger.debug(f"Writing content into JSON file {filename}")
            json.dump(content, json_file, indent=2)
            logger.info(f"Content successfully written to {filename}")
    except Exception as e:
        logger.error(f"An error occurred while saving to {filename}: {e}")



async def fetch_world_map(logger: Logger, area_names: List[str]):
    async with aiohttp.ClientSession() as session:
        tasks = create_area_tasks(logger, area_names, session)
        responses = await asyncio.gather(*tasks)
        return responses


async def main(logger: Logger):
    result = []
    areas = get_areas_from_world_config(world_conf_url, logger)
    responses = await fetch_world_map(
        logger, areas
    )
    for resp in responses:
        resp_text = await resp.text()
        locations = parse_area_xml(logger, resp_text)
        result.extend(locations)
    save_world_map_to_json(logger, result)
