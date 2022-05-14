import asyncio
from scrap import Forums_api


async def get_demoforum():
    forums_api = Forums_api()
    async for forum in forums_api.forums(max_forums=900):
        async for topic in forums_api.topics(forum):
            async for post in forums_api.posts(topic['link-do-post']):
                print(post)
                print('')
                print('===========================================')
                print('')            
            
asyncio.run(get_demoforum())

'''
            print(f"Titulo: {topic['titulo']}")
            print(topic['link-do-post'])
            print(f"Autor: {topic['autor']}")
            print(f"DATA: {topic['time']}")
            print('')
            print('===========================================')
            print('')

'''