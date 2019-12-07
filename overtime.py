# -*- coding: utf-8 -*-
"""
Created on Thu Dec  5 10:45:44 2019

@author: Dexter Jr
"""
import datetime

class Employee:    
    def __init__(self, companyID="", name="", rate=0.0,cal=None):
        self.companyID = companyID
        self.name = name
        self.rate = rate
        self.cal=cal
        self.rprt_day_ls = []
        if rate<=0.0:
            print('No rate for '+self.displayID())
        
    def addWorkday(self,**kwargs):
        day = Workday(**kwargs)
        self.rprt_day_ls.append(day)
        
    def displayID(self):
        return '{} {}'.format(self.name, self.companyID)
    
    def has_overtime(self):
        for day in self.rprt_day_ls:
            if day.has_overtime()== True:
                return True
        return False
    def report_001(self):
        week_day=sat_day=sun_day =0.0
        for day in self.rprt_day_ls:
            if day.has_overtime()== True:
                overtime = sum(x[0] for x in day.get_overtime_hours())/8
                if(day.get_date().isoweekday()<6 and day.is_workday()):
                    week_day +=overtime
                elif day.get_date().isoweekday()==6:
                    sat_day += overtime
                else:
                    sun_day +=overtime
        #return '{} {} {} {} {}'.format(self.name, self.companyID,round(week_day,2),round(sat_day,2),round(sun_day,2))
        return [self.name, self.companyID,round(week_day,2),round(sat_day,2),round(sun_day,2)]
    
    def report_002(self):
        result = []
        for day in self.rprt_day_ls:
            if day.has_overtime()== True:
                if(day.get_date().isoweekday()<6 and day.is_workday()):
                    coeficient = 1.5
                elif day.get_date().isoweekday()==6:
                    coeficient = 1.5
                else:
                    coeficient = 2.0 
                for overtime in day.get_overtime_hours():
                    result.append([self.name,self.companyID,int(overtime[1]),round(overtime[0]/8*coeficient,2),round(overtime[0]/8*coeficient*self.rate,2)])
        return result
      
                        
                
                


class Workday:
    def __init__(self, **kwargs): #date = datetime.date.today()):
        self.day = kwargs.pop('date',datetime.date.today())
        self.rpt_time = kwargs.pop('time',[[0.0,0]])
        self.cal = kwargs.pop('calendar',None)
        self.overtime = []
        if  self.cal is not None and self.cal.is_working_day(self.day):
            self.work_day = True
        elif self.day.isoweekday()<6:
            self.work_day = True
        else:
            self.work_day = False
        self.calc_overtime_hours()
        
    def get_date(self):
        return self.day
    
    def get_hours(self):
        return self.rpt_time
    
    def get_overtime_hours(self):
        return self.overtime
    
    def is_workday(self):
        return self.work_day
    
    def calc_overtime_hours(self):
        if self.work_day==False:
            self.overtime = self.rpt_time[:]
            return self.overtime
        work_hour = 8.0
        for a_time in self.rpt_time:
            work_hour = round(work_hour-a_time[0],2)
            if work_hour>=0.0:
                pass
            else:
                self.overtime.append([abs(work_hour),a_time[1]])
                work_hour = 0.0
        return self.overtime
    
    def has_overtime(self):
        if self.overtime == []:
            return False
        else:
            return True
    
                    