# -*- coding: utf-8 -*-
import scrapy


class JobspiderSpider(scrapy.Spider):
    name = 'jobspider'
    allowed_domains = ['www.indeed.com']
    
    def start_requests(self):
        yield scrapy.Request(url='https://www.indeed.com/jobs?q=python%20developer&explvl=entry_level/', callback=self.parse, headers={
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/97.0.4692.71 Safari/537.36'
        })

    def parse(self, response):

        for job in response.xpath("//a[contains(@class, 'tapItem')]"):
            job_link = job.xpath(".//@href").get()
            yield response.follow(url=job_link, callback=self.parse_job)
            
        next_page = response.xpath('//a[@aria-label="Next"]/@href').get()
        
        if next_page:
            yield scrapy.Request(url=f'https://www.indeed.com{next_page}', callback=self.parse, headers={
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/97.0.4692.71 Safari/537.36'
        })
            
            
    def parse_job(self, response):
        title = response.xpath("//h1/text()").get()
        company = response.xpath('//div[contains(@class, "icl-u-lg-mr--sm")][1]/text()').get()
        
        text = response.xpath('//div[@class="jobsearch-jobDescriptionText"]/descendant::*/text()').getall()
        
        yield {
            'title': title,
            'company':company,
            'text': text
        }
