# -*- coding: utf-8 -*-

# Scrapy settings for CaseSystem project
#
# For simplicity, this file contains only settings considered important or
# commonly used. You can find more settings consulting the documentation:
#
#     https://docs.scrapy.org/en/latest/topics/settings.html
#     https://docs.scrapy.org/en/latest/topics/downloader-middleware.html
#     https://docs.scrapy.org/en/latest/topics/spider-middleware.html
LOG_LEVEL = "WARNING"
BOT_NAME = 'CaseSystem'

SPIDER_MODULES = ['CaseSystem.spiders']
NEWSPIDER_MODULE = 'CaseSystem.spiders'

# Crawl responsibly by identifying yourself (and your website) on the user-agent
# USER_AGENT = 'CaseSystem (+http://www.yourdomain.com)'

# Obey robots.txt rules
ROBOTSTXT_OBEY = False

# Configure maximum concurrent requests performed by Scrapy (default: 16)
CONCURRENT_REQUESTS = 6

# Configure a delay for requests for the same website (default: 0)
# See https://docs.scrapy.org/en/latest/topics/settings.html#download-delay
# See also autothrottle settings and docs
# DOWNLOAD_DELAY = 3
# The download delay setting will honor only one of:
# CONCURRENT_REQUESTS_PER_DOMAIN = 16
# CONCURRENT_REQUESTS_PER_IP = 16

# Disable cookies (enabled by default)
# COOKIES_ENABLED = False

# Disable Telnet Console (enabled by default)
# TELNETCONSOLE_ENABLED = False

# Override the default request headers:
DEFAULT_REQUEST_HEADERS = {
    "Host": "qualcomm-cdmatech-support.my.salesforce.com",
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.149 Safari/537.36",
    "Referer": "https://qualcomm-cdmatech-support.my.salesforce.com/500?fcf=00B30000006aPoN",
}

# Enable or disable spider middlewares
# See https://docs.scrapy.org/en/latest/topics/spider-middleware.html
# SPIDER_MIDDLEWARES = {
#    'CaseSystem.middlewares.CasesystemSpiderMiddleware': 543,
# }

# Enable or disable downloader middlewares
# See https://docs.scrapy.org/en/latest/topics/downloader-middleware.html
DOWNLOADER_MIDDLEWARES = {
    'CaseSystem.middlewares.CasesystemDownloaderMiddleware': 543,
    'CaseSystem.middlewares.CaseCookieMiddleware': 400,
}

# Enable or disable extensions
# See https://docs.scrapy.org/en/latest/topics/extensions.html
# EXTENSIONS = {
#    'scrapy.extensions.telnet.TelnetConsole': None,
# }

# Configure item pipelines
# See https://docs.scrapy.org/en/latest/topics/item-pipeline.html
ITEM_PIPELINES = {
    'CaseSystem.pipelines.CasesystemPipeline': 300,
    'CaseSystem.pipelines.Mysql_Pipeline': 304,
    'CaseSystem.pipelines.RedisPipeline': 312,
}

# Enable and configure the AutoThrottle extension (disabled by default)
# See https://docs.scrapy.org/en/latest/topics/autothrottle.html
# AUTOTHROTTLE_ENABLED = True
# The initial download delay
# AUTOTHROTTLE_START_DELAY = 5
# The maximum download delay to be set in case of high latencies
# AUTOTHROTTLE_MAX_DELAY = 60
# The average number of requests Scrapy should be sending in parallel to
# each remote server
# AUTOTHROTTLE_TARGET_CONCURRENCY = 1.0
# Enable showing throttling stats for every response received:
# AUTOTHROTTLE_DEBUG = False

# Enable and configure HTTP caching (disabled by default)
# See https://docs.scrapy.org/en/latest/topics/downloader-middleware.html#httpcache-middleware-settings
# HTTPCACHE_ENABLED = True
# HTTPCACHE_EXPIRATION_SECS = 0
# HTTPCACHE_DIR = 'httpcache'
# HTTPCACHE_IGNORE_HTTP_CODES = []
# HTTPCACHE_STORAGE = 'scrapy.extensions.httpcache.FilesystemCacheStorage'

# MYSQL相关变量
MYSQL_HOST = '127.0.0.1'
MYSQL_USER = 'root'
MYSQL_PWD = '123456'
MYSQL_DB = 'casedb'
MYSQL_CHAR = 'utf8'

# Redis 相关
REDIS_HOST = '127.0.0.1'
REDIS_PORT = 6379
REDIS_DB = 8

# sql
# create database casedb charset=utf8;
# create table base_info (id int primary key auto_increment,Case_Number char(8) not null,Case_link char(70),Account_Name varchar(70),Open_Time varchar(25),Case_Owner varchar(40),Contact_Name varchar(40),Country varchar(40),Subject varchar(200),Description varchar(8000),PA1 varchar(100),PA2 varchar(100),PA3 varchar(100),OS_Android varchar(40),Software_Product varchar(50),Resolution_Summary varchar(300),ResponsivenessToTheCase varchar(20),QualityOfTechnicalSupport varchar(20),ProfessionalismOfQCEngineer varchar(20));
# create table Attachments ( Case_Number char(8) not null,link varchar(120),name varchar(100),Description varchar(250),type varchar(10),uploader varchar(20),size varchar(30));
# create table Case_Comments(Case_Number char(8) not null,name varchar(50),time varchar(50),content varchar(5000));
# create table Case_KBA_Doc(Case_Number char(8) not null,link varchar(75),name varchar(50),Title varchar(100));
