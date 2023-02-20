import requests
import hashlib
import sys
import re

# Function that queries the Pwned Passwords API for a given set of characters
def request_api_data(query_char):
    url = f'https://api.pwnedpasswords.com/range/{query_char}'
    res = requests.get(url)
    if res.status_code != 200:
        raise RuntimeError(f'Error fetching: {res.status_code}, check the api and try again.')
    return res

# Function that checks the number of times a password has been found in data breaches
def get_password_leaks_count(hashes, hash_to_check):
    # Split the hashes by line and store as tuples with the hash and count
    hashes = (line.split(':') for line in hashes.text.splitlines())
    # Check each tuple for the hash to check and return the count if found
    for h, count in hashes:
        if h == hash_to_check:
            return count
    return 0

# Function that checks the strength of a password and returns suggestions if necessary
def check_password_strength(password):
    # Check the length of the password
    if len(password) < 8:
        return "Your password is too short. Try adding more characters."
    # Check for at least one number
    if re.search('[0-9]', password) is None:
        return "Your password should include at least one number."
    # Check for at least one uppercase letter
    if re.search('[A-Z]', password) is None:
        return "Your password should include at least one uppercase letter."
    # Check for at least one lowercase letter
    if re.search('[a-z]', password) is None:
        return "Your password should include at least one lowercase letter."
    # If no issues are found, return None
    return None

# Function that checks a single password and returns the results
def check_password(password):
    # Hash the password using SHA-1 and convert to uppercase hex format
    sha1password = hashlib.sha1(password.encode('utf-8')).hexdigest().upper()
    # Split the hash into the first five characters and the rest
    first5_char, tail = sha1password[:5], sha1password[5:]
    # Query the API for the first five characters of the hash
    response = request_api_data(first5_char)
    # Check the number of times the password has been found in data breaches
    count = get_password_leaks_count(response, tail)
    return count

# Function that checks multiple passwords and returns the results
def check_passwords(passwords):
    results = []
    for password in passwords:
        # Check the password for data breaches
        count = check_password(password)
        if count:
            # If the password has been found, suggest changing it
            results.append(f"{password} was found {count} times... You should probably change your password.")
        else:
            # If the password has not been found, check the strength and suggest improvements if necessary
            strength_suggestion = check_password_strength(password)
            if strength_suggestion is not None:
                results.append(f"{password} was NOT found! {strength_suggestion}")
            else:
                results.append(f"{password} was NOT found! Good password!")
    return results

# Function that parses command line arguments and prints the results
def main():
    args = sys.argv[1:]
    results = check_passwords(args)
    for result in results:
        print(result)

if __name__ == '__main__':
    main()
