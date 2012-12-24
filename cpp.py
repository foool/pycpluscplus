import os
import sys
import re
import urllib
import urllib2

class WebGet(object):
    base_url = ""
    urls_list = []
    history_list = []
    replace_ch={}
	
    def __init__(self, base_url):
        self.base_url = base_url[:-1]
        self.urls_list.append('/')
        self.replace_ch[">>"] = "%3E%3E"
        self.replace_ch["<<"] = "%3C%3C"
        self.replace_ch["::"] = "%3A%3A"
    
    def recurseGet(self):
        '''Get page data recursively'''
        while(len(self.urls_list) != 0):
            url_suffix = self.urls_list[0]
            self.urls_list.remove(url_suffix)
            self.history_list.append(url_suffix)
            url_to_get = self.base_url + url_suffix
            
            "Get page data with url"
            print "To get",url_to_get
            page_data = urllib2.urlopen(url_to_get).read()
            page_data_done = self.pageHandle(page_data)
            
            "Write the page data into file"
            if url_suffix[-1] == '/':
                url_suffix = url_suffix[:-1]
            if url_suffix == '':
                url_suffix = "index"
            elif url_suffix[0] == '/':
                url_suffix = url_suffix[1:]
            url_suffix=url_suffix.replace('>','%3E')
            url_suffix=url_suffix.replace('<','%3C')
            url_suffix=url_suffix.replace(':','%3A')
            url_suffix=url_suffix.replace('^','%5E')
            url_suffix=url_suffix.replace('~','%7E')
            url_suffix=url_suffix.replace('*','%2A')            
            url_suffix=url_suffix.replace(' ','%20')            
            file_str = "/home/cpp/"+url_suffix
            if file_str.rfind("/") != 12:
                new_dir = file_str[:file_str.rfind("/")+1]
                if os.path.isdir(new_dir) == False:
                    print "create dir:",new_dir
                    os.mkdir(new_dir)
            file_str = file_str.strip()+".html"
            print "write file",file_str
            f_page = open(file_str, "wb")
            f_page.write(page_data_done)
            f_page.close
            
    
    def pageHandle(self, page_data):
        page_data = page_data.replace("http://www.cplusplus.com/","/")
	#remove ads
	re_rule = '(<div class="C\_ad\d\d\d">[\S\s]{250,450}</script>[\n]</div>)'
	list_ad = re.findall(re_rule, page_data)
	for eachad in list_ad:
	    page_data = page_data.replace(eachad, '')
	
	#remove footer
	re_rule = '(<div id="I_bottom">[\S\s]{200,300}</div>\n</div>)' 
	list_ad = re.findall(re_rule, page_data)
	for eachad in list_ad:
	    page_data = page_data.replace(eachad, '')

	#remove I_research
	re_rule = '(<div id="I_search">[\S\s]{130,180})<div id="I_bar">'
	list_se = re.findall(re_rule, page_data)
	for each in list_se:
	    page_data = page_data.replace(each, '')
	
	#remove I_user
	i_user = '<div id="I_user" class="C_LoginBox"><span title="ajax"></span></div>'
	page_data = page_data.replace(i_user, '')
	#replace Reference
	i_ref = '<li><a href="/reference/">Reference</a></li>'
	page_data = page_data.replace(i_ref, '<li><a href="/reference/index.html">Reference</a></li>')
	#replace logo
	#page_data = page_data.replace('<div id="I_logo"><a href="/" title="cplusplus.com"><div></div></a></div>','')

	#remove I_root
	re_rule = '(<div class="sect root">[\S\s]{300,500})<div class="C_BoxLabels C_BoxSort sect" id="reference_box">'
	list_se = re.findall(re_rule, page_data)
	for each in list_se:
	    page_data = page_data.replace(each, '')
	
	#save items
        re_rule = '<a href="/reference(/[\S\s]{3,40}/)\">'
        list_page_urls = re.findall(re_rule, page_data)
        for each in list_page_urls:
            if each in self.history_list:
                continue
            elif each in self.urls_list:
                continue
            elif each == '/':
                continue                
            self.urls_list.append(each)
	
	#replace escape ch
        re_rule = '("/reference/[\S\s]{3,40}/")'
        list_page_urls = re.findall(re_rule, page_data)
        for each in list_page_urls:
	    neweach = each
            neweach=neweach.replace('>','%3E')
            neweach=neweach.replace('<','%3C')
            neweach=neweach.replace(':','%3A')
            neweach=neweach.replace('^','%5E')
            neweach=neweach.replace('~','%7E')
            neweach=neweach.replace('*','%2A')
            neweach=neweach.replace(' ','%20') 
            page_data = page_data.replace(each, neweach)

       	#replace urls 
        re_rule = '("/reference/[\S\s]{3,43}/")'
        list_page_urls = re.findall(re_rule, page_data)
        for each in list_page_urls:
	    neweach = each
	    neweach = neweach[:-2]+'.html"'
            page_data = page_data.replace(each, neweach)

        return page_data

def main():
	url = "http://www.cplusplus.com/reference/"
	fc = WebGet(url)
	fc.recurseGet()
    
if __name__ == "__main__":
	main()
