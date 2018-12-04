import re
import requests
from bs4 import BeautifulSoup


def request_page(url1):
    proxy_address = {'http': '121.201.33.100'}
    headers = {
        'User-Agent':
            'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.99 '
            'Safari/537.36'}
    try:
        response = requests.get(url1, headers=headers, proxies=proxy_address)
        soup1 = BeautifulSoup(response.text, "lxml")
        return soup1
    except ConnectionError:
        print('connection failed!')


def page_parse():
    data = []
    info = soup.select('.grid_view li')
    for s in info:
        movie_name = s.find('span', {'class': 'title'}).get_text()
        movie_rating = s.find('span', {'class': 'rating_num'}).get_text()
        rating_person = s.find(text=re.compile('人评价$'))  # 利用正则来匹配评价人数
        movie_inq = s.find('span', {'class': 'inq'})
        if not movie_inq:
            movie_inq = '暂无评价！'
        else:
            movie_inq = movie_inq.get_text()
        data.append(movie_name + "，" + rating_person + "，评分：" + movie_rating + "，一句话评价：" + movie_inq)
        data.append(movie_name)
    next_page = soup.find('span', {'class': 'next'}).find('a')
    if next_page:
        return data, next_page['href']
    else:
        return data, None


if __name__ == '__main__':
    url = "https://movie.douban.com/top250"
    next_url = ''
    with open('D:\\song\\douban_movie.txt', 'w+', encoding='utf-8') as f:
        while next_url or next_url == '':
            soup = request_page(url + next_url)
            movie_data, next_url = page_parse()
            f.write('\n'.join(movie_data))
