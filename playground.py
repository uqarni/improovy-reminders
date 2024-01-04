from supabase_client import SupabaseClient


db = SupabaseClient()

db_contact = db.fetch_by_contact_phone_and_orgid('contacts', "xxxx", 'improovy')

if db_contact == None:
    print('none')