
import asyncio
from telethon import TelegramClient, events, sync
from telethon.tl.functions.channels import GetParticipantsRequest
from telethon.tl.types import ChannelParticipantsSearch
from telethon.tl.functions.messages import GetDialogsRequest
from telethon.tl.types import InputPeerEmpty
from telethon.tl.types import InputPeerChannel, PeerChannel, PeerChat, Chat, Channel
from telethon.tl.functions.channels import GetFullChannelRequest
from telethon.tl.functions.messages import AddChatUserRequest
from telethon.tl.functions.channels import InviteToChannelRequest
from telethon.tl.functions.contacts import ResolveUsernameRequest
from telethon.tl.functions.messages import GetDialogsRequest
from telethon.tl.types import InputPeerEmpty
from telethon.tl.types import InputPeerChannel, PeerChannel, PeerChat, Chat, Channel
from telethon.tl.types import InputPeerUser
import re
import xlsxwriter
from telethon.tl.functions.channels import InviteToChannelRequest, JoinChannelRequest
from get_user import getUser
from send_messages import send_messages
# client
api_id = ""
api_hash = ""
client = TelegramClient('session_name', api_id, api_hash)
client.connect()
phone = '+'
if not client.is_user_authorized():
    client.send_code_request(phone)
    client.sign_in(phone, input('Enter the code: '))
else:
    print('Already authorized!')

groupName = ''
groupLink = ''
message = ''
number = 0
handler = []
remain = 0


async def sendmsg(chat, message):
    await client.send_message(entity=chat, message=message)


@client.on(events.NewMessage(chats='me'))
async def my_event_handler(event):
    if event.raw_text == '!sendadd':
        if len(handler) == 0:
            global groupName, groupLink, message, number
            handler.append('send')
            groupName = ''
            groupLink = ''
            message = ''
            number = 0
            await event.reply('نام گروه را با یک /g وارد کنید مثال \n/g groupname')

            @client.on(events.NewMessage(chats='me'))
            async def my_event_handler(event):
                if "/g" in event.raw_text and handler[-1] == 'send':
                    handler.append('gname')
                    global groupName
                    groupName = event.raw_text[3:]
                    # print('1' + groupName)
                    await event.reply('لینک گروه را با یک /l وارد کنید مثال \n/l link')

                    @client.on(events.NewMessage(chats='me'))
                    async def my_event_handler(event):
                        if "/l" in event.raw_text and handler[-1] == 'gname':
                            handler.append('link')
                            global groupLink
                            groupLink = event.raw_text[3:]
                            # print('2' + groupLink)
                            number = await getUser(groupName, groupLink, client)
                            await event.reply('تعداد اعضا : ' + str(number))
                            await event.reply('ذخیره شد')
                            await event.reply(
                                ' تعداد اعضایی که میخواهید برای انها پیام ارسال  شود را انتخاب کنید \n مثال \n /n 100')

                            @client.on(events.NewMessage(chats='me'))
                            async def my_event_handler(event):
                                if "/n" in event.raw_text and handler[-1] == 'link':
                                    handler.append('number')
                                    global number
                                    number = int(event.raw_text[3:])
                                    # print('3' + str(number))
                                    await event.reply('پیام خود را وارد کنید \n مثال \n /m پیام')

                                    @client.on(events.NewMessage(chats='me'))
                                    async def my_event_handler(event):
                                        if "/m" in event.raw_text and handler[-1] == 'number':
                                            # global remain, message
                                            # handler.append('message')
                                            # await client.download_media(event.media, "./media/photo.jpg")

                                            # message = event.raw_text[3:]
                                            # remain = await send_messages(message=message, number=number, client=client)
                                            # await event.reply('پیام ها ارسال شدند')
                                            # await event.reply('تعداد اعضایی که پیام ارسال نشده اند : ' + str(remain))
                                            # await event.reply('برای ارسال مجدد پیام از دستور !sendagain استفاده کنید')
                                            # print(remain)
                                            handler.append('message')
                                            global message
                                            message = event.message.raw_text[3:]
                                            await client.download_media(event.message.media, "./media/photo.jpg")
                                            # await client.send_file('me', "./media/photo.jpg", caption=message)
                                            print('4' + message)
                                            remain = await send_messages(message=message, number=number, client=client)
                                            # await client.forward_messages('me', event.message)
                                            await event.reply('پیام ها ارسال شدند')
                                            await event.reply('تعداد اعضایی که پیام ارسال نشده اند : ' + str(remain))
                                            await event.reply('برای ارسال مجدد پیام از دستور !sendagain استفاده کنید')
                                else:
                                    return 0
                        else:
                            return 0
                else:
                    pass
        else:
            await event.reply(' ربات هم اکنون در حال ارسال پیام است\
                \n میتوانید با دستور !reset ربات را ریست کنید')

    elif event.raw_text == '!sendagain':
        # global remain
        # print(remain,number,message)
        # remain = await send_messages(message=message, number=number, client=client)
        # if remain > 0:
            
            
        #     print('done')
        #     await event.reply('پیام ها ارسال شدند')
        #     await event.reply('تعداد اعضایی که پیام ارسال نشده اند : '+str(remain))
        # else:
        #     await event.reply('پیام ارسال نشده ای وجود ندارد')
        #     await event.reply('برای ریست ربات از دستور !reset استفاده کنید')
        remain = await send_messages(message=message,number=number,client=client)
        if remain > 0 and handler[-1] == 'message':
            
            await event.reply('پیام ها ارسال شدند')
            await event.reply('تعداد اعضایی که پیام ارسال نشده اند : '+str(remain))
        else:
            await event.reply('پیام ارسال نشده ای وجود ندارد')
            await event.reply('برای ریست ربات از دستور !reset استفاده کنید')

    elif event.raw_text == '!reset':
        await event.reply('ربات ریست شد')
        handler.clear()
        groupName = ''
        groupLink = ''
        message = ''
        number = 0


client.run_until_disconnected()
