#######################################################################################
# Yourname:
# Your student ID:
# Your GitHub Repo: 

#######################################################################################
# 1. Import libraries for API requests, JSON formatting, time, os, (restconf_final or netconf_final), netmiko_final, and ansible_final.
import os
import requests
import time
import json
import netconf_final
import restconf_final

#######################################################################################
# 2. Assign the Webex access token to the variable ACCESS_TOKEN using environment variables.

ACCESS_TOKEN = os.environ['ACCESS_TOKEN']

#######################################################################################
# 3. Prepare parameters get the latest message for messages API.

# Defines a variable that will hold the roomId
roomIdToGetMessages = (
    "Y2lzY29zcGFyazovL3VybjpURUFNOnVzLXdlc3QtMl9yL1JPT00vZTFmNjU5NTAtN2Q4Ny0xMWVmLThiYjAtNjM4ZjA5NTg3NzUz"
)

while True:
    # always add 1 second of delay to the loop to not go over a rate limit of API calls
    time.sleep(1)

    # the Webex Teams GET parameters
    #  "roomId" is the ID of the selected room
    #  "max": 1  limits to get only the very last message in the room
    getParameters = {"roomId": roomIdToGetMessages, "max": 1}

    # the Webex Teams HTTP header, including the Authoriztion
    getHTTPHeader = {"Authorization": 'Bearer {}'.format(ACCESS_TOKEN)}
# 4. Provide the URL to the Webex Teams messages API, and extract location from the received message.
    
    # Send a GET request to the Webex Teams messages API.
    # - Use the GetParameters to get only the latest message.
    # - Store the message in the "r" variable.
    r = requests.get(
        "https://webexapis.com/v1/messages",
        params=getParameters,
        headers=getHTTPHeader,
    )
    # verify if the retuned HTTP status code is 200/OK
    if not r.status_code == 200:
        raise Exception(
            "Incorrect reply from Webex Teams API. Status code: {}".format(r.status_code)
        )

    # get the JSON formatted returned data
    json_data = r.json()

    # check if there are any messages in the "items" array
    if len(json_data["items"]) == 0:
        raise Exception("There are no messages in the room.")

    # store the array of messages
    messages = json_data["items"]
    
    # store the text of the first message in the array
    message = messages[0]["text"]
    print("Received message: " + message)

    # check if the text of the message starts with the magic character "/" followed by your studentID and a space and followed by a command name
    #  e.g.  "/66070123 create"
    if message.startswith("/65070135"):

        # extract the command
        parts = message.split()  # แยกข้อความออกเป็นคำตามช่องว่าง
        command = parts[1] if len(parts) > 1 else None  # ดึงคำสั่งจากข้อความถ้ามี
        print(command)

# 5. Complete the logic for each command

        if command == "create":
           responseMessage = restconf_final.create()  
        elif command == "delete":
           responseMessage = restconf_final.delete()
        elif command == "enable":
           responseMessage = restconf_final.enable()
        elif command == "disable":
           responseMessage = restconf_final.disable()
        elif command == "status":
            responseMessage = restconf_final.status()
        #  elif command == "gigabit_status":
        #     <!!!REPLACEME with code for gigabit_status command!!!>
        # elif command == "showrun":
        #     <!!!REPLACEME with code for showrun command!!!>
        else:
            responseMessage = "Error: No command or unknown command"
        
# 6. Complete the code to post the message to the Webex Teams room.

        # The Webex Teams POST JSON data for command showrun
        # - "roomId" is is ID of the selected room
        # - "text": is always "show running config"
        # - "files": is a tuple of filename, fileobject, and filetype.

        # the Webex Teams HTTP headers, including the Authoriztion and Content-Type
        
        # Prepare postData and HTTPHeaders for command showrun
        # Need to attach file if responseMessage is 'ok'; 
        # Read Send a Message with Attachments Local File Attachments
        # https://developer.webex.com/docs/basics for more detail

        # if command == "showrun" and responseMessage == 'ok':
            # filename = "<!!!REPLACEME with show run filename and path!!!>"
            # fileobject = <!!!REPLACEME with open file!!!>
            # filetype = "<!!!REPLACEME with Content-type of the file!!!>"
            # postData = {
            #     "roomId": <!!!REPLACEME!!!>,
            #     "text": "show running config",
            #     "files": (<!!!REPLACEME!!!>, <!!!REPLACEME!!!>, <!!!REPLACEME!!!>),
            # }
            # postData = MultipartEncoder(<!!!REPLACEME!!!>)
            # HTTPHeaders = {
            # "Authorization": ACCESS_TOKEN,
            # "Content-Type": <!!!REPLACEME with postData Content-Type!!!>,
            # }
        # other commands only send text, or no attached file.
        # else:
        postData = {"roomId": roomIdToGetMessages, "text": responseMessage}
        postData = json.dumps(postData)

        # the Webex Teams HTTP headers, including the Authoriztion and Content-Type
        HTTPHeaders = {"Authorization": 'Bearer {}'.format(ACCESS_TOKEN), 
                "Content-Type": "application/json"}   

        # Post the call to the Webex Teams message API.
        r = requests.post(
            "https://webexapis.com/v1/messages",
            data=postData,
            headers=HTTPHeaders,
        )
        if not r.status_code == 200:
            raise Exception(
                "Incorrect reply from Webex Teams API. Status code: {}".format(r.status_code)
            )
