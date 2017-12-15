import asyncio
from  ..utils.EventHook import EventHook
from ..utils.MainObjects import Context, User
from time import time



class Twitch:
    """ Twitch Chat """ 

    def __init__(self):
        self.onConnect = EventHook()
        self.onConnect += self._listen
        self.onRaw = EventHook()
        self.onRaw += self._parse_message
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
            data = data.strip()
            #print(data)
            if data.startswith('PING'):
                data = data.split()
                self.writer.write(b'PONG %s\r\n' % data[1].encode("utf-8"))
            else:
                self.onRaw(data)

    async def _parse_message(self, data):
        data = data.split()
        if data[0].startswith('@'):
            tags = data.pop(0)
            tag_dict = {}
            tags = tags.lstrip('@').split(';')
            for i in tags:
                tag = i.split('=')
                tag_dict[tag[0]] = tag[1]
        else:
            tags = None
            tag_dict = {}

        if data[1] == 'PRIVMSG':
            displayname = tag_dict.get('display-name', '')
            username = displayname.lower()
            mention = '@' + displayname
            uid = tag_dict.get('user-id', None)
            message = ' '.join(data[3:])[1:] #remove first character, data[3:] == :<message>
            channel = data[2]
            service = 'twitch'
            timestamp = int(tag_dict.get('tmi-sent-ts', 0)) or time()
            permissions = []
            for i in ['mod', 'subscriber']:
                if tag_dict.get(i, False) == '1':
                    permissions += [i]
            if 'broadcaster' in tag_dict.get('badges', ''):
                permissions += ['broadcaster']
                
            author = User(uid=uid, username=username, displayname=displayname, mention=mention )
            ctx = Context(
                service=service, server=service, channel=channel, 
                message=message, timestamp=timestamp, author=author, 
                permissions=permissions, tags=tag_dict
                )

            self.onMsg(ctx)
        if data[1] == 'JOIN': #probably gonna just change to "onTwitchCommand or something"
            pass

    async def join_channel(self, channel):
        self.writer.write(b"JOIN #{}".format(channel.lower()))

    async def send_message(self, channel, message):
        self.writer.write(b"PRIVMSG #{0} :{1}\r\n".format(channel.lower(), message))

    async def send_raw(self, command):
        self.writer.write(command.encode('utf-8'))

def setup(bot):
    
    n = Twitch()
    asyncio.get_event_loop().create_task(n.connect('sweetiebot_', 'oauth:msivmpb3q3a5fv5qlof1cl05jhn3eh', 'x_thehiddengamer_x'))

    bot.register(n, name='twitch')