from sys import argv
import requests


def fetch_npm_package(package_name, version=None):
    url = f"https://registry.npmjs.org/{package_name}"
    response = requests.get(url)
    if response.status_code == 200:     # package found
        package_info = response.json()
        if version:     # specific version
            if version in package_info['versions']:
                return package_info['versions'][version]
            else:
                print("Version not found!")
                return None
        else:
            return package_info
    else:
        print("Package not found!")
        return None


def get_previous_versions(package_name, versions):
    package_info = fetch_npm_package(package_name)
    if package_info == None:
        return None
    if package_name:
        versions = list(package_info['versions'].keys())
    print(versions)


def main():
    if len(argv) != 3:   # the name and at the amount of versions to check
        print("Invalid execution! python main.py {npm_package} {number_of_last_versions}")
        return
    package_name = argv[1]
    versions = int(argv[2])
    if versions <= 1:   # check at least 2 versions
        print("Invalid execution! The amount of versions has to be greater than 1")
        return
    list_versions = get_previous_versions(package_name, versions)
    if list_versions == None:
        return
    print(list_versions)
    
    



if __name__ == "__main__":
    main()