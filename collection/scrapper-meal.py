import datetime
import pandas as pd
import requests
from bs4 import BeautifulSoup
import pickle

data = []
dining_halls = ["bursley", "east-quad", "markley", "mosher-jordan", "north-quad", "south-quad", "twigs-at-oxford"] #list of dining halls
dates = pd.date_range(datetime.datetime(2019, 3, 18),datetime.datetime(2020, 3, 17)).tolist()
# dates = [datetime.datetime(2019, 3, 18)]
for date in dates:
    for dh in dining_halls:
        r = requests.get("https://dining.umich.edu/menus-locations/dining-halls/{}/?menuDate={}".format(dh, str(date.date())))
        soup = BeautifulSoup(r.text, "html5lib")
        course_title = soup.find("div", {"id": "mdining-items"}).find_all("h3")
        course_list = soup.find("div", {"id": "mdining-items"}).find_all("div", {"class": "courses"})
        for i in range(len(course_list)):
                curr_course_items = [x.text for x in course_list[i].find_all("div", {"class":"item-name"})]
                for item in curr_course_items:
                    data.append((item,  "".join(course_title[i].strings), dh, str(date.date())))
        with open('temp.pkl', 'wb') as f:
            pickle.dump(data, f)
    print(f'processed {str(date.date())}...')
print()

with open('final.pkl', 'wb') as f:
            pickle.dump(data, f)

df = pd.DataFrame(x,columns = ['Item','Course','Dining Hall', 'Date'])
df.to_csv('course-data.csv')