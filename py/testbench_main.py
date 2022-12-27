
import sys
import time
import bootstrap
import zap_parser
import redis_db as cloud_db

def report_test(func):
    def inner(*args, **kwargs):
        print(f'\n*** Running test: {func.__name__.upper()} ***')
        t0 = time.time()
        res = func(*args, **kwargs)
        t1 = time.time()
        print('--- {} took {:.3f} [ms]\n'.format(func.__name__.upper(), (t1 - t0) * 1000))
        return res
    return inner


def get_default_urls():
    urls = [
        'https://www.zap.co.il/model.aspx?modelid=1172336',
        'https://www.zap.co.il/model.aspx?modelid=1068730',
        'https://www.zap.co.il/model.aspx?modelid=1067697'
        ]
    return urls


@report_test
def test_zap(urls=None):
    if urls is None or len(urls) == 0:
        urls = get_default_urls()

    for url in urls:
        statistics = zap_parser.process_url(url)
        print('{}: timestamp={:.1f} low={:.0f}, high={:.0f}, avg={:.2f}'.
              format(url, statistics['timestamp'], statistics['min'], statistics['max'], statistics['avg']))
    pass


@report_test
def test_cloud(urls=None):

    if urls is None or len(urls)==0:
        urls = get_default_urls()

    cloud_db.push_urls(urls)
    print('URLs are pushed to the cloud DB')

    bootstrap.run_task()


def test_all(urls=None):
    test_zap(urls)
    test_cloud(urls)


if __name__ == '__main__':
    if len(sys.argv) > 1:
        tests = sys.argv[1:]
    else:
        tests = ['test_all']

    for test in tests:
        func = locals()[test]
        func(sys.argv[2:])

