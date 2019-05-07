# -*- coding: utf-8 -*-
__author__ = 'olily'

import requests

html = requests.get("https://company.51job.com/p1/")
html.encoding="gbk"

print(html.text)