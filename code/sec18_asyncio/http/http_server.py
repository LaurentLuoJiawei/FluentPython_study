"""
    Des：section17 aiohttp 实现web服务器
    Date: 2021.06.30
"""
import sys
import asyncio
import aiohttp
from aiohttp import web
import charfinder
from charfinder import UnicodeNameIndex
#
#
# TEMPLATE_NAME = 'http_charfinder.html'
# CONTENT_TYPE = 'text/html; charset=UTF-8'
# SAMPLE_WORDS = ('bismillah chess cat circled Malayalam digit'
#                 ' Roman face Ethiopic black mark symbol dot'
#                 ' operator Braille hexagram').split()
#
# ROW_TPL = '<tr><td>{code_str}</td><th>{char}</th><td>{name}</td></tr>'
# LINK_TPL = '<a href="/?query={0}" title="find &quot;{0}&quot;">{0}</a>'
# LINKS_HTML = ', '.join(LINK_TPL.format(word) for word in
#                        sorted(SAMPLE_WORDS, key=str.upper))
#
# index = UnicodeNameIndex()
#
# async def init(loop, address, port):
#     app = web.Application(loop=loop)
#     app.router.add_route('GET','/', home)       # 将路由把URL模式银蛇到处理函数上。将 GET / 路由映射到home 函数上
#     handler = app.make_handler()
#     server = await loop.create_server(handler, address, port)
#
#     return server.sockets[0].getsockname()
#
#
# def main(address='127.0.0.1', port= 2323):
#     port = int(port)
#     loop = asyncio.get_event_loop()
#     host = loop.run_until_complete(init(loop, address, port))
#     print("Serving on {}, Hit CTRL-C to stop".format(host))
#     try:
#         loop.run_forever()
#     except KeyboardInterrupt:
#         pass
#     print("Server shutting down")
#     loop.close()
#
# def home(request):
#     """
#     路由处理函数，参数是web.request 实例
#     :param request:
#     :return:
#     """
#     query = request.GET.get('query', '').strip()        # 获取查询字符串
#     print("Query： {!r}".format(query))
#     if query:
#         descrptions = list(index.find_descriptions(query))
#         res = '\n'.join()
#
#

import sys
import asyncio
from aiohttp import web

from charfinder import UnicodeNameIndex

TEMPLATE_NAME = 'http_charfinder.html'
CONTENT_TYPE = 'text/html; charset=UTF-8'
SAMPLE_WORDS = ('bismillah chess cat circled Malayalam digit'
                ' Roman face Ethiopic black mark symbol dot'
                ' operator Braille hexagram').split()

ROW_TPL = '<tr><td>{code_str}</td><th>{char}</th><td>{name}</td></tr>'
LINK_TPL = '<a href="/?query={0}" title="find &quot;{0}&quot;">{0}</a>'
LINKS_HTML = ', '.join(LINK_TPL.format(word) for word in
                       sorted(SAMPLE_WORDS, key=str.upper))


index = UnicodeNameIndex()
with open(TEMPLATE_NAME) as tpl:
    template = tpl.read()
template = template.replace('{links}', LINKS_HTML)

# BEGIN HTTP_CHARFINDER_HOME
def home(request):  # <1>
    query = request.GET.get('query', '').strip()  # <2>
    print('Query: {!r}'.format(query))  # <3>
    if query:  # <4>
        descriptions = list(index.find_descriptions(query))
        res = '\n'.join(ROW_TPL.format(**descr._asdict())
                        for descr in descriptions)
        msg = index.status(query, len(descriptions))
    else:
        descriptions = []
        res = ''
        msg = 'Enter words describing characters.'

    html = template.format(query=query, result=res,  # <5>
                           message=msg)
    print('Sending {} results'.format(len(descriptions)))  # <6>
    return web.Response(content_type=CONTENT_TYPE, text=html) # <7>
# END HTTP_CHARFINDER_HOME


# BEGIN HTTP_CHARFINDER_SETUP

async def init(loop, address, port):  # <1>
    app = web.Application(loop=loop)  # <2>
    app.router.add_route('GET', '/', home)  # <3>
    handler = web.AppRunner(app=app)
    server = await loop.create_server(handler,
                                           address, port)  # <5>
    return server.sockets[0].getsockname()  # <6>

def main(address="127.0.0.1", port=8888):
    port = int(port)
    loop = asyncio.get_event_loop()
    host = loop.run_until_complete(init(loop, address, port))  # <7>
    print('Serving on {}. Hit CTRL-C to stop.'.format(host))
    try:
        loop.run_forever()  # <8>
    except KeyboardInterrupt:  # CTRL+C pressed
        pass
    print('Server shutting down.')
    loop.close()  # <9>


if __name__ == '__main__':
    main(*sys.argv[1:])
# END HTTP_CHARFINDER_SETUP
