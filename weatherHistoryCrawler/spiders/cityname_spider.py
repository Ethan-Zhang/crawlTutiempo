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

class CityNameSpider(scrapy.Spider):
    name ="cityname"
    start_urls = ["http://en.tutiempo.net/climate/china.html"]

    def parse(self, response):
        cities = response.xpath('//div[@class="mlistados mt10"]/ul/li/a/text()').extract()
        for city in cities:
            yield {'city':city}
        next_page = response.xpath('//div[@class="AntSig"]/ul/li/a[contains(strong, "Next")]/@href').extract_first()
        if next_page:
            next_page = response.urljoin(next_page)
            yield scrapy.Request(next_page, callback=self.parse)

