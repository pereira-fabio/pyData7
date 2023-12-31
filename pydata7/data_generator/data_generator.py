import requests
from pydata7.scripts.json_file_generation import json_file_generation

# API url
baseurl = 'https://services.nvd.nist.gov/rest/json/cves/2.0'


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


# Small variable function
def vul_cve(response, x):
    return get_vulnerabilities(response)[x]['cve']


# gets the cve url for each vulnerability
def get_cve_patched(response):
    # creating a list of dictionaries
    vulnerabilities_list = []
    # for loop to go through all the vulnerabilities in the page
    for x in range(0, get_results_per_page(response)):
        # for loop to go through all the references in the vulnerability
        for y in range(0, len(vul_cve(response, x)['references'])):
            # checks if there is a tag
            if 'tags' in vul_cve(response, x)['references'][y]:
                if 'Patch' in vul_cve(response, x)['references'][y]['tags']:
                    # The vulnerability has a patch and the patch value is set to true
                    char_patched = {
                        'cve_id': vul_cve(response, x)['id'],
                        'url': vul_cve(response, x)['references'][y]['url'],
                        'published': vul_cve(response, x)['published'],
                        'lastModified': vul_cve(response, x)['lastModified'],
                        'cvss': get_cvss(response, x),
                        'patch': 1
                    }
                    # appends the dictionary to the list
                    vulnerabilities_list.append(char_patched)
                else:
                    # The vulnerability has no patch and the patch value is set to false
                    char_no_patched = {
                        'cve_id': vul_cve(response, x)['id'],
                        'url': vul_cve(response, x)['references'][y]['url'],
                        'published': vul_cve(response, x)['published'],
                        'lastModified': vul_cve(response, x)['lastModified'],
                        'cvss': get_cvss(response, x),
                        'patch': 0
                    }
                    # appends the dictionary to the list
                    vulnerabilities_list.append(char_no_patched)
            else:
                # The vulnerability has no tag, this means that there is no info, therefore Nan
                char_no_tag = {
                    'cve_id': vul_cve(response, x)['id'],
                    'url': vul_cve(response, x)['references'][y]['url'],
                    'published': vul_cve(response, x)['published'],
                    'lastModified': vul_cve(response, x)['lastModified'],
                    'cvss': get_cvss(response, x),
                    'patch': 'n/a'
                }
                # appends the dictionary to the list
                vulnerabilities_list.append(char_no_tag)
    # returns the list of dictionaries
    return vulnerabilities_list


# an empty list to store all the results
all_results = []

# results per page (default at 2000/page)
resultsPerPage = 2000

# This will help to get the total results of the API
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
    return json_file_generation(all_results, "raw_data")


if __name__ == "__main__":
    data_retrieval()
