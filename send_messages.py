# telegram bot to send message to all members of a channel

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

import pandas as pd

async def send_messages(message,number,client):
    



# read info from excel


    df = pd.read_excel('usres.xlsx')
# print(df)


# pop 50 users

    number = number
    if number > len(df):
        number = len(df)
    selected_users = df.head(number)
    df = df.drop(df.index[range(number)])



# # send message to 50 users


    async def sendmsg(user, message):
        await client.send_message(entity=user, message=message)

    users = selected_users[['User ID','user hash','Username']]

    listedUsers  = users.values.tolist()
    for user in listedUsers:

  

        receiver = InputPeerUser(user[0], user[1])
    
        try:
            # asyncio.get_event_loop().run_until_complete(sendmsg(receiver, message=message))
            # await client.send_message(receiver, message)
            await client.send_file(receiver, "./media/photo.jpg", caption=message)
        except:
            try:
                # await client.send_message(user[2], message=message)
                await client.send_file(user[2], "./media/photo.jpg", caption=message)
                pass
            except:
                pass
            pass



# create new excel file with remaining users

    df.to_excel('usres.xlsx', index=False)
    return len(df)




