from Function.db import *
import requests , re


def DEF_GET_INBOUNDS(CHATID) :
    PANEL_USER, PANEL_PASS, PANEL_DOMAIN = DEF_IMPORT_DATA (CHATID)
    PANEL_TOKEN = DEF_PANEL_ACCESS(PANEL_USER, PANEL_PASS, PANEL_DOMAIN)
    URL = f"https://{PANEL_DOMAIN}/api/inbounds"
    RESPONCE = requests.get(url=URL, headers=PANEL_TOKEN)
    if RESPONCE.status_code == 200:
        RESPONCE_DATA = RESPONCE.json()
        INBOUNDS = json.loads(RESPONCE.text)
        INBOUNDS_ALL = []
        INBOUNDS_SELECT = {}
        for group, ITEMS in RESPONCE_DATA.items():
            for ITEM in ITEMS:
                TAG = ITEM.get('tag')
                if TAG:
                    INBOUNDS_ALL.append(TAG)
                    INBOUNDS_SELECT[TAG] = True       
    else :
        INBOUNDS = {}
        INBOUNDS_ALL = []
        INBOUNDS_SELECT = {}
    return INBOUNDS , INBOUNDS_ALL ,INBOUNDS_SELECT


def DEF_SELECT_INBOUNDS_AND_PROXIES(INBOUNDS , SELECTS) :
    INBOUNDS_ALL = {}
    PROXIES = {}
    for CATAGORY, ITEMS in INBOUNDS.items():
        TAGS = [ITEM['tag'] for ITEM in ITEMS if SELECTS.get(ITEM['tag'], True)]
        if TAGS:
            INBOUNDS_ALL[CATAGORY] = TAGS
            PROXIES[CATAGORY] = {}
    return INBOUNDS_ALL , PROXIES

def DEF_CREATE_USER(CHATID, USERNAME, DATA, DATE, PROXIES, INBOUNDS):
    PANEL_USER, PANEL_PASS, PANEL_DOMAIN = DEF_IMPORT_DATA(CHATID)
    PANEL_TOKEN = DEF_PANEL_ACCESS(PANEL_USER, PANEL_PASS, PANEL_DOMAIN)
    DATA_TO_BYTES = int(float(DATA) * (1024**3))
    DATE_TO_SECOND = int(DATE) * (24*60*60)
    
    # Create user data
    DATA = {
        "username": USERNAME,
        "proxies": PROXIES,
        "inbounds": INBOUNDS,
        "data_limit": DATA_TO_BYTES,
        "data_limit_reset_strategy": "no_reset",
        "status": "on_hold",
        "note": "by holderbot",
        "on_hold_timeout": "2034-11-03T20:30:00",
        "on_hold_expire_duration": DATE_TO_SECOND
    }
    
    # Create user
    URL = f"https://{PANEL_DOMAIN}/api/user"
    POST_DATA = json.dumps(DATA)
    RESPONSE = requests.post(url=URL, headers=PANEL_TOKEN, data=POST_DATA)
    
    if RESPONSE.status_code == 200:
        # After successful creation, set the flow to "xtls-rprx-vision"
        if set_user_flow(PANEL_DOMAIN, PANEL_TOKEN, USERNAME, "xtls-rprx-vision"):
            print(f"Flow set to 'xtls-rprx-vision' for user {USERNAME}")
        else:
            print(f"Failed to set flow for user {USERNAME}")
        
        # Get user details and subscription URL
        URL = f"https://{PANEL_DOMAIN}/api/user/{USERNAME}"
        RESPONSE = requests.get(url=URL, headers=PANEL_TOKEN)
        if RESPONSE.status_code == 200:
            RESPONSE_DATA = json.loads(RESPONSE.text)
            TEXT = RESPONSE_DATA.get("subscription_url")
        else:
            TEXT = f"❌<b> I can't find user.</b>\n<pre>{RESPONSE.text}</pre>"
    else:
        TEXT = f"❌<b> I can't create user {USERNAME}.</b>\n<pre>{RESPONSE.text}</pre>"
    
    return TEXT

def set_user_flow(domain, token, username, flow):
    """Set the flow for a user's vless proxy"""
    url = f'https://{domain}/api/user/{username}'
    
    try:
        # First, get the current user details
        response = requests.get(url, headers=token)
        response.raise_for_status()
        user_details = response.json()
        
        # Check if user has vless proxies
        if 'proxies' in user_details and 'vless' in user_details['proxies']:
            # Set the flow for vless protocol
            user_details['proxies']['vless']['flow'] = flow
            
            # Clear links and subscription_url as shown in your helper code
            user_details['links'] = []
            user_details['subscription_url'] = ""
            
            # Remove empty inbounds as shown in your helper code
            keys_to_remove = []
            for inbound_protocol in user_details.get('inbounds', {}):
                if not user_details['inbounds'][inbound_protocol]:
                    keys_to_remove.append(inbound_protocol)
            
            # Remove empty keys
            for key in keys_to_remove:
                user_details['inbounds'].pop(key, None)
                user_details['proxies'].pop(key, None)
            
            # Update the user with new flow setting
            response = requests.put(url, json=user_details, headers=token)
            response.raise_for_status()
            return True
        else:
            print(f"User {username} does not have vless proxies")
            return False
            
    except requests.exceptions.RequestException as e:
        print(f'Error occurred while setting flow for user {username}: {e}')
        return False


def DEF_USERNAME_STARTER(TEXT, MUCH_NUMBER):
    LETTERS_MATCH = re.sub(r'\d+', '', TEXT)
    DIGIT_MATCH = re.search(r'\d+$', TEXT)
    if DIGIT_MATCH:
        START_NUMBER = int(DIGIT_MATCH.group()) + 1
    else:
        START_NUMBER = 1
    RESULT_LIST = []
    for _ in range(int(MUCH_NUMBER)):
        RESULT_LIST.append(LETTERS_MATCH + str(START_NUMBER))
        START_NUMBER += 1
    return RESULT_LIST
