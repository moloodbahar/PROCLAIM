
import pandas as pd


def Dateharmonize(x):
    Date=x['value']
#     print(Date)
#     Date=x
    year=''
    day=''
    month=''
    check = False
    check1=False
    fullMonth   = ['JANUARY','FEBURARY','MARCH','APRIL','MAY', 'JUNE','JULY', 'AUGUST', 'SEPTEMBER', 'OCTOBER', 'NOVEMBER', 'DECEMBER']
    Month=['JAN','FEB','MAR','APR','MAY','JUN','JUL','AUG','SEP','OCT',"NOV",'DEC']
    Daynames =['MONDAY', 'TUESDAY', 'WEDNESDAY', 'THURSDAY', 'FRIDAY', 'SATURDAY', 'SUNDAY']
    Daynameabbr = ['MON', 'TUE', 'WED', 'THU', 'FRI', 'SAT', 'SUN']
#     if (len(Date.split('/'))==2 and Date.split("/")[0].find('-')>=-1):
#         Date ==Date.split('/')[1:]
#         print(Date, Date.split('/')[1:])
    Date = Date.replace("/", "-")
    Date = Date.replace(",", " ")
    Date = Date.replace("  ", " ")
    
    if Date.isdigit() and len(Date)>= 8:
        Date=str(Date)[0:8]
        if 1700 <=int(Date[0:4])<2030 and  1<=int(Date[4:6])<=12 and 1<=int(Date[6:8])<=31:
            Date=Date[0:4] + '-'+ Date[4:6]+ '-'+Date[6:8]
        else:
            Date=''                                                                
    if '@' in Date:
         Date = Date.split("@")[0].rstrip()
    if ' ' in Date:
        ngram=Date.split(" ")
#         print(len(ngram))
#         print(Date.find('-'))
        if len(ngram)== 3:
            year=ngram[2]
            month=ngram[1].upper()
            day = ngram[0].upper()
            if day.isdigit():
                day=int(day)
            if month.isdigit():
                month=int(month)
            Date=str(day) + '-'+ str(month) + '-'+ str(year)
        elif len(ngram)== 2 and Date.find('-')== -1 :
            year ='UNKNOWN'
            month=ngram[1].upper()
            day = ngram[0].upper()
            Date= str(day + '-'+ month + '-'+ year)
#     print(Date)
    if len(Date.split(" "))> 2:
            for i in range(0,len(Date.split(" "))):
                if Date.split(" ")[i] in (Month + fullMonth):
                    month= Date.split(" ")[i]
                elif Date.split(" ")[i].isdigit() or Date.split(" ")[i][0:4].isdigit() :
                    if len(Date.split(" ")[i]) ==4 and  1800 <= int(Date.split(" ")[i]) <= 2025 :
                        year= Date.split(" ")[i]
                    elif len(Date.split(" ")[i][0:4])==4 and 1800 <= int(Date.split(" ")[i][0:4]) <= 2025:
                        year= Date.split(" ")[i][0:4]
                    elif len(Date.split(" ")[i]) in [1,2] and (1 <= int(Date.split(" ")[i]) <=31):
                        if day == '':
                            day=Date.split(" ")[i]
                    if len(Date.split(" ")[i]) ==2 and i==(len(Date.split(" "))-1) and year =='':
                        year = Date.split(" ")[i]
            if (month + day +year == ''):
                check = True
                pass
            else:
                Date=str(day + '-'+ month + '-'+ year)
            
#     print('mmm' + Date)
#     print(Date.find('-'))
#     print(Date)
    Date1 = ''.join(i for i in Date if i.isdigit())
    #and (Date1 != Date)
#     print('Date1 is ' + Date1)
    if len(Date.split("-"))< 3:
        Date= Date
        check1=True
#     print(check, check1 , len(Date.split(" ")), len(Date.split("-")), Date.find('-'), Date1, Date)
    if (((check == True) or Date.find('-')>= -1 or ((len(Date.split(" "))<= 2 and Date.find('-')>= -1) and (Date1 != Date))) and check1==False):
#             print(check, check1 , len(Date.split(" ")), len(Date.split("-")), Date.find('-'), Date1, Date)
            year=Date.split("-")[2]
            month=Date.split("-")[1].upper()
            day = Date.split("-")[0]
#             print('here ' + str(Date))
            if month=='SEPT':
                month='SEP'                 
            if year.upper()=='SEPT':
                        year='SEP'
            if day.upper()=='SEPT':
                        day='SEP'
            if year in (fullMonth + Month) and Date.split("-")[3]:
                try: 
                    day=month
                    month= year.upper()
                    year=Date.split("-")[3]
                except KeyError:
                    return Date 
            if day in (fullMonth + Month): 
                    temp= day
                    day=month
                    month=temp
            if day=='0' or month=='0':
                Date= ''
                return Date
#             print( day , month , year)
            if month in fullMonth:
                monthindex =fullMonth.index(month)
                #print(monthindex)
                month= Month[monthindex]
            elif month.isdigit(): 
                if(1 <=int(month)<=12):
                    pass
                else:
                    temp=day
                    day=month
                    month=temp
                if month.isdigit() and 1 <=int(month)<=12:
                    month= Month[int(month)-1]
                else:
                    Date=''
                    return (Date)
            #occur = Month[int(month)-1]
            #occur =Month.index(month)
            for item in ['TH','ND','RD','ST']:
                    if item in day:
                        day=day[:-2]
                    elif item in year:
                        year=year[:-2]
            if len(day.split(' '))> 1 :
                day=day.split(' ')[1]
            if len(year.split(' '))> 1 :
                year=year.split(' ')[0]
#             print('Here' + str(day + '-'+ month + '-'+ year))
            year=''.join(filter(lambda x: x.isdigit(), year))
            day =''.join(filter(lambda x: x.isdigit(), day))
            if day.isdigit() and year.isdigit():
                if (int(day) >= 31 and 1 <= int(year) <= 31):
                    temp=day
                    day=year
                    year=temp
            if len(year.split(' '))> 1:
                    year=year.split(' ')[0]
            if len(day)in [1,2] and len(year)==2:
                    if 32 <= int(year) <= 99:
                        year = '19' + year
                    elif 0 <= int(year) <= 23 :
                        year = '20' + year
            if len(year)==3:
                    if 32 <= int(year[-2:]) <= 99:
                        year = '19' + year[-2:]
                    elif 0 <= int(year[-2:]) <= 23 :
                        year = '20' + year[-2:]
            if len(day)== 4 and len(year)>=2 :
                temp=year[0:2]
                year=day
                day=temp
            if len(year) in [1,2] and len(day)>=4 :
                temp=day[0:4]
                day=year
                year=temp
            return (str(day + '-'+ month + '-'+ year) )
    else:
        for item in (Daynames + Daynameabbr):
            #print(item)
            if item in Date:
                Date = Date.replace(item, "")
                Date = Date.replace(',', "")
        if Date in ['N-A', 'NULL','','UNKNOWN','NOT GIVEN','A'] :
            Date= ''
        return (Date)


#this function is going to use for making a date as 05-nov-2006 as same as 5-nov-2006
def finalDateharmonize(x):
    Date=x['value']
    year=''
    day=''
    month=''
    if '-' in Date:
        ngram=Date.split("-")
        if len(ngram)== 3:
            year=ngram[2]
            #print(year)
            month=ngram[1].upper()
            day = ngram[0].upper()
            if day.isdigit():
                day=int(day)
            if month.isdigit():
                month=int(month)
            if year.isdigit():
                year=int(year)
            Date= Date=str(day) + '-'+ str(month) + '-'+ str(year)
            #print (Date)
    return(Date)

Wbid_f={}
def find_pattern_WBID(x):
    Wbid_f1=[]
    wbid=x['wbi']
    if len(wbid.split('-'))==3:
        Wbid_f1.append(wbid.split('-')[0])
        Wbid_f1.append(wbid.split('-')[1])
        Wbid_f1.append(wbid.split('-')[2])
        if wbid not in  Wbid_f:
                Wbid_f[wbid]=Wbid_f1
    else:
        Wbid_f1.append(wbid)
        Wbid_f[wbid]=Wbid_f1
    return Wbid_f

def cleannonevalueID(df):
    if df['wbi']=="NONE" or df['wbi']=='None' or df['wbi']==None:
        uidw=str(df.uid)
        possibleID=uidw.split("-")[0:3]
        possibleIDstr = str(possibleID[0])+'-'+str(possibleID[1])+'-'+str(possibleID[2])
        df['wbi']=possibleIDstr
        return(possibleIDstr)
    else:
        return(str(df['wbi']))

#chane first wbi to second format
def uniqueid(row):
    wbi=row['wbi']
    labeldf=pd.read_csv('labeldf.csv', sep=',')
    if labeldf['Wbi1'].tolist().count(wbi)>0:
            ind=labeldf[labeldf['Wbi1']==wbi].index.tolist()
            wbiname1=labeldf.loc[ind[0], 'Wbi1'].split('-')
            wbiname2=labeldf.loc[ind[0], 'Wbi2'].split('-')
            if labeldf.loc[ind[0], 'Label']== "1":
                wbi=labeldf.loc[ind[0], 'Wbi2'] 
                row['wbi']=wbi
            # THE FOLLOWING PART IS BASED ON THE FOUND PATTERN FOR MATCHED IDs
            if labeldf.loc[ind[0], 'Wbi2'].replace('-','').isdigit() and labeldf.loc[ind[0], 'Wbi1'].replace('-','').isdigit():
                if int(wbiname1[0])==int(wbiname2[0]) and int(wbiname1[1])==int(wbiname2[1]) and int(wbiname1[2][-1])==int(wbiname2[2]):
                    wbi=labeldf.loc[ind[0], 'Wbi2']
                    labeldf.loc[ind[0], 'Label']= 1
                    row['wbi']=wbi 
    return row['wbi']
        