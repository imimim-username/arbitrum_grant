# Network name is input, and it outputs usable Alchemy API endpoint with API key
# Current acceptable inputs are as follows:
# mainnet
# optimism

def endpoint (network):

    import requests
    import json

    match network:
        case 'mainnet':
            api_key = open("/home/imimim/alchemix/arbitrum/alchemy_api_key_mainnet.txt", "r")
            # get the alchemy_api_key

            alchemy_key = api_key.read()
            # read the key from the file

            api_key.close()
            # close the opened file

            apiString = "https://eth-mainnet.g.alchemy.com/v2/" + alchemy_key
            # constructs the alchemy api key
        case 'optimism':
            api_key = open("/home/imimim/alchemix/arbitrum/alchemy_api_key_mainnet.txt", "r")
            # get the alchemy_api_key

            alchemy_key = api_key.read()
            # read the key from the file

            api_key.close()
            # close the opened file

            apiString = "https://opt-mainnet.g.alchemy.com/v2/" + alchemy_key
            # constructs the alchemy api key
        case 'arbitrum':
            api_key = open("/home/imimim/alchemix/arbitrum/alchemy_api_key_mainnet.txt", "r")
            # get the alchemy api key

            alchemy_key = api_key.read()
            # read the key from the file

            api_key.close()
            # close the opened file

            apiString = "https://arb-mainnet.g.alchemy.com/v2/" + alchemy_key
            # constructs the alchemy endpoint url with key

    return apiString
