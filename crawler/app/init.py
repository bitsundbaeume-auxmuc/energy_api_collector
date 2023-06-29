import os
import logging

logging.basicConfig(format='%(asctime)s - %(levelname)s - %(module)s - %(message)s',
                    datefmt='%Y-%m-%d %H:%M:%S',
                    level=logging.INFO)
logger = logging.getLogger()
logger.setLevel(logging.INFO)

# Nextcloud-Data
NEXTCLOUD_URL = os.getenv('NEXTCLOUD_URL', '')
NEXTCLOUD_BASE_FOLDER = os.getenv('NEXTCLOUD_BASE_FOLDER', 'app_data/')
NEXTCLOUD_USER_NAME = os.getenv('NEXTCLOUD_USER_NAME', '')
NEXTCLOUD_PASSWORD = os.getenv('NEXTCLOUD_PASSWORD', '')

NEXTCLOUD_WEBDAV_URL_RELATIVE = os.getenv('NEXTCLOUD_WEBDAV_URL_RELATIVE',
                                          f"/remote.php/dav/files/{NEXTCLOUD_USER_NAME}/{NEXTCLOUD_BASE_FOLDER}")
NEXTCLOUD_WEBDAV_URL_ABSOLUTE = os.getenv('NEXTCLOUD_WEBDAV_URL_ABSOLUTE',
                                          NEXTCLOUD_URL + NEXTCLOUD_WEBDAV_URL_RELATIVE)

one_is_empty = False
for config_name in [
    'NEXTCLOUD_URL',
    'NEXTCLOUD_USER_NAME',
    'NEXTCLOUD_PASSWORD'
]:
    if globals()[config_name] == '':
        raise ValueError(f"The environment variable '{config_name}' cannot be empty.")

logger.info(f"Initialized and loaded environment variables into config.")
