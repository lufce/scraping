import requests as webs
from lxml import etree
import os, re, sys, time, mojimoji, csv

def get_kuchikomi_rating(hotel_html_text, hotel):
    
    #クチコミの値を探す
    count = 0
    
    for line in hotel_html_text.splitlines():
        if re.match(r".*jlnpc-td05.*>.+</td>", line):
            #見つけたのでカウントを増やす
            count = count + 1
            
            #カウントが想定の範囲内かどうか調べて処理
            if count <= 6:
                m = re.match(r".*>(.+)</td>",line)
                hotel[3+count] = m.group(1)
                
            else:
                #カウントが想定の範囲外
                hotel[4] = 'error'
                break
    
    if 0 <= count and count < 6:
        for deff in range(6-count):
            hotel[8-deff] = 'error'
            deff += 1
    
    
def test():
    s1 = "-"
    s2 = "3.2"
    
    try:
        float(s1)
        
    except ValueError:
        print('f1 is error')
        
    try:
        float(s2)
    
    except ValueError:
        print('f2 is error')
        
    print('end')

def get_hotel_detail_html(results):
    
    for hotel in results[1:]:
        
        if hotel[2] != 'error' and hotel[3] != '-':
            
            time.sleep(1.0)
            req = webs.get(hotel[2])
            req.encoding = req.apparent_encoding
            
            get_kuchikomi_rating(req.text, hotel)
            
        else:
            for deff in range(7):
                hotel[3+deff] = '-'


def get_hotel_xml(results):
    
    count = 0
    
    for hotel in results[1:]:
        count = count + 1
        
        url = 'http://jws.jalan.net/APIAdvance/HotelSearch/V1/?key={0}&h_name={1}&count=1&xml_ptn=1' \
            .format(os.environ['JALAN_KEY'], hotel[0])
        
        time.sleep(1.0)
        req = webs.get(url)
        req.encoding = req.apparent_encoding
        tree = etree.XML(req.content)
        
        for element in tree.iter('{jws}HotelName','{jws}HotelDetailURL', '{jws}Rating'):
            if element.tag == '{jws}HotelName':
                if element.text is not None:
                    results[count][1] = element.text
                else:
                    results[count][1] = 'error'
            
            elif element.tag == '{jws}HotelDetailURL':
                if element.text is not None:
                    results[count][2] = element.text
                else:
                    results[count][2] = 'error'
                
            elif element.tag == '{jws}Rating':
                if element.text is not None:
                    results[count][3] = element.text
                else:
                    results[count][3] = '-'
                
            
            
#         output = open('my{}.xml'.format(count), 'w')
#         output.write(etree.tostring(tree).decode('UTF-8'))
#         output.close()

def set_input_hotel_name(results, text_path):
    #テキストファイルから検索すべきホテル名を登録する
    
    count = 1    #1行目は項目名なので、0スタートにしてはいけない。
    try:
        for line in open(text_path, encoding='utf-8_sig'):
            line = mojimoji.han_to_zen(line,digit=False)
            results[count][0] = line.rstrip()
            count = count + 1
    except UnicodeDecodeError:
        try:
            for line in open(text_path):
                line = mojimoji.han_to_zen(line,digit=False)
                results[count][0] = line.rstrip()
                count = count + 1
        except:
            raise
    
    
def init_result_list(hotel_number):
    #引数はint型
    #入力されたホテル数を受け取って結果リストを初期化する。
    #ホテルの数より１つ多く行を作って、一行目は項目名行にする。
    
    results = [[0 for col in range(10)] for row in range(hotel_number + 1)]

    results[0][0] = 'input hotel name'
    results[0][1] = 'found hotel name'
    results[0][2] = 'Hotel Detail URL'
    results[0][3] = 'クチコミ総合'
    results[0][4] = 'クチコミ部屋'
    results[0][5] = 'クチコミお風呂'
    results[0][6] = 'クチコミ朝食'
    results[0][7] = 'クチコミ夕食'
    results[0][8] = 'クチコミサービス'
    results[0][9] = 'クチコミ清潔感'
    
    return results

def get_hotel_number(text_path):
    try:
        return len(open(text_path, encoding='utf-8_sig').readlines())
    except UnicodeDecodeError:
        try:
            return len(open(text_path).readlines())
        except:
            raise
    
if __name__ == '__main__':
    """
    'error'はエラーコードとして定数化すべき
    項目名も同様に定数化すべき
    """
    
    text_path = "hotels.txt"
    try:
        hotel_num = get_hotel_number(text_path)
    except FileNotFoundError:
        sys.exit('The file of the hotel name list is not found.')
    except:
        sys.exit(1)
    
    results = init_result_list(hotel_num)
    set_input_hotel_name(results, text_path)
    get_hotel_xml(results)
    get_hotel_detail_html(results)
    
    count = 0
    while count < 100:
        count += 1
        try:
            result_file = open('results{}.csv'.format(count),'w')
            writer = csv.writer(result_file, lineterminator = "\r")
            writer.writerows(results)
            result_file.close()
            break
        except:
            pass
    
    if count == 100:
        sys.exit("failed to save the csv file!")
    else:
        print('finished')
    
        
    #results = initResultsList(1)
        
#     getRatingFromHotelHTML()