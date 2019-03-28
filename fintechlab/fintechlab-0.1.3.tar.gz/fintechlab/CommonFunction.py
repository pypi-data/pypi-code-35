
# coding: utf-8

# ### Common Function

# In[1]:


from isoweek import Week


# In[2]:


def lagweek(yearweekA, yearweekB):

    yearweekA = int(yearweekA)
    yearweekB = int(yearweekB)
    yearA = int((yearweekA)/100)
    yearB = int((yearweekB)/100)

    if(abs(yearA-yearB) > 0):
        yearweekBig = yearweekA
        if(yearweekA <= yearweekB):
            yearweekBig = yearweekB
        yearweekSmall = yearweekA 
        if(yearweekA >= yearweekB): 
            yearweekSmall = yearweekB

        bigLag = yearweekBig - int(str(yearweekBig)[0:4]+"00")
        x = datetime.date(int(str(yearweekSmall)[0:4]), 12,31).isocalendar()[1]
        if x!=53:
            x=52
        else:
            x=53
        smallLag = int(str(yearweekSmall)[0:4] + str(x)) - yearweekSmall
        return (bigLag + smallLag)
    else:
        return (abs(yearweekA - yearweekB))


# In[3]:


# 연주차정보와 과거 gap 주차정보를 입력받아 과거 주자정보를 반환한다.
# 파라미터 : inputYearWeek, gapWeek
# 리턴 : 과거 연주차정보
def preWeek(inputYearWeek,gapWeek):

    inputYearWeek=str(inputYearWeek)
    gapWeek =int(gapWeek)
    currYear = int(inputYearWeek[0:4])
    currWeek = int(inputYearWeek[4:6])
    
    #calendar.setTime(dateFormat.parse(currYear + "1231"));
    Week.last_week_of_year(currYear).week
    
    if(currWeek <=gapWeek):
        iterGap= gapWeek -currWeek
        iterYear = currYear -1
        
        iterWeek= Week.last_week_of_year(iterYear).week
        
        while iterGap >0:
            if iterWeek <= iterGap:
                iterGap = iterGap -iterWeek
                iterYear = iterYear - 1
                iterWeek = Week.last_week_of_year(iterYear).week
            else:
                iterWeek = iterWeek - iterGap
                iterGap =0 
                
        
        return str(iterYear)+"{:02d}".format(iterWeek)
    else:
        resultYear = currYear
        resultWeek = currWeek -gapWeek
        
        return str(resultYear)+"{:02d}".format(resultWeek)


# In[4]:


# 연주차정보와 미래 gap 주차정보를 입력받아 미래 주자정보를 반환한다.
# 파라미터 : inputYearWeek, gapWeek
# 리턴 : 미래 연주차정보
def postWeek(inputYearWeek, gapWeek):
   # inputYearWeek.astype("str")
    # gapWeek.astype("int")
    inputYearWeek=str(inputYearWeek)
    gapWeek =int(gapWeek)
    currYear = int(inputYearWeek[0:4])
    currWeek = int(inputYearWeek[4:6])
    
    maxWeek = Week.last_week_of_year(currYear).week
    
    if(maxWeek <currWeek +gapWeek):
        iterGap = gapWeek +currWeek - maxWeek
        iterYear = currYear +1 
        
        iterWeek = Week.last_week_of_year(iterYear).week
        
        while iterGap >0:
            if iterWeek < iterGap:
                iterGap = iterGap- iterWeek
                iterYear = iterYear +1 
                iterWeek = Week.last_week_of_year(iterYear).week
            else:
                iterWeek = iterGap 
                iterGap =0 
        
        return  str(iterYear)+"{:02d}".format(iterWeek)
    else:
        return str(currYear) +"{:02d}".format(currWeek+gapWeek)
            
    

