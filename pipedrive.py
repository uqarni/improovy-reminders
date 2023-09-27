
import requests
import json

api_token = "0a267f5c893e31a9dca5ff9bb3d0397266f69443"

class PipedriveClient:
    def __init__(self, api_token):
        self.api_token = api_token
        self.base_url = "https://api.pipedrive.com/v1/"

    def contactIDs_from_num(self, phone_number):
        persons_url = self.base_url + "persons/search?term={}&start=0&api_token={}"
        try:
            response = requests.get(persons_url.format(phone_number, self.api_token))
            response.raise_for_status()  # Raises a HTTPError if the status is 4xx, 5xx

            contactids = []
            data = json.loads(response.text)
            if data['success']:
                data = data['data']['items']
                for person in data:
                    contactids.append(person['item']['id'])
            return contactids

        except requests.RequestException as e:
            raise SystemExit(e)

    def leadInfo_from_contactID(self, lead_id):
        person_url = self.base_url + "persons/{}?api_token={}"
        try:
            response = requests.get(person_url.format(lead_id, self.api_token))
            response.raise_for_status()  # Raises a HTTPError if the status is 4xx, 5xx

            data = json.loads(response.text)
            if data['success']:
                if data['data']:
                    return data['data']
                else:
                    return None  # No lead found with this ID.
            else:
                raise Exception("The API request was not successful.")
        except requests.RequestException as e:
            raise SystemExit(e)

    def deals_from_contactID(self, person_id):
        deals_url = self.base_url + "deals/search?term=proposal&person_id={}&api_token={}"
        try:
            response = requests.get(deals_url.format(person_id, self.api_token))
            response.raise_for_status()  # Raises a HTTPError if the status is 4xx, 5xx

            data = json.loads(response.text)
            return data
            if data['success']:
                if data['data']:
                    return data['data']
                else:
                    return None  # No deals found for this person.
            else:
                raise Exception("The API request was not successful.")
        except requests.RequestException as e:
            raise SystemExit(e)
        

    def add_note(self, content, dealid = None, personid = None):
        url = f"https://api.pipedrive.com/v1/notes?api_token={self.api_token}"

        if dealid == None:
            payload = {"content": content,
                   "person_id": personid,
                   'pinned_to_person_flag': True
                   }
        elif personid == None:
            payload = {"content": content,
                   "deal_id": dealid,
                   'pinned_to_deal_flag': True, 
                   }
        else:
            payload = {"content": content,
                   "deal_id": dealid,
                   "person_id": personid,
                   'pinned_to_deal_flag': True, 
                   'pinned_to_person_flag': True
                   }
        headers = {
        'Content-Type': 'application/json',
        'Accept': 'application/json',
        }

        response = requests.request("POST", url, headers=headers, data=json.dumps(payload))

        return json.loads(response.text)

    def deals_from_personID(self, person_id):
        url = f"https://api.pipedrive.com/v1/persons/{person_id}/deals?start=0&status=all_not_deleted&api_token={self.api_token}"

        payload = {}
        headers = {
        'Accept': 'application/json',
        }

        response = requests.request("GET", url, headers=headers, data=payload)
        return json.loads(response.text)
    
    def get_pipedrive_deal_info(self, term):
        url = f"https://api.pipedrive.com/v1/deals/search?term=form {term}&api_token={api_token}"

        headers = {
            'Accept': 'application/json',
            'Cookie': '__cf_bm=rqNd2dXNRORNsL_GpE3axqFopi.91X0yQQSvbJwIcJ8-1689315548-0-ATxpaQhCG9GFf+nRqCqEENfhu1qd8oU8uUUxf3agwvPVWnfXcw53E9SJq6aF4J0cxIvlWanoNiYo2lH1NjlhF+s='
        }

        response = requests.request("GET", url, headers=headers)
        response = json.loads(response.text)

        # Find the spreadsheet link
        spreadsheet_link = next((x for x in response['data']['items'][0]['item']['custom_fields'] if 'https://docs.google.com/spreadsheets' in x), None)
        
        description = json.loads(response['data']['items'][0]['item']['custom_fields'][-1])

        response = {
            'project_title': response['data']['items'][0]['item']['title'],
            'status': response['data']['items'][0]['item']['status'],
            'stage': response['data']['items'][0]['item']['stage']['name'],
            'lead_full_name': response['data']['items'][0]['item']['person']['name'],
            'desired_color': description['Color'],
            'address': description['Address'],
            'timeline': description['Start Date'],
            'spreadsheet': spreadsheet_link,
            'zipcode': description['Zip Code'],
            'initial_description': description['Initial Description'],
            'additional_notes': description['Additional Notes'],
            'interior_surfaces': description['Interior Surfaces'],
            'interior_wall_height': description['Interior Wall Height'],
            'exterior_surfaces': description['Exterior Surfaces'],
            'exterior_wall_height': description['Exterior Wall Height'],
            'geography': description['Geography'],
            'square_footage': description['Square Footage']
        }

        return response








# ImproovyCRM = PipedriveClient(api_token)
# test = ImproovyCRM.add_note("this is the newest note", dealid = 22163)
# print(test)
############################################################################################################

# data = ImproovyCRM.contactIDs_from_num("+17372740772")
# print(json.dumps(data,indent=1))


# me = ImproovyCRM.leadInfo_from_contactID(21297)
# print(json.dumps(me,indent=1))

#me = ImproovyCRM.deals_from_contactID(21297)
#print(json.dumps(me,indent=1))
# me = ImproovyCRM.contactIDs_from_num("+17372740771")
# #me = ImproovyCRM.get_pipedrive_deal_info("form uzair+testing@hellogepeto")
# print(json.dumps(me,indent=1))


output1 = '''
[
 {
  "result_score": 0.169745,
  "item": {
   "id": 21270,
   "type": "person",
   "name": "uzair qarni",
   "phones": [
    "+17372740771"
   ],
   "emails": [
    "uzair@hellogepeto.com"
   ],
   "primary_email": "uzair@hellogepeto.com",
   "visible_to": 3,
   "owner": {
    "id": 12567244
   },
   "organization": null,
   "custom_fields": [
    "6c51722f-d86b-45e9-b731-b4ec13b05601"
   ],
   "notes": [],
   "update_time": "2023-07-10 21:09:01"
  }
 },
 {
  "result_score": 0.169745,
  "item": {
   "id": 21167,
   "type": "person",
   "name": "New JustCall Contact",
   "phones": [
    "+17372740771"
   ],
   "emails": [],
   "primary_email": null,
   "visible_to": 3,
   "owner": {
    "id": 16916391
   },
   "organization": null,
   "custom_fields": [
    "9ed0911b-9562-49bc-a5f8-fa5e3b89f21a"
   ],
   "notes": [],
   "update_time": "2023-07-10 19:14:51"
  }
 }
]
'''
############################################################################################################


output2 = '''
{
 "id": 21270,
 "company_id": 7915969,
 "owner_id": {
  "id": 12567244,
  "name": "Bids",
  "email": "bids@improovy.com",
  "has_pic": 1,
  "pic_hash": "fd0c57a90dab0064f243d401e5b39823",
  "active_flag": true,
  "value": 12567244
 },
 "org_id": null,
 "name": "uzair qarni",
 "first_name": "uzair",
 "last_name": "qarni",
 "open_deals_count": 1,
 "related_open_deals_count": 0,
 "closed_deals_count": 0,
 "related_closed_deals_count": 0,
 "participant_open_deals_count": 0,
 "participant_closed_deals_count": 0,
 "email_messages_count": 8,
 "activities_count": 1,
 "done_activities_count": 0,
 "undone_activities_count": 1,
 "files_count": 0,
 "notes_count": 0,
 "followers_count": 1,
 "won_deals_count": 0,
 "related_won_deals_count": 0,
 "lost_deals_count": 0,
 "related_lost_deals_count": 0,
 "active_flag": true,
 "phone": [
  {
   "label": "work",
   "value": "+17372740771",
   "primary": true
  }
 ],
 "email": [
  {
   "label": "work",
   "value": "uzair@hellogepeto.com",
   "primary": true
  }
 ],
 "first_char": "u",
 "update_time": "2023-07-10 21:09:01",
 "delete_time": null,
 "add_time": "2023-07-10 18:53:47",
 "visible_to": "3",
 "picture_id": null,
 "next_activity_date": "2023-07-10",
 "next_activity_time": "21:00:00",
 "next_activity_id": 271545,
 "last_activity_id": null,
 "last_activity_date": null,
 "last_incoming_mail_time": "2023-07-10 21:08:30",
 "last_outgoing_mail_time": "2023-07-10 21:06:02",
 "label": null,
 "im": [
  {
   "value": "",
   "primary": true
  }
 ],
 "postal_address": null,
 "postal_address_subpremise": null,
 "postal_address_street_number": null,
 "postal_address_route": null,
 "postal_address_sublocality": null,
 "postal_address_locality": null,
 "postal_address_admin_area_level_1": null,
 "postal_address_admin_area_level_2": null,
 "postal_address_country": null,
 "postal_address_postal_code": null,
 "postal_address_formatted_address": null,
 "notes": null,
 "birthday": null,
 "job_title": null,
 "org_name": null,
 "marketing_status": "pending_upgrade",
 "doi_status": 1,
 "cc_email": "improovy2@pipedrivemail.com",
 "primary_email": "uzair@hellogepeto.com",
 "owner_name": "Bids",
 "030b08a14d47cbe268c54597f240647670ceabc5": null,
 "bbdde27ff064761d1d73a8fea7dab4ecc699820a": null,
 "d0699cf6516607704f938550890bfd8abc5a9a4e": null,
 "b8424bc4575cf9bbd02ff6272696940aecde7c78": null,
 "b86a7ce0bf079efcc5dee585edc4d178cbc98013": null,
 "3389942748ab85be7d00b9b552abb9496abd66db": null,
 "6100b6d47418fa65763c4003ceb3ebbc52c677aa": null,
 "ea66354cdc71fd9fcf23ee8f9b0650a705fb82b5": null,
 "51141c4991b98a966ff92c5778f9cca16cba9bd5": null,
 "2402aaae3b3c6fc074032eae9b8fd1f25c4f3769": null,
 "fb3764c2880020c57690aff597687816d03c671e": null,
 "0f9df4a5956454f44646468af41626a406533d30": null,
 "b4b780ad15fc08c70f023c18842953b29efa6871": null,
 "8aa12c2006b2a2a6964b69679969b800f8df63b0": null,
 "3fd4a63fda1ead2fdb8d0ef6c8eef7cfd0ac8ab1": "6c51722f-d86b-45e9-b731-b4ec13b05601",
 "88a4f838702be0a47df31fb237ccd732898930a3": "239",
 "870cb5151bdf7a2c1130c5ef2cd300c7c0fd1883": null,
 "913212ee5b5dc445f060735b6941cb49599c2779": null
}
'''



output3 = '''
{
 "items": [
  {
   "result_score": 1.092828,
   "item": {
    "id": 21662,
    "type": "deal",
    "title": "21662 - Proposal - uzair qarni",
    "value": 4580,
    "currency": "USD",
    "status": "open",
    "visible_to": 3,
    "owner": {
     "id": 12567244
    },
    "stage": {
     "id": 3,
     "name": "Estimated"
    },
    "person": {
     "id": 21270,
     "name": "uzair qarni"
    },
    "organization": {
     "id": 1,
     "name": ".",
     "address": null
    },
    "custom_fields": [
     ".",
     "IF WALLS\r+ Pole sand walls and/or ceilings prior to painting top coats.\r+ Patch any minor holes, minor nail pops or small minor cracks as necessary and spot prime when required with a latex drywall primer prior to painting top coats.\r+ Patch large drywall repairs when included in specified scope above.\r+ Apply two coats on the wall (unless otherwise stated) with paint specified; all colors to be determined.\r....... \nIF CEILINGS\r+ Pole sand walls and/or ceilings prior to painting top coats.\r+ Patch any minor holes, minor nail pops or small minor cracks as necessary and spot prime when required with a latex drywall primer prior to painting top coats.\r+ Patch large drywall repairs when included in specified scope above.\r+ Apply two coats on ceiling with flat white ceiling paint unless otherwise mentioned above.\r....... \nIF TRIM (Baseboards, Window and Door Casings, Door Jambs, Crown Molding)\r+ Lightly scuff sand trim and remove dust prior to painting top coats to ensure proper adhesion to existing finish. \r+ Caulk between trim and walls (as well as between separate trim components) where necessary and fill any holes from installation (if applicable) of trim prior to painting top coats. \r+ Paint trim two coats with paint specified, unless otherwise mentioned above\r....... \nIF DOORS\r+ Remove hardware or protect as necessary prior to painting.\r+ If painting doors is included in the specified scope above, lightly scuff sand each door side and remove dust prior to painting top coats to ensure proper adhesion to existing finish.\r....... \nIF WINDOWS\r+ Remove hardware or protect as necessary prior to painting. \r+ Lightly scuff sand surface of window to be painted and remove dust prior to painting top coats to ensure proper adhesion to existing finish. \r+ Depending on the time of year and type of window, some windows can be removed to paint and then be re-installed when paint dries. Otherwise, windows will be painted in place and will need to be left cracked open until dry.\r....... \n  \n \n \n",
     "Surface:  Color | Product Brand | Sheen \n(Ex: Walls:  Agreeable Grey | Duration | Flat)\n",
     "Entire Unit\n--------------\n+   Walls  |  2 Coats | Cashmere Interior \n+   Ceilings (Flat)  |  2 Coats | Ceiling Paint - Flat \n+   Baseboards & Door Casings (3\" Repaint)  |  2 Coats | Pro-Classic or Advance \n+  8 Door Sides  |  Panel  |  2 Coats | Pro-Classic or Advance \n+   Window Sills  |  2 Coats | Pro-Classic or Advance \n \n \n \n \n \n \n \n \n \n \n \n \n \n \n \n \n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n \n \n \n \n \n \n \n \n \n ",
     "4580",
     "3435",
     "91",
     "2519",
     "Preferred Cadence of Communication:\nParking Availability/Cost: \nOccupied: \nPets: \nSpouse/Other occupants names: \nOther Info: ",
     "1600 Pennsylvania avenue",
     "08/01",
     "0",
     "- Moving Furniture\n- Ceilings \n- Baseboards And Door Casings \n- Crown Moulding\n- Doors\n- Window Casings\n- Window Interiors \n- Closet Interiors \n- Accent Walls - Basement - Three or more coats (unless otherwise stated)\n\n\n\n\n\n\n",
     "https://improovy-customer-portal.herokuapp.com/#/estimate/21662",
     "91",
     "https://drive.google.com/drive/folders/1xaCKtRWfZmOnFe5DBQUU52kohOTpq5xg",
     " https://docs.google.com/spreadsheets/d/11dN2o1-pgnDfPa5Kc93JsJ3tM55jmV3Y-hy1ttCQBqw/edit?usp=drivesdk",
     "43.1",
     "2519",
     "32b82931-efdf-421f-aaf7-e519c88bbe7f",
     "1145",
     "4580",
     "2701",
     "15.02",
     "Initial Description: I need a painter to paint the whole universe. [THIS IS A TEST]"
    ],
    "notes": []
   }
  }
 ]
}
'''