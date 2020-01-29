import hashlib
import json
import sys
import argparse
import requests

def printHelp():
   print('Program sprawdzający istnienie pary NIP, nr rachunku bankowego na liście czynnych podatników VAT Ministerstwa Finansów.')
   print()
   print('Parametry:')
   print('-n, --nip        nr NIP podmiotu sprawdzanego,')
   print('-r, --rach       nr rachunku bankowego podmiotu sprawdzanego,')
   print('-d, --data       data sprawdzenia,')
   print('-p, --plik       ścieżka do pliku z danymi')
   print('-h, --help       wyświetlenie pomocy')

def downloadFile(date):
   url='https://plikplaski.mf.gov.pl/pliki/'+date+'.7z'
   path='tmp/'+date+'.7z'
   print('pobieram plik '+url)

   with open(path, "wb") as file:
      response = requests.get(url)
      file.write(response.content)
   return path

def getJson(path):
   with open(path) as file:
      data=json.load(file)
   return data

def getIterations(data):
   header=data['naglowek']
   iter=header['liczbaTransformacji']
   return int(iter)

def search(data, query):
   body=data['skrotyPodatnikowCzynnych']

   if query in body:
      return True
   else:
      return False

def calculateHash(input, iterations):
   for i in range(0, iterations):
      input=input.encode('utf-8')
      input=hashlib.sha512(input).hexdigest()
   return input 

def printOutput(input, output, result, date, nip, account, iterations):
   print('data sprawdzenia: '+date)
   print('nr NIP: '+nip)
   print('nr rachunku: '+account)
   print('wejście dla funkcji skrótu: '+input)
   print('liczba transformacji: '+str(iterations))
   print('wynik obliczenia funcji skrótu SHA512:') 
   print(output)
   print('wynik sprawdzenia:')

   if result:
      print('POZYTYWNY')
   else:
      print('NEGATYWNY')

def main(args):

   if(args.pobierz!=None):
      downloadFile(args.pobierz)
      sys.exit()

   date=str(args.data)
   nip='7851769827'
   account='05102041600000290202075596'
   path='/home/sikorskim/Downloads/'+date+'.json'

   data=getJson(path)
   input=date+nip+account
   iterations=getIterations(data)
   output=calculateHash(input, iterations)
   result=search(data, output)

   printOutput(input, output, result, date, nip, account, iterations)   
 
if __name__ == "__main__":
   parser = argparse.ArgumentParser()
   parser.add_argument('-d', '--data', help='data sprawdzenia')#, required=True)
   parser.add_argument('-n', '--nip', help='NIP podmiotu sprawdzanego')
   parser.add_argument('-p', '--pobierz', help='pobiera plik płaski ze strony Ministerstwa Finansów')
   args = parser.parse_args()

   main(args)