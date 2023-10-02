# Project-Hidra
![Foto](/media/Screenshot_1.png)
If you assign the request request you capture with burp to the project-hydra tool, it will automatically give you the hydra brute force command.




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


[<img src="https://github.com/mel4mi/Project-Hidra/blob/main/media/Screenshot_1.png" width="50%">](https://github.com/mel4mi/Project-Hidra/blob/main/media/project-hidra.mp4 "Now in Android: 55")
