#Modules om requests te doen en met hashlib te werken (op de site van Marvel moeten characters gevonden worden 
# en zoekt het programma met een unieke url die met de api werkt; urllib.parse, requests en hashlib helpen bij het vormen hiervan
import urllib.parse
import requests
import hashlib

#connect op de api van de characters; anders straks rommelig met code om characters te raadplegen.
#enkel characters nodig om op te vragen (niet in comics zoeken, maar bij characters (comics staan ook gebonden bij characters))
api = "http://gateway.marvel.com/v1/public/characters?"
#public key van marvel gekregen (public key van Gerd Janssens; please do not re-use))
public_key = "17b5457665f46432924d720f735997de"
#Give a timestamp
timestamp = "1"
#private key van marvel gekregen (private key van Gerd Janssens; please do not re-use)
#pre_hash is later nodig
private_key = "0f937d97549dfab595cf3f5eb6be0bfb23c5c203"
pre_hash = timestamp + private_key + public_key
#MD5 hash, die gebruikt wordt bij het oproepen van de correcte url om data in te lezen (thanks youtube)
result = hashlib.md5(pre_hash.encode())

#while loop om op Marvel characters te zoeken
while True:
    name = input("Character to search for: ")
    #bij leeglaten (no input) stopt het programma (forced closen is niet mooi coderen)
    if name == "":
        break
    #de url die moet worden ingevoerd door het programma om op de correcte pagina te komen; key is nodig en de hash die gevormd wordt laat ons op het correcte uitkomen
    url = api + urllib.parse.urlencode({"name": name, "ts":timestamp, "apikey":public_key, "hash":result.hexdigest()})
    #data die uitgelezen is, in json
    data = requests.get(url).json()
    status = data["code"]
    #200 = alles is gelukt; dus als dit er is is het goed
    if status == 200:
        #bonus voor errormessage als er niks gevonden is; de pagina gaf dan een 0 voor de data d
        if data["data"]["total"] == 0:
            print("Character not found: is it a Marvel character? (ex. Batman is DC)")
        else:
            #bij success en data vondst kan alles geprint worden; naam, description, comics waar character voorkomt zijn nuttige zaken
            print("Name: " + name)
            print("Description: " + str(data["data"]["results"][0]["description"]))
            print("This character appeared in the following comics: ")
            #lijn om netjes te maken (zoals opgave ongeveer)
            print("---------- - - - - - - - - - - ----------")
            #for-lus om alle comics af te gaan
            for each in data["data"]["results"][0]["comics"]["items"]:
                print(each["name"])
                #lijn om netjes te maken (zoals opgave ongeveer) met einde regel
            print("---------- - - - - - - - - - - ----------\n")