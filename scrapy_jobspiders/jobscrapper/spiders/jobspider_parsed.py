# -*- coding: utf-8 -*-
import scrapy
from scraper_api import ScraperAPIClient

api_key = 'aae9e621f59a0c1978bfcc4c42cf08dc'

client = ScraperAPIClient(api_key)

class JobspiderSpider(scrapy.Spider):
    name = 'indeed_html_spider'
    allowed_domains = ['www.indeed.com']
    
    def start_requests(self):
        url='https://www.indeed.com/jobs?q=programmer&vjk=f6b6d87dd30650a8'
        yield scrapy.Request(client.scrapyGet(url=url), callback=self.parse, headers={
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
        # company_info = response.xpath("//div[@class='jobsearch-CompanyInfoContainer']/descendant::*/text())").getall()
        job_details = response.xpath("//div[@id='jobDetailsSection']/descendant::*/text()").getall()
        qualifications = response.xpath("//div[@id='qualificationsSection']/descendant::*/text()").getall()
        benefits = response.xpath("//div[@id='coinfp-benefits-panel']/descendant::*/text()").getall()
        full_job_description = response.xpath("//div[@id='jobDescriptionText']/descendant::*/text()").getall()
        
        
        yield {
            
            'title': title,
            # 'company_info': company_info,
            'job_details': job_details,
            'qualifications': qualifications,
            'benefits': benefits,
            'full_job_description': full_job_description
        }
