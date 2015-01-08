from BeautifulSoup import BeautifulSoup
import logging
import time
from connect import authenticate

FORMAT = '%(asctime)-15s %(message)s'
logging.basicConfig(format=FORMAT,filename='icecast2_kick.log',level=logging.DEBUG)

list_url='http://listen.gsb.fm:8888/admin/listclients.xsl'
kill_url='http://listen.gsb.fm:8888/admin/killclient.xsl'

def ic2kick():
    try:
        session = authenticate()
        resp = session.get(list_url)
        soup = BeautifulSoup(resp.text)
        tables = soup.findChildren('table')
        my_table = tables[-1]
        rows = my_table.findChildren(['tr'])
        for row in rows[1:]:
            cells = row.findChildren('td')
            if "ripper" in cells[2].string:
                kill_host_td = cells[3]
                host_url = kill_host_td.find('a',href=True)['href']
                host_id = host_url.split('&')[-1].split('=')[1]
                seconds = cells[1].contents[0]
                if int(seconds)>35:
                   host_status = kill_host(session,host_id)
                   if(host_status):
                       ip = cells[0].contents[0]
                       agent = cells[2].string
                       print 'Killed %s' % ip
                       logging.info('Killed host %s on %s[%s] with %s seconds (%d)' %(host_id, ip, agent,seconds, len(rows)-1))
        session.close()
    except Exception, e:
        print e
        logging.error(str(e))


def kill_host(session,host):
    session.params['id'] = host
    resp = session.get(kill_url)
    #print resp.url
    if(resp.ok):
        return True
    else:
        print resp.status_code
        return False

if __name__ == "__main__":
    while True:
        ic2kick()
        time.sleep(150)
