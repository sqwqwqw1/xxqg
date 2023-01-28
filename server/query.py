import requests, re
from bs4 import BeautifulSoup

def query(key):
    url = 'http://www.syiban.com/search/index/init.html?modelid=1&q='
    headers = {
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/109.0.0.0 Safari/537.36',
        'Referer': 'http://www.syiban.com/',
    }
    r = requests.get('{}{}'.format(url,key),headers=headers)
    soup = BeautifulSoup(r.text,'lxml')
    li = soup.find_all('div','yzm-news-right')
    answer_li = []
    for i in li:
        question = i.find('span','title_color').text
        question = re.sub(r'\u200b', '', question)
        answer = re.sub(r'\u200b|答案：|A、|B、|C、|D、|E、|F、|A\.|B\.|C\.|D\.|E\.|F\.|\s', '', i.find_all('span')[-1].text)
        item = {'question':question,
               'answer':answer}
        answer_li.append(item)
    return answer_li

def run_query(q):
    try:
        if len(query(q))!=0:
            data = {'status':'success','data': query(q)}
            data.update({'total':len(data['data'])})
        else:
            data = {'status':'failed','error': '查询结果为空！'}
    except:
        data = {'status':'failed','error': '查询失败，没有相应结果！'}
    return data