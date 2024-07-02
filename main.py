from sys import argv
from re import sub, search
import requests
from openai import OpenAI
import google.generativeai as palm


OPENAI_API_KEY = ''
GOOGLE_API_KEY = 'AIzaSyBmorRwYPDzpmHTRybhvPE7C_sBhUqhuRU'



def execution_checker():
    if len(argv) != 3 or not argv[2].isnumeric():   # checks that the file executed with the right amount of args and format
        print("Invalid execution! python main.py {npm_package_name} {number_of_last_versions}")
        return False
    if int(argv[2]) <= 1:   # check at least 2 versions
        print("Invalid execution! The amount of versions has to be greater than 1")
        return False
    return True


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
    url = package.get('repository')
    if url == None:
        print("Repository not found!")
        return None, None
    url = url["url"]
    url = sub(r'^git\+|\.git$', '', url)  # Clean up the URL
    return url.split(".com/")[1].split("/")


def get_repo_tags(owner, repo):
    url = f"https://api.github.com/repos/{owner}/{repo}/tags"
    response = requests.get(url)
    if response.status_code == 200:     # repo found
        tags = response.json()
        return [tag['name'] for tag in tags if not search(r'[a-zA-Z]', tag['name'])]     # only versions
        # return [tag['name'] for tag in tags]      # with betas and alphas
    else:
        print("Repo not found!")
        return None


def get_readme_content(owner, repo, tag):
    url = f"https://api.github.com/repos/{owner}/{repo}/readme"
    headers = {"Accept": "application/vnd.github.VERSION.raw"}
    params = {"ref": tag}
    response = requests.get(url, headers=headers, params=params)
    if response.status_code == 200:
        return response.text
    return None


def chatgpt_ans(readmes):
    client = OpenAI(api_key=OPENAI_API_KEY)
    prompt = "I have an npm package with multiple README files, each corresponding to a different version. I will provide you with {amount} README files. Please compare the README files for each consecutive version and identify and summarize any breaking changes. {readmes}".format(amount=len(readmes), readmes=str(readmes.values()))
    chat_completion = client.chat.completions.create(
        messages = [
            {
                "role": "user", 
                "content": prompt
            }
        ],
        model="gpt-3.5-turbo"
    )
    return chat_completion.choices[0].message.content


def google_ai_ans(readmes):
    palm.configure(api_key=GOOGLE_API_KEY)
    prompt = "I have an npm package with multiple README files, each corresponding to a different version. I will provide you with {amount} README files. Please compare the README files for each consecutive version and identify and summarize any breaking changes. {readmes}".format(amount=len(readmes), readmes=str(readmes.values()))
    completion = palm.generate_text(
        model='models/text-bison-001',
        prompt=prompt,
        temperature=0,
        candidate_count=1
    )
    return completion.candidates[0]["output"]


def main():
    if not execution_checker():
        return
    package_name = argv[1]
    amount_of_versions = int(argv[2])
    package = fetch_npm_package(package_name)
    if package == None:     # check if found
        return
    owner, repo = get_owner_repo(package)
    if owner == None or repo == None:     # check if found
        return
    tags = get_repo_tags(owner, repo)
    if tags == None:     # check if found
        return
    if len(tags) < amount_of_versions:      # check if there is enough versions
        print("There is only {amount} versions to this package".format(len(tags)))
        return
    latest_tags = tags[:amount_of_versions]  # Get the amount_of_versions latest tags
    readmes = {}
    for tag in latest_tags:
        readme_content = get_readme_content(owner, repo, tag)
        if readme_content == None:     # check if found
            print("Couldn't find README file for verison {version}".format(tag))
        elif readme_content:
            readmes[tag] = readme_content
    print(google_ai_ans(readmes))
    # print(chatgpt_ans(readmes))   # if you want to use chatgpt


if __name__ == "__main__":
    main()