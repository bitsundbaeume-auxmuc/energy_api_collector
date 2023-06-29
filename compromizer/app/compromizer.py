from datetime import datetime, timedelta
import io

import py7zr

import webdav_connector


def compress_files(file_data_array):
    compressed_data = io.BytesIO()
    with py7zr.SevenZipFile(compressed_data, 'w') as archive:
        for file_data in file_data_array:
            file_name = file_data['file_name']
            file_content = file_data['file_content']

            if isinstance(file_content, str):
                file_content = file_content.encode()

            archive.writestr(file_content, file_name)
    compressed_data.seek(0)
    return compressed_data


def get_all_file_names_from_yesterday():
    file_names = []
    file_names_raw = webdav_connector.list_folder_contents('crawled_json/')

    yesterday = (datetime.now() - timedelta(days=1)).strftime('%Y_%m_%d')
    for file_name in file_names_raw:
        if file_name.startswith('crawled_json/' + yesterday):
            file_names.append(file_name.removeprefix('crawled_json/'))

    return file_names


def run_compromizer():
    file_names = get_all_file_names_from_yesterday()
    files = webdav_connector.get_files('crawled_json/', file_names)
    compressed_file = compress_files(files)
    compressed_file_name = (datetime.now() - timedelta(days=1)).strftime('%Y_%m_%d') + '.7z'
    if webdav_connector.save_file('compressed_json/', compressed_file_name, compressed_file):
        webdav_connector.delete_files('crawled_json/', file_names)
