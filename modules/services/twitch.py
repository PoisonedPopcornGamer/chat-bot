import asyncio
from  ..utils.EventHook import EventHook
from ..utils.MainObjects import Context, User



class Twitch:
    """ Twitch Chat """ 

    def __init__(self):
        self.onConnect = EventHook()
        self.onConnect += _listen
        self.onRaw = EventHook()
        self.onMsg = EventHook()
        self.onJoin = EventHook()

    async def connect(self, user, oauth=None, channel=None, *, loop=None):
        """one server per bot class for now.. opens a connection to passed host"""
        if not loop:
            loop = asyncio.get_event_loop()
        self.reader, self.writer = await asyncio.open_connection('irc.chat.twitch.tv', 6667, loop=loop)
        if oauth is not None:
            self.writer.write(b'PASS ' + oauth.encode('utf-8') + b'\r\n')
        self.writer.write(b'NICK ' + user.encode('utf-8') + b'\r\n')
        self.writer.write(b'CAP REQ :twitch.tv/tags\r\n')
        if channel:
            self.writer.write(b'JOIN #' + channel.encode('utf-8')+ b'\r\n')
        self.onConnect()
        return True

    async def _listen(self):
        """listens for messages, replies to pings"""
        await asyncio.sleep(1) #wait to be sure the bot is connected to the server before listening. - assuming ping is under ~1 second. 
        while True:
            try:
                data = (await self.reader.readuntil(b'\n')).decode("utf-8")
            except asyncio.streams.IncompleteReadError: #server disconnect..
                raise ConnectionError
                break
            if not data:
                continue
                #normally shouldn't happen, just makes sure server didn't send \n\n somehow.
            data = data.rstrip()
            data = data.split()
            if data[0].startswith('@'):
                tags = data.pop(0)
            else:
                tags = None
            if data[0] == 'PING':
                self.writer.write(b'PONG %s\r\n' % data[1].encode("utf-8"))
            else:
                self.onRaw(data, tags)
            if data[1] == 'PRIVMSG':
                self.onMsg(data, tags)
            if data[1] == 'JOIN':
                self.onJoin(data, tags)

    async def join_channel(self, channel):
        self.writer.write(b"JOIN #{}".format(channel.lower()))

    async def send_message(self, channel, message):
        self.writer.write(b"PRIVMSG #{0} :{1}\r\n".format(channel.lower(), message))

    async def send_raw(self, command):
        self.writer.write(command.encode('utf-8'))
