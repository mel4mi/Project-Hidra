# Project-Hidra
![Foto](/media/Screenshot_1.png)
If you assign the request you capture with burp to the project-hydra tool, it will automatically give you the hydra brute force command.


### Logic: 
it checks the login request you specify and stores the required parameter. it gets the IP address and path information from the login request and sends a normal get request. after the get request is registered, it sends another login request with a wrong password attempt and aims to catch the wrong error message. after receiving the error message, it combines all the components and generates the command for Hydra.

### Installation:

```
git clone https://github.com/mel4mi/Project-Hidra.git
```

```
cd Project-Hidra
```

```
pip3 install -r requirements.txt
```

```
python3 Project-Hidra -u <username> -r <request_file.txt>
```



### Example Usage:
1. Capture the Request *
2. Save as a .txt
 ```
  python3 Project-hidra.py -r requests.txt -u admin 
 ```
 ```
  python3 Project-hidra.py -r requests.txt -u admin -p path/to/password_list
 ```
 ```
  python3 Project-hidra.py -r requests.txt -u /path/to/username_list 
 ```

### Example Video

![example](https://github.com/mel4mi/Project-Hidra/blob/main/media/example2.gif)
