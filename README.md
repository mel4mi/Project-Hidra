# Project-Hidra
If you assign the request request you capture with burp to the project-hydra tool, it will automatically give you the hydra brute force command.



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

