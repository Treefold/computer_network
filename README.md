# Tema 2

## Informații temă
Punctaj: 20% din total pentru laborator.
Deadline: **27 martie 2020**, se va lucra individual.

**UPDATE**: Predarea soluției se va face într-un repository de github.
Pentru a va inscrie folositi acest link: [https://classroom.github.com/a/9xUyiMpD](https://classroom.github.com/a/9xUyiMpD)

În repository scrieti sub forma de text sau markdown rezultatele voastre, puteți adăuga printscreen-uri din terminal, bucăți de cod și observații sau explicații pentru soluționarea exercițiilor. 

Pentru printscreen, asigurați-vă că este vizibil usernameul cu care faceți apelulrile din terminal.

## Cerințe

1. Citiți informațiile despre [HTTP/S din capitolul2](https://github.com/senisioi/computer-networks/tree/2020/capitolul2#https). 
2. Citiți informațiile despre [UDP din capitolul2](https://github.com/senisioi/computer-networks/tree/2020/capitolul2#socket)
3. Citiți informațiile despre [TCP din capitolul2](https://github.com/senisioi/computer-networks/tree/2020/capitolul2#tcp)


Rezolvați:
- exercițiile de la sectiune [HTTP](https://github.com/senisioi/computer-networks/tree/2020/capitolul2#exercitii_http) (3%)
- exercitiile de la secțiunea [UDP](https://github.com/senisioi/computer-networks/tree/2020/capitolul2#exercitii_udp) (10%)
- exercițiile de la secțiunea [TCP](https://github.com/senisioi/computer-networks/tree/2020/capitolul2#exercitii_tcp). (7%)



# Exemplu solutie cu markdown


## Exerciții HTTP/S
1. Cloudflare are un serviciu DoH care ruleaza pe IP-ul [1.1.1.1](https://blog.cloudflare.com/announcing-1111/). Urmăriți [aici documentația](https://developers.cloudflare.com/1.1.1.1/dns-over-https/json-format/) pentru request-uri de tip GET către cloudflare-dns și scrieți o funcție care returnează adresa IP pentru un nume dat ca parametru. Indicații: setați header-ul cu {'accept': 'application/dns-json'}.
```python
import requests

def functie(nume):
    response = requests.get('https://cloudflare-dns.com/dns-query?name=' + nume,
                            headers={'accept': 'application/dns-json',})
    return response.json()['Answer'][0]['data']
    
print (functie('fmi.unibuc.ro'))
```
---

2. Executati pe containerul `rt1` scriptul 'simple_flask.py' care deserveste API HTTP pentru GET si POST. Daca accesati in browser [http://localhost:8001](http://localhost:8001) ce observati?
```
Apare in browser ceva interesant
```
![alt text](https://github.com/nlp-unibuc/tema-2-Treefold/blob/master/tema2_1http-2.png)
---

3. Conectați-vă la containerul `docker-compose exec rt2 bash`. Testati conexiunea catre API-ul care ruleaza pe rt1 folosind curl: `curl -X POST http://rt1:8001/post  -d '{"value": 10}' -H 'Content-Type: application/json'`. Scrieti o metoda POST care ridică la pătrat un numărul definit în `value`. Apelați-o din cod folosind python requests.
```python
import requests
url = 'http://rt1:8001/post'
headers = {}
data = {}
requests.post(url, ...)
```
![alt text](https://github.com/nlp-unibuc/tema-2-Treefold/blob/master/tema2_1http-3.png)
---

4. Urmăriți alte exemple de request-uri pe [HTTPbin](http://httpbin.org/)
```
Am aflat de metodele HTTP, GET, POST, PUT, DELETE si de [Redirects](http://httpbin.org/#/Redirects/)
```

---


## Exerciții UDP
1. Executați serverul apoi clientul fie într-un container de docker fie pe calculatorul vostru personal: `python3 udp_server.py` și `python3 udp_client.py "mesaj de trimis"`.

![alt text](https://github.com/nlp-unibuc/tema-2-Treefold/blob/master/tema2_2udp-1.png)

---

2. Modificați adresa de pornire a serverului din 'localhost' în IP-ul rezervat descris mai sus cu scopul de a permite serverului să comunice pe rețea cu containere din exterior. 
```python
port = 10000
adresa = '0.0.0.0'
server_address = (adresa, port)
```

---

3. Porniți un terminal în directorul capitolul2 și atașați-vă la containerul rt1: `docker-compose exec rt1 bash`. Pe rt1 folositi calea relativă montată în directorul elocal pentru a porni serverul: `python3 /elocal/src/udp_server.py`. 
```
root@11771184abbd:/# python3 /elocal/src/udp_server.py     
[LINE:13]# INFO     [2020-03-13 19:19:13,671]  Serverul a pornit pe localhost si portnul portul 10000
[LINE:16]# INFO     [2020-03-13 19:19:13,671]  Asteptam mesaje...
```

---

4. Modificați udp_client.py ca el să se conecteze la adresa serverului, nu la 'localhost'. Sfaturi: puteți înlocui localhost cu adresa IP a containerului rt1 sau chiar cu numele 'rt1'.
```python
port = 10000
adresa = 'rt1'
server_address = (adresa, port)
```

---

5. Porniți un al doilea terminal în directorul capitolul2 și rulați clientul în containerul rt2 pentru a trimite un mesaj serverului:  `docker-compose exec rt2 bash -c "python3 /elocal/src/udp_client.py salut"`
![alt text](https://github.com/nlp-unibuc/tema-2-Treefold/blob/master/tema2_2udp-2345.png)
---

6. Deschideți un al treilea terminal și atașați-vă containerului rt1: `docker-compose exec rt1 bash`. Utilizați `tcpdump -nvvX -i any udp port 10000` pentru a scana mesajele UDP care circulă pe portul 10000. Apoi apelați clientul pentru a genera trafic.

![alt text](https://github.com/nlp-unibuc/tema-2-Treefold/blob/master/tema2_2udp-6.png)

---

7. Containerul rt1 este definit în [docker-compose.yml](https://github.com/senisioi/computer-networks/blob/2020/capitolul2/docker-compose.yml) cu redirecționare pentru portul 8001. Modificați serverul și clientul în așa fel încât să îl puteți executa pe containerul rt1 și să puteți să vă conectați la el de pe calculatorul vostru sau de pe rețeaua pe care se află calculatorul vostru.

Modificam portul din .yml: ports: - "8080:8001/udp"

``` python3 (docker-compose exec rt1 bash)
# Receiver - rt1 
import socket
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock.bind(('0.0.0.0', 8001))
print (sock.recvfrom(1))
```

``` python3 
# Sender - My PC (cmd)
import socket
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock.bind(('0.0.0.0', 8001))
print (sock.recvfrom(1))
```

```
Tcpdump: 
IP (tos 0x0, ttl 64, id 13826, offset 0, flags [DF], proto UDP (17), length 29)
    172.111.111.1.56752 > 172.111.0.1.8001: UDP, length 1
```

![alt text](https://github.com/nlp-unibuc/tema-2-Treefold/blob/master/tema2_2udp-7.png)

---


## Exerciții TCP

1. Executați serverul apoi clientul fie într-un container de docker fie pe calculatorul vostru personal: `python3 tcp_server.py` și `python3 tcp_client.py "mesaj de trimis"`.

![alt text](https://github.com/nlp-unibuc/tema-2-Treefold/blob/master/tema2_3tcp_1.png)
---

2. Modificați adresa de pornire a serverului din 'localhost' în IP-ul rezervat '0.0.0.0' cu scopul de a permite serverului să comunice pe rețea cu containere din exterior. Modificați tcp_client.py ca el să se conecteze la adresa serverului, nu la 'localhost'. Pentru client, puteți înlocui localhost cu adresa IP a containerului rt1 sau chiar cu numele 'rt1'.

3. Într-un terminal, în containerul rt1 rulați serverul: `docker-compose exec rt1 bash -c "python3 /elocal/src/tcp_server.py"`. 

4. Într-un alt terminal, în containerul rt2 rulați clientul: `docker-compose exec rt1 bash -c "python3 /elocal/src/tcp_client.py TCP_MESAJ"`

```
Printscreen pentru 2, 3, si 4
```
![alt text](https://github.com/nlp-unibuc/tema-2-Treefold/blob/master/tema2_3tcp-234.png)

---

5. Mai jos sunt explicați pașii din 3-way handshake captați de tcpdump și trimiterea unui singur byte de la client la server. Salvați un exemplu de tcpdump asemănător care conține și partea de [finalizare a conexiunii TCP](http://www.tcpipguide.com/free/t_TCPConnectionTermination-2.htm). Sfat: Modificați clientul să trimită un singur byte fără să facă recv. Modificați serverul să citească doar un singur byte cu recv(1) și să nu facă send. Reporniți serverul din rt1. Deschideți un al treilea terminal, tot în capitolul2 și rulați tcpdump: `docker-compose exec rt1 bash -c "tcpdump -Snnt tcp"` pentru a porni tcpdump pe rt1. 
```
-- Se incepe 3-way handshake --
IP 172.111.0.2.60294 > 172.111.0.1.10000: Flags [S], seq 1526734854, win 29200, options [mss 1460,sackOK,TS val 835152867 ecr 0,nop,wscale 7], length 0
S-a trimis SYN catre server (un client vrea sa inceapa o comunicatie cu serverul)
IP 172.111.0.1.10000 > 172.111.0.2.60294: Flags [S.], seq 4138783454, ack 1526734855, win 28960, options [mss 1460,sackOK,TS val 1972025320 ecr 835152867,nop,wscale 7], length 0
S-a trimis SYN si ACK (serverul accepta comunicatia si ii spune clientului asta)
IP 172.111.0.2.60294 > 172.111.0.1.10000: Flags [.], ack 4138783455, win 229, options [nop,nop,TS val 835152867 ecr 1972025320], length 0
S-a trimis ACK (clientul ii transmite serverului ca a inteles ca serverul a acceptat conexiunea)
-- se termina 3-way handshake = conexiune acceptata --

-- se transmit datele (1 byte) --
IP 172.111.0.2.60294 > 172.111.0.1.10000: Flags [P.], seq 1526734855:1526734856, ack 4138783455, win 229, options [nop,nop,TS val 835155874 ecr 1972025320], length 1
clientul transmite catre server 1 byte
IP 172.111.0.1.10000 > 172.111.0.2.60294: Flags [.], ack 1526734856, win 227, options [nop,nop,TS val 1972028327 ecr 835155874], length 0
serverul ii spune clientului cati bytes a primit
IP 172.111.0.2.60294 > 172.111.0.1.10000: Flags [F.], seq 1526734856, ack 4138783455, win 229, options [nop,nop,TS val 835155875 ecr 1972028327], length 0
clientul ii tansmite serverului ca toti bytes au fost ca toti bytes au fost trimisi, asa ca incheie transferul
IP 172.111.0.1.10000 > 172.111.0.2.60294: Flags [.], ack 1526734857, win 227, options [nop,nop,TS val 1972028368 ecr 835155875], length 0
severul ii transmite clientului ca a inteles ca a primit toti bytes si transferul s+a incheiat
-- toate datele trimise au fost primite de server --

-- clientul initializeaza terminarea conexiunii cu serverul --
IP 172.111.0.1.10000 > 172.111.0.2.60294: Flags [F.], seq 4138783455, ack 1526734857, win 227, options [nop,nop,TS val 1972030333 ecr 835155875], length 0
clientul a trimis ACK si FIN (clientul vrea sa incheie conexiunea cu serverul)
IP 172.111.0.2.60294 > 172.111.0.1.10000: Flags [.], ack 4138783456, win 229, options [nop,nop,TS val 835157880 ecr 1972030333], length 0
serverul trimite ACK (serverul ii trimite clentului ca a inteles ca s+a terminat comexiunea)
-- conexiune terminata --
```
