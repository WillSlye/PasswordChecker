import requests
import hashlib
import sys

def request_api_data(query_char):
    url = f'https://api.pwnedpasswords.com/range/{query_char}'
    res = requests.get(url)
    if res.status_code != 200:
        raise RuntimeError(f'Error fetching: {res.status_code}, check the api and try again.')
    return res

def get_password_leaks_count(hashes, hash_to_check):
    hashes = (line.split(':') for line in hashes.text.splitlines())
    for h, count in hashes:
        if h == hash_to_check:
            return count
    return 0

def check_password(password):
    sha1password = hashlib.sha1(password.encode('utf-8')).hexdigest().upper()
    first5_char, tail = sha1password[:5], sha1password[5:]
    response = request_api_data(first5_char)
    count = get_password_leaks_count(response, tail)
    return count

def check_passwords(passwords):
    results = []
    for password in passwords:
        count = check_password(password)
        if count:
            results.append(f"{password} was found {count} times... You should probably change your password.")
        else:
            results.append(f"{password} was NOT found! Good password!")
    return results

def main():
    args = sys.argv[1:]
    results = check_passwords(args)
    for result in results:
        print(result)

if __name__ == '__main__':
    main()

# end of file
