# -*- coding: utf-8 -*-

# Define here the models for your spider middleware
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/spider-middleware.html

from scrapy import signals


class CasesystemSpiderMiddleware(object):
    # Not all methods need to be defined. If a method is not defined,
    # scrapy acts as if the spider middleware does not modify the
    # passed objects.

    @classmethod
    def from_crawler(cls, crawler):
        # This method is used by Scrapy to create your spiders.
        s = cls()
        crawler.signals.connect(s.spider_opened, signal=signals.spider_opened)
        return s

    def process_spider_input(self, response, spider):
        # Called for each response that goes through the spider
        # middleware and into the spider.

        # Should return None or raise an exception.
        return None

    def process_spider_output(self, response, result, spider):
        # Called with the results returned from the Spider, after
        # it has processed the response.

        # Must return an iterable of Request, dict or Item objects.
        for i in result:
            yield i

    def process_spider_exception(self, response, exception, spider):
        # Called when a spider or process_spider_input() method
        # (from other spider middleware) raises an exception.

        # Should return either None or an iterable of Request, dict
        # or Item objects.
        pass

    def process_start_requests(self, start_requests, spider):
        # Called with the start requests of the spider, and works
        # similarly to the process_spider_output() method, except
        # that it doesn’t have a response associated.

        # Must return only requests (not items).
        for r in start_requests:
            yield r

    def spider_opened(self, spider):
        spider.logger.info('Spider opened: %s' % spider.name)


class CasesystemDownloaderMiddleware(object):
    # Not all methods need to be defined. If a method is not defined,
    # scrapy acts as if the downloader middleware does not modify the
    # passed objects.

    @classmethod
    def from_crawler(cls, crawler):
        # This method is used by Scrapy to create your spiders.
        s = cls()
        crawler.signals.connect(s.spider_opened, signal=signals.spider_opened)
        return s

    def process_request(self, request, spider):
        # Called for each request that goes through the downloader
        # middleware.

        # Must either:
        # - return None: continue processing this request
        # - or return a Response object
        # - or return a Request object
        # - or raise IgnoreRequest: process_exception() methods of
        #   installed downloader middleware will be called
        return None

    def process_response(self, request, response, spider):
        # Called with the response returned from the downloader.

        # Must either;
        # - return a Response object
        # - return a Request object
        # - or raise IgnoreRequest
        return response

    def process_exception(self, request, exception, spider):
        # Called when a download handler or a process_request()
        # (from other downloader middleware) raises an exception.

        # Must either:
        # - return None: continue processing this exception
        # - return a Response object: stops process_exception() chain
        # - return a Request object: stops process_exception() chain
        pass

    def spider_opened(self, spider):
        spider.logger.info('Spider opened: %s' % spider.name)


class CaseCookieMiddleware(object):
    def process_request(self,request,spider):
        cookies = self.get_cookies()
        # Request()中所有参数都是请求对象 request 的属性
        request.cookies = cookies


    # 把cookie处理为字典
    def get_cookies(self):
        cookie='oid=00D300000008JGC; web_core_geoCountry=cn; web_core_geoRedirected=true; optimizelyEndUserId=oeu1564982002363r0.8859554810860668; s_ecid=MCMID%7C24304494925481912030866445369063099816; _ga=GA1.2.194731266.1564982039; iv=54f39184-faad-4e1e-b642-2b74ca94fc09; webact=%7B%22l_vdays%22%3A68%2C%22l_visit%22%3A1566458561770%2C%22session%22%3A1571047481160%2C%22l_search%22%3A%22%22%2C%22l_dtype%22%3A%22SFDC%20Network%22%2C%22l_page%22%3A%22SFDC%3Acn%3Ahomepage%22%2C%22counter%22%3A3%2C%22pv%22%3A2%2C%22f_visit%22%3A1564982002089%2C%22seg%22%3A%22customer%3Acn%22%2C%22d%22%3A%2270130000000sUW0%22%2C%22customer%22%3A1564982048214%7D; AMCV_8D6C67C25245AF020A490D4C%40AdobeOrg=-1891778711%7CMCIDTS%7C18184%7CMCMID%7C24304494925481912030866445369063099816%7CMCAAMLH-1571652281%7C11%7CMCAAMB-1571652281%7CRKhpRz8krg2tLO6pguXWp5olkAcUniQYPHaMWWgdJ3xzPWQmdj0y%7CMCOPTOUT-1571054681s%7CNONE%7CMCAID%7CNONE%7CMCSYNCSOP%7C411-18121%7CvVersion%7C2.4.0; OptanonConsent=landingPath=NotLandingPage&datestamp=Mon+Oct+14+2019+18%3A04%3A50+GMT%2B0800+(%E4%B8%AD%E5%9B%BD%E6%A0%87%E5%87%86%E6%97%B6%E9%97%B4)&version=4.4.0&EU=false&groups=1%3A1%2C0_165883%3A1%2C0_165890%3A1%2C3%3A1%2C0_166673%3A1%2C4%3A1%2C0_166674%3A1%2C0_167477%3A1%2C0_167478%3A1%2C0_167479%3A1%2C0_167480%3A1%2C0_167481%3A1%2C0_165873%3A1%2C0_165874%3A1%2C0_165876%3A1%2C0_165878%3A1%2C0_165880%3A1%2C0_167482%3A1%2C0_165882%3A1%2C0_165884%3A1%2C0_165886%3A1%2C0_165888%3A1%2C0_165891%3A1%2C0_177554%3A1%2C0_165875%3A1%2C0_165877%3A1%2C0_177553%3A1%2C0_165879%3A1%2C0_165881%3A1%2C0_165885%3A1%2C0_165887%3A1%2C0_165889%3A1&AwaitingReconsent=false; BrowserId=v4a7cGdkEequvWVz0hn3hA; BrowserId_sec=v4a7cGdkEequvWVz0hn3hA; oinfo=c3RhdHVzPUFjdGl2ZSZ0eXBlPVVubGltaXRlZCtFZGl0aW9uJm9pZD0wMEQzMDAwMDAwMDhKR0M=; autocomplete=0; QCQQ=GLLbirOjJl1; sfdc_lv2=KxG83HRYGrj0l/p8fbRzYv6BQjufLKZmGK+c5R1vZBLC0mMRZ5r9RWzYxA2WdvIPo=; disco=3A:00D300000008JGC:0053A00000DliSm:1; sid=00D300000008JGC!ARIAQEnBZPoQ8j4mqSEwQZkCeO6Las0LcMy1PGLM0gaksdTgnMjWvAfnwdXGqe0cY1ubBweOnvYtDpKUO8kAGSImr1GehjQP; sid_Client=A00000DliSm00000008JGC; clientSrc=112.65.126.162; sfdc-stream=!sHIyJGOKrhfmwczHYm8HV3/Yy6KAx7BlcfGyY0SDWkLHvuf7/5dkh6nig9FcWdlY/4Uh3eDxOpFBJw==; lastlist=/500?fcf=00B3A00000Ap8ED&rolodexIndex=-1&page=1'
        cookies = {}
        c_list = cookie.split('; ')
        for c in c_list:
            cookies[c.split('=')[0]] = c.split('=')[1]
        return cookies

class CaseHeaderMiddleware(object):
    def process_request(self,request,spider):
        request.headers={"Host":"qualcomm-cdmatech-support.my.salesforce.com",
                         "User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.149 Safari/537.36",
                         "Referer":"https://qualcomm-cdmatech-support.my.salesforce.com/500?fcf=00B30000006aPoN",}