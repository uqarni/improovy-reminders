from supabase_client import SupabaseClient


db = SupabaseClient()

contacts = db.fetch_by_contact_phone_and_orgid('contacts', "+17372740771", 'improovy')
print(contacts)