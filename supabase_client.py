# supabase_client.py
from supabase import create_client
import logging
import os
from datetime import datetime


class SupabaseClient():

    def __init__(self):
        url: str = os.environ.get("SUPABASE_URL")
        key: str = os.environ.get("SUPABASE_KEY")
        self.db = create_client(url, key)


    def insert(self, table_name:str, row:dict):
        try:
            return self.db.table(table_name).insert([row]).execute() 
        except Exception as e:
            logging.exception("Exception occurred")
    
    def fetch(self, table_name):
        try:
          return self.db.table(table_name).select("*").eq("org_id", "improovy").execute() 
        except Exception as e:
            logging.exception("Exception occurred")
    
    def fetch_by_id(self, table_name, id):
        try:
            return self.db.table(table_name).select("*").eq("contactid", id).execute() 
        except Exception as e:
            logging.exception("Exception occurred")
    
    def fetch_by_contact_phone(self, table_name, contact_phone):
        try:
            return self.db.table(table_name).select("*").eq("contact_phone", contact_phone).execute() 
        except Exception as e:
            logging.exception("Exception occurred")
    
    def get_system_prompt(self, table_name, org_id):
        try:
           return self.db.table(table_name).select("*").order("created_at", desc=True).limit(1).eq("org_id", org_id).execute() 
        except Exception as e:
            logging.exception("Exception occurred")
    
    def update(self, table_name:str, row:dict, id:str):
        try:
            return self.db.table(table_name).update([row]).eq("id", id).execute()
        except Exception as e:
            logging.exception("Exception occurred")
    
    def update_by_org_id(self, table_name:str, row:dict, org_id:str):
        try:
            return self.db.table(table_name).update([row]).eq("org_id", org_id).execute()
        except Exception as e:
            logging.exception("Exception occurred")
    
    def delete(self, table_name, id):
        try:
           return self.db.table(table_name).delete().eq("id", id).execute() 
        except Exception as e:
            logging.exception("Exception occurred")
    
    def check_by_contact_phone(self, table_name, contact_phone):
        try:
           return self.db.table(table_name).select("*").eq("contact_phone", contact_phone).eq("org_id", 'improovy').execute() 
        except Exception as e:
            logging.exception("Exception occurred")
    
    def fetch_messages(self, table_name, direction, org_id, contact_phone):
        try:
            return self.db.table(table_name).select("utc_datetime, content, direction").order("utc_datetime", desc=False).eq("direction", direction).eq("org_id", org_id).eq("contact_phone", contact_phone).execute() 
        except Exception as e:
            logging.exception("Exception occurred")

    ##UQ ADDED
    def fetch_all_messages(self, table_name, contactid):
        try:
            return self.db.table(table_name).select("*").order("utc_datetime", desc=False).eq("contactid", contactid).execute() 
        except Exception as e:
            logging.exception("Exception occurred")

    def fetch_all_messages_by_phone_and_org(self, table_name, contact_phone, org_id):
        try:
            return self.db.table(table_name).select("*").order("utc_datetime", desc=False).eq("contact_phone", contact_phone).eq("org_id", org_id).execute().data
        except Exception as e:
            logging.exception("Exception occurred")

    def transform_messages(self, raw_messages):
        ai_messages = []
        for raw_message in raw_messages:
            ai_message = {}
            if raw_message['direction'] == 'outbound':
                ai_message['role'] = 'assistant'
            else:
                ai_message['role'] = 'user'
            ai_message['content'] = raw_message['content']
            ai_messages.append(ai_message)
        return ai_messages

    def get_prompt(self, bot_name):
        try:
           return self.db.table('bots').select("*").eq("id", bot_name).execute() 
        except Exception as e:
            logging.exception("Exception occurred")


    def transform_inbound_justcall_message(self, raw_message, contactid):
        message = {
            'org_id': 'improovy',
            'content': raw_message.get('content', None),
            'channel': 'sms',
            'utc_datetime': raw_message['datetime'],
            'direction': 'inbound' if raw_message['direction'] == 1 else 'outbound',
            'contact_id': contactid,
            'contact_phone': raw_message['contact_number'] if raw_message['contact_number'][0] == '+' else '+' + raw_message['contact_number'],
            'org_phone': str(raw_message['justcall_number']) if str(raw_message['justcall_number'])[0] == '+' else '+' + str(raw_message['justcall_number']),
            'owner': 'mike',
            'contact_email': raw_message.get('contact_email', None)}
        return message
    
    def transform_outbound_justcall_message(self, org_id, content, contactid, contact_phone, org_phone, owner, contact_email, prompt_tokens, completion_tokens):
        message = {
            'org_id': org_id,
            'content': content,
            'channel': 'sms',
            'utc_datetime': datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            'direction': 'outbound',
            'contact_id': contactid,
            'contact_phone': contact_phone,
            'org_phone': org_phone,
            'owner': owner,
            'contact_email': contact_email,
            'prompt_tokens': prompt_tokens,
            'completion_tokens': completion_tokens}
        return message
    
    def update_by_org_id_and_id(self, table_name:str, row:dict, org_id:str, id:str):
        try:
            return self.db.table(table_name).update([row]).eq("org_id", org_id).eq("id",id).execute()
        except Exception as e:
            logging.exception("Exception occurred")

    def update_by_org_id_and_contact_phone(self, table_name:str, row:dict, org_id:str, contact_phone:str):
        try:
            return self.db.table(table_name).update([row]).eq("org_id", org_id).eq("contact_phone",contact_phone).execute()
        except Exception as e:
            logging.exception("Exception occurred")

    def fetch_by_contact_phone_and_orgid(self, table_name, contact_phone, org_id):
        try:
            contact = self.db.table(table_name).select("*").eq("contact_phone", contact_phone).eq("org_id",org_id).execute().data
            if len(contact) > 0:
                return contact[0]
            else:
                return None
        except Exception as e:
            logging.exception("Exception occurred")
            return None


    def get_system_prompt_prod(self, table_name, id):
        try:
            prompt_data = self.db.table(table_name).select("*").eq("id", id).execute() 
            return prompt_data.data[0]['system_prompt']
        except Exception as e:
            logging.exception("Exception occurred")