import requests
import lxml.html
html = requests.get('https://store.steampowered.com/explore/new/')
doc = lxml.html.fromstring(html.content)
new_releases = doc.xpath('//div[@id="tab_newreleases_content"]')[0]

titles = new_releases.xpath('.//div[@class="tab_item_name"]/text()')
prices = new_releases.xpath('.//div[@class="discount_final_price"]/text()')
tags_divs = new_releases.xpath('.//div[@class="tab_item_top_tags"]')
tags = [div.text_content() for div in tags_divs]

platforms_div = new_releases.xpath('.//div[@class="tab_item_details"]')
total_platforms = []
temp = []
platforms=[]
for game in platforms_div:
    temp = game.xpath('.//span[contains(@class, "platform_img")]')
    platforms = [t.get('class').split(' ')[-1] for t in temp]
    if 'hmd_separator' in platforms:
        platforms.remove('hmd_separator')
    total_platforms.append(platforms)

'''discounts = []
for d in new_releases:
    if bool(d.xpath('.//div[@class="discount_pct"]/text()')) == False:
        discounts.append('0%')
    else:
        discounts.append(d.xpath('.//div[@class="discount_pct"]/text()')[0])'''
     
#Hey I got it!
discounts = ['0%' if bool(d.xpath('.//div[@class="discount_pct"]/text()')) is False else d.xpath('.//div[@class="discount_pct"]/text()')[0] for d in new_releases]

output = []
for info in zip(titles, prices, discounts, tags, total_platforms):
    resp = {}
    resp['title'] = info[0]
    resp['price'] = info[1]
    resp['discounts'] = info[2]
    resp['tags'] = info[3]
    resp['platforms'] = info[4]
    output.append(resp)
    
print(output)
