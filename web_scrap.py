
# ------------------------------ Importing Libraries ---------------------------------------

import bs4 as bs
import requests
import json
import pandas as pd

# ------------------------------------------------------------------------------------------

url = "https://filehippo.com/info/sitemap/"
req = requests.get(url)

final_links = []
soup = bs.BeautifulSoup(req.text, 'lxml')
main_links = soup.findAll('div',{"class":"sitetext"})

for url in main_links:
	link_list = url.findAll('ul',{"class":"windows-software"})
	for i in link_list:
		z = i.findAll("li")
		for x in z:
			final_links.append(x.a["href"])

with open ("windows-software.txt","w+") as file:
	for i in final_links:
		file.write(i)
		file.write(",")

# ------------------------------------- Section Completed ------------------------------------------
#  This will find out all the links to any of the filehippo sub page if there is any Internal  page. 
# -------------------------------------------><><---------------------------------------------------


final_links = []
with open ("windows-software.txt","r") as file:
	data = file.read()
	for i in data.split(","):
		final_links.append(i)
sub_links = []
iter = 1
for inner_url in final_links:

	req = requests.get(inner_url)
	soup = bs.BeautifulSoup(req.text, 'lxml')
	content = soup.body.findAll("div",{"class":"pager-container"})
	if content ==[]:
		sub_links.append(inner_url)
	else:
		val = content[0]
		a_tags = val.findAll("a",{"class":"pager-page-link"})
		sub_links.append(inner_url)
		for i in a_tags:
			sub_links.append(i["href"])
	print(iter, " Epoch Completed")
	iter +=1
with open ("final_windows_links.txt","w+") as file:
	for i in sub_links:
		file.write(i)
		file.write(",")

# ------------------------------------- Section 2 Completed ----------------------------------------
#                       This will find names of Articles from all gives links. 
#  ------------------------------------------><><---------------------------------------------------


final_links = []
with open ("final_windows_links.txt","r+") as file:
	links = file.read()
	for i in links.split(","):
		final_links.append(i)

name_list = []
itr = 1
for inner_url in final_links:
	req = requests.get(inner_url)
	soup = bs.BeautifulSoup(req.text, 'lxml')
	content = soup.body.findAll("div",{"class":"pager-container"})
	links_to_pages = soup.body.findAll("div",{"class":"program-entry-header"})
	for i in links_to_pages:
		name_list.append(i.a.text)
		name_list.append(i.a["href"])
	print(itr, "Page Completed....")
	itr+=1

with open ("final_names_and_links.txt","w+") as file:
	for i in name_list:
		file.write(i)

# # ============================ Compare files & Create Json-CSV ===============================



data = [ """ list of all the names and links that you get in final_names_and_links.txt""" ]

words_to_links = dict(zip(data[::2],data[1::2]))

with open('filehippo.json', 'w') as file:
	json.dump(words_to_links, file, indent = 2)

with open('filehippo.json') as file:
	data = json.load(file)

# ---------------

names1 = []
names2 = []
final_names = []

with open('filehippo.json') as file:
	data_json = json.load(file)
for i in data_json.keys():
	names1.append(i)

with open ("softonyx_articles.txt", "r+") as file:
	data = file.read()
for i in data.split("\n"):
	names2.append(i)

for i in names1:
	if i in names2:
		pass
	else:
		final_names.append(i)
final_dict = dict()
for i in final_names:
	final_dict[i] = data_json[i]

with open("missing_articles.json", "w") as file:
	json.dump(final_dict, file, indent = 2)

with open("missing_articles.json") as file:
	json_data = json.load(file)

data_frame = pd.DataFrame(final_dict.items(), columns = ["Articles Name", "Links"])
data_frame.to_csv("excel_filehippo.csv")