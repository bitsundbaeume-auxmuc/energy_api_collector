from init import logger
import webdav_connector
import compromizer


def main():
    webdav_connector.check_nextcloud_connection()
    compromizer.run_compromizer()
    logger.info("Finished execution.")


if __name__ == '__main__':
    main()
