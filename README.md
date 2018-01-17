# Scraping Glassdoor to Determine Highest Demand Job Skills

## Motivation
While searching for a data science job, I had the idea to use aggregated job listing data to find which skills were most highly sought after by employers across the board. I mostly wanted this data to help prioritize my time when studying and working on projects that would improve my candidacy for a DS job.

## Project Overview
There are two parts to the project:

1. A python script to scrape Glassdoor job postings. This is actually in two files - scrape_glassdoor.py (main) and helpers.py (helper functions). The files are fairly well annotated if you want to know what each line of code is doing.
2. A Jupyter Notebook that contains analysis of the scraped data

## Scraping Overview
I started out trying to use Beautiful Soup to parse the raw html, but quickly found that many of the large employers and top job sites do not include job posting text in the raw html. Rather it seems that they are populating the job posting data into the DOM using Javascript. This makes things a bit more complicated, but not insurmountable. Instead of Beautiful Soup, I ended up using a tool called Selenium (python library) to select DOM elements and scrape. Selenium is a browser driver, ie. automated browser that can programmaticaly emulate any actions a normal user would do. If you want to try this on your computer, you may need to download a web driver. I used geckodriver since I was working with Firefox.

Most of the other libraries used in the web scraping script are fairly standard. I used nltk in conjunction with collections to count keywords in job postings. I used pandas to create dataframes to structure the data and pickle to save dataframe objects for archival purposes.

Lastly, while I was building this project, I found a few others that had attempted a similar python scraping script. I feel that my code ended up a bit more streamlined and hopefully is more clear and concise for anyone looking to use this as an example for their own project.

## Analysis Overview
Originally I had hoped to apply some NLP machine learning techniques, primarly keyword extraction. I experimented with a RAKE algorithm for keyword/phrase extraction. Unfortunately, the best results I got were much less useful than hardcoding the anticipated keywords and counting from the hardcoded dictionaries.

The analysis in the Jupyter Notebook shows a pareto of skills as well as a simple "80/20" type analysis. I may come back to this project in the future to do some more NLP analysis using the corpus of job postings that I scraped.


