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
                return None
        else:
            return package_info
    else:
        print("Package not found!")
        return None


def get_previous_versions(package_name, amount_of_versions):
    package_info = fetch_npm_package(package_name)
    if package_info == None:
        return None
    if package_name:
        versions = list(package_info['versions'].keys())[::-1]  # reverse it to go from latest to oldest
        if len(versions) < amount_of_versions:      # checks if there is enough versions
            print("The package has only {} versions".format(len(versions)))
            return None
    return versions[:amount_of_versions]


def get_readme_for_version(package):
    return package.get('readme', '')


def main():
    if len(argv) != 3 or not argv[2].isnumeric():   # checks that the file executed with the right amount of args and format
        print("Invalid execution! python main.py {npm_package} {number_of_last_versions}")
        return
    package_name = argv[1]
    amount_of_versions = int(argv[2])
    if amount_of_versions <= 1:   # check at least 2 versions
        print("Invalid execution! The amount of versions has to be greater than 1")
        return
    package = fetch_npm_package(package_name, '3.3.0')
    print(package.keys())
    # latest_versions = get_previous_versions(package_name, amount_of_versions)
    # if latest_versions == None:
    #     return
    # latest_packages = []
    # for version in latest_versions:
    #     package = fetch_npm_package(package_name, version)
    #     if package == None:
    #         return
    #     latest_packages.append(package)
    # print(get_readme_for_version(latest_packages[0]))
    
    
    



if __name__ == "__main__":
    main()