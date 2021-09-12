import warnings
warnings.filterwarnings("ignore")
print('Please wait...\n\nImporting Necessary Packages\n')


import pandas as pd
from bs4 import BeautifulSoup
import requests
import re
import os
import time
import matplotlib.pyplot as plt
import seaborn as sns
from nltk import tokenize
from operator import itemgetter
import math
import nltk
from nltk.corpus import stopwords

# If you have not already downloaded stopwords, you need to uncomment and run the following line. This only needs to be done once.
# nltk.download('stopwords')

from nltk.tokenize import word_tokenize 
import csv
from tqdm import tqdm
from collections import Counter
from multi_rake import Rake
from gensim.summarization import keywords
import unicodedata
import numpy as np
from mpl_toolkits.basemap import Basemap
import numpy as np
import datetime as dt

stop_words = set(stopwords.words('english'))
# get_ipython().run_line_magic('matplotlib', 'inline')

sns.set()
# sns.set()

# pd.reset_option('^display.', silent=True)
pd.options.display.max_rows = 999


# In[3]:


# Search Inputs
import pickle

with open("test.txt", "rb") as fp:
	Search = pickle.load(fp)

Keyword = Search[0]
City = Search[1]
State = Search [2]
Path = Search[3]

os.remove("test.txt")

import os
os.chdir(Path)

# In[4]:


# Save Directory
try:
    os.mkdir(str(Path)+str(Keyword)+'_'+str(City))
except:
    pass
os.chdir(str(Path)+str(Keyword)+'_'+str(City))


# In[5]:


# Software
software = ['Microsoft Office','MS Office',
           'Microsoft Word','MS Word',
           'Microsoft Excel','Excel','excel','csv','xlsx','pivot tables',
           'VBA','visual basic','Visual Basic', 
           'Microsoft Powerpoint','Powerpoint','ppt',
           'Microsoft Publisher','Publisher',
           'Power BI','PowerBI','BI Tools','Tableau','tableau',
           'Python','Pandas','pandas','numpy','matplotlib','scipy',
           ' R ','R ','PyCharm','PySpark',
           'HTML','Webscraping','webscrape',
           'C#','c#','c++','C++','Java','Java Script',
           'Dashboard','dashboard','dashboards','Dashboards',
           'Oracle','oracle','Xero','IBM','IBM cloud','Google Cloud','cloud','Cloud','AWS','Amazon',
           'Azure','Google','Ruby','ruby','ruby on rails','SPSS','SAP','SAS','SQL','mySQL',
           'Bloomberg']

qualities = ['fast learner','tenacious','dedicated','Team','team','independent','solitary',
             'polite','team-oriented','team oriented','honest','social','sociable',
            'committed','commitment','social','confident','confidence','communicator','communication',
            'puntual']

skills = ['negotiate','Present','present','Presentation','presenation','mine','mining','script','code','staff management',
         'mentor','maintain','clean','network','relationship','manage','management','train','Train','training','learn',
         'read','mathematics','thinking','thinker','warehousing','econometrics','statistics','regression']

industries = ['Actuary','Actuarial','Business','Finance','Science','Health','Economics','Mathematics','Accounting',
              'Human Resources','HR','Recruitment','consumer services','Retail','IT','Software Design']

education = ['CFA','CPA','CA','CIPM','Master','Bachelor','Diploma','Certificate','certificate','certification',
             'MPA','PhD','Doctorate','Udemy','Skillshare','Coursera','University','TAFE','Udacity',
             'Pluralsight','degree','Degree']


# In[6]:


# def Download_Jora():

if City == '':
    url = requests.get('https://au.jora.com/j?sp=search&q='+Keyword+'&l=')
elif City != '' and  State != '':
    url = requests.get('https://au.jora.com/j?sp=homepage&q='+Keyword+'&l='+City+'+'+State)
else:
    print('Error: Please input State')

soup = BeautifulSoup(url.content, 'html.parser')

page_count = soup.find("div",{"class":"search-results-count"}).text
job_count = page_count.split()[0]
current_page = page_count.split()[~2]

no_pages = page_count.split()[~0]
# no_pages = 2

df = pd.DataFrame()

print('\nAccessing au.jora.com\n')
for idx, n in enumerate(range(0,int(no_pages))):
    print('Downloading: Page '+str(idx+1)+'/'+str(no_pages))
    containers = soup.find_all(class_='job-item')

    # Job Title
    c2 = []
    for c in containers:
        try:
            c1 = c.find(class_='job-title').text
            c2.append(c1)
        except:
            c1 = 'n/a'
            c2.append(c1)               
    Title = pd.DataFrame(c2,columns=['Title'])

    # Job Salary
    c2 = []
    for c in containers:
        try:
            c1 = c.find(class_='badge -default-badge').text
            c2.append(c1)
        except:
            c1 = 'n/a'
            c2.append(c1)               
    Salary = pd.DataFrame(c2,columns=['Salary'])

    # Company
    c2 = []
    for c in containers:
        try:
            c1 = c.find(class_='job-company').text
            c2.append(c1)
        except:
            c1 = 'n/a'
            c2.append(c1)               
    Company = pd.DataFrame(c2,columns=['Company'])

    # Location
    c2 = []
    for c in containers:
        try:
            c1 = c.find(class_='job-location').text
            c2.append(c1)
        except:
            c1 = 'n/a'
            c2.append(c1)               
    Location = pd.DataFrame(c2,columns=['Location'])

    # Abstract
    c2 = []
    for c in containers:
        try:
            c1 = c.find(class_='job-abstract').text
            c2.append(c1)
        except:
            c1 = 'n/a'
            c2.append(c1)               
    Abstract = pd.DataFrame(c2,columns=['Abstract'])

    # Listing Date
    c2 = []
    for c in containers:
        try:
            c1 = c.find(class_='job-listed-date').text
            c2.append(c1)
        except:
            c1 = 'n/a'
            c2.append(c1)               
    Listed = pd.DataFrame(c2,columns=['Listed'])

    # URL
    c2 = []
    for c in containers:
        try:
            c1 = 'https://au.jora.com'+str(c['href'])
            c1 = c1.split("?from", 1)[0]
            c2.append(c1)
        except:
            c1 = 'n/a'
            c2.append(c1)               
    URL = pd.DataFrame(c2,columns=['URL'])

    df1 = pd.concat([Company,Title,Listed,Salary,Location,Abstract,URL],axis=1)

    df = pd.concat([df,df1])

    try:
        next_page_url = soup.find("a",{"class":"next-page-button"})
        next_page_url = 'https://au.jora.com'+str(next_page_url['href'])
        url = requests.get(next_page_url)
        soup = BeautifulSoup(url.content, 'html.parser')
    except:
        pass

df.reset_index(inplace=True)
try:
    df.drop(columns={'index'},inplace=True)
except:
    pass
try:
    df.drop(columns={'level_0'},inplace=True)
except:
    pass

df['monthFiltered'] = df['Listed'][df['Listed'].str.contains("month")] 
df['monthFiltered'] = df.monthFiltered.str.extract('(\d+)')
df['monthFiltered'] = df['monthFiltered'].replace({'1':'30','2':'60'})

df['hourFiltered'] = np.where(df['Listed'].str.contains("hour"), '0', 'NaN')
df['daysFiltered'] = df['Listed'][df['Listed'].str.contains("day")] 
df['daysFiltered'] = df.daysFiltered.str.extract('(\d+)')

df['LMerge'] = df['daysFiltered'].fillna(df['hourFiltered'])
df['LMerge'] = df['LMerge'].replace('NaN',df['monthFiltered'])
df['LMerge'] = df['LMerge'].fillna(0)
df['LMerge'] = df['LMerge'].astype(int)
df['LAge'] = df['LMerge']

start = dt.datetime.now()
df['Date'] = start - df['LMerge'].map(dt.timedelta)
df = df.sort_values(by='Date', ascending=False).reset_index(drop=True)
df['Date'] = pd.to_datetime(df['Date']).dt.date
df['Listed'] = df['Date']
df.drop(columns=['Date', 'monthFiltered', 'daysFiltered','hourFiltered','LMerge'],inplace=True)

df.to_csv('Data_Downloaded.csv', index=False)


# In[7]:


df2 = df

dp1 = pd.DataFrame()
ldf = len(df2)

print('\nAnalysing Jobs\n')
for idx, (u, n, c, l, x, s, a) in enumerate(zip(df2['URL'], df2['Title'], df2['Company'], df2['Listed'], df2['Location'], df2['Salary'], df2['Abstract'])):
    print(str(idx+1)+'/'+ str(ldf) +' - '+c+': '+n)
    url = requests.get(u)
    soup = BeautifulSoup(url.content, 'html.parser')
    
    # Key Points - Dot point string
    lists = []
    for i in soup.find_all('li'):
        lists.append(i.text)
    dp = pd.DataFrame([[lists]],columns=['Key_Points'])
#     dp = dp.explode('Key_Points')



    # Machine Learning Key Phrase Identification
    kphrases = []
    tt = soup.get_text()
    try:
        rake = Rake()
        keywords = rake.apply(tt)
        words = pd.DataFrame(keywords,columns={'Key_Phrases','Frequency'})
        Key_Phrases = list(words['Key_Phrases'])
        kphrases.append(Key_Phrases)
    except:
        kphrases.append("n/a")
#     dp['KPhrases'] = kphrases

    
    # Machine Learning Key Phrase Identification
    from gensim.summarization import keywords
    txt = soup.get_text()
    words = pd.DataFrame((keywords(txt,scores = True,lemmatize = True)),columns={'Keywords','Frequency'})
    kwords = [list(words['Frequency'])]  
    dp['Kwords'] = kwords
    
    
    
    # Experience
    try:
        Experience = []
        tt = tt.lower()
        try:
            define_words = "experience"
            m = re.search("[^.]*" +define_words+ "[^.]*\.",tt)    
            Experience.append(m.group(0))
        except:
            m = 'n/a'
            Experience.append(m)
        dp['Experience'] = Experience
    except:
        pass
        
        
        
        
    # Years            
    try:
        Years = []
        tt = tt.lower()
        try:
            define_words = "years"
            m = re.search(r"[0-9]+\s+"+define_words+"\W|[0-9]+\s"+str(define_words),tt)    
            Years.append(m.group(0))
        except:
            m = 'n/a'
            Years.append(m)
        dp['Years'] = Years
    except:
        pass
        
        
    
    
    # Minimum
    try:
        minimum = []
        tt = tt.lower()
        try:
            define_words = "minimum"
            m = re.search("[^.]*" +define_words+ "[^.]*\.",tt)    
            minimum.append(m.group(0))
        except:
            m = 'n/a'
            minimum.append(m)
        dp['Minimum'] = minimum
    except:
        pass
        
        
        
     # Qualification
    try:
        Qualification = []
        tt = tt.lower()
        try:
            define_words = "qualification"
            m = re.search("[^.]*" +define_words+ "[^.]*\.",tt)    
            Qualification.append(m.group(0))
        except:
            m = 'n/a'
            Qualification.append(m)
        dp['qualification'] = Qualification
    except:
        pass     
        
    
    dp['Title'] = n
    dp['Company'] = c
    dp['Listed'] = l
    dp['Location'] = x
    dp['Salary'] = s
    dp['Abstract'] = a
    dp1 = dp1.append(dp)
    dp2 = dp1


# In[8]:


try:
    Title = dp1.groupby('Title').count()
    Title = Title.drop(columns=['Key_Points','Listed','Location','Salary','Abstract','Kwords',
                            'Experience','Years','Minimum','qualification'])
    Title.rename(columns={'Title':'Count'},inplace=True)
    Title = Title.sort_values(by='Count',ascending=False)
    Title.reset_index(inplace=True)
    Title.to_csv('Job_Title.csv', index=False)

    Company = dp1.groupby('Company').count()
    Company = Company.drop(columns=['Key_Points','Listed','Location','Salary','Abstract','Kwords',
                            'Experience','Years','Minimum','qualification'])
    Company.rename(columns={'Company':'Count'},inplace=True)
    Company = Company.sort_values(by='Count',ascending=False)
    Company.reset_index(inplace=True)
    # Company = Company[~Company.Company.str.contains("n/a")]
    Company.to_csv('Company.csv', index=False)
except:
    pass


# In[9]:



dp3 = dp2[dp2['Years']!='n/a']
dp4 = dp3[dp3.Years.str.split().str.get(0).astype(int) <= 13]
dp4.Years.str.split().str.get(0).astype(int)

def describe_helper(series):
    splits = str(series.describe()).split()
    keys, values = "", ""
    for i in range(0, len(splits), 2):
        keys += "{:8}\n".format(splits[i])
        values += "{:>.7}\n".format(splits[i+1])
    return keys, values

fig, ax = plt.subplots()
exps = dp4.Years.str.split().str.get(0).astype(int)

ax.hist(exps, bins=[1,3,5,7,9,11,13])
plt.figtext(.95, .49, describe_helper(pd.Series(exps))[0])
plt.figtext(1.05, .49, describe_helper(pd.Series(exps))[1])

#     sns.set()

plt.ylabel('Frequency')
plt.xlabel('Years of Experience')
plt.title('Minimum Years of Experience: '+str(Keyword)+' '+str(City))
plt.savefig(str(Keyword)+'_'+str(City)+'_Experience.png',dpi=300, bbox_inches = "tight")


# In[10]:


from itertools import accumulate

count = exps.count()
vals = pd.DataFrame(exps.value_counts()).reset_index().sort_values(by='index')
vals['Percentile'] = vals['Years'] / count
vals['Percentile'] = vals['Percentile'].cumsum()

val2 = pd.DataFrame([[0, 0, 0]], columns = ['index', 'Years', 'Percentile'])
vals = pd.concat([val2, vals]).reset_index(drop=True)

vals


# In[11]:


try:
    kwords2 = []
    for sublist in dp2['Kwords']:
        for item in sublist:
            kwords2.append(item)

    from collections import Counter

    c = Counter(kwords2)
    kwords_count = pd.DataFrame.from_dict(c, orient='index')
    kwords_count.reset_index(inplace=True)
    kwords_count.rename(columns={'index':'Keyword',0:'Frequency'},inplace=True)
    kwords_count = kwords_count.sort_values(by='Frequency', ascending=False)
    kwords_count = kwords_count[kwords_count['Frequency']<400]
    kwords_count = kwords_count[kwords_count['Frequency']>50]
    kwords_count.reset_index(inplace=True)
    kwords_count.drop(columns={'index'},inplace=True)
    kwords_count.to_csv('KWords.csv')
    kwords_count
except:
    pass


# In[12]:


try:
    Software = {}
    Qualities = {}
    Skills = {}
    Industries = {}
    Education = {}

    metric = [software, qualities, skills, industries, education]
    mstring = ('Software','Qualities','Skills', 'Industries','Education')
    dframes = (Software, Qualities, Skills, Industries, Education)

    print('\n')
    for m, ms, dfs in zip(metric, mstring, dframes):
        df = pd.DataFrame()
        for n in dp1['Key_Points']:
        #     try:
        #         print(n+'\n\n')
                if n == '[]':
                    continue

                text_tokens = word_tokenize(str(n))
                tokens_without_sw = [word for word in text_tokens if word in m]

                if tokens_without_sw == []:
                    continue
        #         print(tokens_without_sw)
        #         split_it = tokens_without_sw.split()
                count = Counter(tokens_without_sw) 
                most_occur = count.most_common(20) 
        #         print(most_occur)
        #         print('\n\n')
                df = df.append(most_occur)

        df = df.reset_index()
        df = df.reset_index()
    #     df.rename(index={'level_0': 'Index'},inplace=True)
        df2 = df.pivot(index='level_0',values=1,columns=0)
        soft = list(df2)
        df2.T.groupby(soft).sum()
        df2 = df2.T
        df2 = df2.fillna(0)
        df2['Total_Count'] = ((df2.sum(axis=1)))

        df2['Total%'] = ((df2['Total_Count'])/len(dp2['Key_Points']))*100

        # df2['Total_Count'] = Toral 
        df3 = df2[{'Total_Count','Total%'}]
        df3 = df3.sort_values('Total_Count', ascending=False)
        df3 = df3.reset_index()
        df3 = df3.rename(columns={0:ms})

        dfs.update(df3)

        print(str(ms))
    #     print(df3)
    #     print('\n\n')

    Software = pd.DataFrame(Software)
    Qualities = pd.DataFrame(Qualities)
    Skills = pd.DataFrame(Skills)
    Industries = pd.DataFrame(Industries)
    Education = pd.DataFrame(Education)

    Software.to_csv('Software.csv', index=False)
    Qualities.to_csv('Qualities.csv', index=False)
    Skills.to_csv('Skills.csv', index=False)
    Industries.to_csv('Industries.csv', index=False)
    Education.to_csv('Education.csv', index=False)

    # Integrate all keywords as column names and each cell value is denoted as a boolean if present in
    # job advert - Find way to classify columns. Perhaps multiple dataframes for each type of keyword.
except:
    pass


# In[13]:


Company


# In[14]:


import matplotlib.colors as mcolors
# sns.set()

clist = [(0, "blue"), (0.2, "green"), (1.0, "white")]

rvb = mcolors.LinearSegmentedColormap.from_list("", clist)
N = 60
# plt.rcParams['font.family'] = 'sans-serif'
# plt.rcParams['font.sans-serif'] = 'Helvetica'
plt.rcParams['axes.edgecolor']='#333F4B'
plt.rcParams['axes.linewidth']=0.8
plt.rcParams['xtick.color']='#333F4B'
plt.rcParams['ytick.color']='#333F4B'

try:
	dfs = [Software, Qualities, Skills, Industries, Education, Title, Company]
	names = ['Software','Qualities','Skills','Industries','Education','Title','Company']
	for d, n in zip(dfs, names):
	    my_range=list(range(1,len(d.index)+1))
	    x = np.arange(N).astype(float)
	    y = np.random.uniform(0, 5, size=(N,))
	    plt.rcdefaults()
	    fig, ax = plt.subplots()
	    try:
	        ax.barh(d[n][:15], d['Total_Count'][:15], align='center', color=rvb(x/N))

	    except:
	        ax.barh(d[n][:15], d['Count'][:15], align='center', color=rvb(x/N))

	    ax.invert_yaxis()  # labels read top-to-bottom
	    ax.set_title('Keyword: '+str(Keyword)+' '+str(City)+' - Top 15 '+ n)
	    
	    ax.set_xlabel('Keyword Frequency')
	    ax.set_ylabel('')

	    
	    ax.spines['top'].set_color('none')
	    ax.spines['right'].set_color('none')
	    ax.spines['left'].set_smart_bounds(True)
	    ax.spines['bottom'].set_smart_bounds(True)
	    plt.savefig('TopKeywords_'+str(n)+'.png',dpi=300, bbox_inches = "tight")
except:
	pass

	# In[15]:


try:
    loc = pd.DataFrame(dp1['Location'])
    loc['count'] = 1
    loc['State'] = loc['Location'].apply(lambda x: x.split()[-1])
    loc['City'] = loc['Location'].apply(lambda x: x.split()[~-1])
    loc3 = pd.DataFrame(loc.replace({'State':{'Adelaide':'SA','Brisbane':'QLD','Coast':'QLD',
                                              'Hobart':'TAS','Hunter':'NSW','Melbourne':'VIC',
                                              'Murray':'VIC','Perth':'WA','Queensland':'QLD',
                                              'Sydney':'NSW','Territory':'NT','Victoria':'VIC',
                                              'Wales':'NSW','East':'NSW','Country':'NSW','Australia':'NSW'}}))
    state = loc3.groupby('State').sum()

    state = state.loc[{'NSW','VIC','QLD','SA','ACT','NT','WA','TAS'}]
    state = pd.DataFrame(state, index=['NSW','VIC','QLD','SA','ACT','NT','WA','TAS'],columns=['count'])
    state = state.sort_values('count', ascending=False)
    
    loc['City'].unique()
    city = loc.groupby('City').sum()
    city = pd.DataFrame(city, index=['Sydney','Brisbane','Melbourne','Adelaide','ACT','Canberra','Perth','Darwin','Hobart'],columns=['count'])
    city = city.sort_values('count', ascending=False)
    print('City')
    print('State')

    city.to_csv('City.csv')
    state.to_csv('State.csv')
except:
    pass


# In[16]:


# Location HeatMap
# try:
if City == '':
    state = state.drop_duplicates()
    state = state.reset_index()
    
    # try:
    state = state.rename(columns={'index':'State'})
    # except:
    #     pass
#     print(state)

    city = ['Sydney','Brisbane','Melbourne','Adelaide','ACT','Canberra','Perth','Darwin','Hobart']
    states = ['NSW', 'QLD', 'VIC', 'SA', 'ACT', 'ACT', 'WA', 'NT', 'TAS']
    lats = [-33.8688, -27.4705, -37.8136, -34.9285, -35.2809, -35.2809, -31.9523, -12.4637, -42.8826]
    longs = [151.2093, 153.0260, 144.9631, 138.6007, 149.1300, 149.1300, 115.8613, 130.8444, 147.3257]

    data = {}
    for c, l1, l2, s in zip(city, lats, longs, states):
        d = {c:[l1, l2, s]}
        data.update(d)
    cities = pd.DataFrame.from_dict(data).T
    cities.rename(columns={0:'latd', 1:'longd', 2:'State'}, inplace=True)
   
    cities = pd.merge(state, cities, on='State') 

    # Extract the data we're interested in
    lat = cities['latd'].values
    lon = cities['longd'].values
    count = cities['count'].values

    # 1. Draw the map background
    fig = plt.figure(figsize=(8, 6))
    m = Basemap(projection='lcc', resolution='h', 
                lat_0=-27.2744, lon_0=133.7751,
                width=0.45E7, height=0.4E7)
    m.shadedrelief()
    m.drawcoastlines(color='gray')
    m.drawcountries(color='gray')
    m.drawstates(color='gray')

    # # 2. scatter city data, with color reflecting population and size reflecting area
    m.scatter(lon, lat, latlon=True,c=count, s=500,cmap='Reds', alpha=1)
    
    # # 3. create colorbar and legend
    plt.colorbar(label='Colourbar Scale')
    plt.clim(0, 500)
    plt.title('Location Heat Map\nKeyword: '+str(Keyword))
    plt.savefig('JobsLocation_'+str(Keyword)+'.png',dpi=300, bbox_inches = "tight")
#     else:
#         pass
# except:
#     pass

# In[17]:


try:
    sal = pd.DataFrame()
    sal['min'] = ((dp1['Salary'].dropna()).str.rsplit("-", n=0, expand=True)[0]).str.lstrip('$').str.replace(',', '')
    sal['max'] = (((dp1['Salary'].dropna()).str.rsplit("-", n=0, expand=True)[1]).str.rsplit(" ", n=0, expand=True)[1]).str.lstrip('$').str.replace(',', '')
    sal = sal.dropna().reset_index()
    sal.loc[sal['min'].str.len() <= 3, 'min'] = sal['min'].astype(int)*1900
    sal.loc[sal['max'].str.len() <= 3, 'max'] = sal['max'].astype(int)*1900
    sal['mean'] = ((sal['min'].astype(int) + sal['max'].astype(int)) / 2).astype(int)
    try:
        sal.drop(columns=['index'],inplace=True)
    except:
        pass
    sal.to_csv('Salary.csv', index=False)
    print('Salary')
    print('\nSummaries Saved!')
except:
    pass


# In[18]:


try:
    def describe_helper(series):
        splits = str(series.describe()).split()
        keys, values = "", ""
        for i in range(0, len(splits), 2):
            keys += "{:8}\n".format(splits[i])
            values += "{:>.7}\n".format(splits[i+1])
        return keys, values

    fig, ax = plt.subplots()
    sals = (sal['mean']/1000)

    ax.hist(sals)
    plt.figtext(.95, .49, describe_helper(pd.Series(sals))[0])
    plt.figtext(1.05, .49, describe_helper(pd.Series(sals))[1])

#     sns.set()

    plt.ylabel('Frequency')
    plt.xlabel('Annual Wage')
    plt.title('Keyword: '+str(Keyword)+' '+str(City)+' - Salary $K pa')
    sns.set()
    sns.set()
    plt.savefig(str(Keyword)+'_'+str(City)+'_Salary.png',dpi=300, bbox_inches = "tight")
except:
    pass


# In[19]:


try:
    MySalary = []
    for n in (vals['Percentile']):
        MySalary.append(np.quantile(sals, n))

    Est_Salary = {'Years':vals['index'], 'Salary':MySalary}
    Est_Salary = pd.DataFrame(Est_Salary)
    Est_Salary
    # sns.set()
#     # Regress Salary on Years and extract Beta
#     import statsmodels.api as sm
#     Y = Est_Salary['Salary']
#     X = Est_Salary['Years']
#     X = sm.add_constant(X)
#     model = sm.OLS(Y,X)
#     results = model.fit()
#     Beta = results.params[1]

    # Estimate missing using regression beta
    e = pd.Series(range(0,12))
    Est_Salary2 = pd.DataFrame(e, columns=['Years']).set_index('Years')
    Est_Salary = Est_Salary.set_index('Years')
    frames = [Est_Salary2, Est_Salary]
    Est_Salary3 = pd.merge(Est_Salary2, Est_Salary, left_index=True, right_index=True, how="outer")
    Est_Salary3 = Est_Salary3.reset_index()

    # Estimate Missing using Interpolate function - cumulative regression based calc
    
    Est_Salary3['Salary'] = Est_Salary3['Salary'].interpolate()
    Est_Salary = Est_Salary3

    # Optional - Collapse to data
#     N = 3
#     Est_Salary = Est_Salary.groupby(Est_Salary.index // N).mean()
#     Est_Salary['Years'] = np.ceil(Est_Salary.Years).astype(int)

    # Plot 
    plt.bar(Est_Salary['Years'], Est_Salary['Salary'])
    plt.xticks(Est_Salary['Years'])
    plt.ylabel('Salary $,000')
    plt.xlabel('Years of Experience')
    plt.title('Keyword: '+str(Keyword)+'\nSalary Projection Based on Experience \n'+str(City)+' '+str(State))
    plt.savefig(str(Keyword)+'_'+str(City)+'_Projected_Salary.png', dpi=300, bbox_inches = "tight")
except:
    pass


# In[20]:


try:
    # Date = pd.DataFrame()
    # Date['Number'] = ((dp1['Listed'].dropna()).str.rsplit(" ", n=0, expand=True)[0])
    # Date['Freq'] = ((dp1['Listed'].dropna()).str.rsplit(" ", n=0, expand=True)[1])
    # Date['Listed'] = dp1['Listed']

    # # Date.loc[Date['Freq'].str == 'days', 'FF'] = Date['Number'] != 'about'
    # if Date['Freq'].str == 'days':
    #    Date['Freq'] == (Date['Number'])
    # else:
    #     pass

    # Date = Date[~Date.Number.str.contains("about")]
    # Date = Date[~Date.Freq.str.contains("minutes")]
    # Date = Date[~Date.Freq.str.contains("hours")]
    # Date = Date[~Date.Freq.str.contains("months")]

    # from datetime import date
    # Date['Today'] = date.today()
    # Date['Listed'] = Date['Today'] - pd.to_timedelta(Date['Number'].astype(int), unit='d')
    # Date['Listed'] = pd.to_datetime(Date['Listed'], errors='coerce')

    # # Date['Listed'] = Date['Listed'].dt.strftime("%d/%B")
    # Date['Listed'] = pd.to_datetime(Date['Listed']).dt.date

    Date = dp1.groupby(by=['Listed']).count().reset_index()
    plt.figure(figsize=(10,2))
    plt.plot(Date['Listed'], Date['Company'])

    plt.title('Keyword: '+str(Keyword)+' '+str(City)+' - Job Listings')
    plt.ylabel('Number of New Listings')
    # plt.xlabel('Listing Date')
    plt.xticks(Date['Listed'], Date['Listed'], rotation='vertical')
    # sns.set()
    plt.savefig(str(Keyword)+'_'+str(City)+'_ListingsDate.png',dpi=500, bbox_inches = "tight")
except:
    pass


# In[21]:


try:
    Date['Date'] = pd.to_datetime(Date['Listed'], errors = 'coerce')
except:
    pass


# In[22]:


try:
    dp1.to_csv('dataframe.csv')
except:
    pass


# # Clear Memory by dropping all DataFrames
# frames = [var for var in dir() if isinstance(eval(var), pd.core.frame.DataFrame)]
# for frame in frames:
#     print(frame)
#     del frame

# frames = [var for var in dir() if isinstance(eval(var), pd.core.frame.DataFrame)]
# print(frames)