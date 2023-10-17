import requests

# TODO: before everything else, check if it exists -> error 404 or 200
# TODO: if it is 404, then skip it and a tag '404' to the database
# TODO: work with the commit from github. While going through the files, check if commit is in the link
# TODO: if it is, then add it to the database


url = "https://github.com/KDE/kde1-kdebase/commit/04906bd5de2f220bf100b605dad37b4a1d9a91a6"

try:
    r = requests.get(url)
    r.raise_for_status()

    html_content = r.text
    print(html_content)

except requests.exceptions.RequestException as err:
    raise SystemExit(err)