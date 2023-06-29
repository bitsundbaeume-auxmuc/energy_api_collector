import requests

import init as CONFIG
from init import logger


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
        return response.content
    else:
        logger.error(f'Fehler beim Herunterladen der Datei {file_path}{file_name_with_extension}.' +
                     f'Statuscode: {response.status_code}')
        return None


def check_nextcloud_connection():
    try:
        requests.request('PROPFIND', CONFIG.NEXTCLOUD_WEBDAV_URL_ABSOLUTE, auth=(
            CONFIG.NEXTCLOUD_USER_NAME, CONFIG.NEXTCLOUD_PASSWORD))
        logger.info(f"Connected successfully to {CONFIG.NEXTCLOUD_WEBDAV_URL_ABSOLUTE}.")
    except requests.exceptions.RequestException:
        raise ConnectionError(f"The connection to {CONFIG.NEXTCLOUD_WEBDAV_URL_ABSOLUTE} failed.")
