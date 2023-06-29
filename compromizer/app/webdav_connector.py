import concurrent.futures

import requests
import xml.etree.ElementTree as ET

import init as CONFIG
from init import logger


def list_folder_contents(folder_path):
    files = []
    response = requests.request('PROPFIND', CONFIG.NEXTCLOUD_WEBDAV_URL_ABSOLUTE + folder_path, auth=(CONFIG.NEXTCLOUD_USER_NAME, CONFIG.NEXTCLOUD_PASSWORD))
    if response.status_code == 207:
        xml_content = response.content
        namespace = {'d': 'DAV:'}
        root = ET.fromstring(xml_content)
        for response_tag in root.findall('.//d:response', namespace):
            href_tag = response_tag.find('d:href', namespace)
            if href_tag is not None:
                href = href_tag.text
                href = href.replace(CONFIG.NEXTCLOUD_WEBDAV_URL_RELATIVE, '')
                if len(href) > 0:
                    files.append(href)
        return files
    else:
        logger.error(f'Fehler beim Abrufen des Ordnerinhalts. Statuscode: {response.status_code}')


def create_folder(folder_path):
    folder_path += '/'
    response = requests.request('PROPFIND', CONFIG.NEXTCLOUD_WEBDAV_URL_ABSOLUTE + folder_path,
                                auth=(CONFIG.NEXTCLOUD_USER_NAME, CONFIG.NEXTCLOUD_PASSWORD))

    if response.status_code == 404:
        parent_folder = '/'.join(folder_path.strip('/').split('/')[:-1])  # Path of the parent folder
        if parent_folder:
            create_folder(parent_folder)  # Recursive call to create the parent folder

        headers = {'Content-Type': 'application/mkdir'}
        response = requests.request('MKCOL', CONFIG.NEXTCLOUD_WEBDAV_URL_ABSOLUTE + folder_path, headers=headers,
                                    auth=(CONFIG.NEXTCLOUD_USER_NAME, CONFIG.NEXTCLOUD_PASSWORD))

        if response.status_code == 201:
            logger.info(f'Folder {folder_path} created successfully.')
        else:
            logger.error(
                f'Error creating folder {folder_path}. Status code: {response.status_code}, {response.content}')
    elif response.status_code == 207:
        logger.info(f'Folder {folder_path} already exists.')
    else:
        logger.error(f'Error checking folder {folder_path}. Status code: {response.status_code}, {response.content}')


def save_file(file_path, file_name_with_extension, file_content):
    headers = {'Content-Type': 'application/octet-stream',
               'OCS-APIRequest': 'true'}

    create_folder(file_path)
    response = requests.put(CONFIG.NEXTCLOUD_WEBDAV_URL_ABSOLUTE + file_path + '/' + file_name_with_extension,
                            data=file_content, headers=headers,
                            auth=(CONFIG.NEXTCLOUD_USER_NAME, CONFIG.NEXTCLOUD_PASSWORD))
    if response.status_code == 201:
        logger.info(f'Datei {file_name_with_extension} erfolgreich hochgeladen.')
        return True
    else:
        logger.error(f'Fehler beim Hochladen der Datei {file_name_with_extension}. Statuscode: {response.status_code}')
        return False


def get_file(file_path, file_name_with_extension):
    response = requests.get(CONFIG.NEXTCLOUD_WEBDAV_URL_ABSOLUTE + file_path + file_name_with_extension,
                            auth=(CONFIG.NEXTCLOUD_USER_NAME, CONFIG.NEXTCLOUD_PASSWORD))
    if response.status_code == 200:
        return {
            'file_name': file_name_with_extension,
            'file_content': response.content
        }

    else:
        logger.error(f'Error while downloading file {file_path}{file_name_with_extension}.' +
                     f'Status code: {response.status_code}')
        return None


def get_files(file_path, file_names):
    files = []
    with concurrent.futures.ThreadPoolExecutor() as executor:
        results = [executor.submit(get_file, file_path, file_name) for file_name in file_names]

        for future in concurrent.futures.as_completed(results):
            files.append(future.result())

    return files


def delete_file(file_path, file_name_with_extension):
    url = CONFIG.NEXTCLOUD_WEBDAV_URL_ABSOLUTE + file_path + file_name_with_extension
    response = requests.delete(url, auth=(CONFIG.NEXTCLOUD_USER_NAME, CONFIG.NEXTCLOUD_PASSWORD))
    if response.status_code == 204:
        logger.info(f"File {file_path}{file_name_with_extension} deleted successfully.")
        return True
    else:
        logger.error(f"Error while deleting file {file_path}{file_name_with_extension}. " +
                     f"Status code: {response.status_code}")
        return False


def delete_files(file_path, file_names):
    with concurrent.futures.ThreadPoolExecutor() as executor:
        results = [executor.submit(delete_file, file_path, file_name) for file_name in file_names]

        for future in concurrent.futures.as_completed(results):
            future.result()


def check_nextcloud_connection():
    try:
        requests.request('PROPFIND', CONFIG.NEXTCLOUD_WEBDAV_URL_ABSOLUTE, auth=(
            CONFIG.NEXTCLOUD_USER_NAME, CONFIG.NEXTCLOUD_PASSWORD))
        logger.info(f"Connected successfully to {CONFIG.NEXTCLOUD_WEBDAV_URL_ABSOLUTE}.")
    except requests.exceptions.RequestException:
        raise ConnectionError(f"The connection to {CONFIG.NEXTCLOUD_WEBDAV_URL_ABSOLUTE} failed.")
