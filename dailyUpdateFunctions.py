
def rpcRequest(requestPayload):
    from alchemyEndpoint import endpoint  #(inputQueryString, graphURL)
    import requests
    import json
    import time

    apiCall = endpoint('arbitrum')

    #print('API string: ', apiCall)

    request_headers = {
        "Content-Type": "application/json"
    }
    # alchemy api call request headers
    while True:
        api_post = requests.post(apiCall, headers=request_headers, data=json.dumps(requestPayload))
        # calls the alchemy api to look up the token balance at the given block

        result = api_post.json()
        # turns the result into a usable json

        if 'result' in result:
            break #success getting result, exit loop to return

        if 'error' in result:
            print("Error calling RPC",result['error'])

        time.sleep(0.5)
        print("Retrying RPC request")

    #print(result)
    time.sleep(0.25)    #delay to avoid overwhelming RPC on success

    return (result)


def getAddressDebt (blockNumber, alchemist, address):
    from twos_complement import twos_complement

    dataStr = '0x5e5c06e2000000000000000000000000' + address[2:]
    #payload data string

    requestPayload = {
        "id": 1,
        "jsonrpc": "2.0",
        "method": "eth_call",
        "params": [
            {
                "to": alchemist,
                "data": dataStr
            },
        blockNumber
        ]
    } # payload to get address debt

    result = rpcRequest(requestPayload)

    result = twos_complement(result['result'][:66])

    print('Debt ', result)

    return(result)

def convertToUnderlying (blockNumber, alchemist, yieldToken, numShares):
    from twos_complement import twos_complement

    dataStr = '0xa4a5da43000000000000000000000000' + str(yieldToken)[2:] + str(numShares)[2:]

    requestPayload = {
        "id": 1,
        "jsonrpc": "2.0",
        "method": "eth_call",
        "params": [
            {
                "to": alchemist,
                "data": dataStr
            },
        blockNumber
        ]
    }
    # payload to convert number of shares to underlying.

    #print(requestPayload)

    result = rpcRequest(requestPayload)

    print('Underlying balance')
    print(result)

    return(twos_complement(result['result']))


def getUserBalance (blockNumber, address, alchemist, yieldToken):
    from twos_complement import twos_complement

    dataStr = '0x4bd21445000000000000000000000000' + address[2:]

    dataStr = dataStr + yieldToken[2:].zfill(64)

    requestPayload = {
        "id": 1,
        "jsonrpc": "2.0",
        "method": "eth_call",
        "params": [
            {
                "to": alchemist,
                "data": dataStr
            },
            blockNumber
        ]
    }
    # payload to make api calls

    result = rpcRequest(requestPayload)
    # turns the result into a usable json

    result = result['result'][0:66]
    # get the relevant part of the result that contains the number of shares

    print('Number of shares')
    print(result)

    return(result)


def getTokenBalance (blockNumber, tokenAddress, address):

    dataStr = '0x70a08231000000000000000000000000' + address[2:]

    requestPayload = {
        "jsonrpc": "2.0",
        "id": 1,
        "method": "eth_call",
        "params": [
            {
                "data": dataStr,
                "to": tokenAddress
            },
            blockNumber
        ]
    }

    result = rpcRequest(requestPayload)

    print(result)

    return (result['result'])


def convertYieldTokenBalanceToUnderlying (blockNumber, alchemist, yieldToken, balance):
    from twosComplement import twos_complement

    dataStr = '0x46bb87c2000000000000000000000000' + yieldToken[2:] + balance[2:]

    requestPayload = {
        "jsonrpc": "2.0",
        "id": 1,
        "method": "eth_call",
        "params": [
            {
                "data": dataStr,
                "to": alchemist
            },
            blockNumber
        ]
    }

    print('looking up underlying')
    result = rpcRequest(requestPayload)

    print('Underlying')
    print(result['result'])
    print(twos_complement(result['result']))

    return(twos_complement(result['result']))

def getHarvestRepaid (blockNumber,alchemist,harvestTxId):
    from twosComplement import twos_complement

    requestPayload = {
        "jsonrpc": "2.0",
        "id": 1,
        "method": "eth_getLogs",
        "params": [
            {
                "address": alchemist,
                "fromBlock": hex(blockNumber),
                "toBlock": hex(blockNumber),
                #"topics": ["0x88dcaca629d63d86330e97adc358b13dd0ebd703239aea96b7ea2fb331b16f4e"] #topic for Donate(address sender, address yieldToken, uint256 amount)
            }
        ]
    }

    result = rpcRequest(requestPayload)

    print(result)
    answer = {'donation': 0, 'yieldRepaid': 0}

    for event in result['result']:
        if event['transactionHash']==harvestTxId:
            match event['topics'][0]:
                case '0x4534f107610758c3931de9ad1e176476fcfb8c74adf920167e1d54ee84fcfe76':
                    #harvest event
                    #topic[1] = yieldToken
                    #data[2:66] = minimumAmountOut
                    #data[66:130] = totalHarvested
                    #data[130:194] = credit
                    answer['yieldRepaid'] += twos_complement("0x"+event['data'][130:194])
                    print("harvest", answer['yieldRepaid'])
                case '0x88dcaca629d63d86330e97adc358b13dd0ebd703239aea96b7ea2fb331b16f4e':
                    #donate event
                    #topic[1] = sender
                    #topic[2] = yieldToken
                    #data[2:66] = amount
                    answer['donation'] += twos_complement(event['data'])
                    print("donate",answer['donation'])

    return (answer)