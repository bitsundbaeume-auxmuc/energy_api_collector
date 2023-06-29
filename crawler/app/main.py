from init import logger
import webdav_connector
import crawler


def main():
    webdav_connector.check_nextcloud_connection()
    crawler.run_crawler()
    logger.info("Finished execution.")


if __name__ == '__main__':
    main()
