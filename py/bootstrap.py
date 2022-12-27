

import zap_parser
import redis_db as cloud_db

def run_task():

    db = cloud_db.CloudDb()
    db.connect()
    urls = db.fetch_urls()
    print(f'URLs are fetched: {urls}')

    statistics = zap_parser.process_urls(urls)
    print('Statistics from ZAP has been calculated')

    db.push_data(statistics)
    print('Statistics has been pushed to the cloud DB')

if __name__ == '__main__':
    run_task()