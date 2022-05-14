import re
import httpx
import asyncio
from bs4 import BeautifulSoup
import selectors
import sys




class Forums_api:
    def __init__(self):
        self.base_url = 'https://demonforums.net'                
        self.session = httpx.AsyncClient()
    
    async def login(self, url):
        dados = {"action": "do_login",
                "url": "",
                "quick_login": 1,
                "my_post_key": "2dc2b997b84ef0c9132990419eab3abd",
                "quick_username": "*********",
                "quick_password": "********",
                "quick_remember": "yes",
                "submit": "Login"}
        page = await self.session.post(url, data=dados)

    async def forums(self, max_forums:int):
        count = 0 
        list_topics = []
        try:
            page =  await self.session.get(f'{self.base_url}')
            site =  BeautifulSoup(page.content, 'html.parser')
            rows =  site.select('div.name')
            for row in rows:
                a_links =  row.select_one('a')
                href_append = a_links.get('href')
                list_topics.append(f'{self.base_url}/{href_append}')
                count +=1
                yield f'{self.base_url}/{href_append}' 
                if count == max_forums:
                    return
        except:
            pass
        for topic in list_topics:
            try: 
                page = await self.session.get(f'{topic}')
                site = BeautifulSoup(page.content, 'html.parser')
                if site.select('div.name'):
                    get_a =  site.select_one('div.name a')
                    href_append = get_a.get("href")
                    list_topics.append(f'{self.base_url}/{href_append}')
                    count += 1  
                    yield f'{self.base_url}/{href_append}' 
                    if count == max_forums:
                        return        
                else:
                    rows =  site.select('div.inline_row')
                    for row in rows:
                        get_spans = row.select('span.subject_old')
                        for get_span in get_spans:
                            get_a = get_span.select_one('a')
                            href_append = get_a.get('href')
                            list_topics.append(f'{self.base_url}/{href_append}')
                            count +=1   
                            yield f'{self.base_url}/{href_append}'                        
                            if count == max_forums:
                                return     
            except:
                pass

    async def topics(self,link_href:str):
        link_next = link_href
        new_link = 'pass'
        dict = {'link-do-post': '',
                'titulo': '',
                'autor': '',
                'time': ''}
        page = await self.session.get(f'{link_href}')
        site = BeautifulSoup(page.content, 'html.parser')
        if site.select_one('a.pagination_next'):
            while site.select_one('a.pagination_next') != None and link_href != f'{self.base_url}/{new_link}':
                try:
                    page = await self.session.get(f'{link_next}')
                    site = BeautifulSoup(page.content, 'html.parser')
                    posts = site.select('tr.inline_row')
                    for rows in posts:
                        href_and_title = rows.select_one("span.subject_new a")
                        href_append = href_and_title.get("href")
                        title = href_and_title.text
                        authors = rows.select_one('span.smalltext')                        
                        
                        text_time =  authors.text
                        regex_time = re.compile("[0-9][0-9]-[0-9][0-9]-[0-9][0-9][0-9][0-9] - [0-9][0-9]:[0-9][0-9] [A-Z][A-Z]")
                        regex_autor = re.compile(" [a-zA-Z]+")
                        check_time =  regex_time.findall(text_time)
                        check_autor = regex_autor.findall(text_time)
                        
                        dict['titulo'] = title
                        dict['link-do-post'] = f'{self.base_url}/{href_append}'
                        dict['autor'] = check_autor[1]
                        dict['time'] = check_time
                        
                        new = site.select_one("a.pagination_next")
                        new_link = new.get("href")
                        link_next = f'{self.base_url}/{new_link}'
                        yield dict
                except:
                   pass
        
        else:
            posts = site.select('tr.inline_row')
            for rows in posts:
                try:
                    href_and_title = rows.select_one("span.subject_new a")
                    href_append = href_and_title.get("href")
                    authors =  rows.select_one('span.smalltext')
                    title = href_and_title.text
                    
                    text_time =  authors.text
                    regex_time = re.compile("[0-9][0-9]-[0-9][0-9]-[0-9][0-9][0-9][0-9] - [0-9][0-9]:[0-9][0-9] [A-Z][A-Z]")
                    regex_autor = re.compile(" [a-zA-Z]+")
                    check_time =  regex_time.findall(text_time)
                    check_autor = regex_autor.findall(text_time)
                    
                    dict['titulo'] = title
                    dict['link-do-post'] = f'{self.base_url}/{href_append}'
                    dict['autor'] = check_autor[1]
                    dict['time'] = check_time
                except:
                    pass
                yield dict
    async def posts(self, topics: str):
        page = await self.session.get(topics)
        site = BeautifulSoup(page.content, 'html.parser')
        post_site = site.select(".widthPage.clearbb")
        for post in post_site:
            rows = post.select_one('div.post_content')
            print(rows)
        print("MATHEUS")
        await self.session.aclose()
    
    
async def main():
    forums_api = Forums_api()
    await forums_api.login(url="https://demonforums.net/member.php")
    await forums_api.posts(topics="https://demonforums.net/Thread-DF-Gadget?page=1")    
    
    
asyncio.run(main())        

