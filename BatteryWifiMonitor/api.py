import json

import utils

def networks_json():
    """
    This function simply calls convert_networks_list_to_json() with the output
    of networks_search().
    It is separated from convert_networks_list_to_json() to make writing tests
    more straightforward.
    """
    networks_list = utils.networks_search()
    return convert_networks_list_to_json(networks_list)

def convert_networks_list_to_json(networks_list):
    """
    Create a new response dictionary and convert it to JSON.
    """
    response_data = {}
    response_data['networks'] = networks_list
    return json.dumps(response_data)

def battery_json():
    """
    This function simply calls convert_battery_dict_to_json() with the output
    of battery_status().
    It is separated from convert_battery_dict_to_json() to make writing tests
    more straightforward.
    """
    battery_info = utils.battery_status()
    return convert_battery_dict_to_json(battery_info)

def convert_battery_dict_to_json(battery_info):
    """
    Convert battery_info dictionary to JSON.
    """
    return json.dumps(battery_info)