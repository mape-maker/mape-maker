import pandas as pd


def replace_negative(df, x):
    # and warn about zeros
    index = df[df[x]<0].index
    if len(index) == 0 :
        print("No negative X values found.")
    else:
        print("Replacing negative values by 0 at indexes : ")
        for i, ind in enumerate(index):
            print("     *{}, value = {}".format(ind, float(df.loc[ind][x])))
            if i > 5:
                print("{} negative values replaced and not displayed"\
                      .format(len(index)-5))
                break
        df[df[x] < 0] = 0

    index = df[df[x]==0].index
    if len(index) != 0 :
        print("WARNING: {} X values at zero are present.".\
              format(len(index)))
        
    return df
