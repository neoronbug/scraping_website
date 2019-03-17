
# ----------------------------- Collects All Details About Softwares ------------------------------  

import requests
import bs4 as bs
import json
with open("article_links.json") as file:
	links = json.load(file)

keys = [i for i in links.keys()]

full_dict_of_values = dict()
itr = 1
for link in keys:
	url = links[link]
	req = requests.get(url)
	soup = bs.BeautifulSoup(req.text, 'lxml')
	content = soup.body.find("h1",{"class":"title-text"})

	full_name = content.findAll("span",{}) # Full Name of Software
	name = full_name[0].text
	version = full_name[1].text

	technical_page = soup.find("div",{"class":"tab-content clearfix"})
	technical_page.find("div",{"id":"2b"})
	values = technical_page.findAll("span",{"class":"field-value"})
	try:
		soft_main_link = links[link] # Filehippo main link 

		main = str(values[7]) #  Author Name & Website
		end = str(values[7]).index("<br/>")
		sliced = main[:end]
		start = sliced.rfind("  ")
		author_name = main[start:end]
		author_website = values[7].a["href"]

		download_link = str(values[1]) # Download link in exe or zip
		final_link = download_link
		start_lisc = sliced.rfind("  ")
		end_link = download_link.find("</span>")
		final_link_val = download_link[start_lisc:end_link]

		liscence = str(values[5]) # Liscence 
		final_lis = liscence
		start_lisc = sliced.rfind("  ")
		end_lisc = liscence.find("</span>")
		liscence_value = liscence[start_lisc:end_lisc]
	except:
		final_link_val = "missing"
		author_name    = "missing" 
		author_website = "missing"
		liscence_value = "missing"

	data_array = [] # Writes Final Values to Dictionay
	data_array.append(link)
	data_array.append(final_link_val)
	data_array.append(version)
	data_array.append(author_name)
	data_array.append(author_website)
	data_array.append(liscence_value)
	data_array.append(soft_main_link)
	full_dict_of_values[link] = data_array


	print(itr, "/",len(keys)," Epochs are Completed!!!")
	itr = itr+1


with open("updated_values_filehippo.json", "w") as file:
	json.dump(full_dict_of_values, file, indent=2)

# --------------------------------  Json Data to CSV --------------------------

import json
import pandas as pd 

with open("updated_values_filehippo.json") as file:
	data = json.load(file)

key = [i for i in data.keys()]
values = [data[ke] for ke in key]

df = pd.DataFrame(values, columns=["Name","Download Link", "Version", "Author Name", "Developer Link", "Liscence", "Software Link"])
df.to_csv("update_csv_filehippo.csv")
