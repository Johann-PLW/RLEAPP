import os
import datetime
import json
import shutil
from pathlib import Path	

from scripts.artifact_report import ArtifactHtmlReport
from scripts.ilapfuncs import logfunc, tsv, timeline, kmlgen, is_platform_windows

def get_instagramLogout(files_found, report_folder, seeker, wrap_text):
    
    for file_found in files_found:
        file_found = str(file_found)
        
        filename = os.path.basename(file_found)
    
        if filename.startswith("logout_activity.json"):
            data_list =[]
            with open(file_found, "rb") as fp:
                deserialized = json.load(fp)
                
            login = (deserialized['account_history_logout_history'])
            for x in login:
                
                title = (x.get('title', ''))
                cookiename = (x['string_map_data']['Cookie Name'].get('value', ''))
                ipaddress = (x['string_map_data']['IP Address'].get('value', ''))
                langagecode = (x['string_map_data']['Language Code'].get('value', ''))
                timestamp = (x['string_map_data']['Time'].get('timestamp', ''))
                useragent = (x['string_map_data']['User Agent'].get('value', ''))
                if timestamp > 0:
                    timestamp = (datetime.datetime.fromtimestamp(int(timestamp)).strftime('%Y-%m-%d %H:%M:%S'))
                    
                data_list.append((timestamp, title, ipaddress, useragent, langagecode, cookiename))
                
                
            if data_list:
                report = ArtifactHtmlReport('Instagram Archive - Logout Activity')
                report.start_artifact_report(report_folder, 'Instagram Archive - Logout Activity')
                report.add_script()
                data_headers = ('Timestamp', 'Title', 'IP Address', 'User Agent', 'Language Code', 'Cookie Name')
                report.write_artifact_data_table(data_headers, data_list, file_found)
                report.end_artifact_report()
                
                tsvname = f'Instagram Archive - Logout Activity'
                tsv(report_folder, data_headers, data_list, tsvname)
                
                tlactivity = f'Instagram Archive - Logout Activity'
                timeline(report_folder, tlactivity, data_list, data_headers)
                
            else:
                logfunc('No Instagram Archive - Logout Activity data available')
                
__artifacts__ = {
        "instagramLogout": (
            "Instagram Archive",
            ('*/login_and_account_creation/logout_activity.json'),
            get_instagramLogout)
}