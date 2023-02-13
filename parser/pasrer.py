# -*- coding: utf-8 -*-
import ssl
import time

import requests
import requests.auth
from requests.auth import HTTPProxyAuth

from fake_headers import Headers
from requests.adapters import HTTPAdapter
from urllib3.poolmanager import PoolManager
from urllib3.util import ssl_
import requests
from datetime import date
from bs4 import BeautifulSoup
from tg_bot.config.config import bot, dp, db
import asyncio




CIPHERS = """ECDHE-RSA-AES256-GCM-SHA384:ECDHE-ECDSA-AES256-GCM-SHA384:ECDHE-RSA-AES256-SHA384:ECDHE-ECDSA-AES256-SHA384:ECDHE-RSA-AES128-GCM-SHA256:ECDHE-RSA-AES128-SHA256:AES256-SHA"""
class TlsAdapter(HTTPAdapter):

    def __init__(self, ssl_options=0, **kwargs):
        self.ssl_options = ssl_options
        super(TlsAdapter, self).__init__(**kwargs)

    def init_poolmanager(self, *pool_args, **pool_kwargs):
        ctx = ssl_.create_urllib3_context(ciphers=CIPHERS, cert_reqs=ssl.CERT_REQUIRED, options=self.ssl_options)
        self.poolmanager = PoolManager(*pool_args, ssl_context=ctx, **pool_kwargs)



# https://stackoverflow.com/questions/13506455/how-to-pass-proxy-authentication-requires-digest-auth-by-using-python-requests
class HTTPProxyDigestAuth(requests.auth.HTTPDigestAuth):
    def handle_407(self, r):
        """Takes the given response and tries digest-auth, if needed."""

        num_407_calls = r.request.hooks['response'].count(self.handle_407)

        s_auth = r.headers.get('Proxy-authenticate', '')

        if 'digest' in s_auth.lower() and num_407_calls < 2:

            self.chal = requests.auth.parse_dict_header(s_auth.replace('Digest ', ''))

            # Consume content and release the original connection
            # to allow our new request to reuse the same one.
            r.content
            r.raw.release_conn()

            r.request.headers['Authorization'] = self.build_digest_header(r.request.method, r.request.url)
            r.request.send(anyway=True)
            _r = r.request.response
            _r.history.append(r)

            return _r

        return r

    def __call__(self, r):
        if self.last_nonce:
            r.headers['Proxy-Authorization'] = self.build_digest_header(r.method, r.url)
        r.register_hook('response', self.handle_407)
        return r



# https://github.com/serkuksov/avito_bot
# После 12 запросов подряд avito блочит
async def pars():
    session = requests.session()
    adapter = TlsAdapter(ssl.OP_NO_TLSv1 | ssl.OP_NO_TLSv1_1)
    session.mount("https://", adapter)

    header = Headers(
        browser="firefox",  # Generate only Chrome UA
        os="win",  # Generate ony Windows platform
        headers=True  # generate misc headers
    )

    proxie2s = {  # IPV4 https name:pass@ip@port
        "http": "http://91.188.243.18:9588",
        "https": "https://91.188.243.18:9588"
    }

    proxies2 = "https://91.188.243.18:9588"  # IPV4 https name:pass@ip@port

    auth = HTTPProxyAuth("Q5WEco", "Ew9Zb6")

    session.proxies = proxies2
    session.auth = auth  # Set authorization parameters globally

    # Подключиться к базе, получить id и список ссылок
    # получить список id
    list_user_id = db.get_all_id_user()
    for user_id in list_user_id:
        print(user_id)

        # Подписка действует ?
        us_time = db.get_time_subscribe(user_id)

        # Текущая дата
        # Текущее время
        tek_ti = time.time()

        # Если подписка законченна
        if int(tek_ti) > int(us_time):
            pass
        # Если подписка действует
        elif int(tek_ti) < int(us_time):

            await asyncio.sleep(20.0)

            list_hist_links_us = db.get_my_list_hist_links(int(user_id)) # список ссылок проверенных
            list_hist_links_us = list_hist_links_us.replace(',', '').split()

            list_links_us = db.get_my_list_links(int(user_id)) # список ссылок на проверку
            list_links_us = list_links_us.replace(',', '').split()

            num_links = 0 # Считаем число проверенных ссылок

            # перебирать id и получать ссылки,
            for link in list_links_us:
                print(link)

                num_links += 1
                if num_links == 8:
                    num_links = 0
                    await asyncio.sleep(20.0)

                # print(f"user: {user_id} | link: {link}")

                headers = header.generate()

                try:
                    r = session.request('GET', link, headers=headers, timeout=30) #, proxies=proxies, auth=auth)  # Добавь рандомизатор

                    # print(headers)
                    # print(r.headers)
                    # print(r.request.headers)
                    # print(session.cookies.get_dict())

                    soup = BeautifulSoup(r.content, 'html.parser')

                    print(soup)

                    for div in soup.find_all("div", class_='items-items-kAJAg'):  # берем блок обьявлений всех

                        title = div.find_all("h3",
                                             class_="title-root-zZCwT iva-item-title-py3i_ title-listRedesign-_rejR title-root_maxHeight-X6PsH text-text-LurtD text-size-s-BxGpL text-bold-SinUO")

                        price = div.find_all("span", class_="price-text-_YGDY text-text-LurtD text-size-s-BxGpL")

                        link = div.find_all("a",
                                            class_="link-link-MbQDP link-design-default-_nSbv title-root-zZCwT iva-item-title-py3i_ title-listRedesign-_rejR title-root_maxHeight-X6PsH")

                        description = div.find_all("div",
                                                   class_="iva-item-text-Ge6dR iva-item-description-FDgK4 text-text-LurtD text-size-s-BxGpL")

                        if div.find_all("div", class_="items-extraTitle-JFe8_"):
                            break

                        _l = zip(title, description, price, link)
                        for i in _l:
                            link = "https://avito.ru" + str(i[3].get('href'))

                            # Сверяем с базой ссылку,
                            if "https://avito.ru" + str(i[3].get('href')) in list_hist_links_us:
                                pass # Если есть в базе, то игнорим
                            elif "https://avito.ru" + str(i[3].get('href')) not in list_hist_links_us:
                                # Если нету, отправляем текст человеку и добавляем ссылку в базу
                                db.add_hist_links_in_db(user_id, link)

                                try:
                                    await bot.send_message(
                                        user_id,
                                        "[Новый товар]" +
                                        "\nЗаголовок: " + str(i[0].text) +
                                        "\nЦена: " + str(i[2].text) +
                                        "\nОписание: " + str(i[1].text) +
                                        "\nСсылка: https://avito.ru" + i[3].get('href'))
                                except Exception as e:
                                    pass
                                    # await bot.send_message(admin, e)

                except Exception as e:
                    print(e)
                    # await bot.send_message(admin, e)




# Проверяем товар и сохраняем ссылки в базе
async def save_link(user_id, link):
    pass
