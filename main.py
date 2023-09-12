# main.py
from apscheduler.schedulers.blocking import BlockingScheduler
import redis
import os
import json
import requests
from datetime import datetime, timedelta
import requests
import json
import openai
from justcall import send_text, assign_to_group
import time
import logging
import platform
import hashlib

#improovy justcall info
improovy_api_key = "a475b0ecf1d1ba78ec7a9bc49d60f225531f3617"
improovy_api_secret = "bed00ba3e48de573ab7841e11971c32948edff6f"


# Connect to Redis server
redis_host = os.environ.get("REDIS_1_HOST")
redis_port = 25061
redis_password = os.environ.get("REDIS_1_PASSWORD")

operating_system = platform.system()
# Set the CA certificates file path based on the operating system
if operating_system == 'Linux':
    ssl_ca_certs = "/etc/ssl/certs/ca-certificates.crt"
elif operating_system == 'Darwin':  # macOS
    ssl_ca_certs = "/etc/ssl/cert.pem"  # Update to macOS path
else:
    raise ValueError(f"Unsupported operating system: {operating_system}")

rd = redis.Redis(host=redis_host, port=redis_port, password=redis_password, ssl=True, ssl_ca_certs=ssl_ca_certs)

def add_space_after_url(s):
    words = s.split()
    for i, word in enumerate(words):
        if word.startswith('http://') or word.startswith('https://'):
            if word[-1] in '.,!?;:':
                words[i] = word[:-1] + ' ' + word[-1] + ' '
            else:
                words[i] = word + ' '
    return ' '.join(words)

def improovy_reminder():
    logging.basicConfig(level=logging.INFO)
    logging.info("Running my function...")
    #counter to return
    counter = 0

    #openai key
    openai.api_key = os.environ.get("OPENAI_API_KEY")


    #extract all conversation statuses
    allconvos_status = []
    for number in rd.hgetall("last_message-+16084205020"):
        number = number.decode('utf-8')
        status = rd.hget("last_message-+16084205020", number).decode('utf-8')
        allconvos_status.append((number,status))

            # status of the form +18326470488: 0-2023-05-01 06:05:40
    for numbstat in allconvos_status:
        print(numbstat)


    print('\n')
    #pull list of booked leads from db
    booked_leads = []
    raw_leads = rd.lrange("improovy_booking", 0, -1)
    for lead in raw_leads:
        booked_leads.append(lead.decode('utf-8'))

    #create a new list that only has the open leads
    to_follow_up = [(key, value) for (key, value) in allconvos_status if key not in booked_leads]


    #pull list of within 24 hours
    now = datetime.now()

    filtered_data = [
        item for item in to_follow_up
        if now - datetime.strptime(item[1][2:], "%Y-%m-%d %H:%M:%S") > timedelta(hours=23) and item[1][2:] != "X-"
    ]

    #tara number
    # ("14067294654-followup_count", "3")
    # ("14067294654-secret_message")
    us_num = "+16084205020"
    #pull recurrence value
    recurrence = rd.get("13128472321-followup_count").decode('utf-8')
    #message those that are remaining 

    secret_message = rd.get("13128472321-secret_message").decode('utf-8')
    secret_message = secret_message.format(recurrence = recurrence)
    print("secret_message is " + secret_message)
    injected_message_dict = {"role": "user", "content": secret_message}
    injected_message = json.dumps(injected_message_dict)
 
    #hack to solve duplicate
    already_sent = []

    # Filtering filtered_data to include only numbers that belong to group 'a'
    #filtered_data = [number for number in filtered_data if assign_to_group(str(number[0])) != 0]

    for number in filtered_data:
        if number == '+17372740771' or number == '+17736206534':
            continue

        #followups
        followups = rd.hget('improovy_followup_count', them_num).decode('utf-8')
        if not followups:
            rd.hset('improovy_followup_count', them_num,"0")
            followups = '0'
        if int(followups) >= int(recurrence):
            continue
        rd.hset('improovy_followup_count', them_num, str(int(followups) + 1))
        #end followups

        time.sleep(10)
        print(number)
        them_num = str(number[0])
        #create messages
        #remember, message chain key format is 14067294654-+17372740771
        key = us_num + "-" + them_num

        messages = []
        for message in rd.lrange(key, 0, -1):
            messages.append(json.loads(message.decode('utf-8')))

        #append secret message to messages
        messages.append(json.loads(injected_message))

        # get all the info from the db
        try:
            hash_data = rd.hgetall('improovy_lead-' + them_num)
            data_dict = {}
            for subkey, value in hash_data.items():
                value_str = value.decode()
                if not value_str:
                    value_str = 'unknown'
                data_dict[subkey.decode()] = value_str

            # find and prepend system prompt
            user_email = 'carr@improovy.com'
            system_prompt = rd.get(user_email + "-systemprompt-01").decode('utf-8')

            # replace with dynamic booking link
            booking_link = 'https://calendly.com/d/y7c-t9v-tnj/15-minute-meeting-with-improovy-painting-expert '

            # replace with name variable
            name = "Mike"

            interior_surfaces = str(data_dict.get('interior_surfaces')) if data_dict.get('interior_surfaces') else 'unknown'
            interior_wall_height = str(data_dict.get('interior_wall_height')) if data_dict.get('interior_wall_height') else 'unknown'
            exterior_surfaces = str(data_dict.get('exterior_surfaces')) if data_dict.get('exterior_surfaces') else 'unknown'
            exterior_wall_height = str(data_dict.get('exterior_wall_height')) if data_dict.get('exterior_wall_height') else 'unknown'


            system_prompt = system_prompt.format(
                #hardcoded
                name=name,
                booking_link=booking_link,
                #from contact
                personid=data_dict.get('personid', 'unknown'),
                email=data_dict.get('email', 'unknown'),
                owner=data_dict.get('owner', 'unknown'),
                #from deal
                project_title=data_dict.get('project_title', 'unknown'),
                status=data_dict.get('status', 'unknown'),
                stage=data_dict.get('stage', 'unknown'),
                lead_full_name=data_dict.get('lead_full_name', 'unknown'),
                address=data_dict.get('address', 'unknown'),
                timeline=data_dict.get('timeline', 'unknown'),
                spreadsheet=data_dict.get('spreadsheet', 'unknown'),
                zipcode=data_dict.get('zipcode', 'unknown'),
                initial_description=data_dict.get('initial_description', 'unknown'),
                additional_notes=data_dict.get('additional_notes', 'unknown'),
                sqft = data_dict.get('square_footage', 'unknown'),
                color = data_dict.get('desired_color', 'unknown'),
                interior_surfaces = interior_surfaces,
                interior_wall_height = interior_wall_height,
                exterior_surfaces = exterior_surfaces,
                exterior_wall_height = exterior_wall_height,
                #from booking
                resched_link=data_dict.get('resched_link', 'unknown'),
                cancel_link=data_dict.get('resched_link', 'unknown'),
                meeting_booked=data_dict.get('meeting_booked', 'unknown'),
                meeting_time=data_dict.get('meeting_time', 'unknown')
            )
        except Exception as e:
            print(e)
            send_text(us_num, "+17372740771", "Improovy Follow Up To: " + them_num + "\nFrom: " + us_num + "\nMessage: " + "Error in system prompt", improovy_api_key, improovy_api_secret)
        
        system_prompt = {"role": "system", "content": system_prompt}

        messages.insert(0,system_prompt)

        #generate OpenAI response
        for i in range(5):
            try:
                response = openai.ChatCompletion.create(model = "gpt-4", messages = messages, max_tokens = 600)
                rd.hset('improovy_usage', str(now), str(response['usage']))
                response = response["choices"][0]["message"]["content"] 
                response = add_space_after_url(response)
                break
            except Exception as e:
                error_message = f"Attempt {i + 1} failed: {e}"
                print(error_message)
                if i < 4:
                    time.sleep(5)
        else:
            final_error_message = f"Failed all {i + 1} attempts to call the API."
            print(error_message)
            send_text(us_num, "+17372740771", final_error_message + "-From: " + us_num + ".\nTo: " + them_num, improovy_api_key, improovy_api_secret)
            continue
    
        #response = openai.ChatCompletion.create(model = "gpt-4", messages = messages, max_tokens = 600)
        

        now = datetime.now()
        now = now.strftime("%Y-%m-%d %H:%M:%S")

        i = 0
        #check for secret code 
        upper_response = response.upper()
        if ('DO'in upper_response and 'NOT' in upper_response and 'SEND' in upper_response and 'THIS' in upper_response and 'YO' in upper_response):
            print("NOPE " + response)
            #if yes, update record and exit loop
            rd.hset("last_message-" + us_num, them_num, 'X-' + now)
            time.sleep(0.5)

        #if not, send to customer 
        
        else:
            #delete if and deindent after tsting
            if them_num in already_sent:
                continue
            send_text(us_num, them_num, response, improovy_api_key, improovy_api_secret)
            send_text(us_num, "+17736206534", 'Improovy Follow Up To: ' + them_num + '\nFrom :' + us_num + '\nMessage: ' + response, improovy_api_key, improovy_api_secret)

            already_sent.append(them_num)
            counter += 1
            print(response)
            rd.hset("last_message-" + us_num, them_num, '0-' + now)
            #update record and exit loop
            to_append = {"role": "assistant", "content": response}
            rd.rpush(key, injected_message)
            rd.rpush(key, json.dumps(to_append))
            time.sleep(0.5)
    print(counter)
    return {"status": "success", "counter": counter}

if __name__ == "__main__":
    scheduler = BlockingScheduler()
    # Schedule the function to run daily at the time of your choosing (e.g., 5:30 PM)
    hour = rd.get("13128472321-reminder_hour").decode('utf-8')
    hour = int(hour)
    minute = 0
    scheduler.add_job(improovy_reminder, 'cron', hour=hour, minute=minute)
    logging.basicConfig(level=logging.INFO)
    logging.info(f"Starting the scheduler. will run at {hour}:{minute}")
    scheduler.start()













