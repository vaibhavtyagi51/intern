import requests
from bs4 import BeautifulSoup as bs4
from urllib.request import urlopen
from datetime import datetime
import pandas as pd


def scrap_internshala(data_dict, df):
    for name, url in data_dict.items():

        uClient = urlopen(url)
        internshala_page = uClient.read()
        uClient.close()

        page_beautify = bs4(internshala_page, "html.parser")

        total_no_pages = page_beautify.find("span", {"id":"total_pages"}).text

        try:
            for i in range(1, int(total_no_pages)+1):
                next_url = url+"/page-"+str(i)

                next_page_content = requests.get(next_url)
                beautify_nextPage = bs4(next_page_content.text, "html.parser")
                big_boxes = beautify_nextPage.find_all("div", {"class":"individual_internship"})

                for box in big_boxes:
                    try:
                        now = datetime.now()
                        date_time = now.strftime("%Y-%m-%d %H:%M:%S")
                    except :
                        date_time = "2/11/2020"

                    try:
                        profile = box.find("div", {"class":"profile"}).a.text
                    except:
                        profile = "Nothing"

                    try:
                        company = box.find("div", {"class":"company_name"}).a.text.strip().replace("\n", "")
                    except :
                        company = "Nothing"
                    
                    try:
                        location = box.find("a", {"class":"location_link"}).text
                    except:
                        location = "Nothing"

                    try:
                        start_date = box.find("span", {"class":"start_immediately_desktop"}).text
                    except:
                        start_date = "Nothing"

                    try:
                        stipend = box.find("span", {"class":"stipend"}).text
                    except:
                        stipend = "Nothing"

                    try:
                        duration_row = box.find_all("div", {"class":"other_detail_item"})
                        duration = duration_row[1].find("div", {"class":"item_body"}).text.strip().replace("\n", "")
                    except:
                        duration = "Nothing"

                    try:
                        apply_by = box.find("div", {"class":"apply_by"})
                        apply_by_date = apply_by.find("div", {"class":"item_body"}).text
                    except:
                        apply_by_date = "Nothing"

                    try:
                        offer = box.find("div", {"class":"label_container label_container_mobile"}).text.strip().replace("\n", "")
                    except :
                        offer = "Nothing"


                  
                    myDict = {
                        "Name":name,
                        "Date Time":date_time,
                        "profile":profile, 
                        "company":company,
                        "Location":location,
                        "Start Date":start_date,
                        "Stipend":stipend,
                        'Duration':duration,
                        'Apply by Date':apply_by_date,
                        "Offer":offer,
                    }

                    df = df.append(myDict, ignore_index=True)

            df.to_csv(f"scrapped-dataset/{name}.csv", index=False)    
        except :
            print("Next")
    


if __name__ == '__main__':

    df = pd.DataFrame(columns=['Name', 'Date Time', 'profile', 'company', 'Location', 'Start Date', 'Stipend', 'Duration', 'Apply by Date', 'Offer'])
    data_dict = {
        "INTERNATIONAL": "https://internshala.com/internships/international-internship",
        "CHENNAI": "https://internshala.com/internships/internship-in-chennai",
        "FRESHERS":"https://internshala.com/fresher-jobs",
        "WORKFROMHOME": "https://internshala.com/internships/work-from-home-jobs",
        "DELHI": "https://internshala.com/internships/internship-in-delhi%20ncr",
        "BANGALORE": "https://internshala.com/internships/internship-in-bangalore",
        "MUMBAI": "https://internshala.com/internships/internship-in-mumbai",
        "HYDERABAD": "https://internshala.com/internships/internship-in-hyderabad",
        "KOLKATA": "https://internshala.com/internships/internship-in-kolkata",
    }

    scrap_internshala(data_dict, df)


