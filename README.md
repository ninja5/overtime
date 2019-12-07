# overtime
A python program to calculate overtime from monthly reports

Idea is to extract only overtime from a report from SAP. two types of reports are needed, first is by emplyee second is by project.
First a https://peopledoc.github.io/workalendar/ is used as calendar to detemine the bank holiday on specific country. 
Source is excel file with single sheet where following coulmns must exist(names are explenatory) 'Personnel Number' 'Name of employee or applicant'
'Project time' 'Date TE position' 'Project number'. Simple grapthic interface is made to select the file and generate the report
