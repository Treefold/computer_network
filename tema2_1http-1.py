import requests

def functie(nume):
    response = requests.get('https://cloudflare-dns.com/dns-query?name=' + nume, headers={'accept': 'application/dns-json',})
    return response.json()['Answer'][0]['data']

print (functie('facebook.com'))