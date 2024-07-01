from sys import argv
import re
import requests


def fetch_npm_package(package_name, version=None):
    url = f"https://registry.npmjs.org/{package_name}"
    if version:
        url += f"/{version}"
    response = requests.get(url)
    if response.status_code == 200:     # package found
        package_info = response.json()
        return package_info
    else:
        print("Package not found!")
        return None


def get_owner_repo(package):
    url = package.get('repository')['url']
    url = re.sub(r'^git\+|\.git$', '', url)  # Clean up the URL
    return url.split(".com/")[1].split("/")



def get_repo_tags(owner, repo):
    url = f"https://api.github.com/repos/{owner}/{repo}/tags"
    response = requests.get(url)
    response.raise_for_status()
    tags = response.json()
    return [tag['name'] for tag in tags if not re.search(r'[a-zA-Z]', tag['name'])]     # only versions
    # return [tag['name'] for tag in tags]      # with betas and alphas


def get_readme_content(owner, repo, tag):
    url = f"https://api.github.com/repos/{owner}/{repo}/readme"
    headers = {"Accept": "application/vnd.github.VERSION.raw"}
    params = {"ref": tag}
    response = requests.get(url, headers=headers, params=params)
    if response.status_code == 200:
        return response.text
    return None


def main():
    if len(argv) != 3 or not argv[2].isnumeric():   # checks that the file executed with the right amount of args and format
        print("Invalid execution! python main.py {npm_package} {number_of_last_versions}")
        return
    package_name = argv[1]
    amount_of_versions = int(argv[2])
    if amount_of_versions <= 1:   # check at least 2 versions
        print("Invalid execution! The amount of versions has to be greater than 1")
        return
    package = fetch_npm_package(package_name)
    owner, repo = get_owner_repo(package)
    tags = get_repo_tags(owner, repo)
    latest_tags = tags[:amount_of_versions]  # Get the three latest tags
    readmes = {}
    for tag in latest_tags:
        readme_content = get_readme_content(owner, repo, tag)
        if readme_content:
            readmes[tag] = readme_content
    print(list(readmes.keys()))


if __name__ == "__main__":
    main()