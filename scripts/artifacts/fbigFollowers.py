import os
import datetime
import json
import shutil
from bs4 import BeautifulSoup
from pathlib import Path	

from scripts.artifact_report import ArtifactHtmlReport
from scripts.ilapfuncs import logfunc, tsv, timeline, kmlgen, is_platform_windows, utf8_in_extended_ascii, media_to_html

def get_fbigFollowers(files_found, report_folder, seeker, wrap_text):
    
    for file_found in files_found:
        file_found = str(file_found)
        
        filename = os.path.basename(file_found)
    
        if filename.startswith('records.html') or filename.startswith('preservation'):
            rfilename = filename
            
            
            with open(file_found, encoding='utf-8') as fp:
                soup = BeautifulSoup(fp, 'lxml')
                
            data_list = []
            pairs_list = []
            uni = soup.find_all("div", {"id": "property-followers"})
            
            divs = uni[0].find_all('div', class_='div_table inner')
            for index, div in enumerate(divs):
                if index > 1:
                    divinn = (div.find('div', class_='most_inner'))
                    divtext = (divinn.get_text())
                    pairs_list.append(divtext)
                    if len(pairs_list) == 2:
                        data_list.append((pairs_list[1],pairs_list[0]))
                        pairs_list =[]
        
        if data_list:
            report = ArtifactHtmlReport(f'Facebook & Instagram - Followers - {rfilename}')
            report.start_artifact_report(report_folder, f'Facebook Instagram - Followers - {rfilename}')
            report.add_script()
            data_headers = ('Timestamp','User')
            report.write_artifact_data_table(data_headers, data_list, file_found, html_no_escape=[''])
            report.end_artifact_report()
            
            tsvname = f'Facebook Instagram - Followers - {rfilename}'
            tsv(report_folder, data_headers, data_list, tsvname)
            
            tlactivity = f'Facebook Instagram - Followers - {rfilename}'
            timeline(report_folder, tlactivity, data_list, data_headers)
        
        else:
            logfunc(f'No Facebook Instagram - Followers - {rfilename}')
                
__artifacts__ = {
        "fbigFollowers": (
            "Facebook - Instagram Returns",
            ('*/records.html', '*/preservation*.html'),
            get_fbigFollowers)
}