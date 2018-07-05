import mechanize
import re
import csv

user_info = []

fb_url = 'http://www.facebook.com/100004210542493'
br = mechanize.Browser()
br.set_handle_robots(False)

br.open(fb_url)
all_html = br.response().get_data()
print (all_html)

city = re.search('fsl fwb fcb">(.+?)</a></div><div class="aboutSubtitle fsm fwn fcg', all_html).group(1)

user_info = [fb_url, city]
print (user_info)