import requests
import warnings
from multiprocessing.dummy import Pool as ThreadPool
from colorama import *
#Coded by Klaxxon and Sems
headers = {
	"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:107.0)"
}

def check(url):
	try:
		if 'http' not in url:
			url = 'https://' + url
		req = requests.get(url, headers=headers, timeout=3)
		if "AccessDenied" in req.text:
			print(Fore.GREEN + "Akamai " + url)
			open("akamai.txt", "a").write(url + "\n")
		if "AccessDenied" not in req.text:
			print(Fore.RED + "Akamai Değil " + url)
	except:
		pass

def loadlist():
    try:
        load = input("Enter a List  > ")
        try:
            with open(load, 'r') as (get):
                read = get.read().splitlines()
        except IOError:
            pass
        read = list(read)
        try:
            pp = ThreadPool(100)
            pr = pp.map(check, read)
        except:
            pass
    except:
        pass
loadlist()
		