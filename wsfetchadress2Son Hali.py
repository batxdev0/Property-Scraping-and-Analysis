
#last upgrade 15.10.2024

#fetchs immobiliere torino properties
# show them by the locations
# show the average prices by room
# possible adding feature: average price of x room by location : no-progress/
from ctypes import addressof
import requests
from bs4 import BeautifulSoup
import re
from collections import defaultdict
baseurl = 'https://www.immobiliare.it/en/vendita-appartamenti/?criterio=rilevanza&utm_source=google&utm_medium=cpc&utm_campaign=search%7Ccategory%7Ccontract%7Cen%7Call%7Cit&gad_source=1&gbraid=0AAAAADOX7jJx3wYe7CkMuMhcPTHXQ1ACO&gclid=CjwKCAjw9p24BhB_EiwA8ID5Bm-p8SqwMTPlYr1ZYgJYVot255vl24s_Ln2HDle8Al5-TPrNjL2G2BoCRPwQAvD_BwE'
header = {
    'User-Agent':'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.4 Safari/605.1.15'
}

locations = [
    "San Paolo", "Superga", "San Donato", "Pozzo Strada", "Nizza Millefonti", 
    "Gran Madre", "Cittadella", "Parella", "Crocetta", "San Secondo", 
    "San Salvario", "Quadrilatero Romano", "Mirafiori Nord", "Giardini Reali", 
    "Cavoretto", "Piazza Solferino", "Cenisia", "Aurora", "Vanchiglia", 
    "Madonna del Pilone", "Borgo Po", "Santa Rita", "Lingotto", "Barriera di Milano", 
    "Regio Parco","Lucento","Vanchiglietta","VITTORIO EMANUELE II","Sassi","Borgo Vittoria",
    "Via Roma","Madonna di Campagna","Cit Turin","Campidoglio","Colle della Maddalena","Rebaudengo",
    "Mirafiori","Le Vallette","Centro Europa","Barriera di Lanzo"
]

productlink = []
for x in range(1, 4):  # Scraping 2 pages, adjust as needed
    r = requests.get(f'https://www.immobiliare.it/en/vendita-case/torino/?pag={x}')
    soup = BeautifulSoup(r.content, 'lxml')
    productlist = soup.find_all('ul', class_='nd-list in-searchLayoutList ls-results')
    for item in productlist:
        for link in item.find_all('a', href=True):
            productlink.append(link['href'])

print(f"Total links found: {len(productlink)}")

def extract_property_features(link):
    r = requests.get(link, headers=header)
    soup = BeautifulSoup(r.content, 'lxml')
    
    title = soup.find('h1', class_='re-title__title')
    title = title.text.strip() if title else "N/A"
    
    price = soup.find('div', class_='re-overview__price')
    price = price.text.strip() if price else "N/A"
    
    
    address_spans = soup.find_all('span', class_='re-title__location')
    addresses = [span.text.strip() for span in address_spans]
    full_address = ", ".join(addresses) if addresses else "N/A"
    
    features = {}
    fets = soup.find('dl', class_='re-featuresGrid__list re-featuresGrid__list--twoColumnsOnMobile')
    if fets:
        for dt, dd in zip(fets.find_all('dt', class_='re-featuresItem__title'),
                          fets.find_all('dd', class_='re-featuresItem__description')):
            features[dt.text.strip()] = dd.text.strip()
    
    return {
        "Title": title,
        "Price": price,
        "Address": full_address,
        "Features": features
    }

location_counts = {location: 0 for location in locations}
total_properties = 0
unfetched_properties = []
# ... [previous code for scraping remains the same] ...

# Initialize a dictionary to store properties for each location
import requests
from bs4 import BeautifulSoup
import re
from collections import defaultdict

# ... [previous code for scraping and extract_property_features function remains the same] ...

# Initialize a dictionary to store properties for each location
total_price_1rooms = 0
count_1rooms = 0
total_price_2rooms = 0
count_2rooms = 0
total_price_3rooms = 0
count_3rooms = 0
total_price_4rooms = 0
count_4rooms = 0
properties_by_location = defaultdict(list)

for index, link in enumerate(productlink, 1):
    property_info = extract_property_features(link)
    
    location_found = False
    for location in locations:
        if re.search(r'\b' + re.escape(location) + r'\b', property_info["Address"], re.IGNORECASE):
            properties_by_location[location].append({
                "Link": link,
                "Title": property_info['Title'],
                "Price": property_info['Price'],
                "Address": property_info['Address'],
                "Features": property_info['Features']
            })
            location_found = True
            break
    if 'Rooms' in property_info['Features'] and property_info['Features']['Rooms'] == '1':
        price_str = property_info['Price']
        price_num = re.findall(r'\d+', price_str.replace(',', ''))
        if price_num:
            price = int(''.join(price_num))
            total_price_1rooms += price
            count_1rooms += 1
        
    if 'Rooms' in property_info['Features'] and property_info['Features']['Rooms'] == '2':
        price_str = property_info['Price']
        price_num = re.findall(r'\d+', price_str.replace(',', ''))
        if price_num:
            price = int(''.join(price_num))
            total_price_2rooms += price
            count_2rooms += 1
            
    if 'Rooms' in property_info['Features'] and property_info['Features']['Rooms'] == '3':
        price_str = property_info['Price']
        price_num = re.findall(r'\d+', price_str.replace(',', ''))
        if price_num:
            price = int(''.join(price_num))
            total_price_3rooms += price
            count_3rooms += 1
    
    if 'Rooms' in property_info['Features'] and property_info['Features']['Rooms'] == '4':
        price_str = property_info['Price']
        price_num = re.findall(r'\d+', price_str.replace(',', ''))
        if price_num:
            price = int(''.join(price_num))
            total_price_4rooms += price
            count_4rooms += 1
    
    if not location_found:
        properties_by_location["Other Areas"].append({
            "Link": link,
            "Title": property_info['Title'],
            "Price": property_info['Price'],
            "Address": property_info['Address'],
            "Features": property_info['Features']
        })
        

# Print properties divided by location
for location, properties in properties_by_location.items():
    print(f"\n{location.upper()} - Total properties: {len(properties)}")
    print("=" * 50)
    
    for idx, prop in enumerate(properties, 1):
        print(f"\nProperty {idx}:")
        print(f"Title: {prop['Title']}")
        print(f"Price: {prop['Price']}")
        print(f"Address: {prop['Address']}")
        print(f"Link: {prop['Link']}")
        print("Features:")
        for key, value in prop['Features'].items():
            print(f"  {key}: {value}")
        print("-" * 30)


    
    print("-" * 50)

# Print summary
print("\nSUMMARY:")
print("=" * 50)
print(f"Total properties scraped: {sum(len(props) for props in properties_by_location.values())}")
print(f"Total locations found: {len(properties_by_location) - 1}")  # Subtract 1 for "Other Areas"
print(f"Properties in other/unfetched areas: {len(properties_by_location['Other Areas'])}")

# Print location counts
print("\nProperties per location:")
for location, properties in sorted(properties_by_location.items(), key=lambda x: len(x[1]), reverse=True):
    if location != "Other Areas":
        print(f"{location}: {len(properties)}")
print(f"Other Areas: {len(properties_by_location['Other Areas'])}")


# Calculate and display the average price for 2-room houses

print("-" * 50)
print("")
print("AVERAGE PRİCES FOR HOUSES PER ROOM")
print("=" * 50)

if count_1rooms > 0:
    avg_price_1rooms = total_price_1rooms / count_1rooms
    print(f"\nAverage price for 2-room houses: €{avg_price_1rooms:,.2f}")
    print(f"Number of 2-room houses found: {count_1rooms}")
else:
    print("\nNo 2-room houses found in the scraped data.")
    
    print("")
    
if count_2rooms > 0:
    avg_price_2rooms = total_price_2rooms / count_2rooms
    print(f"\nAverage price for 2-room houses: €{avg_price_2rooms:,.2f}")
    print(f"Number of 2-room houses found: {count_2rooms}")
else:
    print("\nNo 2-room houses found in the scraped data.")
    
print("")

if count_3rooms > 0:
    avg_price_3rooms = total_price_3rooms / count_3rooms
    print(f"\nAverage price for 3-room houses: €{avg_price_3rooms:,.2f}")
    print(f"Number of 3-room houses found: {count_3rooms}")
else:
    print("\nNo 3-room houses found in the scraped data.")

print("")
    
if count_4rooms > 0:
    avg_price_4rooms = total_price_4rooms / count_4rooms
    print(f"\nAverage price for 4-room houses: €{avg_price_4rooms:,.2f}")
    print(f"Number of 4-room houses found: {count_4rooms}")
else:
    print("\nNo 4-room houses found in the scraped data.")