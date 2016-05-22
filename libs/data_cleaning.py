def percent_outcome(df,outcome_tag):
    # series should have pandas.DataFrame interface
    # return a pandas.Series of probabilities
    
    return df.groupby(outcome_tag).apply(lambda x:float(len(x))/len(df))
# end def percent_outcome

def age2day(age):
    # convert age column from year,month,week to day
    # use as: df.AgeuponOutcome.apply(age2day)

    if type(age) != type("1 year"):
        return np.nan
    # end if
    num_days = {"year":365,"years":365
                ,"month":30,"months":30
                ,"week":7,"weeks":7
                ,"day":1,"days":1}
    num,unit = age.split()
    return int(num)*num_days[unit]
# end def age2day
