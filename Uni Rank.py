import numpy as np  # import numpy

import pandas as pd  # import pandas

from bs4 import BeautifulSoup  # import beautifulsoup
from selenium import webdriver  # import webdriver


def getRankData(URL, fileNameToSave):
    driver = webdriver.Firefox()
    driver.get(URL)
    html = driver.page_source

    soup = BeautifulSoup(html, "lxml")  # use beautifulsoup to get lxml info
    results = soup.find("table", id="datatable-1")  # find "table" under in="datatable-1"
    find_all_rows = results.find("tbody")  # find "tbody" from results
    allTr = find_all_rows.find_all("tr")  # find all "tr" info from find_all_rows

    df = pd.DataFrame([], columns=["rank", "name", "location", "student number", "student staff ratio",
                                   "international students percentage", "female male ratio"])  # Creating dataframe

    for itter, curTr in enumerate(allTr):

        rank = curTr.find("td", class_="rank sorting_1 sorting_2")
        # find "td" under "rank sorting_1 sorting_2"
        try:
            rankText = rank.text  # try to get text from rank
        except:
            rankText = ""  # if there is no text info from rank, then leave it empty

        name = curTr.find("td", class_="name namesearch")
        # find "td" under class="name namesearch"
        try:
            nameText = name.text  # try to get text from name
        except:
            nameText = ""  # if there is no text info from name, then leave it empty

        location = curTr.find("div", class_="location")
        # find "div" under class="location"
        try:
            locationText = location.text  # try to get text info from location
        except:
            locationText = ""  # if there is no text info from location,then leave it empty

        student_number = curTr.find("td",class_="stats stats_number_students")
        # find "td" under class "stats stats_number_students"
        try:
            student_numberText = student_number.text  # try to get text from student_numbertext
        except:
            student_numberText = ""  # if there is no text info from student_number, then leave it empty

        student_staff_ratio = curTr.find("td", class_="stats stats_student_staff_ratio")
        # find "td"under class="stats stats_student_staff_ratio"
        try:
            student_staff_ratioText = student_staff_ratio.text # try to get text from stats stats_student_staff_ratio
        except:
            student_staff_ratioText = ""  # if there is no text info from stats stats_student_staff_ratio,leave it empty

        pc_international_std = curTr.find("td", class_="stats stats_pc_intl_students")
        # find "td" under class_= stats stats_pc_intl_students
        try:
            pc_international_stdText = pc_international_std.text # try to get text from pc_international_std
        except:
            pc_international_stdText = ""  # if there is no text info from pc_international_std,then leave it empty

        female_male_ratio = curTr.find("td", class_="stats stats_female_male_ratio")
        # find "td" under class_=stats stats_female_male_ratio
        try:
            female_male_ratioText = female_male_ratio.text # try to get text from female_male_ratio
        except:
            female_male_ratioText = "" # if there is no text info from female_male_ratio, then leave it empty

        df = df.append({"rank": rankText,
                        "name": nameText,
                        "location": locationText,
                        "student number": student_numberText,
                        "student staff ratio": student_staff_ratioText,
                        "international students percentage": pc_international_stdText,
                        "female male ratio": female_male_ratioText}, ignore_index=True)
         # call the function and append them
    df.to_csv(fileNameToSave)   # save it as csv file


def plottingTest(fileNameToSave):
    df = pd.read_csv(fileNameToSave)   # read csv file
    df["rank"] = df.index.values + 1   # set rank column as index,then get the value, add number 1
    df["student number"] = df["student number"].str.replace(",", "")
    # get the string from student number column and replace comma by empty space
    df["international students percentage"] = pd.to_numeric(
        df["international students percentage"].str.replace("%", ""), errors='coerce').fillna(0)
    df["female male ratio"] = df["female male ratio"].fillna("50:50") # fill the empty cell with "50:50"
    tempArrSplit = df["female male ratio"].str.split(":").values
      # get the string of column "female male ratio" and split the number into two part, then get values
    df["female percent"] = np.array([curElem[0] for curElem in tempArrSplit]).astype(int)
    # add "female percent" column by getting this from the split values
    df["male percent"] = np.array([curElem[1] for curElem in tempArrSplit]).astype(int)
    # add "male percent" column by getting this from the split values
    df.to_csv("university rank1.csv")  # save this file named "university rank1" and csv type


if __name__ == "__main__":
    fileNameToSave = f"UniversityRank.csv"
    URL = "https://www.timeshighereducation.com/world-university-r%C3%A0nkings/2022#!/page/0/length/-1/sort_by/rank/sort_order/asc/cols/stats"

    plottingTest(fileNameToSave)
