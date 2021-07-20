"""
    Des：section17 asyncio_18 实现TCP服务器
    Date: 2021.06.30
"""
# import asyncio
# import sys
# from charfinder import UnicodeNameIndex
#
# CRLF = b'\r\n'
# PROMPR = b'?>'
# index = UnicodeNameIndex()
#
# async def handle_queries(reader:asyncio.streams.StreamReader , writer:asyncio.streams.StreamWriter):
#     while True:
#         writer.write(PROMPR)
#         await writer.drain()
#         data = await reader.readline()
#         try:
#             query = data.decode().strip()
#         except UnicodeDecodeError:
#             query = '\x00'
#         client = writer.get_extra_info('peername')
#         print("Receive from {}:{}".format(client, query))
#         if query:
#             print(query)
#             if ord(query[:-1]) < 32:
#                 break
#             lines = list(index.find_description_strs(query))
#             if lines:
#                 writer.writelines(line.encode() + CRLF for line in lines)
#             writer.write(index.status(query, len(lines)).encode() + CRLF)
#             await writer.drain()
#             print("Sent {} results".format(len(lines)))
#
#     print("close the client socket")
#     writer.close()
#
# def main(address='127.0.0.1', port=2323):
#     port = int(port)
#     loop = asyncio.get_event_loop()
#     server_coro = asyncio.start_server(handle_queries, host=address, port=port, loop=loop)
#     server = loop.run_until_complete(server_coro)
#     host = server.sockets[0].getsockname()
#     # host = server.sockets
#     print("Server on {}: Hit CTRL-C to stop".format(host))
#     try:
#         loop.run_forever()
#     except KeyboardInterrupt:
#         pass
#     print("Server shutting down")
#     server.close()
#     loop.run_until_complete(server.wait_closed())
#     loop.close()
#
#
# if __name__ == '__main__':
#     main(*sys.argv[1:])

# BEGIN TCP_CHARFINDER_TOP
import sys
import asyncio

from fluentPython.asyncio_18.tcp.charfinder import UnicodeNameIndex  # <1>

CRLF = b'\r\n'
PROMPT = b'?> '

index = UnicodeNameIndex()  # <2>


async def handle_queries(reader, writer):  # <3>
    while True:  # <4>
        writer.write(PROMPT)  # can't yield from!  # <5>
        await writer.drain()  # must yield from!  # <6>
        data = await reader.readline()  # <7>
        try:
            query = data.decode().strip()
        except UnicodeDecodeError:  # <8>
            query = '\x00'
        client = writer.get_extra_info('peername')  # <9>
        print('Received from {}: {!r}'.format(client, query))  # <10>
        if query:
            if ord(query[:1]) < 32:  # <11>
                break
            lines = list(index.find_description_strs(query)) # <12>
            if lines:
                writer.writelines(line.encode() + CRLF for line in lines) # <13>
            writer.write(index.status(query, len(lines)).encode() + CRLF) # <14>

            await writer.drain()  # <15>
            print('Sent {} results'.format(len(lines)))  # <16>

    print('Close the client socket')  # <17>
    writer.close()  # <18>
# END TCP_CHARFINDER_TOP

# BEGIN TCP_CHARFINDER_MAIN
def main(address='127.0.0.1', port=2323):  # <1>
    port = int(port)
    loop = asyncio.get_event_loop()
    server_coro = asyncio.start_server(handle_queries, address, port,
                                       loop=loop) # <2>
    server = loop.run_until_complete(server_coro) # <3>

    host = server.sockets[0].getsockname()  # <4>
    print('Serving on {}. Hit CTRL-C to stop.'.format(host))  # <5>
    try:
        loop.run_forever()  # <6>
    except KeyboardInterrupt:  # CTRL+C pressed
        pass

    print('Server shutting down.')
    server.close()  # <7>
    loop.run_until_complete(server.wait_closed())  # <8>
    loop.close()  # <9>


if __name__ == '__main__':
    main(*sys.argv[1:])  # <10>