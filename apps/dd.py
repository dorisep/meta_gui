from os import path
from datetime import datetime as dt

def tryelse(tryThisFunc, elseReturnValue):
    try: return tryThisFunc()
    except: return elseReturnValue

baseurl = 'https://www.metacritic.com'
starturl = '/browse/albums/release-date/new-releases/date'
url = baseurl+starturl

user_agent = 'Mozilla/5.0 (X11; Linux x86_64; rv:68.0) Gecko/20100101 Firefox/68.0'
headers = {'User-Agent': user_agent}
response = requests.get(url, headers=headers)

page = html.fromstring(response.content)

artists    = [artist.strip()[3:] for artist in page.xpath('//td[@class="clamp-summary-wrap"]/div/div[@class="artist"]/text()')]
albumname  = page.xpath('//td[@class="clamp-summary-wrap"]/a/h3/text()')
links      = page.xpath('//td[@class="clamp-summary-wrap"]/a/@href')
dates      = page.xpath('//td[@class="clamp-summary-wrap"]/div/span/text()')
metascores = page.xpath('//td[@class="clamp-summary-wrap"]/div/div[@class="clamp-metascore"]/a/div/text()')
userscores = page.xpath('//td[@class="clamp-summary-wrap"]/div/div[@class="clamp-userscore"]/a/div/text()')

recordlabels = []
criticCounts = []
userCounts = []
MetaCriticAlbumGenres = []
count = 0

reviews = ['Positive:','Mixed:','Negative:']

for link in links:
    picklefile = path.join('pickles',str(b64encode(link.encode("utf-8")),"utf-8"))

    if path.exists(picklefile) and dt.fromtimestamp(path.getctime(picklefile)).day==dt.now().date().day:
        with open(picklefile,'rb') as pickleLoad:
            content = load(pickleLoad)
    else:
        content = requests.get(baseurl+link, headers=headers).content
        with open(picklefile,'wb') as pickleSave:
            dump(content, pickleSave)
    
    page = html.fromstring(content)
    criticCounts.append(0)
    userCounts.append(0)
    for r in reviews:
        review = page.xpath(f'//span[contains(text(),"{r}")]/following-sibling::span/a/span/span/text()')
        criticCounts[-1] += tryelse(lambda: int(review[0]),0)
        userCounts[-1] += tryelse(lambda: int(review[2]),0)

    recordlabel = page.xpath('//span[contains(@class,"label") and contains(text(),"Record Label")]/following-sibling::span/text()')
    recordlabels.append(recordlabel[2])
    print(recordlabel[2])

    MetaCriticAlbumGenres.append(page.xpath('//span[contains(@itemprop,"genre")]/text()'))
    # add wiki genre search
    # add google genre search

    sleep(1)
    count += 1
    if count > 9:
        break

maybe = zip(artists[:10], albumname[:10], recordlabels, dates[:10], metascores[:10], userscores[:10], criticCounts[:10], userCounts[:10], MetaCriticAlbumGenres[:10])

print(list(maybe))
