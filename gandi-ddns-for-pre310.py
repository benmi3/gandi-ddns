__author__ = 'Benmi'

import sys
from configparser import ConfigParser
from requests import Response, request, codes
import logging
from os import path


def logging_tool(name):
    cur_dir = path.dirname(path.realpath(__file__))
    filepath = path.join(cur_dir, "logfile.log")

    file_formatter = logging.Formatter(
        '%(asctime)s~%(levelname)s~%(message)s~module:%(module)s~function:%(module)s')
    console_formatter = logging.Formatter('%(levelname)s -- %(message)s')

    file_handler = logging.FileHandler(filepath)
    file_handler.setLevel(logging.INFO)
    file_handler.setFormatter(file_formatter)
    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging.INFO)
    console_handler.setFormatter(console_formatter)

    logger = logging.getLogger(name)
    logger.addHandler(file_handler)
    logger.addHandler(console_handler)
    logger.setLevel(logging.INFO)

    return logger


# start logging for easy debug
log = logging_tool(__name__)


def get_ip(record_type=str()):
    try:
        # if a record get ipv4
        # if aaaa record get ipv6
        if record_type == 'A':
            url = "https://api.ipify.org"
        elif record_type == 'AAAA':
            url = "https://api64.ipify.org"
        else:
            sys.exit()
        # get the current ipv4 address
        response = request("GET", url)
        # if request worked return text
        # else return status_code
        if response.status_code == codes.ok:
            return response.text
        else:
            return response.status_code
    except Exception as e:
        # if this fails, its most likely to internet connection
        log.error(e)
        sys.exit()


template = '''[section1]
# gandi.net API key
apikey = s3cr3t4p1k3y
# Domain
domain = example.com
# record name
rrset_name = @
# record type
rrset_type = A
# rrset_ttl value 300 ~ 2592000
rrset_ttl = 320'''


def create_example_config(filepath):
    # create config.ini if not existing
    with open(filepath, 'x') as f:
        # write example config
        f.write(template)
    return True


def get_record(apikey=str(),
               domain=str(),
               rrset_name=str(),
               rrset_type=str()):
    # url for api
    url = f"https://api.gandi.net/v5/livedns/domains/{domain}/records/{rrset_name}/{rrset_type}"
    # header for api
    headers = {'authorization': f'Apikey {apikey}'}
    # try a request
    response = request("GET", url, headers=headers)
    # return response
    return response


def put_record(apikey=str(),
               domain=str(),
               rrset_name=str(),
               rrset_type=str(),
               rrset_ttl=int(),
               ipaddress=str()):
    # url for api
    url = f"https://api.gandi.net/v5/livedns/domains/{domain}/records/{rrset_name}/{rrset_type}"
    # data payload
    payload = f"{{\"rrset_type\":\"{rrset_type}\",\"rrset_values\":[\"{ipaddress}\"],\"rrset_ttl\":{rrset_ttl}}}"
    # correct headers
    headers = {
        'authorization': f"Apikey {apikey}",
        'content-type': "application/json"
    }

    response = request("PUT", url, data=payload, headers=headers)

    return response


def status_translator(status_code=int()):
    if status_code == 200:
        return "Same record already exists. Nothing was changed"
    elif status_code == 201:
        return "Record was created"
    elif status_code == 400:
        return f"Failed to update record"
    elif status_code == 401:
        return "Bad authentication attempt because of a wrong API Key."
    elif status_code == 403:
        return "Access to the resource is denied. Mainly due to a lack of permissions to access it."
    elif status_code == 409:
        return "A record with that name / type pair already exists"
    else:
        return "unknown error occurred"


def main():
    cur_dir = path.dirname(path.realpath(__file__))
    filepath = path.join(cur_dir, "config.ini")

    # first check if config file is there
    if not path.exists(filepath):
        # if no config file create one
        log.error("Error: config file not found")
        if not create_example_config(filepath):
            # if it could not create file
            # raise error
            log.error("Could not create example file")
        # exit the program and wait for user to run it again
        # with a fixed config file
        sys.exit()
    # start configparser
    config = ConfigParser()
    # read the config file
    config.read(filepath)
    # get ipv4
    a = get_ip('A')
    # get ipv6
    aaaa = get_ip('AAAA')
    # sections
    for section in config.sections():
        # get the apikey from config
        apikey = config.get(section, 'apikey')
        # get the domain from config
        domain = config.get(section, 'domain')
        # get the rrset_name from config
        rrset_name = config.get(section, 'rrset_name')
        # get the rrset_type from config
        rrset_type = config.get(section, 'rrset_type')
        # get the rrset_ttl from config
        rrset_ttl = config.getint(section, 'rrset_ttl')
        # if type is A get IPv4
        # if type is AAAA get IPv6
        # currently only support those types
        # all else is will raise error and break
        supported_types = ['A', 'AAAA']
        if rrset_type in supported_types:
            if rrset_type == supported_types[0]:
                ipaddress = a
            elif rrset_type == supported_types[1]:
                ipaddress = aaaa
            else:
                ipaddress = str("type_error")
        else:
            log.warning(" rrset_type is not A or AAAA.\nCheck config and try again")
            break
        # check if there already exist a record
        current_status = get_record(apikey=apikey,
                                    domain=domain,
                                    rrset_name=rrset_name,
                                    rrset_type=rrset_type)

        cur_value = current_status.json()
        try:
            cur_address = cur_value['rrset_values']
        except KeyError:
            cur_address = ["127.0.0.1"]
        log.info(f"started updating {rrset_name}.{domain}")
        if ipaddress not in cur_address:
            # if there exist a record, update it
            update_record = put_record(apikey=apikey,
                                       domain=domain,
                                       rrset_name=rrset_name,
                                       rrset_type=rrset_type,
                                       rrset_ttl=rrset_ttl,
                                       ipaddress=ipaddress)
        else:
            # if the current value is correct
            # don't update it
            log.info(f"Current value is the same. Skipping {rrset_name}.{domain}")
            continue

        # check the status code
        message = status_translator(status_code=update_record.status_code)
        ok_codes = [200, 201]
        print(update_record.json())
        if update_record.status_code in ok_codes:
            # if status is ok
            # log the message and continue
            log.info(message)
        else:
            # if the status is not ok
            # log the error and exit the program
            log.error(message)
            break


if __name__ == '__main__':
    main()
