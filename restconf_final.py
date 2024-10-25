import json
import requests
requests.packages.urllib3.disable_warnings()

api_url = "https://10.0.15.182/restconf/data/ietf-interfaces:interfaces/interface=Loopback65070135"

# the RESTCONF HTTP headers, including the Accept and Content-Type
# Two YANG data formats (JSON and XML) work with RESTCONF 
headers  = { "Accept": "application/yang-data+json", 
            "Content-type":"application/yang-data+json"
           }
basicauth = ("admin", "cisco")


def create():
    yangConfig = {
    "ietf-interfaces:interface": {
        "name": "Loopback65070135",
        "description": "My firsttime RESTCONF loopback",
        "type": "iana-if-type:softwareLoopback",
        "enabled": True,
        "ietf-ip:ipv4": {
            "address": [
                {
                    "ip": "10.10.10.10",
                    "netmask": "255.255.255.0"
                }
            ]
        },
        "ietf-ip:ipv6": {}
    }
}
    
    resp = requests.put(
        api_url, 
        data=json.dumps(yangConfig), 
        auth=basicauth, 
        headers=headers, 
        verify=False
        )

    if(resp.status_code >= 200 and resp.status_code <= 299):
        print("STATUS OK: {}".format(resp.status_code))
        return "create success"
    else:
        print('Error. Status Code: {}'.format(resp.status_code))
        return "cannot create"


# def delete():
#     resp = requests.<!!!REPLACEME with the proper HTTP Method!!!>(
#         <!!!REPLACEME with URL!!!>, 
#         auth=basicauth, 
#         headers=<!!!REPLACEME with HTTP Header!!!>, 
#         verify=False
#         )

#     if(resp.status_code >= 200 and resp.status_code <= 299):
#         print("STATUS OK: {}".format(resp.status_code))
#         return "<!!!REPLACEME with proper message!!!>"
#     else:
#         print('Error. Status Code: {}'.format(resp.status_code))


# def enable():
#     yangConfig = <!!!REPLACEME with YANG data!!!>

#     resp = requests.<!!!REPLACEME with the proper HTTP Method!!!>(
#         <!!!REPLACEME with URL!!!>, 
#         data=json.dumps(<!!!REPLACEME with yangConfig!!!>), 
#         auth=basicauth, 
#         headers=<!!!REPLACEME with HTTP Header!!!>, 
#         verify=False
#         )

#     if(resp.status_code >= 200 and resp.status_code <= 299):
#         print("STATUS OK: {}".format(resp.status_code))
#         return "<!!!REPLACEME with proper message!!!>"
#     else:
#         print('Error. Status Code: {}'.format(resp.status_code))


# def disable():
#     yangConfig = <!!!REPLACEME with YANG data!!!>

#     resp = requests.<!!!REPLACEME with the proper HTTP Method!!!>(
#         <!!!REPLACEME with URL!!!>, 
#         data=json.dumps(<!!!REPLACEME with yangConfig!!!>), 
#         auth=basicauth, 
#         headers=<!!!REPLACEME with HTTP Header!!!>, 
#         verify=False
#         )

#     if(resp.status_code >= 200 and resp.status_code <= 299):
#         print("STATUS OK: {}".format(resp.status_code))
#         return "<!!!REPLACEME with proper message!!!>"
#     else:
#         print('Error. Status Code: {}'.format(resp.status_code))


def status():
    api_url_status = "https://10.0.15.182/restconf/data/ietf-interfaces:interfaces-state/interface=Loopback65070135"

    resp = requests.get(
        api_url_status, 
        auth=basicauth, 
        headers={ "Accept": "application/yang-data+json", 
            "Content-type":"application/yang-data+json"
           }, 
        verify=False
        )
    
    print("STATUS OK: {}".format(resp.status_code))
    print(resp.json())
    
    if(resp.status_code >= 200 and resp.status_code <= 299):
         print("STATUS OK: {}".format(resp.status_code))
         response_json = resp.json()
         admin_status = response_json['ietf-interfaces:interface']['admin-status']
         oper_status = response_json['ietf-interfaces:interface']['oper-status']
         if admin_status == 'up' and oper_status == 'up':
            return "up"
         elif admin_status == 'down' and oper_status == 'down':
            return "down"
    elif(resp.status_code == 404):
        print("STATUS NOT FOUND: {}".format(resp.status_code))
        return "not found"
    else:
        print('Error. Status Code: {}'.format(resp.status_code))