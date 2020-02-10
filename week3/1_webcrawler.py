import logging
import asyncio
import aiohttp
from urllib.parse import urljoin, urlparse
from lxml import html as lh


class AsyncCrawler:

    def __init__(self, start_url, crawl_depth, max_concurrency=10):
        self.start_url = start_url
        self.base_url = '{}://{}'.format(urlparse(self.start_url).scheme, urlparse(self.start_url).netloc)
        self.crawl_depth = crawl_depth
        self.seen_urls = set()
        self.semaphore = asyncio.Semaphore(max_concurrency)

    async def do_http_request(self, page_url, session):
        print('Fetching: {}'.format(page_url))
        async with self.semaphore:
            async with session.get(page_url, timeout=10) as response:
                html = await response.read()
                return html

    def find_urls(self, html):
        found_urls = []
        dom = lh.fromstring(html)
        for href in dom.xpath('//a/@href'):
            url = urljoin(self.base_url, href)
            if url not in self.seen_urls and url.startswith(self.base_url):
                found_urls.append(url)
        return found_urls

    async def extract_async(self, in_url, session):
        data = await self.do_http_request(in_url, session)
        found_urls = set()
        if data:
            for in_url in self.find_urls(data):
                found_urls.add(in_url)
        return in_url, data, sorted(found_urls)

    async def extract_multi_async(self, to_fetch, session):
        futures, results = [], []
        for web_url in to_fetch:
            if web_url in self.seen_urls:
                continue
            self.seen_urls.add(web_url)
            futures.append(self.extract_async(web_url, session))

        for crwl_future in asyncio.as_completed(futures):
            try:
                results.append((await crwl_future))
            except Exception as e:
                logging.warning('Encountered exception: {}'.format(e))
        return results

    async def crawl_async(self):
        session = aiohttp.ClientSession()
        to_fetch = [self.start_url]
        results = []
        for depth in range(self.crawl_depth + 1):
            batch = await self.extract_multi_async(to_fetch, session)
            to_fetch = []
            for url, data, found_urls in batch:
                results.append((depth, url))
                to_fetch.extend(found_urls)
        await session.close()
        return results


if __name__ == '__main__':
    url = 'https://justinjackson.ca/words.html'
    crawler = AsyncCrawler(url, 2)
    future = asyncio.Task(crawler.crawl_async())
    loop = asyncio.get_event_loop()
    loop.run_until_complete(future)
    loop.close()
    print(len(future.result()))
