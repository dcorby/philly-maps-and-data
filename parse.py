import sys
import pandas as pd
import re
import pprint as pp

pathname = "/home/dmc7z/dev/philly/data/housing-characteristics/ACSDP5Y2021.DP04-Data.csv"

def get():
    df = pd.read_csv(pathname, skiprows=1)
    """ Drop columns we don't need """
    def drop_column(name):
        if name in ["Geography", "Geographic Area Name"]:
            return False
        if re.match("Estimate.*YEAR STRUCTURE BUILT.*Total housing units", name):
            return False
        return True
    df.drop(columns=[c for c in df if drop_column(c)], inplace=True)

    """ Rename columns """
    to_rename = {}
    for frm in df.columns:
        to = frm
        to = to.replace("Estimate!!YEAR STRUCTURE BUILT!!Total housing units", "")
        to = to.replace("Built ", "").replace(" ", "-").replace("!!", "")
        if to == "":
            to = "total"
        to = to.lower()
        to_rename[frm] = to
    df.rename(columns=to_rename, inplace=True)

    """ Drop rows with <= 100 houses """
    df = df[df["total"] >= 100]

    """ Calc the weighted mean range """
    fields = ["2020-or-later", "2010-to-2019", "2000-to-2009", "1990-to-1999", "1980-to-1989", 
                "1970-to-1979", "1960-to-1969", "1950-to-1959", "1940-to-1949", "1939-or-earlier"]

    # https://stackoverflow.com/questions/19914937/applying-function-with-multiple-arguments-to-create-a-new-pandas-column
    def mean(x):
        wt_sum = 0.0
        for field in fields:
            wt_sum += x[field]*fields.index(field)
        return wt_sum / x["total"]
    df["mean"] = df.apply(lambda x: mean(x), axis=1)

    return fields, df

if __name__ == "__main__":
    get()
