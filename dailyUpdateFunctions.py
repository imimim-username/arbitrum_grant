def getAddressDebt (blockNumber, alchemist, address):
    import requests
    import json
    import time
    from twos_complement import twos_complement

    alchemyLocation = "/home/imimim/alchemix/user_debt/alchemy_api_key_arbitrum.txt"
    api_key = open(alchemyLocation, "r")
    # get the alchemy api key for network

    keyValue = api_key.read()
    # read the key from the file

    api_key.close()
    # close the opened file

    apiCall = "https://arb-mainnet.g.alchemy.com/v2/" + keyValue

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

    request_headers = {
        "Content-Type": "application/json"
    }
    # alchemy api call request headers'''

    api_post = requests.post(apiCall, headers=request_headers, data=json.dumps(requestPayload))
        # calls the alchemy mainnet API for alusd debt using the above settings

    result = api_post.json()
    # turns the result into a usable json

    result = twos_complement(result['result'][:66])

    print('Debt ', result)

    return(result)

def convertToUnderlying (blockNumber, alchemist, yieldToken, numShares):
    import requests
    import json
    import time
    from twos_complement import twos_complement

    alchemyLocation = "/home/imimim/alchemix/user_debt/alchemy_api_key_arbitrum.txt"
    api_key = open(alchemyLocation, "r")
    # get the alchemy api key for network

    keyValue = api_key.read()
    # read the key from the file

    api_key.close()
    # close the opened file

    apiCall = "https://arb-mainnet.g.alchemy.com/v2/" + keyValue

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

    request_headers = {
        "Content-Type": "application/json"
    }
    # alchemy api call request headers'''

    api_post = requests.post(apiCall, headers=request_headers, data=json.dumps(requestPayload))
        # calls the alchemy mainnet API for alusd debt using the above settings

    result = api_post.json()
    # turns the result into a usable json

    #result = twos_complement(result['result'])

    print('Underlying balance')
    print(result)

    time.sleep(0.25)
    #pausing so as to not upset alchemy.
    return(twos_complement(result['result']))


def getUserBalance (blockNumber, address, alchemist, yieldToken):
    import requests
    import json
    import time
    from twos_complement import twos_complement

    alchemyLocation = "/home/imimim/alchemix/user_debt/alchemy_api_key_arbitrum.txt"
    api_key = open(alchemyLocation, "r")
    # get the alchemy api key for network

    keyValue = api_key.read()
    # read the key from the file

    api_key.close()
    # close the opened file

    apiCall = "https://arb-mainnet.g.alchemy.com/v2/" + keyValue

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

    request_headers = {
        "Content-Type": "application/json"
    }
    # alchemy api call request headers

    api_post = requests.post(apiCall, headers=request_headers, data=json.dumps(requestPayload))
        # calls the alchemy mainnet API for alusd debt using the above settings

    result = api_post.json()
    # turns the result into a usable json

    result = result['result'][0:66]
    # get the relevant part of the result that contains the number of shares

    print('Number of shares')
    print(result)

    time.sleep(0.25)
    #pausing so as to not upset alchemy
    return(result)


def getTokenBalance (blockNumber, tokenAddress, address):

    from alchemyEndpoint import endpoint  #(inputQueryString, graphURL)
    import requests
    import json

    apiCall = endpoint('arbitrum')

    #print('API string: ', apiCall)

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

    request_headers = {
        "Content-Type": "application/json"
    }
    # alchemy api call request headers

    api_post = requests.post(apiCall, headers=request_headers, data=json.dumps(requestPayload))
    # calls the alchemy api to look up the token balance at the given block

    result = api_post.json()
    # turns the result into a usable json

    return (result['result'])


def convertYieldTokenBalanceToUnderlying (blockNumber, alchemist, yieldToken, balance):

    from alchemyEndpoint import endpoint  #(inputQueryString, graphURL)
    import requests
    import json
    from twosComplement import twos_complement

    apiCall = endpoint('arbitrum')

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

    request_headers = {
        "Content-Type": "application/json"
    }
    # alchemy api call request headers

    print('looking up underlying')
    api_post = requests.post(apiCall, headers=request_headers, data=json.dumps(requestPayload))
    # calls the alchemy api to look up the token balance at the given block

    result = api_post.json()
    # turns the result into a usable json

    print('Underlying')
    print(result['result'])
    print(twos_complement(result['result']))

    return(twos_complement(result['result']))

