import pandas as pd


def replace_negative(df, x):
    index = df[df[x]<0].index
    if len(index) == 0 :
        print("No negative values found. Good to go.")
        return df
    else:
        print("Replacing negative values by 0 at indexes : ")
        for i, ind in enumerate(index):
            print("     *{}, value = {}".format(ind, float(df.loc[ind][x])))
            if i > 5:
                print("{} negative values replaced and not displayed".format(len(index)-5))
                break
        df[df[x] < 0] = 0
        return df

