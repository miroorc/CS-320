import re
import netaddr
from bisect import bisect
import pandas as pd
import zipfile

ip = pd.read_csv("ip2location.csv")
low = list(ip['low'])
def lookup_region(ip_addr):
    global ip
    global low
    ip_addr = re.sub(r"[a-zA-Z]", '0', ip_addr)
    val = int(netaddr.IPAddress(f'{ip_addr}'))
    index = bisect(low, val)
    return ip.iloc[index-1]['region']


class Filing:
    def __init__(self, html):
        self.dates = re.findall(r"20[\d]{2}-[\d]{2}-[\d]{2}|19[\d]{2}-[\d]{2}-[\d]{2}", html)
        self.addresses = []
        self.hi = html
        sic = re.findall(r"SIC=([\d]{3,4})", html)
        if sic==[]:
            self.sic = None
        else:
            self.sic = int(sic[0])
    
        for addr_html in re.findall(r'<div class="mailer">([\s\S]+?)</div>', html):
            lines = []
            for line in re.findall(r'<span class="mailerAddress">[\\n]*([\s\S]+?)[\s]*</span>', addr_html):
                lines.append(line.strip())
            if lines != []:
                self.addresses.append('\n'.join(lines))
                
    def state(self):
        state = []
        test = str(self.hi)
        state = re.search(r'([A-Z]{2})\s[0-9]{5}', test)
        #return print("state",state)
        if state != None:
            return state.group(1)
        else:
            return None