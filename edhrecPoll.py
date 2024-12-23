import requests
baseUrlCards = 'https://json.edhrec.com/pages/top/year.json'
baseUrlLands = 'https://json.edhrec.com/pages/top/lands.json'
#for the first url
responseCards = requests.get(baseUrlCards)
responseLands = requests.get(baseUrlLands)
filePathCards = 'edhrecDump/year-past2years-0.json'
filePathLands = 'lands-toplands(past2years)-0.json'

if responseCards.status_code == 200:
    with open(filePathCards, 'wb') as file:
        file.write(responseCards.content)

else:
    print('Fail cards')
        
if responseLands.status_code == 200:
    with open(filePathLands, 'wb') as file:
        file.write(responseLands.content)

else:
    print('Fail lands')

#for the iterative urls
baseUrlCards = 'https://json.edhrec.com/pages/top/year-past2years-' 
baseUrlLands = 'https://json.edhrec.com/pages/top/lands-toplands(past2years)-'
basePathCards = 'edhrecDump/year-past2years-'
basePathLands = 'edhrecDump/lands-toplands(past2years)-'
for i in range(1, 100):
    response = requests.get(baseUrlCards + str(i) + '.json')
    if response.status_code == 200:
        with open(basePathCards + str(i) + '.json', 'wb') as file:
            file.write(response.content)
    else:
        print('Fail')
        break

for i in range(1, 10):
    response = requests.get(baseUrlLands + str(i) + '.json')
    if response.status_code == 200:
        with open(basePathLands + str(i) + '.json', 'wb') as file:
            file.write(response.content)
    else:
        print('Fail')
        break
