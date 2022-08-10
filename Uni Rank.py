import numpy as np

import pandas as pd

from bs4 import BeautifulSoup
from selenium import webdriver


def getRankData(URL, fileNameToSave):
    driver = webdriver.Firefox()
    driver.get(URL)
    html = driver.page_source

    soup = BeautifulSoup(html, "lxml")
    results = soup.find("table", id="datatable-1")
    find_all_rows = results.find("tbody")
    allTr = find_all_rows.find_all("tr")

    df = pd.DataFrame([], columns=["rank", "name", "location", "student number", "student staff ratio",
                                   "international students percentage", "female male ratio"])  # Creating dataframe

    for itter, curTr in enumerate(allTr):

        rank = curTr.find("td", class_="rank sorting_1 sorting_2")
        try:
            rankText = rank.text
        except:
            rankText = ""

        name = curTr.find("td", class_="name namesearch")

        try:
            nameText = name.text
        except:
            nameText = ""

        location = curTr.find("div", class_="location")
        try:
            locationText = location.text
        except:
            locationText = ""

        student_number = curTr.find("td", class_="stats stats_number_students")
        try:
            student_numberText = student_number.text
        except:
            student_numberText = ""

        student_staff_ratio = curTr.find("td", class_="stats stats_student_staff_ratio")
        try:
            student_staff_ratioText = student_staff_ratio.text
        except:
            student_staff_ratioText = ""

        pc_international_std = curTr.find("td", class_="stats stats_pc_intl_students")
        try:
            pc_international_stdText = pc_international_std.text
        except:
            pc_international_stdText = ""

        female_male_ratio = curTr.find("td", class_="stats stats_female_male_ratio")
        try:
            female_male_ratioText = female_male_ratio.text
        except:
            female_male_ratioText = ""

        df = df.append({"rank": rankText,
                        "name": nameText,
                        "location": locationText,
                        "student number": student_numberText,
                        "student staff ratio": student_staff_ratioText,
                        "international students percentage": pc_international_stdText,
                        "female male ratio": female_male_ratioText}, ignore_index=True)

    df.to_csv(fileNameToSave)


def plottingTest(fileNameToSave):
    df = pd.read_csv(fileNameToSave)
    # newDf = df.replace("=","")
    df["rank"] = df.index.values + 1
    df["student number"] = df["student number"].str.replace(",", "")
    df["international students percentage"] = pd.to_numeric(
        df["international students percentage"].str.replace("%", ""), errors='coerce').fillna(0)
    df["female male ratio"] = df["female male ratio"].fillna("50:50")
    tempArrSplit = df["female male ratio"].str.split(":").values
    df["female percent"] = np.array([curElem[0] for curElem in tempArrSplit]).astype(int)
    df["male percent"] = np.array([curElem[1] for curElem in tempArrSplit]).astype(int)

    df.to_csv("university rank1.csv")


if __name__ == "__main__":
    fileNameToSave = f"UniversityRank.csv"
    URL = "https://www.timeshighereducation.com/world-university-r%C3%A0nkings/2022#!/page/0/length/-1/sort_by/rank/sort_order/asc/cols/stats"

    plottingTest(fileNameToSave)
