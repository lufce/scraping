#TODO: 例外処理

import lxml.html, lxml.etree

DATE_XPATH       = '//*[@id="forecasttablefont"]/tr[{}]/th/text()'
WEATHER_XPATH    = '//*[@id="forecasttablefont"]/tr[{}]/th/img/@alt'
INFO_XPATH       = '//*[@id="forecasttablefont"]/tr[{}]/td[1]/text()'
RAINFALL_XPATH   = '//*[@id="forecasttablefont"]/tr[{}]/td[2]/div/table/tr/td[2]/text()'
MIN_TEMPAR_XPATH = '//*[@id="forecasttablefont"]/tr[{}]/td[3]/div/table/tr[2]/td[2]/text()'
MAX_TEMPAR_XPATH = '//*[@id="forecasttablefont"]/tr[{}]/td[3]/div/table/tr[2]/td[3]/text()'

def make_page_file_from_string(html_string):
    #htmlのテキストからhtmlElementを作る。
    
    my_parser = lxml.html.HTMLParser(encoding='utf-8')
    page = lxml.html.fromstring(html = html_string, parser = my_parser)
    
    return page  

def get_simple_text(page, parent_xpath):
    #京都の南部の今日と明日の何かを取る。
    
    contents = []
    for i in range(2,4):
        xpath_exp = parent_xpath.format(i)
        find_weather = lxml.etree.XPath(xpath_exp)
        info_list = find_weather(page)
        
        if len(info_list) == 0:
            #何かのエラーで値が取得できなかった場合は-!-を入れる
            contents.append("-!-")
            
        elif parent_xpath == RAINFALL_XPATH:
            #降水確率は要素全てがほしい
            contents.append(info_list)
            
        else:
            contents.append(info_list[0])
    
    return contents

def make_pretty_text(date, weather, info, rainfall, min_tempar, max_tempar):
    #メール送信用の本文を整形する。
    
    today_rain    = ",  ".join(rainfall[0])
    tomorrow_rain = ",  ".join(rainfall[1])
    
    today_tempar    = "最低 {}　最高 {}".format(min_tempar[0],max_tempar[0])
    tomorrow_tempar = "最低 {}　最高 {}".format(min_tempar[1],max_tempar[1])
    
    #dateの最初に改行文字が入っているみたいなので、date[0]だけstripする
    text =        "{}  {}\n-　{}\n-　{}\n-　{}\n".format(date[0].strip(),weather[0],today_rain,   today_tempar,   info[0])
    text = text + "{}  {}\n-　{}\n-　{}\n-　{}"  .format(date[1]        ,weather[1],tomorrow_rain,tomorrow_tempar,info[1])

    return text

def make_all(html_string):
    page = make_page_file_from_string(html_string)
    
    date         = get_simple_text(page, DATE_XPATH)
    weather      = get_simple_text(page, WEATHER_XPATH)
    info         = get_simple_text(page, INFO_XPATH)
    rainfall     = get_simple_text(page, RAINFALL_XPATH)
    min_tempar   = get_simple_text(page, MIN_TEMPAR_XPATH)
    max_tempar   = get_simple_text(page, MAX_TEMPAR_XPATH)
    
    return make_pretty_text(date, weather, info, rainfall, min_tempar, max_tempar)
    