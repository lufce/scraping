#181204  ver 1.0  完成。エラーログとかを取れるようにしたい。

import mailer, scraper
import requests as webs
import time

WEATHER_URL = "https://www.jma.go.jp/jp/yoho/333.html"
    
#ウェブサイトに接続
time.sleep(1.0)
web = webs.get(WEATHER_URL)
if web.status_code < 200 and 299 < web.status_code:
    #TODO: そのうち接続に成功しなかった場合の処理を書かねばなるまい。
    print("status code: {]".format(web.status_code))
    exit()

body = scraper.make_all(web.content)
mailer.mailing(body)
