''' 
Author: Vishal Pattabiraman
Company: intelia
Date Created: 20/4/2023
Version: 1.0

Tool Mainly used for extracting portions of PDF that follow a specific format and saving it as Json object.
Code uses pyPDF2 which is sourced from Poppler
Find more here : https://pypdf2.readthedocs.io/en/stable/index.html 

'''
from PyPDF2 import PdfReader
import re
import json
import os

# Read the Config file
setup= open('config.json',encoding='utf-8')
config= json.load(setup)

# Declare variables
writepath = '.\output'
pg_start = config['pagestart'] if config['pagestart'] else 0


# Read the PDFs
files = sorted(os.listdir(config['pdfs_location']),reverse=True)
for file in files:

    try:
        # Locate PDF from input location
        if os.path.isfile(os.path.join(config['pdfs_location'], file)) and str(file).endswith('.pdf'):
        
            reader = PdfReader(os.path.join(config['pdfs_location'], file))
            number_of_pages = len(reader.pages)
            pg_end= number_of_pages if config['pageend']==0 else config['pageend']
            text_concat = ''
            final = {}

            # Merge the whole document into a single container
            for i in range(pg_start,pg_end):
                page = reader.pages[i]
                text = page.extract_text()
                text_concat=''.join([text_concat,text])

            # Prune content from search start and search end from the document.
            if config['search_start']!='' and config['search_end']!='':
                temp=re.split(config['search_start'],text_concat)[1]
                text_concat=re.split(config['search_end'],temp)[0]

            # Remove headings and unwanted words
            if len(config['remove_headings'])>0:
                text_concat=re.sub(rf"(?!\B\w)(?:{'|'.join(map(re.escape,config['remove_headings'] ))})", '', text_concat)

            # Remove footer
            if config['footer_regex']!='':
                text_concat=re.sub(config['footer_regex'],'',text_concat)

            # Tranformations to identify questions and answers
            questions=re.findall(config['paragraph_regex'],text_concat)
            answer=re.split(config['paragraph_regex'],text_concat)
            ans_start=answer.index(questions[0])
            answer=answer[ans_start:]
            answer=answer[1::2]

            # Question Correction to remove unwanted space
            if config['para_correction_regex']!='':
                for i in range(0,len(questions)):
                    # Split the question
                    q_start = re.search(config['para_correction_regex'],questions[i]).group(1)
                    q_end = re.search(config['para_correction_regex'],questions[i]).group(2)
                    q_start=q_start.replace(' ','')
                    questions[i]= q_start+' '+q_end
                        
            # Convert into Dictionary
            for i in range(0,len(questions)):
                k,v=questions[i],answer[i]
                final[k]=v

            # Write to file
            fname=writepath+'\\'+str(file).replace('.pdf','')+'_scrapped.json'
            with open(fname,'w+',encoding='utf-8') as fb:
                fb.write(json.dumps(final))

    except Exception as e:
        print('Exception Occured:\n',e)
    
    else:
        print('{} - Completed'.format(file))
