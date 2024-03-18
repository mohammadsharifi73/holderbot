from pyrogram import *
from pyrogram.types import *
from pyrogram.errors.exceptions import *
import requests
import json
import traceback
from Function.db import *
from Function.keyboards import *
from Function.qr import *
from Function.search import *
from Function.admins import *
from Function.users import *
from Function.nodes import *
from Function.create import *
from Function.stase import *
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton


from datetime import datetime, timedelta
import re , os
# Define the callback data constants
EDIT_DATA_LIMIT = "edit_data_limit"
EDIT_EXPIRE_DURATION = "edit_expire_duration"

user_session = {}
app = Client( 
    "holder",      
    api_id=26410400,
    api_hash="408bf51732560cb81a0e32533b858cbf",
    bot_token=DEF_GET_BOT_TOKEN()) #from db , bot table

@app.on_message(filters.private)
async def holderbot(client: Client, message: Message) :
    
    MESSAGE_CHATID = message.chat.id 

    if DEF_CHECK_BOSS(MESSAGE_CHATID):
    
        if message.caption :
            MESSAGE_TEXT = message.caption
        elif message.text :
            MESSAGE_TEXT = message.text
        else :
            return
        
        #print(MESSAGE_TEXT)
        
        if MESSAGE_TEXT in ["🔙 cancel" , "/cancel" , "cancel" , "❌ NO ,forget." ]  :
            await client.send_message(chat_id=MESSAGE_CHATID , text=f"🏛" , reply_markup=KEYBOARD_HOME)
            UPDATE_STEP = DEF_UPDATE_STEP(MESSAGE_CHATID,"None")
            return
        
        CHECK_STEP = DEF_CHECK_STEP(MESSAGE_CHATID)
        if CHECK_STEP == "None" :

            if MESSAGE_TEXT == "/start" :
                TEXT = "<b>Hello boss,I'm HolderBot (version 4.4.2)\n\nI am an open-source Telegram bot designed to provide unique and special features. All my commands are clear, but you can still refer to the <a href='https://github.com/erfjab/holderbot/wiki'>Wiki</a> for tutorials and guidance, open an <a href='https://github.com/erfjab/holderbot/issues'>issue</a> for bugs and suggestions, and join the <a href='https://t.me/ErfjabHolderbot'>channel</a> for important news.\n\nBy the way, boss, to enhance my capabilities, you can help my developer by forking the project on GitHub. Even if you're not familiar with coding, you can still contribute by <a href='https://github.com/erfjab/holderbot'>starring</a> the project. Either way, thank you.</b>"
                await client.send_message(chat_id=MESSAGE_CHATID , text=TEXT , reply_markup=KEYBOARD_HOME , parse_mode=enums.ParseMode.HTML , disable_web_page_preview=True)

            elif MESSAGE_TEXT == "💬 Help" :
                TEXT = "<b>Hello boss, It seems you've encountered an issue! Don't worry, first check the <a href='https://github.com/erfjab/holderbot/wiki'>Github Wiki</a> or <a href='https://t.me/ErfjabHolderbot'>Telegram channel</a>. If your problem persists, open an <a href='https://github.com/erfjab/holderbot/issues'>issue on Github</a> so that my developer can respond to you promptly.\n\nAdditionally, a file containing my logs has been sent to you, which my developer needs for debugging and resolving the issue. Thank you for your cooperation, boss.</b>"
                await client.send_message(chat_id=MESSAGE_CHATID , text=TEXT , reply_markup=KEYBOARD_HOME , parse_mode=enums.ParseMode.HTML , disable_web_page_preview=True)
                await client.send_document(chat_id=MESSAGE_CHATID , document="nohup.out" , file_name="holderlogs.txt" , caption=f'<b>{datetime.now().strftime("%d/%m/%Y, %H:%M")}</b>' , parse_mode=enums.ParseMode.HTML )

            elif MESSAGE_TEXT == "🖼 QR Code" :
                TEXT = "<b>Please send your link.</b>"
                await client.send_message(chat_id=MESSAGE_CHATID , text=TEXT , reply_markup=KEYBOARD_CANCEL , parse_mode=enums.ParseMode.HTML)
                UPDATE_STEP = DEF_UPDATE_STEP(MESSAGE_CHATID,"qrcode | wait to send link")

            elif MESSAGE_TEXT == "🔍 Search" :
                await client.send_message(chat_id=MESSAGE_CHATID , text="<b>Please send me the words.</b>" , reply_markup=KEYBOARD_CANCEL , parse_mode=enums.ParseMode.HTML)
                UPDATE_STEP = DEF_UPDATE_STEP(MESSAGE_CHATID,"search | wait to send words")

            elif MESSAGE_TEXT == "👨🏻‍💻 Admins" :
                KEYBOARD_ADMINS = KEYBOARD_ADMINS_LIST(MESSAGE_CHATID)
                await client.send_message(chat_id=MESSAGE_CHATID , text="<b>Please select an admin or add a new admin?</b>" , reply_markup=KEYBOARD_ADMINS , parse_mode=enums.ParseMode.HTML)
                UPDATE_STEP = DEF_UPDATE_STEP(MESSAGE_CHATID,"admins | wait to select or add admin")

            elif MESSAGE_TEXT == "👤 Users" :
                WAIT_MESSGAE = await client.send_message(chat_id=MESSAGE_CHATID, text=f"<b>⏳️ in progress...</b>" , reply_markup=ReplyKeyboardRemove() , parse_mode=enums.ParseMode.HTML)
                TEXT = DEF_ALL_USERS(MESSAGE_CHATID)
                await client.send_message(chat_id=MESSAGE_CHATID , text=TEXT , reply_markup=KEYBOARD_USERS , parse_mode=enums.ParseMode.HTML)               
                await WAIT_MESSGAE.delete()
                UPDATE_STEP = DEF_UPDATE_STEP(MESSAGE_CHATID,"users | wait to select list")

            elif MESSAGE_TEXT == "🎗 Nodes" :
                KEYBOARD_NODES_LIST = DEF_NODES_LIST(MESSAGE_CHATID)
                await client.send_message(chat_id=MESSAGE_CHATID , text=f"<b>Please select node.</b>" , reply_markup=KEYBOARD_NODES_LIST, parse_mode=enums.ParseMode.HTML)
                UPDATE_STEP = DEF_UPDATE_STEP(MESSAGE_CHATID,"nodes | wait to select node")

            elif MESSAGE_TEXT == "🎛 Monitoring" :
                BOSS_CHATID , NODE_STATUS , CHECK_NORMAL , CHECK_ERROR = DEF_MONITORING_DATA()
                if NODE_STATUS == "off" :
                    TEXT = f"<b>🔴 Monitoring is <code>off</code></b>"
                    KEYBOARD_MONITORING = KEYBOARD_OFF_MONITORING
                else :
                    TEXT = f"<b>🟢 Monitoring is <code>on</code>\nMonitoring timer : <code>{CHECK_NORMAL} second</code>\nError timer : <code>{CHECK_ERROR} second</code></b>"
                    KEYBOARD_MONITORING = KEYBOARD_ON_MONITORING  
                await client.send_message(chat_id=MESSAGE_CHATID , text=TEXT , reply_markup=KEYBOARD_MONITORING , parse_mode=enums.ParseMode.HTML , disable_web_page_preview=True )
                UPDATE_STEP = DEF_UPDATE_STEP(MESSAGE_CHATID,"monitoring | wait to select command")
                
            elif MESSAGE_TEXT == "🗃 Templates" :
                KEYBOARD_TEMPLATES = KEYBOARD_TEMPLATES_LIST()
                await client.send_message(chat_id=MESSAGE_CHATID , text=f"<b>Please select a templates or add a new templates?</b>" , reply_markup=KEYBOARD_TEMPLATES , parse_mode=enums.ParseMode.HTML , disable_web_page_preview=True )
                UPDATE_STEP = DEF_UPDATE_STEP(MESSAGE_CHATID,"templates | wait to select command")
            
            elif MESSAGE_TEXT == "🚀 Create User" :
                KEYBOARD_TEMPLATES = KEYBOARD_CREATE_LIST()
                await client.send_message(chat_id=MESSAGE_CHATID , text=f"<b>Please select a template or create user manually.</b>" , reply_markup=KEYBOARD_TEMPLATES , parse_mode=enums.ParseMode.HTML , disable_web_page_preview=True )
                UPDATE_STEP = DEF_UPDATE_STEP(MESSAGE_CHATID,"create | wait to select command")
            
            elif MESSAGE_TEXT == "✏️ Edit Users" :

                user_session[MESSAGE_CHATID] = {'edit_field': ['data_limit', 'expire_duration']}
                await client.send_message(chat_id=MESSAGE_CHATID , text=f"<b>Please enter the User and the new data limit in GB and the new expire duration in day separated in space:</b>" , parse_mode=enums.ParseMode.HTML , disable_web_page_preview=True )
            elif MESSAGE_TEXT == "🎖 Notice" :
                await client.send_message(chat_id=MESSAGE_CHATID , text=f"<b>Welcome to the Messages section! This feature has been added with sponsorship the <a href='https://t.me/GrayServer'>Gray</a> collection.❤️ You can visit the Gray collection channel and bot for purchasing servers on an hourly and monthly basis, with a wide variety of locations and specifications, accompanied by clean IPs at the lowest prices.\n\nTo utilize this feature, you first need to create an inbound according to the tutorial on GitHub Wiki or the Telegram channel tutorial for Holderbot. Then, in the host setting section of that inbound, write down the texts you desire to be displayed to the user upon completion of the configuration update.\n\nYour Messages is <code>{DEF_GET_MESSAGE_STATUS(MESSAGE_CHATID)}</code></b>" , reply_markup=KEYBOARD_MESSAGES , parse_mode=enums.ParseMode.HTML , disable_web_page_preview=True )
                UPDATE_STEP = DEF_UPDATE_STEP(MESSAGE_CHATID,"message | wait to select command")
            else :
                if MESSAGE_TEXT == "🧨" or ("boss of one") in MESSAGE_TEXT or "set the messages." in MESSAGE_TEXT or "(Checker)" in MESSAGE_TEXT :
                    return
                if not user_session:
                    TEXT , KEYBOARD_UPDATE_STASE = DEF_STASE_USER (MESSAGE_CHATID , MESSAGE_TEXT , KEYBOARD_HOME)
                    await client.send_message(chat_id=MESSAGE_CHATID , text=TEXT , reply_markup=KEYBOARD_UPDATE_STASE , parse_mode=enums.ParseMode.HTML)
                    return    
                else:
                    user_id = message.from_user.id
                    #print(user_id,MESSAGE_CHATID)
                    if user_id in user_session and 'edit_field' in user_session[user_id]:
                        user_response = message.text.split()
                        if len(user_response) == 2:
                            username = user_session[user_id]['username']
                            try:
                                data_limit = float(user_response[0])  # Convert first value to float
                                expire_duration = int(user_response[1])  # Convert second value to int
                                # Update user_session
                                if user_id in user_session:
                                    user_session[user_id]['edit_field'] = {'data_limit': data_limit, 'expire_duration': expire_duration}
                                    new_data_limit_gb = float(data_limit)
                                    new_expire_duration_days = int(expire_duration)
                                    success = update_user_data(user_id, username, new_data_limit_gb, new_expire_duration_days)
                                    response_text = "User info updated successfully." if success else "Failed to update data limit."
                                    await message.reply_text(response_text)
                                else:
                                    await message.reply_text("User session not found.")
                            except ValueError:
                                await message.reply_text("Invalid input. Please enter valid numbers for data limit and expire duration.")
                        elif len(user_response) == 1:
                            edit_field = user_session[user_id]['edit_field']
                            username = user_session[user_id]['username']
                            
                            # Handling input for data limit
                            if edit_field == 'data_limit':
                                try:
                                    new_data_limit_gb = float(message.text)
                                    success = update_user_data(user_id, username, new_data_limit_gb, None)
                                    response_text = "Data limit updated successfully." if success else "Failed to update data limit."
                                    await message.reply_text(response_text)
                                except ValueError:
                                    await message.reply_text("Please enter a valid number for data limit in GB.")
                            
                            # Handling input for expire duration
                            elif edit_field == 'expire_duration':
                                try:
                                    new_expire_duration_days = int(message.text)
                                    success = update_user_data(user_id, username, None, new_expire_duration_days)
                                    response_text = "Expire duration updated successfully." if success else "Failed to update expire duration."
                                    await message.reply_text(response_text)
                                except ValueError:
                                    await message.reply_text("Please enter a valid number of days for expire duration.")

                        else:
                            try:
                                input_str=message.text
                                input_str = re.sub(r'\n+', '\n', input_str)
                                lines = input_str.strip().split('\n')
                                for user_response in lines:
                                    user_response=user_response.split()
                                    data_limit = float(user_response[1])  # Convert first value to float
                                    expire_duration = int(user_response[2])  # Convert second value to int
                                    username='user'+user_response[0]
                                    #print(data_limit,expire_duration,username)
                                    # Update user_session
                                    if user_id in user_session:
                                        user_session[user_id]['edit_field'] = {'data_limit': data_limit, 'expire_duration': expire_duration}
                                        new_data_limit_gb = float(data_limit)
                                        new_expire_duration_days = int(expire_duration)
                                        success = update_user_data(user_id, username, new_data_limit_gb, new_expire_duration_days)
                                        response_text = username+" done." if success else username+"Failed."
                                        await message.reply_text(response_text)
                                    else:
                                        await message.reply_text("User session not found.")
                                await message.reply_text("Users info updated successfully.")
                            except Exception as e:
                                tb = traceback.format_exc()
                                print(f"An error occurred: {e}\n{tb}")
                           # except ValueError:
                           #     await message.reply_text("Invalid input. Please enter valid numbers.")
                      
                        # Clear user session after processing
                        del user_session[user_id]

        else :
            MESSAGES_SPLIT = MESSAGE_TEXT.strip().split(" ")
            STEP_SPLIT = CHECK_STEP.strip().split(" ")


            if CHECK_STEP.startswith("qrcode") :
                if CHECK_STEP == "qrcode | wait to send link" :
                    QRCODE_IMG = DEF_CREATE_QRCODE(MESSAGE_TEXT)
                    await client.send_photo(chat_id=MESSAGE_CHATID , photo=QRCODE_IMG,caption=f"<pre>{MESSAGE_TEXT}</pre>" , reply_markup=KEYBOARD_HOME)
                    UPDATE_STEP = DEF_UPDATE_STEP(MESSAGE_CHATID,"None")


            elif CHECK_STEP.startswith("search") :
                if CHECK_STEP == "search | wait to send words" :
                    WAIT_MESSGAE = await client.send_message(chat_id=MESSAGE_CHATID, text=f"<b>⏳️ in progress...</b>" , reply_markup=ReplyKeyboardRemove() ,  parse_mode=enums.ParseMode.HTML)
                    TEXT = DEF_SEARCH_USERS(MESSAGE_CHATID , MESSAGE_TEXT)
                    await client.send_message(chat_id=MESSAGE_CHATID , text=TEXT , reply_markup=KEYBOARD_CANCEL , parse_mode=enums.ParseMode.HTML)               
                    await WAIT_MESSGAE.delete()


            elif CHECK_STEP.startswith("admins") :

                if CHECK_STEP == "admins | wait to select or add admin" :

                    if re.search(r"- (SUDO|N\.SUDO)", MESSAGE_TEXT) and len(MESSAGES_SPLIT) == 3 :
                        await client.send_message(chat_id=MESSAGE_CHATID , text="<b>Please select command.</b>" , reply_markup=KEYBOARD_ADMIN , parse_mode=enums.ParseMode.HTML)
                        UPDATE_STEP = DEF_UPDATE_STEP(MESSAGE_CHATID,f"admins | selected admin {MESSAGES_SPLIT[0]} {MESSAGES_SPLIT[2]}")
                    
                    elif MESSAGE_TEXT == "➕ Add new admin" :
                        await client.send_message(chat_id=MESSAGE_CHATID , text="<b>Please enter new admin username :</b>" , reply_markup=KEYBOARD_CANCEL , parse_mode=enums.ParseMode.HTML)
                        UPDATE_STEP = DEF_UPDATE_STEP(MESSAGE_CHATID,f"admins | add admin")

                else :

                    if CHECK_STEP.startswith("admins | selected") :

                        if CHECK_STEP.startswith("admins | selected admin") :
                            ADMIN_NAME , ADMIN_SUDO = STEP_SPLIT[4:]

                            if MESSAGE_TEXT == "🔐 Change pass" :
                                await client.send_message(chat_id=MESSAGE_CHATID , text="<b>What is the new password of this admin?</b>" , reply_markup=KEYBOARD_CANCEL , parse_mode=enums.ParseMode.HTML)
                                UPDATE_STEP = DEF_UPDATE_STEP(MESSAGE_CHATID,f"admins | selected change password {ADMIN_NAME} {ADMIN_SUDO}")
                            
                            elif MESSAGE_TEXT == "🔐 Change sudo" :
                                await client.send_message(chat_id=MESSAGE_CHATID , text="<b>are you sure?</b>" , reply_markup=KEYBOARD_YES_OR_NOO , parse_mode=enums.ParseMode.HTML)
                                UPDATE_STEP = DEF_UPDATE_STEP(MESSAGE_CHATID,f"admins | selected change sudo {ADMIN_NAME} {ADMIN_SUDO}")

                            elif MESSAGE_TEXT == "🗑 Delete admin" :
                                await client.send_message(chat_id=MESSAGE_CHATID , text="<b>What!!! are you really?</b>" , reply_markup=KEYBOARD_YES_OR_NOO , parse_mode=enums.ParseMode.HTML)
                                UPDATE_STEP = DEF_UPDATE_STEP(MESSAGE_CHATID,f"admins | selected delete this {ADMIN_NAME} {ADMIN_SUDO}")
                        
                        else :
        
                            ADMIN_NAME , ADMIN_SUDO = STEP_SPLIT[5:]
                            if CHECK_STEP.startswith("admins | selected change password") :
                                TEXT = DEF_CHANGE_PASSWORD(MESSAGE_CHATID , ADMIN_NAME , ADMIN_SUDO , MESSAGE_TEXT)
                                await client.send_message(chat_id=MESSAGE_CHATID , text=TEXT , reply_markup=KEYBOARD_HOME , parse_mode=enums.ParseMode.HTML)
                                UPDATE_STEP = DEF_UPDATE_STEP(MESSAGE_CHATID,"None")

                            elif CHECK_STEP.startswith("admins | selected change sudo") :
                                if MESSAGE_TEXT == "✅ YES , sure!" :
                                    TEXT = DEF_CHANGE_SUDO(MESSAGE_CHATID,ADMIN_NAME,ADMIN_SUDO,MESSAGE_TEXT)
                                    await client.send_message(chat_id=MESSAGE_CHATID , text=TEXT , reply_markup=KEYBOARD_HOME , parse_mode=enums.ParseMode.HTML)
                                    UPDATE_STEP = DEF_UPDATE_STEP(MESSAGE_CHATID,"None")
                            
                            elif CHECK_STEP.startswith("admins | selected delete this") :
                                if MESSAGE_TEXT == "✅ YES , sure!" :
                                    TEXT = DEF_DELETE_ADMIN(MESSAGE_CHATID,ADMIN_NAME)
                                    await client.send_message(chat_id=MESSAGE_CHATID , text=TEXT , reply_markup=KEYBOARD_HOME , parse_mode=enums.ParseMode.HTML)
                                    UPDATE_STEP = DEF_UPDATE_STEP(MESSAGE_CHATID,"None")
                    
                    elif CHECK_STEP.startswith("admins | add admin") :
                        
                        if len(STEP_SPLIT) == 4 :
                            await client.send_message(chat_id=MESSAGE_CHATID , text="<b>Please enter new admin password :</b>" , reply_markup=KEYBOARD_CANCEL , parse_mode=enums.ParseMode.HTML)
                            UPDATE_STEP = DEF_UPDATE_STEP(MESSAGE_CHATID,f"admins | add admin {MESSAGE_TEXT}")
                        
                        elif len(STEP_SPLIT) == 5 :
                            ADMIN_NAME = STEP_SPLIT[4] 
                            await client.send_message(chat_id=MESSAGE_CHATID , text="<b>Please select admin is sudo or not?</b>" , reply_markup=KEYBOARD_SUDO , parse_mode=enums.ParseMode.HTML)
                            UPDATE_STEP = DEF_UPDATE_STEP(MESSAGE_CHATID,f"admins | add admin {ADMIN_NAME} {MESSAGE_TEXT}")

                        elif len(STEP_SPLIT) == 6 :
                            ADMIN_NAME = STEP_SPLIT[4] 
                            ADMIN_PASS = STEP_SPLIT[5]
                            ADMIN_SUDO = MESSAGE_TEXT == "✅ YES , is sudo!"
                            TEXT = DEF_ADD_ADMIN(MESSAGE_CHATID,ADMIN_NAME,ADMIN_PASS,ADMIN_SUDO)
                            await client.send_message(chat_id=MESSAGE_CHATID , text=TEXT , reply_markup=KEYBOARD_HOME , parse_mode=enums.ParseMode.HTML)
                            UPDATE_STEP = DEF_UPDATE_STEP(MESSAGE_CHATID,"None")
                

            elif CHECK_STEP.startswith("users") :

                if CHECK_STEP == "users | wait to select list" :
                
                    if MESSAGE_TEXT in ["✅ Active list" , "❌ Disabled list" , "🕰 Expired" , "🪫 Limited" , "🔌 On Hold"] :
                        WAIT_MESSGAE = await client.send_message(chat_id=MESSAGE_CHATID, text=f"<b>⏳️ in progress...</b>" , reply_markup=ReplyKeyboardRemove())
                        USERS_LIST = DEF_USERS_LIST_STATUS(MESSAGE_TEXT , MESSAGE_CHATID)
                
                        if not USERS_LIST :
                            await client.send_message(chat_id=MESSAGE_CHATID , text="<b>❌ I not find any user.</b>" , reply_markup=KEYBOARD_USERS)
                            await WAIT_MESSGAE.delete()
                            return
                
                        else :
                            PDF_NAME = DEF_CREATE_PDF(USERS_LIST)
                            await client.send_document(chat_id=MESSAGE_CHATID , document=PDF_NAME ,caption=f"<b>List of {len(USERS_LIST)} users</b>" ,file_name=f"holderbot.pdf" , reply_markup=KEYBOARD_USERS)
                            await WAIT_MESSGAE.delete()
                            if os.path.exists(PDF_NAME):
                                os.remove(PDF_NAME)   
                
                    elif MESSAGE_TEXT in [ "👀 Online time list" , "📡 Sub Update list"] :
                        await client.send_message(chat_id=MESSAGE_CHATID , text="<b>Please select time.</b>" , reply_markup=KEYBOARD_LIST_TIMES)
                        CATAGORY = {"📡 Sub Update list": "sub_updated_at", "👀 Online time list": "online_at"}.get(MESSAGE_TEXT)
                        UPDATE_STEP = DEF_UPDATE_STEP(MESSAGE_CHATID, f"users | wait to time {CATAGORY}")                
                
                else :

                    if CHECK_STEP.startswith("users | wait to time") :
                        

                        if re.match(r'^\d+\s(min|hour|day)$' , MESSAGE_TEXT) :
                            TIME = DEF_CONVERT_TO_SECEND(MESSAGE_TEXT)
                            CATAGORY = STEP_SPLIT[5]
                            WAIT_MESSGAE = await client.send_message(chat_id=MESSAGE_CHATID, text=f"<b>⏳️ in progress...</b>" , reply_markup=ReplyKeyboardRemove())
                            USERS_LIST_BACK ,  NOT_USER_LIST = DEF_USERS_TIME_LIST(MESSAGE_CHATID , CATAGORY , TIME)
                            
                            if not USERS_LIST_BACK :
                                await client.send_message(chat_id=MESSAGE_CHATID , text="<b>❌ I not find any user.</b>" , reply_markup=KEYBOARD_LIST_TIMES)
                            else :
                                USERS_LIST_BACK_PDF = DEF_CREATE_PDF(USERS_LIST_BACK)
                                await client.send_document(chat_id=MESSAGE_CHATID , document=USERS_LIST_BACK_PDF ,caption=f"<b>List of {len(USERS_LIST_BACK)} users</b>" ,file_name=f"holderbot.pdf" , reply_markup=KEYBOARD_LIST_TIMES)
                                if os.path.exists(USERS_LIST_BACK_PDF):
                                    os.remove(USERS_LIST_BACK_PDF)
                            
                            if not NOT_USER_LIST :
                                await client.send_message(chat_id=MESSAGE_CHATID , text="<b>❌ I not find any user.</b>" , reply_markup=KEYBOARD_LIST_TIMES)
                            else :
                                NOT_IN_LIST_PDF = DEF_CREATE_PDF(NOT_USER_LIST)
                                await client.send_document(chat_id=MESSAGE_CHATID , document=NOT_IN_LIST_PDF ,caption=f"<b>other List of {len(NOT_USER_LIST)} users</b>" ,file_name=f"holderbot.pdf" , reply_markup=KEYBOARD_LIST_TIMES)
                                if os.path.exists(NOT_IN_LIST_PDF):
                                    os.remove(NOT_IN_LIST_PDF)
                            
                            await WAIT_MESSGAE.delete()


            elif CHECK_STEP.startswith("nodes") :

                if CHECK_STEP == "nodes | wait to select node" :
                    
                    if re.match('\(\s*(\d+)\s*\)\s*([^-]+)\s*-\s*([^-]+)', MESSAGE_TEXT) :
                        await client.send_message(chat_id=MESSAGE_CHATID , text=f"<b>You have chosen {MESSAGES_SPLIT[3]} server.\nwhat operation do you need?</b>" , reply_markup=KEYBOARD_NODE)
                        UPDATE_STEP = DEF_UPDATE_STEP(MESSAGE_CHATID,f"nodes | select node {MESSAGES_SPLIT[1]}")

                else :

                    if CHECK_STEP.startswith("nodes | select node") :
                        NODE_ID = int(STEP_SPLIT[4])

                        if MESSAGE_TEXT == "🔏 Usage Coefficient" :
                            TEXT = "<b>Plase enter a float(0.0) number.\nlike this :</b> <code>0.4</code> , <code>1.2</code> , <code>3.5</code> , <code>8.0</code>"
                            await client.send_message(chat_id=MESSAGE_CHATID , text=TEXT , reply_markup=KEYBOARD_CANCEL , parse_mode=enums.ParseMode.HTML)
                            UPDATE_STEP = DEF_UPDATE_STEP(MESSAGE_CHATID,f"nodes | Usage Coefficient {NODE_ID}")
                            
                        else :

                            if MESSAGE_TEXT == "📊 Status" :
                                TEXT = DEF_STASE_NODE(MESSAGE_CHATID , NODE_ID)
                            elif MESSAGE_TEXT == "✅ Activate" :
                                TEXT = DEF_ACTIVE_NODE(MESSAGE_CHATID , NODE_ID)
                            elif MESSAGE_TEXT == "⚡️ Reconnect" :
                                TEXT = DEF_RECONNECT_NODE(MESSAGE_CHATID , NODE_ID)
                            elif MESSAGE_TEXT == "❌ Disable" :
                                TEXT = DEF_DISABLED_NODE(MESSAGE_CHATID , NODE_ID)

                            await client.send_message(chat_id=MESSAGE_CHATID , text=TEXT , reply_markup=KEYBOARD_NODE , parse_mode=enums.ParseMode.HTML)

                    else :

                        if CHECK_STEP.startswith("nodes | Usage Coefficient") :
                            NODE_ID = int(STEP_SPLIT[4])
                            
                            if len(MESSAGES_SPLIT) == 1 and re.match(r'^-?\d+\.\d+$', MESSAGE_TEXT) :
                                TEXT = DEF_USAGE_COEFFICIENT(float(MESSAGE_TEXT) , MESSAGE_CHATID , NODE_ID)
                                await client.send_message(chat_id=MESSAGE_CHATID , text=TEXT , reply_markup=KEYBOARD_NODE , parse_mode=enums.ParseMode.HTML)
                                UPDATE_STEP = DEF_UPDATE_STEP(MESSAGE_CHATID,f"nodes | select node {NODE_ID}")


            elif CHECK_STEP.startswith("monitoring") :

                if CHECK_STEP == "monitoring | wait to select command" :

                    if MESSAGE_TEXT == "🔴 Disable monitoring" :
                        CHANGE = DEF_CHANGE_NODE_STATUS(MESSAGE_CHATID,"off")
                        await client.send_message(chat_id=MESSAGE_CHATID , text="<b>✅ Your Monitoring is disabled.</b>" , reply_markup=KEYBOARD_OFF_MONITORING , parse_mode=enums.ParseMode.HTML , disable_web_page_preview=True )

                    elif MESSAGE_TEXT == "🟢 Monitoring activation" :
                        CHANGE = DEF_CHANGE_NODE_STATUS(MESSAGE_CHATID,"on")
                        await client.send_message(chat_id=MESSAGE_CHATID , text="<b>✅ Your Monitoring is activated.</b>" , reply_markup=KEYBOARD_ON_MONITORING , parse_mode=enums.ParseMode.HTML , disable_web_page_preview=True )
                    
                    elif MESSAGE_TEXT == "⏱ Normal timer" :
                        await client.send_message(chat_id=MESSAGE_CHATID , text="<b>Enter the time you want in seconds.</b>" , reply_markup=KEYBOARD_CANCEL , parse_mode=enums.ParseMode.HTML , disable_web_page_preview=True )
                        UPDATE_STEP = DEF_UPDATE_STEP(MESSAGE_CHATID,"monitoring | timer check_normal")

                    elif MESSAGE_TEXT == "⏱ Error timer" :
                        await client.send_message(chat_id=MESSAGE_CHATID , text="<b>Enter the time you want in seconds.</b>" , reply_markup=KEYBOARD_CANCEL , parse_mode=enums.ParseMode.HTML , disable_web_page_preview=True )
                        UPDATE_STEP = DEF_UPDATE_STEP(MESSAGE_CHATID,"monitoring | timer check_error")
                
                else :

                    if CHECK_STEP.startswith("monitoring | timer") :
                        DB_ROW = STEP_SPLIT[3]
                        if len(MESSAGES_SPLIT) == 1 and MESSAGE_TEXT.isnumeric() :
                            CHANGE = DEF_NODE_STATUS(MESSAGE_CHATID , DB_ROW , MESSAGE_TEXT)
                            await client.send_message(chat_id=MESSAGE_CHATID , text=f"<b>✅ Your {DB_ROW} timer is changed.</b>" , reply_markup=KEYBOARD_ON_MONITORING , parse_mode=enums.ParseMode.HTML , disable_web_page_preview=True )
                            UPDATE_STEP = DEF_UPDATE_STEP(MESSAGE_CHATID,"monitoring | wait to select command")
                

            elif CHECK_STEP.startswith("templates") :

                if CHECK_STEP == "templates | wait to select command" :

                    if re.match(r'(\w+) - ([0-9.]+) GB (\d+) days' , MESSAGE_TEXT) :
                        await client.send_message(chat_id=MESSAGE_CHATID , text=f"<b>You want delete {MESSAGES_SPLIT[0]} template?</b>" , reply_markup=KEYBOARD_YES_OR_NOO , parse_mode=enums.ParseMode.HTML)
                        UPDATE_STEP = DEF_UPDATE_STEP(MESSAGE_CHATID,f"templates | delete {MESSAGES_SPLIT[0]}")

                    elif MESSAGE_TEXT == "➕ Add new tempalte" :
                        await client.send_message(chat_id=MESSAGE_CHATID , text="<b>Please enter template name.\n(just text , no space no number no icon!)\nlike :</b> <code>Test</code> ,<code>Ali</code>, <code>Bulk</code>, <code>Free</code>" , reply_markup=KEYBOARD_CANCEL , parse_mode=enums.ParseMode.HTML)
                        UPDATE_STEP = DEF_UPDATE_STEP(MESSAGE_CHATID,f"templates | add template")

                else :

                    if CHECK_STEP.startswith("templates | delete") :
                        TEMPLATE_NAME = STEP_SPLIT[3]
                        if MESSAGE_TEXT == "✅ YES , sure!" :
                            CHANGE = DEF_TEMPLATES_DELETE(TEMPLATE_NAME)
                            await client.send_message(chat_id=MESSAGE_CHATID , text="<b>✅ Your template is deleted.</b>" , reply_markup=KEYBOARD_HOME , parse_mode=enums.ParseMode.HTML)
                            UPDATE_STEP = DEF_UPDATE_STEP(MESSAGE_CHATID,"None")

                    else :

                        if CHECK_STEP.startswith("templates | add template") :
                            print(STEP_SPLIT)
                            if len(STEP_SPLIT) == 4 and len(MESSAGES_SPLIT) == 1 and re.match("^[A-Za-z]+$" , MESSAGE_TEXT) :
                                if DEF_CHECK_TEMPLATES_NAME(MESSAGE_TEXT) :
                                    return
                                await client.send_message(chat_id=MESSAGE_CHATID , text="<b>Please enter data limit (GB).\nlike : <code>25.5</code>, <code>15</code>, <code>0.5</code>, <code>100</code></b>" , reply_markup=KEYBOARD_CANCEL , parse_mode=enums.ParseMode.HTML)
                                UPDATE_STEP = DEF_UPDATE_STEP(MESSAGE_CHATID,f"templates | add template {MESSAGE_TEXT}")
                            
                            elif len(STEP_SPLIT) == 5 and len(MESSAGES_SPLIT) == 1 and re.match("^\d*\.?\d+$" , MESSAGE_TEXT) :
                                TEMPLATE_NAME = STEP_SPLIT[4]
                                await client.send_message(chat_id=MESSAGE_CHATID , text="<b>Please enter date limit (days).\nLike : <code>1</code>, <code>15</code>, <code>75</code>, <code>150</code></b>" , reply_markup=KEYBOARD_CANCEL , parse_mode=enums.ParseMode.HTML)
                                UPDATE_STEP = DEF_UPDATE_STEP(MESSAGE_CHATID,f"templates | add template {TEMPLATE_NAME} {float(MESSAGE_TEXT)}")

                            elif len(STEP_SPLIT) == 6 and len(MESSAGES_SPLIT) == 1 and MESSAGE_TEXT.isnumeric() :
                                TEMPLATE_NAME , TEMPLATE_DATA = STEP_SPLIT[4:]
                                global INBOUNDS_ALL , INBOUNDS_SELECT
                                INBOUNDS , INBOUNDS_ALL ,INBOUNDS_SELECT = DEF_GET_INBOUNDS(MESSAGE_CHATID)
                                KEYBOARD_INBOUNDS = KEYBOARD_ALL_INBOUNDS(INBOUNDS_ALL , INBOUNDS_SELECT , None , "templates")
                                await client.send_message(chat_id=MESSAGE_CHATID , text=f"<b>Please select inbounds :</b>" , reply_markup=KEYBOARD_INBOUNDS , parse_mode=enums.ParseMode.HTML)
                                UPDATE_STEP = DEF_UPDATE_STEP(MESSAGE_CHATID,f"templates | add template {TEMPLATE_NAME} {TEMPLATE_DATA} {MESSAGE_TEXT}")


            elif CHECK_STEP.startswith("create") :

                if CHECK_STEP == "create | wait to select command" :

                    if MESSAGE_TEXT == "🚀 Manual" :
                        await client.send_message(chat_id=MESSAGE_CHATID , text="<b>Please enter username :</b>" , reply_markup=KEYBOARD_CANCEL , parse_mode=enums.ParseMode.HTML)
                        UPDATE_STEP = DEF_UPDATE_STEP(MESSAGE_CHATID,f"create | manual")

                    elif re.match(r'(\w+) - ([0-9.]+) GB (\d+) days' , MESSAGE_TEXT) :
                        TEMPLATE_NAME = MESSAGES_SPLIT[0]
                        await client.send_message(chat_id=MESSAGE_CHATID , text="<b>Please enter username :</b>" , reply_markup=KEYBOARD_CANCEL , parse_mode=enums.ParseMode.HTML)
                        UPDATE_STEP = DEF_UPDATE_STEP(MESSAGE_CHATID,f"create | select {TEMPLATE_NAME}")
                    
                else :

                    if CHECK_STEP.startswith("create | select") :
                        TEMPLATE_NAME = STEP_SPLIT[3]
                        
                        if len(MESSAGES_SPLIT) == 1 and len(STEP_SPLIT) == 4 :
                            await client.send_message(chat_id=MESSAGE_CHATID , text="<b>how many do you want?</b>" , reply_markup=KEYBOARD_CREATE_MUCH , parse_mode=enums.ParseMode.HTML)
                            UPDATE_STEP = DEF_UPDATE_STEP(MESSAGE_CHATID,f"create | select {TEMPLATE_NAME} {MESSAGE_TEXT}")
                        
                        elif len(MESSAGES_SPLIT) == 1 and len(STEP_SPLIT) == 5 and MESSAGE_TEXT.isnumeric() :
                            USERNAME = STEP_SPLIT[4]
                            NAME , DATA , DATE , PROXIES , INBOUNDS = DEF_TEMPLATES_DATA_ALL(TEMPLATE_NAME)
                            if int(MESSAGE_TEXT) == 1 :
                                USER_SUB = DEF_CREATE_USER(MESSAGE_CHATID , USERNAME , DATA , DATE , json.loads(PROXIES) , json.loads(INBOUNDS))
                                if not "❌" in USER_SUB :
                                    QRCODE_IMG = DEF_CREATE_QRCODE(USER_SUB)
                                    #await client.send_photo(chat_id=MESSAGE_CHATID , photo=QRCODE_IMG,caption=f"<pre>{USER_SUB}</pre>" , reply_markup=KEYBOARD_HOME)
                                    usrnm = USERNAME.replace('user', '')
                                    await client.send_photo(
                                                                chat_id=MESSAGE_CHATID, 
                                                                photo=QRCODE_IMG,
                                                                caption=f"<b>⚜️ کاربر {usrnm}</b>\n\n"
                                                                        f"🔗 روی لینک زیر کلیک کنید تا کپی شود:\n"
                                                                        f"`{USER_SUB}`\n\n"
                                                                        f"❇️ <a href='{USER_SUB}'>برای آموزش چگونگی اتصال و مشاهده باقیمانده اشتراک خود بر روی این متن کلیک کنید‌.</a>"
                                                            )
                                    #await client.send_message(chat_id=MESSAGE_CHATID , text=f"<b>✅ <code>{USERNAME}</code> | {DATA} GB | {DATE} Days</b>" , reply_markup=KEYBOARD_HOME , parse_mode=enums.ParseMode.HTML)
                                    UPDATE_STEP = DEF_UPDATE_STEP(MESSAGE_CHATID,"None")
                                else :
                                    await client.send_message(chat_id=MESSAGE_CHATID , text=USER_SUB , reply_markup=KEYBOARD_HOME , parse_mode=enums.ParseMode.HTML)
                                    UPDATE_STEP = DEF_UPDATE_STEP(MESSAGE_CHATID,"None")
                            else :
                                USERNAMES = DEF_USERNAME_STARTER(USERNAME , int(MESSAGE_TEXT))
                                for USERNAME in USERNAMES :
                                    USER_SUB = DEF_CREATE_USER(MESSAGE_CHATID , USERNAME , DATA , DATE , json.loads(PROXIES) , json.loads(INBOUNDS))
                                    if not "❌" in USER_SUB :
                                        QRCODE_IMG = DEF_CREATE_QRCODE(USER_SUB)
                                        #await client.send_photo(chat_id=MESSAGE_CHATID , photo=QRCODE_IMG,caption=f"<pre>{USER_SUB}</pre>" , reply_markup=ReplyKeyboardRemove())
                                        usrnm = USERNAME.replace('user', '')
                                        await client.send_photo(
                                                                    chat_id=MESSAGE_CHATID, 
                                                                    photo=QRCODE_IMG,
                                                                    caption=f"<b>⚜️ کاربر {usrnm}</b>\n\n"
                                                                            f"🔗 روی لینک زیر کلیک کنید تا کپی شود:\n"
                                                                            f"`{USER_SUB}`\n\n"
                                                                            f"❇️ <a href='{USER_SUB}'>برای آموزش چگونگی اتصال و مشاهده باقیمانده اشتراک خود بر روی این متن کلیک کنید‌.</a>"
                                                                )
                                        #await client.send_message(chat_id=MESSAGE_CHATID , text=f"<b>✅ <code>{USERNAME}</code> | {DATA} GB | {DATE} Days</b>" , reply_markup=ReplyKeyboardRemove() , parse_mode=enums.ParseMode.HTML)
                                    else :
                                        await client.send_message(chat_id=MESSAGE_CHATID , text=USER_SUB , reply_markup=KEYBOARD_HOME , parse_mode=enums.ParseMode.HTML)
                                        UPDATE_STEP = DEF_UPDATE_STEP(MESSAGE_CHATID,"None")
                                        break
                                await client.send_message(chat_id=MESSAGE_CHATID , text=f"🏛" , reply_markup=KEYBOARD_HOME , parse_mode=enums.ParseMode.HTML)
                                UPDATE_STEP = DEF_UPDATE_STEP(MESSAGE_CHATID,"None")

                    else :

                        if CHECK_STEP.startswith("create | manual") :

                            if len(MESSAGES_SPLIT) == 1 and len(STEP_SPLIT) == 3 and len(MESSAGE_TEXT) > 2 :
                                await client.send_message(chat_id=MESSAGE_CHATID , text="<b>Please enter data limit (GB).\nlike : <code>25.5</code>, <code>15</code>, <code>0.5</code>, <code>100</code></b></b>" , reply_markup=KEYBOARD_CANCEL , parse_mode=enums.ParseMode.HTML)
                                UPDATE_STEP = DEF_UPDATE_STEP(MESSAGE_CHATID,f"create | manual {MESSAGE_TEXT}")

                            elif len(MESSAGES_SPLIT) == 1 and len(STEP_SPLIT) == 4 and re.match("^\d*\.?\d+$" , MESSAGE_TEXT) :
                                USERNAME = STEP_SPLIT[3]
                                await client.send_message(chat_id=MESSAGE_CHATID , text="<b>Please enter date limit (days).\nLike : <code>1</code>, <code>15</code>, <code>75</code>, <code>150</code></b>" , reply_markup=KEYBOARD_CANCEL , parse_mode=enums.ParseMode.HTML)
                                UPDATE_STEP = DEF_UPDATE_STEP(MESSAGE_CHATID,f"create | manual {USERNAME} {MESSAGE_TEXT}")
                            
                            elif len(MESSAGES_SPLIT) == 1 and len(STEP_SPLIT) == 5 and MESSAGE_TEXT.isnumeric() :
                                USERNAME , DATA_LIMIT = STEP_SPLIT[3:]
                                await client.send_message(chat_id=MESSAGE_CHATID , text="<b>how many do you want?</b>" , reply_markup=KEYBOARD_CANCEL , parse_mode=enums.ParseMode.HTML)
                                UPDATE_STEP = DEF_UPDATE_STEP(MESSAGE_CHATID,f"create | manual {USERNAME} {DATA_LIMIT} {MESSAGE_TEXT}")

                            elif len(MESSAGES_SPLIT) == 1 and len(STEP_SPLIT) == 6 and MESSAGE_TEXT.isnumeric() :
                                USERNAME , DATA_LIMIT , DATE_LIMIT = STEP_SPLIT[3:]
                                global INBOUNDS__ALL , INBOUNDS__SELECT
                                INBOUNDS , INBOUNDS__ALL ,INBOUNDS__SELECT = DEF_GET_INBOUNDS(MESSAGE_CHATID)
                                KEYBOARD_INBOUNDS = KEYBOARD_ALL_INBOUNDS(INBOUNDS__ALL , INBOUNDS__SELECT , None , "create")
                                await client.send_message(chat_id=MESSAGE_CHATID , text=f"<b>Please select inbounds :</b>" , reply_markup=KEYBOARD_INBOUNDS,  parse_mode=enums.ParseMode.HTML)
                                UPDATE_STEP = DEF_UPDATE_STEP(MESSAGE_CHATID,f"create | manual {USERNAME} {DATA_LIMIT} {DATE_LIMIT} {MESSAGE_TEXT}")


            elif CHECK_STEP.startswith("message") :
                
                if CHECK_STEP == "message | wait to select command" :
                    if MESSAGE_TEXT == "👀 change status" :
                        await client.send_message(chat_id=MESSAGE_CHATID , text=DEF_CHANGE_MESSAGER_STATUS(MESSAGE_CHATID) , reply_markup=KEYBOARD_HOME , parse_mode=enums.ParseMode.HTML , disable_web_page_preview=True )
                        UPDATE_STEP = DEF_UPDATE_STEP(MESSAGE_CHATID,"None")

@app.on_callback_query(filters.regex(r'^templates'))
async def handle_callback_create(client: Client, query: CallbackQuery ):
    
    MESSAGE_CHATID = query.message.chat.id
    CALLBACK_DATA = query.data
    CHECK_STEP = DEF_CHECK_STEP(MESSAGE_CHATID)
    STEP_SPLIT = CHECK_STEP.strip().split(" ")
    global INBOUNDS_ALL , INBOUNDS_SELECT
        
    if CALLBACK_DATA.startswith("templates tag") :

        SELECTED_TAG = CALLBACK_DATA[14:]
        KEYBOARD_INBOUNDS = KEYBOARD_ALL_INBOUNDS(INBOUNDS_ALL, INBOUNDS_SELECT, SELECTED_TAG , "templates")
        await query.edit_message_text(text="<b>Please select inbounds :</b>" , reply_markup=KEYBOARD_INBOUNDS , parse_mode=enums.ParseMode.HTML)

    elif CALLBACK_DATA == "templates yes" :

        INBOUNDS , PUCH1 , PUCH2  = DEF_GET_INBOUNDS(MESSAGE_CHATID)
        INBOUND_FINAL , PROXIES_FINAL = DEF_SELECT_INBOUNDS_AND_PROXIES(INBOUNDS , INBOUNDS_SELECT)
        TEMPLATE_NAME , TEMPLATE_DATA , TEMPLATE_DATE = STEP_SPLIT[4:]
        CHANGE = DEF_TEMPLATES_ADD(TEMPLATE_NAME, TEMPLATE_DATA, TEMPLATE_DATE, PROXIES_FINAL, INBOUND_FINAL)
        await query.message.delete()
        await client.send_message(chat_id=MESSAGE_CHATID , text=f"<b>✅ Template is added.</b>" , reply_markup=KEYBOARD_HOME)
        UPDATE_STEP = DEF_UPDATE_STEP(MESSAGE_CHATID,"None")

    elif CALLBACK_DATA == "templates no" :

        await query.message.delete()
        await client.send_message(chat_id=MESSAGE_CHATID , text=f"🏛" , reply_markup=KEYBOARD_HOME)
        UPDATE_STEP = DEF_UPDATE_STEP(MESSAGE_CHATID,"None")


@app.on_callback_query(filters.regex(r'^create'))
async def handle_callback_create(client: Client, query: CallbackQuery ):
    
    MESSAGE_CHATID = query.message.chat.id
    CALLBACK_DATA = query.data
    CHECK_STEP = DEF_CHECK_STEP(MESSAGE_CHATID)
    STEP_SPLIT = CHECK_STEP.strip().split(" ")
    global INBOUNDS__ALL , INBOUNDS__SELECT
        
    if CALLBACK_DATA.startswith("create tag") :

        SELECTED_TAG = CALLBACK_DATA[11:]
        KEYBOARD_INBOUNDS = KEYBOARD_ALL_INBOUNDS(INBOUNDS__ALL, INBOUNDS__SELECT, SELECTED_TAG , "create")
        await query.edit_message_text(text="<b>Please select inbounds :</b>" , reply_markup=KEYBOARD_INBOUNDS , parse_mode=enums.ParseMode.HTML)

    elif CALLBACK_DATA == "create yes" :

        INBOUNDS , PUCH1 , PUCH2  = DEF_GET_INBOUNDS(MESSAGE_CHATID)
        INBOUND_FINAL , PROXIES_FINAL = DEF_SELECT_INBOUNDS_AND_PROXIES(INBOUNDS , INBOUNDS__SELECT)
        USERNAME , DATA_LIMIT , DATE_LIMIT , HOW_MANY = STEP_SPLIT[3:]
        if int(HOW_MANY) == 1 :
            USER_SUB = DEF_CREATE_USER(MESSAGE_CHATID , USERNAME , DATA_LIMIT , DATE_LIMIT , PROXIES_FINAL , INBOUND_FINAL)
            await query.message.delete()
            if not "❌" in USER_SUB :
                QRCODE_IMG = DEF_CREATE_QRCODE(USER_SUB)
            usrnm = USERNAME.replace('user', '')
            await client.send_photo(
                                        chat_id=MESSAGE_CHATID, 
                                        photo=QRCODE_IMG,
                                        caption=f"<b>⚜️ کاربر {usrnm}</b>\n\n"
                                                f"🔗 روی لینک زیر کلیک کنید تا کپی شود:\n"
                                                f"`{USER_SUB}`\n\n"
                                                f"❇️ <a href='{USER_SUB}'>برای آموزش چگونگی اتصال و مشاهده باقیمانده اشتراک خود بر روی این متن کلیک کنید‌.</a>"
                                    )
                #await client.send_photo(chat_id=MESSAGE_CHATID , photo=QRCODE_IMG,caption=f"<pre>{USER_SUB}</pre>\n\n" , reply_markup=KEYBOARD_HOME)
                #await client.send_message(chat_id=MESSAGE_CHATID , text=f"<b>✅ <code>{USERNAME}</code> | {DATA_LIMIT} GB | {DATE_LIMIT} Days</b>" , reply_markup=KEYBOARD_HOME , parse_mode=enums.ParseMode.HTML)
                UPDATE_STEP = DEF_UPDATE_STEP(MESSAGE_CHATID,"None")
            else :
                await client.send_message(chat_id=MESSAGE_CHATID , text=USER_SUB , reply_markup=KEYBOARD_HOME , parse_mode=enums.ParseMode.HTML)
                UPDATE_STEP = DEF_UPDATE_STEP(MESSAGE_CHATID,"None")
        else :
            USERNAMES = DEF_USERNAME_STARTER(USERNAME , int(HOW_MANY))
            for USERNAME in USERNAMES :
                USER_SUB = DEF_CREATE_USER(MESSAGE_CHATID , USERNAME , DATA_LIMIT , DATE_LIMIT , PROXIES_FINAL , INBOUND_FINAL)
                if not "❌" in USER_SUB :
                    QRCODE_IMG = DEF_CREATE_QRCODE(USER_SUB)
            usrnm = USERNAME.replace('user', '')
            await client.send_photo(
                                        chat_id=MESSAGE_CHATID, 
                                        photo=QRCODE_IMG,
                                        caption=f"<b>⚜️ کاربر {usrnm}</b>\n\n"
                                                f"🔗 روی لینک زیر کلیک کنید تا کپی شود:\n"
                                                f"`{USER_SUB}`\n\n"
                                                f"❇️ <a href='{USER_SUB}'>برای آموزش چگونگی اتصال و مشاهده باقیمانده اشتراک خود بر روی این متن کلیک کنید‌.</a>"
                                    )
                    #await client.send_photo(chat_id=MESSAGE_CHATID , photo=QRCODE_IMG,caption=f"<pre>{USER_SUB}</pre>" , reply_markup=ReplyKeyboardRemove())
                    #await client.send_message(chat_id=MESSAGE_CHATID , text=f"<b>✅ <code>{USERNAME}</code> | {DATA_LIMIT} GB | {DATE_LIMIT} Days</b>" , reply_markup=KEYBOARD_HOME , parse_mode=enums.ParseMode.HTML)
                else :
                    await client.send_message(chat_id=MESSAGE_CHATID , text=USER_SUB , reply_markup=KEYBOARD_HOME , parse_mode=enums.ParseMode.HTML)
                    UPDATE_STEP = DEF_UPDATE_STEP(MESSAGE_CHATID,"None")
                    break
            await client.send_message(chat_id=MESSAGE_CHATID , text=f"🏛" , reply_markup=KEYBOARD_HOME , parse_mode=enums.ParseMode.HTML)
           UPDATE_STEP = DEF_UPDATE_STEP(MESSAGE_CHATID,"None")

    elif CALLBACK_DATA == "create no" :

        await query.message.delete()
        await client.send_message(chat_id=MESSAGE_CHATID , text=f"🏛" , reply_markup=KEYBOARD_HOME)
        UPDATE_STEP = DEF_UPDATE_STEP(MESSAGE_CHATID,"None")


@app.on_callback_query(filters.regex(r'^user info'))
async def handle_callback_user_info(client: Client, query: CallbackQuery):
    CHECK_BOSS = DEF_CHECK_BOSS(query.from_user.id)
    if CHECK_BOSS :
        CALLBACK_DATA = query.data
        PANEL_USER, PANEL_PASS, PANEL_DOMAIN = DEF_IMPORT_DATA (query.from_user.id)
        PANEL_TOKEN = DEF_PANEL_ACCESS(PANEL_USER, PANEL_PASS, PANEL_DOMAIN)
        MESSAGES_SPLIT = CALLBACK_DATA.strip().split(" ")
        CB_USERNAME = MESSAGES_SPLIT[3]
        if CALLBACK_DATA.startswith("user info QRCODE") :
            URL = f"https://{PANEL_DOMAIN}/api/user/{CB_USERNAME}"
            RESPONCE = requests.get(url=URL , headers=PANEL_TOKEN)
            if RESPONCE.status_code == 200 :
                RESPONCE_DATA = json.loads(RESPONCE.text)
            else :
                await query.answer(text=f"<b>❌ I can'n find user.</b>")
                return
            RD_SUB_URL = RESPONCE_DATA.get("subscription_url")
            QRCODE_IMG = DEF_CREATE_QRCODE(RD_SUB_URL)
            #await client.send_photo(chat_id=query.from_user.id, photo=QRCODE_IMG,caption=f"<pre>{RD_SUB_URL}</pre>")
            usrnm = CB_USERNAME.replace('user', '')
            await client.send_photo(
                                        chat_id=query.from_user.id, 
                                        photo=QRCODE_IMG,
                                        caption=f"<b>⚜️ کاربر {usrnm}</b>\n\n"
                                                f"🔗 روی لینک زیر کلیک کنید تا کپی شود:\n"
                                                f"`{RD_SUB_URL}`\n\n"
                                                f"❇️ <a href='{RD_SUB_URL}'>برای آموزش چگونگی اتصال و مشاهده باقیمانده اشتراک خود بر روی این متن کلیک کنید‌.</a>"
                                    )

        elif CALLBACK_DATA.startswith("user info edit_data_limit"):
            #CB_USERNAME = CALLBACK_DATA.split()[1]
            user_session[query.from_user.id] = {'edit_field': 'data_limit', 'username': CB_USERNAME}
            await query.message.reply_text("Please enter the new data limit in GB:")
    
        # Handler to initiate edit process for expire duration
        elif CALLBACK_DATA.startswith("user info edit_expire_duration"):
            user_session[query.from_user.id] = {'edit_field': 'expire_duration', 'username': CB_USERNAME}
            await query.message.reply_text("Please enter the new expire duration in days:")
            
        elif CALLBACK_DATA.startswith("user info edit_data_time"):
            user_session[query.from_user.id] = {'edit_field': ['data_limit', 'expire_duration'], 'username': CB_USERNAME}
            await query.message.reply_text("Please enter the new data limit in GB and the new expire duration in day separated in space:")
            
        elif CALLBACK_DATA.startswith("user info UPDATE") or CALLBACK_DATA.startswith("user info NO") :
            try :
                TEXT , KEYBOARD_UPDATE_STASE = DEF_STASE_USER (query.from_user.id , CB_USERNAME , KEYBOARD_HOME)
                await query.edit_message_text(text=TEXT , reply_markup=KEYBOARD_UPDATE_STASE)
                return 
            except MessageNotModified :
                await query.answer("your info is not changed.")
                return
            
        elif CALLBACK_DATA.startswith("user info DELETE") :
            if CALLBACK_DATA.startswith("user info DELETE_SURE") :
                URL = f"https://{PANEL_DOMAIN}/api/user/{CB_USERNAME}"
                RESPONCE = requests.delete(url=URL , headers=PANEL_TOKEN)
                if RESPONCE.status_code == 200 :
                    RESPONCE_DATA = json.loads(RESPONCE.text)
                else :
                    await query.edit_message_text(text=f"<b>❌ I can'n find user.</b>")
                    return
                await query.edit_message_text(text=f"<b>✅ User is deleted.</b>")
            else :
                KEYBOARD_DELETE = InlineKeyboardMarkup([
                    [InlineKeyboardButton("✅ YES", callback_data=f'user info DELETE_SURE {CB_USERNAME}'),
                    InlineKeyboardButton("🚫 NO", callback_data=f'user info NO {CB_USERNAME}')]])                
                await query.edit_message_text(text=f"<b>Are you sure delete <code>{CB_USERNAME}</code> user ?!</b>", reply_markup=KEYBOARD_DELETE)  
        
def update_user_data(chat_id, username, new_data_limit_gb=None, new_expire_duration_days=None):
    # Import necessary data for API access
    panel_user, panel_pass, panel_domain = DEF_IMPORT_DATA(chat_id)
    panel_token = DEF_PANEL_ACCESS(panel_user, panel_pass, panel_domain)
    user_url = f"https://{panel_domain}/api/user/{username}"

    # Fetch current user data
    response = requests.get(url=user_url, headers=panel_token)
    if response.status_code != 200:
        return False, "Failed to fetch user data"
    
    user_data = response.json()
    #print(user_data)
    #print('***********************')
    # Update data limit if provided
    if user_data["status"] in ['disabled', 'limited', 'expired']:
        user_data["status"] = "active"
    if new_data_limit_gb is not None:
        if user_data["data_limit"]==2 * (1024**3):
            user_data["data_limit"] = int(float(new_data_limit_gb) * (1024**3))
        else:
            user_data["data_limit"] = user_data["data_limit"]+int(float(new_data_limit_gb) * (1024**3))
        
        
        

    # Update expire duration if provided
    if new_expire_duration_days is not None:
        #print(user_data["on_hold_expire_duration"],new_expire_duration_days)
        user_data["on_hold_expire_duration"] = int(new_expire_duration_days) * 24 * 60 * 60
        #print(user_data["on_hold_expire_duration"])
        #print('**')
        if user_data["expire"] is not None:
            future_date = datetime.now() + timedelta(days=new_expire_duration_days+1)
            expiryTime = int(future_date.timestamp())
            user_data["expire"] = expiryTime
    
    #print(user_data)
    # Update the user data
    update_response = requests.put(url=user_url, headers=panel_token, json=user_data)

    if update_response.status_code == 200:
        return True
    else:
        return False



app.run()
