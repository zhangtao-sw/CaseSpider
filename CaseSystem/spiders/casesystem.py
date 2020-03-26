# -*- coding: utf-8 -*-
import scrapy
import json
import re
from ..items import CasesystemItem
import redis
from ..settings import *
from hashlib import md5


class CasesystemSpider(scrapy.Spider):
    name = 'casesystem'
    allowed_domains = ['qualcomm-cdmatech-support.my.salesforce.com']

    # start_urls = ['http://qualcomm-cdmatech-support.my.salesforce.com/']
    def __init__(self):
        self.r = redis.Redis(host=REDIS_HOST, port=REDIS_PORT, db=REDIS_DB)

    def check_url(self, url):
        url_md5 = md5(url.encode()).hexdigest()
        result = self.r.sismember("url", url_md5)
        return result

    def start_requests(self):
        base_url = "https://qualcomm-cdmatech-support.my.salesforce.com/_ui/common/list/ListServlet"
        quene_id = '00B3A00000A9bUP'
        formdata = {
            "action": "newfilter",
            "filterId": quene_id,
            "filterType": "t",
            "page": "1",
            "rowsPerPage": "75",
            "search": "",
            "sort": "",
            "rolodexIndex": '-1',
            "retURL": "/500?fcf=%s&rolodexIndex=%s&page=%s" % (quene_id, '-1', '1')
        }
        yield scrapy.FormRequest(
            url=base_url,
            formdata=formdata,
            callback=self.parse_post,
        )

    def parse_post(self, response):
        num = response.text.find("{")
        resp_str = response.text[num:].strip()
        resp_dic = json.loads(resp_str)
        url_list = resp_dic['listData']['CASES.CASE_NUMBER']
        for url in url_list:
            item = CasesystemItem()
            temp_str = r'<a href="(.*?)">.*?</a>'
            edit_link = re.findall(temp_str, url, re.DOTALL)[0]
            case_url = "https://qualcomm-cdmatech-support.my.salesforce.com" + edit_link
            if self.check_url(case_url):
                print("%s已经下载过" % case_url)
                continue
            yield scrapy.Request(
                url=case_url,
                meta={'item': item, 'case_url': case_url},
                callback=self.parse_case,
            )

    def parse_case(self, response):
        Case_Attachments = []
        Case_KBA_Doc = []
        Case_Comments = []
        item = response.meta['item']
        case_url = response.meta['case_url']
        text = response.text
        try:
            temp_str = '<td class="labelCol">Case Number</td><td class="dataCol col02">(.*?)</td>'
            Case_Number = re.findall(temp_str, text, re.DOTALL)[0].replace("&nbsp;", "").strip().split("<")[0]
            print(Case_Number)
        except Exception as e:
            print(e)
            return
        try:
            temp_str = '<td class="labelCol">Account Name</td>(.*?)</a></td></tr>'
            Account_Name = re.findall(temp_str, text, re.DOTALL)[0].split(">")[-1].strip()
        except Exception as e:
            Account_Name = ""
            print(e)
        try:
            temp_str = '<td class="labelCol">Contact Name</td>(.*?)</a></td></tr>'
            Contact_Name = re.findall(temp_str, text, re.DOTALL)[0].split(">")[-1].strip()
        except Exception as e:
            Contact_Name = ""
            print(e)
        try:
            temp_str = 'Contact Office Country</td><td class="dataCol">(.*?)</td></tr>'
            Country = re.findall(temp_str, text, re.DOTALL)[0].strip()
        except Exception as e:
            Country = ""
            print(e)
        try:
            temp_str = 'Case Owner</td>(.*?)</a>'
            Case_Owner = re.findall(temp_str, text, re.DOTALL)[0].split(">")[-1].strip()
        except Exception as e:
            Case_Owner = ""
            print(e)
        try:
            temp_str = 'Date/Time Opened</td><td class="dataCol">(.*?)</td></tr>'
            Open_Time = re.findall(temp_str, text, re.DOTALL)[0].split(" ")[0]
        except IndexError:
            try:
                temp_str = '>Created By</td><td class="dataCol"><a href=(.*?)</td></tr>'
                Open_Time = re.findall(temp_str, text, re.DOTALL)[0].split(" ")[-3].strip()
            except Exception as e:
                Open_Time = ""
                print(e)
        try:
            temp_str = 'Subject</td><td class="data2Col" colspan="3">(.*?)</td></tr>'
            Subject = re.findall(temp_str, text, re.DOTALL)[0].strip()
        except Exception as e:
            Subject = ""
            print(e)
        try:
            temp_str = 'Description</td><td class="data2Col" colspan="3">(.*?)</td></tr>'
            Description = re.findall(temp_str, text, re.DOTALL)[0].strip()
        except IndexError:
            try:
                temp_str = 'Description</td><td class="last data2Col" colspan="3">(.*?)</td></tr>'
                Description = re.findall(temp_str, text, re.DOTALL)[0].strip()
            except Exception as e:
                Description = ""
                print(e)
        try:
            temp_str = "Please enter a value that best represents the problem area for which you are creating this case.'\\);</script></span></td><td class=(.*?)</td>"
            PA1 = re.findall(temp_str, text, re.DOTALL)[0].split(">")[-1].strip()
        except IndexError:
            try:
                temp_str = "Product<(.*?)</td></tr>"
                PA1 = re.findall(temp_str, text, re.DOTALL)[0].split(">")[-1].strip()
            except Exception as e:
                PA1 = ""
                print(e)
        try:
            temp_str = "Please choose a value that best represents the problem area for which you are creating this case.'\\);</script></span></td><td class=(.*?)</td>"
            PA2 = re.findall(temp_str, text, re.DOTALL)[0].split(">")[-1].strip()
        except IndexError:
            try:
                temp_str = 'Problem Code 1</td><td class="dataCol col02">(.*?)</td>'
                PA2 = re.findall(temp_str, text, re.DOTALL)[0].strip()
            except Exception as e:
                PA2 = ""
                print(e)
        try:
            temp_str = "Please enter value that best describes the problem area for which you are creating this case.'\\);</script></span></td><td class=(.*?)</td>"
            PA3 = re.findall(temp_str, text, re.DOTALL)[0].split(">")[-1].strip()
        except IndexError:
            try:
                temp_str = 'Problem Code 2</td><td class="dataCol">(.*?)</td>'
                PA3 = re.findall(temp_str, text, re.DOTALL)[0].strip()
            except Exception as e:
                PA3 = ""
                print(e)
        try:
            temp_str = 'OS Delivered by Qualcomm</td>.*?>(.*?)</td>'
            OS_Android = re.findall(temp_str, text, re.DOTALL)[0].strip()
        except Exception as e:
            OS_Android = ""
            print(e)
        try:
            temp_str = 'Software Product</td>.*?>(.*?)</td>'
            Software_Product = re.findall(temp_str, text, re.DOTALL)[0].strip()
        except Exception as e:
            Software_Product = ""
            print(e)
        try:
            temp_str = 'Resolution Summary</td>.*?>(.*?)</td>'
            Resolution_Summary = re.findall(temp_str, text, re.DOTALL)[0].strip()
        except Exception as e:
            Resolution_Summary = ""
            print(e)
        try:
            temp_str = '>Responsiveness To The Case<.*?<td .*?>(.*?)</td>'
            ResponsivenessToTheCase = re.findall(temp_str, text, re.DOTALL)[0].strip()
        except Exception as e:
            ResponsivenessToTheCase = ""
            print(e)
        try:
            temp_str = '>Quality Of Technical Support<.*?<td .*?>(.*?)</td>'
            QualityOfTechnicalSupport = re.findall(temp_str, text, re.DOTALL)[0].strip()
        except Exception as e:
            QualityOfTechnicalSupport = ""
            print(e)
        try:
            temp_str = '>Professionalism Of QC Engineer<.*?<td .*?>(.*?)</td>'
            ProfessionalismOfQCEngineer = re.findall(temp_str, text, re.DOTALL)[0].strip()
        except Exception as e:
            ProfessionalismOfQCEngineer = ""
            print(e)
        try:
            temp_str = '>NEW Case Attachments<.*?<!-- ListRow -->(.*?)</tr></table>'
            temp_result = re.findall(temp_str, text, re.DOTALL)[0]
            temp_str = '<th scope="row" class=" dataCell  "><a href="(.*?)" target="_blank">(.*?)</a></th><td class=" dataCell  ">(.*?)</td><td class=" dataCell  ">(.*?)</td><td class=" dataCell  "><a href=".*?">(.*?)</a></td><td class=" dataCell  ">.*?</td><td class=" dataCell  ">(.*?)</td>'
            res_list = re.findall(temp_str, temp_result, re.DOTALL)
            if res_list:
                for res in res_list:
                    temp_dict = {}
                    temp_dict["link"] = 'https://qualcomm-cdmatech-support.my.salesforce.com/apex' + res[0].strip()
                    temp_dict["name"] = res[1].strip()
                    temp_dict["Description"] = res[2].strip()
                    temp_dict['type'] = res[3].strip()
                    temp_dict['uploader'] = res[4].strip()
                    temp_dict['size'] = res[5].strip()
                    Case_Attachments.append(temp_dict)
        except Exception as e:
            print(e)
        try:
            temp_str = '>Case Comments<.*?<!-- ListRow -->(.*?)</tr></table>'
            temp_result = re.findall(temp_str, text, re.DOTALL)[0]
            temp_str =r'Created By: <a href=.*?>(.*?)</a>(.*?)</b>(.*?)</td>'
            res_list = re.findall(temp_str, temp_result, re.DOTALL)
            if res_list:
                for res in res_list:
                    temp_dict = {}
                    temp_dict['name']=res[0].strip()
                    temp_dict['time']=res[1].split(")")[0].replace("(","").strip()
                    temp_dict['content']=res[2].strip()
                    Case_Comments.append(temp_dict)
        except Exception as e:
            print(e)
        try:
            temp_str = '>Case KBA/Documents Associations<.*?<!-- ListRow -->(.*?)</tr></table>'
            temp_result = re.findall(temp_str, text, re.DOTALL)[0]
            temp_str = 'Del</a></td><th scope="row" class=" dataCell  "><a href="(.*?)" target="_blank">(.*?)</a></th><td class=" dataCell  "><a href=".*?">(.*?)</a></td>'
            res_list = re.findall(temp_str, temp_result, re.DOTALL)
            if res_list:
                for res in res_list:
                    temp_dict = {}
                    temp_dict["link"] = res[0].strip()
                    temp_dict["name"] = res[1].strip()
                    temp_dict["Title"] = res[2].strip()
                    Case_KBA_Doc.append(temp_dict)
        except Exception as e:
            print(e)
        item['Case_link'] = case_url
        item['Case_Number'] = Case_Number
        item['Account_Name'] = Account_Name
        item['Open_Time'] = Open_Time
        item['Case_Owner'] = Case_Owner
        item['Contact_Name'] = Contact_Name
        item['Country'] = Country
        item['Subject'] = Subject
        item['Description'] = Description
        item['PA1'] = PA1
        item['PA2'] = PA2
        item['PA3'] = PA3
        item["OS_Android"] = OS_Android
        item["Software_Product"] = Software_Product
        item["Resolution_Summary"] = Resolution_Summary
        item["ResponsivenessToTheCase"] = ResponsivenessToTheCase
        item["QualityOfTechnicalSupport"] = QualityOfTechnicalSupport
        item["ProfessionalismOfQCEngineer"] = ProfessionalismOfQCEngineer
        item['Case_Comments'] = Case_Comments
        item['Case_KBA_Doc'] = Case_KBA_Doc
        item['Case_Attachments'] = Case_Attachments
        yield item
