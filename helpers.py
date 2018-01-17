# -*- coding: utf-8 -*-
"""
Created on Thu Oct 19 17:28:55 2017

@author: Nathan
"""
from time import sleep
import random
import pandas as pd
import nltk
from nltk import word_tokenize
from nltk.corpus import stopwords
from collections import Counter

def search_jobs(driver, job_title_input, location_input):
    """Enter query terms into search box and run job search"""
    job_title = driver.find_element_by_id("KeywordSearch")
    job_title.send_keys(job_title_input)
    location = driver.find_element_by_id("LocationSearch")
    location.clear()
    location.send_keys(location_input)
    driver.find_element_by_id("HeroSearchButton").click()
    return

def read_listings(driver, listings, idx, results):
    """take a list of job listings and record the title, company name, location, and description in a dictionary.
       Return the dictionary and an index representing the number of job listings stored"""
    for listing in listings:
        info = listing.find_element_by_class_name("flexbox.empLoc")
        company = info.find_element_by_tag_name("div")
        company_name, company_location = company.text.split(' – ')
        listing.click()
        sleep(5)
        sleep(random.randint(1,5))
        #check for the pop-up
        '''
        try:
            driver.find_element_by_class_name("mfp-close").click()
        except:
            pass
        '''
        description = driver.find_element_by_class_name("jobDescriptionContent.desc").text
        title = driver.find_element_by_class_name("empInfo.tbl").find_element_by_tag_name("h1").text
        results[idx] =  {'title' : title, 'company' : company_name, 'location' : company_location, 'description' : description}
        idx += 1
    return idx, results

def create_df(results_dict):
    """convert a results dictionary into a pandas Dataframe (and drop duplicate entries)"""
    df = pd.DataFrame(results_dict, index=['company', 'description', 'location', 'title'])
    df = df.transpose()
    print(str(sum(df.duplicated())) + " duplicates found.")
    df = df.drop_duplicates()
    print("dataframe created.")
    return df

def tokenize_description(description):
    """take a job description and return a list of tokens excluding stop words"""
    tokens = word_tokenize(description)
    stopset = set(stopwords.words('english'))
    tokens = [w.lower() for w in tokens if not w in stopset]
    text = nltk.Text(tokens)
    return list(set(text))
        
def find_skills_frequency(results_df):
    """count frequency of key words (as defined in dictionaries within function) appearing in job descriptions and return dataframe with skill frequency"""
    words = []
    for description in results_df['description']:
        words.append(tokenize_description(description))
    
    doc_frequency = Counter()
    [doc_frequency.update(word) for word in words]
    
    prog_lang_dict = Counter({'R':doc_frequency['r'], 'Python':doc_frequency['python'],
                    'Java':doc_frequency['java'], 'C++':doc_frequency['c++'],
                    'Ruby':doc_frequency['ruby'], 'Julia':doc_frequency['julia'],
                    'Perl':doc_frequency['perl'], 'Matlab':doc_frequency['matlab'], 
                    'Mathematica':doc_frequency['mathematica'], 'Php':doc_frequency['php'],
                    'JavaScript':doc_frequency['javascript'], 'Scala': doc_frequency['scala'],
                    'Octave':doc_frequency['octave']})
                      
    analysis_tool_dict = Counter({'Excel':doc_frequency['excel'],  'Tableau':doc_frequency['tableau'],
                        'D3.js':doc_frequency['d3.js'], 'SAS':doc_frequency['sas'],
                        'SPSS':doc_frequency['spss'], 'D3':doc_frequency['d3'],
                        'Spotfire': doc_frequency['spotfire'],'Stata':doc_frequency['stata'],
                        'Power BI': doc_frequency['power bi']})  

    hadoop_dict = Counter({'Hadoop':doc_frequency['hadoop'], 'MapReduce':doc_frequency['mapreduce'],
                'Spark':doc_frequency['spark'], 'Pig':doc_frequency['pig'],
                'Hive':doc_frequency['hive'], 'Shark':doc_frequency['shark'],
                'Oozie':doc_frequency['oozie'], 'ZooKeeper':doc_frequency['zookeeper'],
                'Flume':doc_frequency['flume'], 'Mahout':doc_frequency['mahout']})
    
    other_dict = Counter({'Azure':doc_frequency['azure'], 'AWS':doc_frequency['aws']})
                
    database_dict = Counter({'SQL':doc_frequency['sql'], 'NoSQL':doc_frequency['nosql'],
                    'HBase':doc_frequency['hbase'], 'Cassandra':doc_frequency['cassandra'],
                    'MongoDB':doc_frequency['mongodb']})
                    
    edu_dict = Counter({'Bachelor':doc_frequency['bachelor'],'Master':doc_frequency['master'],\
                          'PhD': doc_frequency['phd'],'MBA':doc_frequency['mba']})
                          
    lang_dict = Counter({'French':doc_frequency['french'],'German':doc_frequency['german'],
                         'Spanish':doc_frequency['spanish'],'Chinese':doc_frequency['chinese'],
                         'Japanese':doc_frequency['japanese']})
          
    education_dict = Counter({'Computer Science':doc_frequency['computer-science'],  
                              'Statistics':doc_frequency['statistics'], 
                              'Mathematics':doc_frequency['mathematics'],
                              'Physics':doc_frequency['physics'], 
                              'Machine Learning':doc_frequency['machine-learning'], 
                              'Economics':doc_frequency['economics'], 
                              'Software Engineer': doc_frequency['software-engineer'],
                              'Information System':doc_frequency['information-system'], 
                              'Quantitative Finance':doc_frequency['quantitative-finance']})
    
    skills = prog_lang_dict + analysis_tool_dict + hadoop_dict \
                           + database_dict + other_dict + education_dict \
                           + lang_dict +  edu_dict
    
    skills_frame = pd.DataFrame(list(skills.items()), columns = ['Term', 'NumPostings'])
    skills_frame.NumPostings = (skills_frame.NumPostings)*100/len(results_df)
    
    # Sort the data for plotting purposes
    skills_frame.sort_values(by='NumPostings', ascending = False, inplace = True)
    return skills_frame

