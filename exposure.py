from urllib import urlopen
from bs4 import BeautifulSoup as soup
import requests,ssl
import pandas as pd
from main import root_path, symbols
import inspect
import matplotlib.pyplot as plt




def info(s = symbols):
    sector_info = pd.DataFrame()
    industry_info = pd.DataFrame()
    weights = pd.read_csv(root_path + '/Daily Data/Portfolio/Portfolio Weights.csv', index_col=0)

    for symbol in s:
        if symbol == 'MINT':
            sector = 'Cash'
            industry = 'Cash'
            sector_info = sector_info.append({'Sector': sector, 'Symbol': symbol}, ignore_index=True)
            industry_info = industry_info.append({'Industry': industry, 'Symbol': symbol}, ignore_index=True)
            continue
        #print symbol,'--------'
        url = 'https://finance.yahoo.com/quote/{0}/profile?p={0}'.format(symbol)
        handle = urlopen(url,context=ssl._create_unverified_context())
        page_html = handle.read()
        handle.close()

        page_soup = soup(page_html, "html.parser")



        try:
            sector_and_industry = page_soup.findAll("span", {"class" : "Fw(600)"})
            if sector_and_industry:
                sector = list(sector_and_industry[0])[0]
                industry = list(sector_and_industry[1])[0]
            else:
                category  = page_soup.findAll("span", {"class" : "Fl(end)"})
                sector = list(category[-1])[0]
                industry = list(category[0])[0]


        except:

            sector = "Others"
            industry = "Others"




        sector_info = sector_info.append({'Sector': sector, 'Symbol': symbol}, ignore_index=True)
        industry_info = industry_info.append({'Industry': industry, 'Symbol': symbol}, ignore_index=True)


    sector_info.set_index('Symbol', inplace=True)
    industry_info.set_index('Symbol', inplace=True)

    #csv file of sector and industry
    Asset_exposure = pd.concat([sector_info, industry_info], axis=1)
    Asset_exposure.to_csv(root_path+'/Daily Data/Portfolio/Asset exposure.csv', index=True)

    #csv file of sectoral weights
    Sectoral_weights = pd.concat([sector_info, weights], axis = 1)
    Sectoral_weights.columns = ["Sector", "Weight"]

    Sectoral_weights = Sectoral_weights.groupby(['Sector']).sum()
    Sectoral_weights.to_csv(root_path+'/Daily Data/Portfolio/Sectoral Weights.csv', index=True)

    plt.pie(
        Sectoral_weights["Weight"],
        labels=Sectoral_weights.index,
        shadow=False,
        startangle=90,
        autopct='%1.1f%%',
    )

    plt.axis('equal')
    plt.suptitle('Sectoral Weights')

    plt.savefig(root_path + '/Figures/sec_ind.png')

    call_name = inspect.stack()[1][3]

    if call_name != "diversification":
        plt.show()
