import requests
import json
import datetime
import os
from dotenv import load_dotenv

load_dotenv()
# API url
baseurl = 'https://services.nvd.nist.gov/rest/json/cves/2.0'
save_path = "../data/"


# Main request to get all data (for the default 2000 first per page)
def main_request(x):
    # f'?startIndex={x}' will help to advance into the next values
    response = requests.get(baseurl + f'?startIndex={x}')
    # checks if the response is 200
    return response.json()


# gets the total results
def get_total_results(response):
    return response['totalResults']


# gets the results per page (default at 2000/page)
def get_results_per_page(response):
    return response['resultsPerPage']


# gets all the information for each vulnerability
def get_vulnerabilities(response):
    return response['vulnerabilities']


# gets the cve id for each vulnerability
def get_cve_id(response):
    charlist = []
    for x in range(0, get_results_per_page(response)):
        charlist.append(get_vulnerabilities(response)[x]['cve']['id'])
    return charlist


# how many vulnerabilities there are per page
def get_length(response):
    return len(response['vulnerabilities'])


# will check if metric has a 'cvssMetric' key.
def get_cvssMetric(response, x):
    cvss_metrics = None
    for key, value in get_vulnerabilities(response)[x]['cve']['metrics'].items():
        if key.startswith('cvssMetric'):
            # data will be saved without needing to know the version of the CVSS (cvssMetricV2 or cvssMetricV3)
            cvss_metrics = value
            break
    # returns the cvss_metrics
    return cvss_metrics


# gets the risk value
def get_cvss(response, x):
    # checks if the get_cvssMetric is None or not
    if get_cvssMetric(response, x) is not None:
        # will return the impactScore of the saved values from get_cvssMetric
        for y in range(0, len(get_cvssMetric(response, x))):
            return get_cvssMetric(response, x)[y]['impactScore']
    else:
        # if there is no cvssMetric, it will return a '-'
        return '-'


# gets the cve url for each vulnerability
def get_cve_patched(response):
    # creating a list of dictionaries
    charlist = []
    # for loop to go through all the vulnerabilities in the page
    for x in range(0, get_results_per_page(response)):
        # for loop to go through all the references in the vulnerability
        for y in range(0, len(get_vulnerabilities(response)[x]['cve']['references'])):
            # checks if there is a tag
            if 'tags' in get_vulnerabilities(response)[x]['cve']['references'][y]:
                if 'Patch' in get_vulnerabilities(response)[x]['cve']['references'][y]['tags']:
                    # The vulnerability has a patch and the patch value is set to true
                    char_patched = {
                        'cve_id': get_vulnerabilities(response)[x]['cve']['id'],
                        'url': get_vulnerabilities(response)[x]['cve']['references'][y]['url'],
                        'published': get_vulnerabilities(response)[x]['cve']['published'],
                        'lastModified': get_vulnerabilities(response)[x]['cve']['lastModified'],
                        'cvss': get_cvss(response, x),
                        'patch': 1
                    }
                    # appends the dictionary to the list
                    charlist.append(char_patched)
                else:
                    # The vulnerability has no patch and the patch value is set to false
                    char_no_patched = {
                        'cve_id': get_vulnerabilities(response)[x]['cve']['id'],
                        'url': get_vulnerabilities(response)[x]['cve']['references'][y]['url'],
                        'published': get_vulnerabilities(response)[x]['cve']['published'],
                        'lastModified': get_vulnerabilities(response)[x]['cve']['lastModified'],
                        'cvss': get_cvss(response, x),
                        'patch': 0
                    }
                    # appends the dictionary to the list
                    charlist.append(char_no_patched)
            else:
                # The vulnerability has no tag, this means that there is no info, therefore Nan
                char_no_tag = {
                    'cve_id': get_vulnerabilities(response)[x]['cve']['id'],
                    'url': get_vulnerabilities(response)[x]['cve']['references'][y]['url'],
                    'published': get_vulnerabilities(response)[x]['cve']['published'],
                    'lastModified': get_vulnerabilities(response)[x]['cve']['lastModified'],
                    'cvss': get_cvss(response, x),
                    'patch': 'Nan'
                }
                # appends the dictionary to the list
                charlist.append(char_no_tag)
    # returns the list of dictionaries
    return charlist


# an empty list to store all the results
all_results = []

# results per page (default at 2000/page)
resultsPerPage = 2000

# This will help to get the total results of the first page for the range
data_0 = main_request(0)
response_code = requests.get(baseurl).status_code


def data_retrieval():
    # total results
    total_results = 0

    # In case of a timeout or a connection error, the program will exit
    try:
        # checks if the response is 200
        if response_code != 200:
            print("API is not available", response_code)
            exit(1)
        else:
            # For loop to go through all the pages
            for start_index in range(0, get_total_results(data_0), resultsPerPage):
                data = main_request(start_index)
                all_results.extend(get_cve_patched(data))
                total_results = total_results + get_length(data)
        print(total_results, 'vulnerabilities were retrieved')
    except requests.exceptions.RequestException as err:
        raise SystemExit(err)
    print(len(all_results), "links were retrieved")
    return json_file_generation()


def json_file_generation():
    # Gets the current date and time as a string. Year - Month - Day _ Hour - Minute - Second
    current_time = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")

    # Saves the data into a json file with the current date and time
    file_name = f"raw_data_{current_time}.json"

    # Creates the path to save the json file
    file_path = os.path.join(save_path, file_name)

    # Writes the data into a json file
    with open(file_path, "w") as json_file:
        json.dump(all_results, json_file)

    # returns the path to the json file, so it can be used in the next function
    return file_path


if __name__ == "__main__":
    data_retrieval()
