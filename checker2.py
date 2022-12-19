import asyncio
import xmltodict
import aiohttp
#Sems ve Klaxxon tarafından itina ile kodlanmıştır
i = 0
async def fetch(session, url):
	global i
	try:
		async with session.request(method="GET", url=url, timeout=10) as resp:
			result = await resp.text()
			status = resp.status
	except asyncio.TimeoutError:
		result = "Problem: TimeoutError"
	except aiohttp.client_exceptions.TooManyRedirects:
		result = "Problem: TooManyRedirects"
	except aiohttp.client_exceptions.ClientOSError:
		result = "Problem: ClientOsError The specified network name is no longer available"
	except aiohttp.client_exceptions.ServerDisconnectedError:
		result = "Problem: Server disconnected"
	except Exception as e:
		result = "Problem: "+e.args[1].strerror

	i += 1
	print(f"try count {i}: "+url,end="")
	if result.startswith("Problem"):
		print("-> "+result)
		return
	elif "<!doctype>" in result.lower() or "<html>" in result.lower():
		print("-> Burası html dönütü verdi.")
		return
	elif status != 403:
		print("-> 403 dönmüyor")
		return
	try:
		resp_dict = xmltodict.parse(result)
	except:
		print("Şu mesajı alıyorsan bir problem var demektir benle irtibata geç. Sems")
		exit()
	if "Error" in resp_dict and resp_dict["Error"]["Code"] == "AccessDenied":
		print("-> Sömürülmeye müsait gözükmekte")
		open("akamai.txt", "a").write(url + "\n")

async def main(urls):
	tasks = []
	async with aiohttp.ClientSession() as session:
		for url in urls:
			task = asyncio.ensure_future(fetch(session, url))
			tasks.append(task)
			if len(tasks) > 100:
				await asyncio.gather(*tasks)
				tasks = []
		if len(tasks) <= 100:
			await asyncio.gather(*tasks)
	# results is a list of everything that returned from fetch().
	# do whatever you need to do with the results of your fetch function
if __name__ == "__main__":
	import pathlib
	here = pathlib.Path(__file__).parent
	load = input("Taranıcak siteleri uzatın  > ")
	try:
		with open(here.joinpath(load)) as infile:
			urls = [x if x.startswith("http") else "http://"+x for x in infile.read().strip().splitlines()]
	except FileNotFoundError:
		print("Böyle bir dosya yok")

	asyncio.get_event_loop().run_until_complete((main(urls)))