#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Copyright 2012 Ethan Zhang<http://github.com/Ethan-Zhang> 
#
# Licensed under the Apache License, Version 2.0 (the "License"); you may
# not use this file except in compliance with the License. You may obtain
# a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
# WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
# License for the specific language governing permissions and limitations
# under the License.

import scrapy
from weatherHistoryCrawler.items import WeatherhistorycrawlerItem
class TutiempoSpider(scrapy.Spider):
    name = "tutiempo"
    start_urls = ["http://en.tutiempo.net/climate/china.html"]
    month_dic = {'January': '01',
                'February': '02',
                'March': '03',
                'April': '04',
                'May': '05',
                'June': '06',
                'July': '07',
                'August': '08',
                'September': '09',
                'October': '10',
                'November': '11',
                'December': '12',
                }

    def __init__(self, *argc, **argv):
        super(TutiempoSpider, self).__init__(*argc, **argv)
        self.city_name =  argv['city']
        self.start_year = int(argv['start_year'])
        self.end_year = int(argv['end_year'])

    def parse(self, response):
        city_a = response.xpath('//div[@class="DobleList"]/ul/li/a[contains(text(), "%s")]/@href' % self.city_name).extract_first()
        next_page = response.xpath('//div[@class="AntSig"]/ul/li/a[contains(strong, "Next")]/@href').extract_first()
        if not city_a and next_page:
            next_page = response.urljoin(next_page)
            yield scrapy.Request(next_page, callback=self.parse)
        elif city_a:
            city_url = response.urljoin(city_a)
            yield scrapy.Request(city_url, callback=self.parse_city)
        else:
            self.logger.error('Invaild city name %s' % self.city_name)

    def parse_city(self, response):
        for year in range(self.start_year, self.end_year+1):
            year_url = response.xpath('//td[@class="tc1"]/a[contains(strong, "%s")]/@href' % year).extract_first()
            request = scrapy.Request(response.urljoin(year_url), callback=self.parse_year)
            request.meta['year']=year
            yield request

    def parse_year(self, response):
        #months = response.xpath('//div[@class="SelClima"]/ul/li/a/@href').extract()
        months = response.xpath('//div[@class="SelClima"]/ul/li')
        for month_block in months:
            month_en = month_block.xpath('a/abbr/@title').extract_first()
            month_url = month_block.xpath('a/@href').extract_first()
            request = scrapy.Request(response.urljoin(month_url), callback=self.parse_month)
            request.meta['year'] = response.meta['year']
            request.meta['month'] = TutiempoSpider.month_dic[month_en]
            yield request

    def parse_month(self, response):
        for data_line in response.xpath('//table[@class="medias mensuales"]/tr'):
            if data_line.xpath('th'):
                continue
            data = data_line.xpath('td/text() | td/strong/text()').extract()
            if not data[0].isdigit():
                continue
            item = WeatherhistorycrawlerItem()
            item['date'] = '%s%s%02d' % (response.meta['year'],
                                        response.meta['month'], 
                                        int(data[0]))
            item['T'] = data[1]
            item['TM'] = data[2]
            item['Tm'] = data[3]
            item['SLP'] = data[4]
            item['H'] = data[5]
            item['PP'] = data[6]
            item['V'] = data[8]
            item['RA'] = data[11]
            item['SN'] = data[12]
            item['TS'] = data[13]
            yield item
