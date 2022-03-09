import pandas as pd
from pytrends.request import TrendReq
import time

pytrend = TrendReq()
DIVIDER = 20    #Changeable
START_FROM = 15  #Changeable, default should be 0

# getSearchCodes method is not used
def getSearchCodes(keywords):
    keywords_codes = [pytrend.suggestions(keyword=i) for i in keywords]
    df_codes = pd.DataFrame(keywords_codes)
    print(df_codes.head())
    df_codes.to_csv('../data/raw_data/search_codes.csv')

def iterateRawTrends(keywords, date_interval, country, category, search_type):
    print("Total", len(keywords))
    for i in range(START_FROM, DIVIDER): #Separately retrieved to avoid Google's 429 error
        print("Run", i+1)
        print(int(i*(len(keywords))/DIVIDER), int((i+1)*(len(keywords))/DIVIDER-1))
        keywords_temp = keywords[int(i*(len(keywords))/DIVIDER):int((i+1)*(len(keywords))/DIVIDER)]
        getRawTrends(keywords_temp, date_interval, country, category, search_type, 'trends_raw'+str(i+1)+'.csv')

def getRawTrends(keywords, date_interval, country, category, search_type, filename):
    individual_keywords = list(zip(*[iter(keywords)] * 1))
    individual_keywords = [list(x) for x in individual_keywords]
    print(individual_keywords)
    dicti = {}
    i = 1
    for keyword in individual_keywords:
        pytrend.build_payload(kw_list=keyword, timeframe=date_interval, geo=country, cat=category, gprop=search_type)
        dicti[i] = pytrend.interest_over_time()
        i += 1
        time.sleep(1)
    df_trends = pd.concat(dicti, axis=1)
    df_trends.columns = df_trends.columns.droplevel(0)
    df_trends = df_trends.drop('isPartial', axis=1)
    print(df_trends.head())
    df_trends.to_csv(f'../data/raw_data/{filename}')

def combineRawFiles():
    df_trends = pd.read_csv('../data/raw_data/trends_raw1.csv')
    for i in range(1, DIVIDER):
        df_read = pd.read_csv('../data/raw_data/trends_raw'+str(i+1)+'.csv')
        print(df_read.head())
        df_trends = pd.merge(df_trends, df_read, on="date")
    df_trends.to_csv('../data/clean_data/aggregate_trends_raw.csv')

def cleanSum():
    df_trends = pd.read_csv('../data/clean_data/aggregate_trends_raw.csv')
    df_trends['date'] = pd.to_datetime(df_trends['date'])
    df_trends = df_trends.groupby(df_trends.date.dt.year).sum()
    df_trends.to_csv('../data/clean_data/trends_cleaned.csv')  #final output file


def main():
    df_salary = pd.read_csv('../data/clean_data/player_salary.csv')
    keywords = df_salary.Player.unique()
    #getSearchCodes(keywords)
    #df_codes = pd.read_csv('search_codes.csv')
    #keywords = df_codes['mid'].to_list()
    date_interval = '2004-01-01 2020-12-31'
    country = ''
    category = 0
    search_type = ''
    iterateRawTrends(keywords, date_interval, country, category, search_type)
    combineRawFiles()
    cleanSum()


if __name__ == "__main__":
    main()
