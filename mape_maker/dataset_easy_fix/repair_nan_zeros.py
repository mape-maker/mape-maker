import pandas as pd


def replace_negative(logger, df, x):
    # and warn about zeros
    index = df[df[x]<0].index
    if len(index) == 0 :
        logger.info("No negative X values found.")
    else:
        logger.info("Replacing negative values by 0 at indexes : ")
        for i, ind in enumerate(index):
            logger.info("     *{}, value = {}".format(ind, float(df.loc[ind][x])))
            if i > 5:
                logger.info("{} negative values replaced and not displayed"\
                      .format(len(index)-5))
                break
        df[df[x] < 0] = 0

    index = df[df[x]==0].index
    if len(index) != 0 :
        logger.warning("WARNING: {} X values at zero are present.".\
              format(len(index)))
        
    return df
