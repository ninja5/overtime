# -*- coding: utf-8 -*-
"""
Created on Thu Dec  5 09:53:01 2019

@author: Dexter Jr
"""

import tkinter as tk
from tkinter import filedialog
import datetime
import pandas as pd
import overtime as overtime
from workalendar.europe import Bulgaria # to be imported from https://peopledoc.github.io/workalendar/

report_file_path = ''
rate_file_path = ''
h_ID = 'Personnel Number'
h_name = 'Name of employee or applicant'
h_time = 'Project time'
h_day = 'Date TE position'
h_prj = 'Project number'
h_cost = 'Cost'

def btn_click_rep_file():
    global report_file_path
    report_file_path = filedialog.askopenfilename()
    output.insert('end', '\nSelected report file is: ')
    output.insert('end', report_file_path)
def btn_click_rate_file():
    global rate_file_path
    rate_file_path = filedialog.askopenfilename()
    output.insert('end', '\nSelected rate file is: ')
    output.insert('end', rate_file_path)
def btn_click_report_file():
    cal = Bulgaria() #loaf bulgarian calendar
    empoyee_ls = []
    try:
        df = pd.read_excel(report_file_path) # PATH = r'C:\Users\Ron\Desktop\Import into Python\Sales_' + x1 + '.csv' #(use "r" before the path string to address special character, such as '\'). Don't forget to put the file name at the end of the path + '.csv'
    except:
        df = pd.DataFrame([],columns=[])
    try:
        df_rate = pd.read_excel(rate_file_path)
        df_rate[df_rate.columns[1]]=pd.to_numeric(df_rate[df_rate.columns[1]], errors='coerce')
        df_rate[df_rate.columns[8]]=pd.to_numeric(df_rate[df_rate.columns[8]], errors='coerce')
    except:
        df_rate = pd.DataFrame([],columns=[])
    print(cal.holidays(year=2019))
    user_ls = df[h_ID].unique().tolist() 
    for user in user_ls:
        try:
            rate = df_rate.loc[df_rate[df_rate.columns[1]]==user,df_rate.columns[8]].iat[0]
        except IndexError:
            rate =-1.0
        emp = overtime.Employee(user,df.loc[df[h_ID]==user,h_name].iat[0],rate)
        empoyee_ls.append(emp)
        rep_usr_days_ls = df.loc[df[h_ID]==user,[h_day,h_time,h_prj]].reindex()
        report_days_ls = rep_usr_days_ls[h_day].unique()
        for day in report_days_ls:
            dday = pd.to_datetime(str(day)).replace(tzinfo=None)
            rep_time_per_day = rep_usr_days_ls.loc[rep_usr_days_ls[h_day]==day,[h_time, h_prj]].sort_values(by=[h_time],ascending=False)
            emp.addWorkday(date=dday,time=rep_time_per_day.values.tolist(),calendar=cal)
    print("Done loading")
    report_01 = []
    for empoee in empoyee_ls:
        if empoee.has_overtime():
            row = empoee.report_001()
            report_01.append(row)
            print(row)
    df_rep01 = pd.DataFrame(report_01, columns=[h_name,h_ID,'Weekday','Saturday','Sunday'])
    print("Done report 1")
    report_02 = []
    for empoee in empoyee_ls:
        if empoee.has_overtime():
            report_02.extend(empoee.report_002())
    df_rep02 = pd.DataFrame(report_02, columns=[h_name,h_ID,h_prj,h_time, h_cost])
    pivot  = df_rep02.pivot_table(values=[h_time, h_cost],index=[h_prj],aggfunc='sum',margins=True)
    print(report_02)
    print("Done report 2")        
    f_name = 'report'+datetime.datetime.now().strftime("%Y%m%d-%H%M%S")+'.xlsx'
    with pd.ExcelWriter(f_name) as writer:
        df_rep01.to_excel(writer, sheet_name='Report_01')
        df_rep02.to_excel(writer, sheet_name='Report_02')
        pivot.to_excel(writer, sheet_name='Report_03')
    output.insert('end', '\nDone. Check the report file')

window = tk.Tk()
window.title('Over time')
tk.Label(window, text='Loading report from excel with one sheet. '\
         'Following columns must be present:\n'\
         'Personnel Number\n'\
         'Name of employee or applicant\n'\
         'Project time\n'\
         'Date TE position\n'\
         'Project number\n'\
         'Click on generate file to get the report in the same folder where is executable').grid(row=0, column=0, columnspan=3, sticky='W')
output = tk.Text(window, width=75, height=6, wrap = 'word')
output.grid(row=8, column=0, columnspan=3)
output.insert('end', report_file_path)
tk.Button(window, text="Slect Report file", width=17, command=btn_click_rep_file).grid(row=1, column=0)
tk.Button(window, text="Slect Rate file", width=17, command=btn_click_rate_file).grid(row=1, column=1)
tk.Button(window, text="Generate report file", width=17, command=btn_click_report_file).grid(row=1, column=2)
window.mainloop()




