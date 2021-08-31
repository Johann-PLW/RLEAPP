import os
import datetime
import json
import magic
import shutil
from bs4 import BeautifulSoup
from pathlib import Path	

from scripts.artifact_report import ArtifactHtmlReport
from scripts.ilapfuncs import logfunc, tsv, timeline, kmlgen, is_platform_windows, utf8_in_extended_ascii, media_to_html

def get_fbigUnifiedmessaging(files_found, report_folder, seeker, wrap_text):
    data_list = []
    for file_found in files_found:
        file_found = str(file_found)
        
        filename = os.path.basename(file_found)
        
        if filename.startswith('index.html'):
            data_list = []
            with open(file_found) as fp:
                soup = BeautifulSoup(fp, 'html.parser')
            #<div id="property-unified_messages" class="content-pane">
            uni = soup.find_all("div", {"id": "property-unified_messages"})
            
            control = 0
            itemsdict = {}
            lmf = []
            for x in uni:
                tables = x.find_all("table")
                
                for table in tables:
                    thvalue = (table.find('th').get_text())
                    tdvalue = (table.find('th').find_next_sibling("td").get_text())
                    if thvalue == 'Unified Messages':
                        for subtable in table.find_all('table'):
                            thvalue = (subtable.find('th').get_text())
                            tdvalue = (subtable.find('th').find_next_sibling("td").get_text())
                            wtag = subtable.find('th').find_next_sibling("td")
                            wtag = str(wtag)
                            if thvalue == 'Thread':
                                split = tdvalue.split(')')
                                threadid = split[0].replace('(','').strip()
                            else:
                                wtag = wtag.replace('<td>', '').replace('</td>', '').strip()
                                if thvalue == 'Current Participants':
                                    current_part = wtag
                                elif thvalue == 'Share':
                                    pass
                                elif thvalue == 'Attachments':
                                    pass
                                else:
                                    if thvalue == 'Author':
                                        author = tdvalue
                                        
                                        itemsdict['author'] = author
                                        if control == 0:
                                            control = 1
                                        else:
                                            itemsdict['threadid'] = threadid
                                            
                                            if len(lmf) > 0:
                                                counterl = 0
                                                agregator = agregator + ('<table>')
                                                for item in lmf:
                                                    if counterl == 0:
                                                        agregator = agregator +('<tr>')
                                                
                                                    thumb = media_to_html(item, files_found, report_folder)
                                                    
                                                    counterl = counterl + 1
                                                    agregator = agregator + f'<td>{thumb}</td>'
                                                    #hacer uno que no tenga html
                                                    if counterl == 2:
                                                        counterl = 0
                                                        agregator = agregator + ('</tr>')
                                                if counterl == 1:
                                                    agregator = agregator + ('</tr>')
                                                agregator = agregator + ('</table><br>')
                                            else:
                                                agregator = ''
                                                
                                            data_list.append((itemsdict.get('sent', ''),itemsdict.get('threadid', ''), itemsdict.get('author', ''), itemsdict.get('body', ''), agregator))
                                            #print(lmf)
                                            #to do: check lmf in dictionary, pull and find the files to attach to the report
                                            agregator = ''
                                            itemsdict = {}
                                            lmf = []
                                    elif thvalue == 'Sent':
                                        sent = tdvalue
                                        itemsdict['sent'] = sent
                                    elif thvalue == 'Body':
                                        body = tdvalue
                                        itemsdict['body'] = body
                                    elif thvalue == 'Date Created':
                                        dcreated = tdvalue
                                        itemsdict['dcreated'] = dcreated
                                    elif thvalue == 'Summary':
                                        summary = tdvalue
                                        itemsdict['summary'] = summary
                                    elif thvalue == 'Title':
                                        title = tdvalue
                                        itemsdict['title'] = title
                                    elif thvalue == 'Url':
                                        url = tdvalue
                                        itemsdict['url'] = url
                                    elif thvalue == 'Duration':
                                        duration = tdvalue
                                        itemsdict['duration'] = duration
                                    elif thvalue == 'Missed':
                                        missed = tdvalue
                                        itemsdict['missed'] = missed
                                    elif thvalue == 'Attachments':
                                        attach = tdvalue
                                        itemsdict['attach'] = attach
                                    elif thvalue == 'Linked Media File:':
                                        lmf.append(tdvalue)
                                        itemsdict['lmf'] = lmf
                                    else:
                                        pass
                        itemsdict['author'] = author
                        itemsdict['threadid'] = threadid
                        data_list.append((itemsdict.get('sent', ''),itemsdict.get('threadid', ''), itemsdict.get('author', ''), itemsdict.get('body', ''), itemsdict.get('lmf', '')))
            
                
    if data_list:
        report = ArtifactHtmlReport('Facebook & Instagram - Unified Messaging')
        report.start_artifact_report(report_folder, 'FBIG - Unified Messaging')
        report.add_script()
        data_headers = ('Timestamp','Thread ID', 'Author', 'Body', 'LMF')
        report.write_artifact_data_table(data_headers, data_list, file_found, html_no_escape=['LMF'])
        report.end_artifact_report()
        
        tsvname = f'FBIG - Unified Messaging'
        tsv(report_folder, data_headers, data_list, tsvname)
        
        tlactivity = f'FBIG - Unified Messaging'
        timeline(report_folder, tlactivity, data_list, data_headers)

    else:
        logfunc('No FBIG - Unified Messaging')
                
        