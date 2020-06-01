import requests
header = {'accept': 'application/dns-json'}

def dns (nume):
    url = 'https://1.1.1.1/dns-query?name=' + nume
    rsp = requests.get(url)
    print (rsp.text)

dns('fmi.unibuc.ro')
