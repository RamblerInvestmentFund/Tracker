import pandas as pd
import os
import datetime as dt
from dateutil.relativedelta import relativedelta
import numpy as np
import performance
import plots
from main import root_path, start_date, symbols, rate, method
#import exposure
import metrics

#Reportlab dependencies
from reportlab.lib.pagesizes import letter, landscape
from reportlab.platypus import *
from reportlab.lib import colors
from reportlab.pdfgen import canvas
from reportlab.lib.units import mm, inch

if not os.path.exists(root_path + '/Reports'):
    os.mkdir(root_path + '/Reports')

end_date = dt.date.today()

class rep():

    def __init__(self, fname, fund_name, logo_path=0):
        self.width, self.height = landscape(letter)
        self.logo_path = logo_path
        self.c = canvas.Canvas(fname, pagesize = landscape(letter))
        self.fund_name = fund_name



    def cover(self):
        fund_name = self.fund_name
        c = self.c
        logo = self.logo_path
        c.setPageSize(landscape(letter))
        print self.height, self.width

        #Title
        c.setFontSize(size=24) #choose your font type and font size
        c.setFillColor(aColor=colors.black)
        c.drawString(x=72,y=420,text=fund_name)

        #Subtitle
        c.setFontSize(size=18)  # choose your font type and font size
        c.setFillColor(aColor=colors.maroon)
        c.drawString(x=72, y=395, text="Portfolio Daily Report: " + str(end_date))

        #Draw Company Logo


        c.drawImage(logo, x = 100 , y=50, width = 600 , height = 300)

        #Line
        c.setFillColor(colors.maroon)
        c.rect(x=0, y=385, height="3", width="842", stroke=0, fill=1)

        #Move to next page
        c.showPage()

    def savePDF(self):
        self.c.save()

import datetime as dt
symbols = ['LVMUY', 'FMS', 'GSK', 'NGG', 'AMZN', 'NLY', 'ARCH', 'BAX', 'BA', 'CELH', 'CL', 'XOM', 'GD', 'LMT', 'MDR', 'MRK', 'MU', 'NOC', 'PANW', 'PXD', 'RTN', 'SNAP', 'TSLA', 'VZ', 'WDC', 'UUP', 'VIXY', 'SHY', 'TLT', 'IAU', 'MINT']
allocations = [158, 250, 1106, 228, 8, 419, 287, 288, 70, 2358, 213, 252, 9, 5, 172, 567, 40, 77, 141, 9, 85, 100, 4, 747, 36, 494, 150, 2490, 425, 6768, 148070]
start_date = dt.date(2019,01,01)
fund_name = "Rambler Investment Fund"
#Benchmark Index
bench_symbol = "SPY"

#RF Syntax: 6 MO, 2 YR etc.
rate = '1 YR'
#CUR, AVG
method = "AVG"

#For Quandl
api_key = ""
root_path = "/Users/zhaoyanbo/Desktop/RIF/nic 4:5:19/Portfolio-Tracker-master"
r = rep(fname=root_path + '/Reports/Daily Report ' + str(end_date) + '.pdf',fund_name=fund_name, logo_path="/Users/zhaoyanbo/Desktop/RIF/nic 4:5:19/Portfolio-Tracker-master/Reports/rif.jpg")

r.cover()
r.savePDF()

#print port_val
#print bench_data
#print float(port_val[port_val.index.isin(dates)])
#print bench_data.index
