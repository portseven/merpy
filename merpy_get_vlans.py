import requests
import json

# Define some variables we need
API_KEY = 'SOMEKEY'
MERAKI_URL = 'https://dashboard.meraki.com/api/v0/'
ORG_KEY = 'SOMEORG'
headers = {'X-Cisco-Meraki-API-Key':API_KEY}

# Function to grab the list of the Networks for the Organisation
def get_net_id():

	net_list = requests.get(MERAKI_URL + 'organizations/' + ORG_KEY + '/networks', headers=headers)
	if net_list.status_code != 200: 
       		print('Incorrect Network Query String'); 
       		exit(1); 
	else: 
		json_list = json.loads(net_list.text)
		return json_list

# Function to grab the VLAN's in the Network, based on Network ID (passed)
def get_vlan_info(passed_id):

	vlan_list = requests.get(MERAKI_URL + 'networks/' + passed_id + '/vlans', headers=headers)
	if vlan_list.status_code != 200: 
       		print('Incorrect VLAN Query String'); 
        	exit(1); 
	else: 
		json_vlist = json.loads(vlan_list.text)
		return json_vlist

def main():

# Get list of networks and ID's
	net_data = get_net_id()
	for i in net_data:
		net_name = i["name"]
		net_id = i["id"]
# Ignore the MDM Network
		if net_name == 'MDM':
			continue
		else:
# Use the ID to get a list of VLAN's per Network
			vlan_data = get_vlan_info(net_id)
			for v in vlan_data:
# Extract just the VLAN Name, and Subnet Range
				sub_net = v["subnet"]
				vlan_name = v["name"]
# Print Results in a CSV Friendly Format
				print(net_name + ', ' + vlan_name + ', ' + sub_net)
main()
