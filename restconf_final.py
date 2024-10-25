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
                    "ip": "172.30.135.1",
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
    statuss = status()
    print(statuss)
    if statuss == "No Interface loopback 65070135":
        if(resp.status_code >= 200 and resp.status_code <= 299):
            print("STATUS OK: {}".format(resp.status_code))
            return "Interface loopback 65070135 is created successfully"
        else:
            print('Error. Status Code: {}'.format(resp.status_code))
            return "Cannot create: Interface loopback 65070135"
    else:
        return "Cannot create: Interface loopback 65070135"

def delete():
    resp = requests.delete(
        "https://10.0.15.182/restconf/data/ietf-interfaces:interfaces/interface=Loopback65070135", 
        auth=basicauth, 
        headers={ "Accept": "application/yang-data+json", 
            "Content-type":"application/yang-data+json"
           }, 
        verify=False
        )
    statuss = status()
    print(statuss)
    if statuss == "Interface loopback 65070135 is enabled" or statuss == "Interface loopback 65070135 is disabled":
        if(resp.status_code >= 200 and resp.status_code <= 299):
            print("STATUS OK: {}".format(resp.status_code))
            return "Interface loopback 65070135 is deleted successfully"
        else:
            print('Error. Status Code: {}'.format(resp.status_code))
            return "Cannot delete: Interface loopback 65070135"
    else:
        return "Cannot delete: Interface loopback 65070135"

def enable():
    yangConfig = {
    "ietf-interfaces:interface": {
        "name": "Loopback65070135",
        "type": "iana-if-type:softwareLoopback",
        "enabled": True,
        
    }
}
    
    resp = requests.put(
        "https://10.0.15.182/restconf/data/ietf-interfaces:interfaces/interface=Loopback65070135", 
        data=json.dumps(yangConfig), 
        auth=basicauth, 
        headers={ "Accept": "application/yang-data+json", 
            "Content-type":"application/yang-data+json"
           }, 
        verify=False
        )
    statuss = status()
   
    if statuss == "Interface loopback 65070135 is disabled":
        if(resp.status_code >= 200 and resp.status_code <= 299):
            print("STATUS OK: {}".format(resp.status_code))
            return "Interface loopback 65070135 is enabled successfully"
        else:
            print('Error. Status Code: {}'.format(resp.status_code))
            return "Cannot enable: Interface loopback 65070135"
    else:
        return "Cannot enable: Interface loopback 65070135"

def disable():
    yangConfig = {
    "ietf-interfaces:interface": {
        "name": "Loopback65070135",
        "type": "iana-if-type:softwareLoopback",
        "enabled": False,
        
    }
}

    resp = requests.put(
        "https://10.0.15.182/restconf/data/ietf-interfaces:interfaces/interface=Loopback65070135", 
        data=json.dumps(yangConfig), 
        auth=basicauth, 
        headers={ "Accept": "application/yang-data+json", 
            "Content-type":"application/yang-data+json"
           }, 
        verify=False
        )
    statuss = status()
    if statuss == "Interface loopback 65070135 is enabled":
        if(resp.status_code >= 200 and resp.status_code <= 299):
            print("STATUS OK: {}".format(resp.status_code))
            return "Interface loopback 65070135 is disable successfully"
        else:
            print('Error. Status Code: {}'.format(resp.status_code))
            return "Cannot disnable: Interface loopback 65070135"
    else:
        return "Cannot disable: Interface loopback 65070135"
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
    
  
    
    if(resp.status_code >= 200 and resp.status_code <= 299):
         print("STATUS OK: {}".format(resp.status_code))
         response_json = resp.json()
         admin_status = response_json['ietf-interfaces:interface']['admin-status']
         oper_status = response_json['ietf-interfaces:interface']['oper-status']
         if admin_status == 'up' and oper_status == 'up':
            return "Interface loopback 65070135 is enabled"
         elif admin_status == 'down' and oper_status == 'down':
            return "Interface loopback 65070135 is disabled"
    elif(resp.status_code == 404):
        print("STATUS NOT FOUND: {}".format(resp.status_code))
        return "No Interface loopback 65070135"
    else:
        print('Error. Status Code: {}'.format(resp.status_code))