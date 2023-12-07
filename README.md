# pyData7
## Introduction

The original project was created by [@electricalwind](https://github.com/electricalwind/). The original project can be found [here](https://github.com/electricalwind/data7).

This project will be fully written in Python and will make use of many Python libraries available.

The goal of this project is to regroup all the valid and useful data provided by [NIST](https://nist.gov/). NIST is the National Institute of Standards and Technology, which provides the official API to all the [CVE (Common Vulnerabilities and Exposures)](https://nvd.nist.gov/developers/vulnerabilities) data. Since the data is provided by many sources, it is not always consistent and can be hard to use. Therefore, the goal of this project is to provide data retrieval and data analysis tools to make the data more useful.

The project will use a regular expression (regexp) created by @electricalwind, which will be used to extract Git repositories from the CVE data. Without this filtering, there would be over 800k links, many of which are no longer valid, and many are not Git repositories.

This project will not be by any means perfect, so if anyone wants to contribute, feel free to do so. As this project is my bachelor project, and after it is finished, I will no longer work on it. Therefore, if anyone wants to take over the project, feel free to do so.

## Installation 
For this application to run properly, I used Poetry. Poetry is a python packaging and management tool. It will allow you, the user, to recreate the same environment.

First you need to install Poetry:
``pip install poetry``

Once installed you have to open the project and locate ``pyproject.toml``. This file contains all the required packages and tools for this project.
After that you need to install the packages to do use the following command:``poetry install``

Now that all packages are install, you can use the environment poetry provides to do so use ``poetry shell``.

After all that you can now run ``python run.py`` 

## MongoDB Compass
If you are using MongoDB Compass, I used the `root` and `example` for the login credentials of the database.
I would recommend changing it later on if needed. The database_manager and fastapi folders should contain files with 
those credential if changement is required. I would even say to use a `doevn` file to store does values. 
Note that in the docker compose file the same credentials where used. 
