import asyncio
import aiohttp
import json
from pydata7.links_analysis.link_filter import data_filtering
from pydata7.scripts.json_file_generation import json_file_generation

# Path to the data from the data_generator
path_to_json = data_filtering()

# For testing purposes
# path_to_json = "../data/filtered_data_2023-10-31_14-38-50.json"

# A list to store the data that contains a commit
contains_commit = []
contains_issues = []

with open(path_to_json, "r") as file:
    data = json.load(file)


def has_commit():
    for item in data:
        if "commit" in item["url"]:
            # Get the organization and project name from the url
            # For GitHub links only
            organization_project = item["url"].split("/")[3:5]
            # Add the organization and project name to the dictionary
            item["organization_project"] = organization_project
            # Add the dictionary to the list
            contains_commit.append(item)
        elif "issues" in item["url"]:
            # Add the dictionary to the list
            contains_issues.append(item)
    # This is generated if needed later
    json_file_generation(contains_issues, "contains_issues")
    # This is the main function that will be used
    return json_file_generation(contains_commit, "contains_commit")


def get_github_projects():
    temp = []

    with open(has_commit(), "r") as f:
        valid_commit_links = json.load(f)

    for item in valid_commit_links:
        parts = item["url"].split("/")
        repository = "https://" + parts[2] + "/" + parts[3] + "/" + parts[4]
        # If temp is empty, add the first repository
        if temp == []:
            temp.append(repository)
        # If the repository is not in temp, add it and check if the link is valid
        if repository not in temp:
            temp.append(repository)

    print(len(temp), "repositories were found")
    return json_file_generation(temp, "temp")


# Async function to check the links much faster
valid_link = []
not_valid_link = []


async def is_valid():
    # valid_link = []
    # Create a session
    async with aiohttp.ClientSession() as session:
        # Get the GitHub projects link
        with open(get_github_projects(), "r") as f:
            github_projects = json.load(f)

        # Async function to check the links
        async def check_url(url):
            try:
                # Send a request to the url
                async with session.head(url) as response:
                    # Check if the response is 200
                    if response.status == 200:
                        # Add the link to the list
                        valid_link.append(url)
                    else:
                        # Print the response code
                        # print(url, response.status)
                        not_valid_link.append(url)
            # Print the error if there is any
            except Exception as e:
                print(f"Error:{url}, {e}")

        # Run the async function
        await asyncio.gather(*[check_url(url) for url in github_projects])

    return json_file_generation(valid_link, "valid_link")


if __name__ == "__main__":
    asyncio.run(is_valid())
    print(len(valid_link), "valid links were found")
    print(len(not_valid_link), "not valid links were found")
