import concurrent.futures
import json
import requests
from datetime import datetime

import init as CONFIG
from init import logger
import webdav_connector


def get_json_from_url(url: str):
    response = requests.get(url)
    data = response.json()
    return data


def get_json_for_region(entity_data: dict):
    if CONFIG.SPECIAL_ARGUMENT:
        api_res = CONFIG.SPECIAL_ARGUMENT
    else:
        api_res = "meter"

    entity_data[f"{api_res}Data"] = get_json_from_url(f"https://api-energiemonitor.eon.com/{api_res}-data?regionCode=" +
                                                      entity_data['regionCode'] + "&tenantId=" +
                                                      entity_data['tenantId'])
    return entity_data


def collect_data():
    tenants = get_json_from_url("https://api-energiemonitor.eon.com/tenants")

    regions = {}
    entities = []
    entities_raw = []
    for tenant_line in tenants:
        hostname = tenant_line['hostnames'][0]

        regions_by_tenant = get_json_from_url(f"https://api-energiemonitor.eon.com/region-data?regionCode=&tenantId=" +
                                              tenant_line['tenantId'])

        regions[tenant_line['tenantId']] = []

        for region_line in regions_by_tenant['regions']:
            condition = True
            # "Landkreis" in region_line['regionName'] or region_line['regionUrlKey'] == 'lew-schwaben'
            if not condition:
                continue
            regions[tenant_line['tenantId']].append(region_line)
            entities_raw.append({
                "tenantId": tenant_line['tenantId'],
                "hostname": hostname,
                "regionCode": region_line['regionCode'],
                "name": region_line['regionName'],
                "urlKey": region_line['regionUrlKey'],
                "fullUrl": hostname + "/" + region_line['regionUrlKey']
            })

    with concurrent.futures.ThreadPoolExecutor() as executor:
        results = [executor.submit(get_json_for_region, entity_data) for entity_data in entities_raw]

        for future in concurrent.futures.as_completed(results):
            entities.append(future.result())

    return {
        "tenants": tenants,
        "regions": regions,
        "entities": entities
    }


def save_collected_data(collected_data: dict):
    file_base_name = datetime.now().strftime('%Y_%m_%d_%H_%M_%S')
    if CONFIG.SPECIAL_ARGUMENT:
        file_base_name = f"{file_base_name}_{CONFIG.SPECIAL_ARGUMENT}"

        with concurrent.futures.ThreadPoolExecutor() as executor:
            [executor.submit(webdav_connector.save_file, 'crawled_json/',
                             f"{file_base_name}_{region_line['regionCode']}.json",
                             json.dumps(region_line, indent=2, separators=(',', ': '))
                             ) for region_line in collected_data['entities']]
        collected_data['entities'] = []
    return webdav_connector.save_file('crawled_json/', f"{file_base_name}.json",
                                      json.dumps(collected_data, indent=2, separators=(',', ': ')))


def run_crawler():
    data = collect_data()
    save_collected_data(data)
    logger.info('Finished Crawler Run.')
