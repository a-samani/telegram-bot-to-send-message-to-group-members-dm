
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

async def getUser(group,link,client):
    workbook = xlsxwriter.Workbook('usres'+'.xlsx')
    worksheet = workbook.add_worksheet()
    worksheet.write(0, 0, 'Username')
    worksheet.write(0, 1, 'first_name')
    worksheet.write(0, 2, 'User ID')
    worksheet.write(0,3,'user hash')

    print('excel created')
# geting user info

    target_groups = [group] 
    async def get_group_members(target_groups):
        
        for gp in target_groups:
        #     try:
        #         await client(JoinChannelRequest(gp))
        #     except Exception as e:
        #         print(f"Couldn't join group {gp}: Error [{e}]")
            members =  await client.get_participants(gp, aggressive=True)
            return members
    await client.get_entity(link)
    users = await (get_group_members(target_groups))


# save user info in excel
    row = 1
    column = 0
    for u in users:
  
        worksheet.write(row, column, u.username)
        column += 1
        worksheet.write(row, column, u.first_name)
        column += 1
        worksheet.write(row, column, str(u.id))
        column += 1
        if u.access_hash<0:
            u.access_hash = u.access_hash*-1
        worksheet.write(row, column, str(u.access_hash))
        column += 1
        column = 0
        row += 1

    workbook.close()
    return row-1
