# runs a subgraph request until it can't anymore
# inputs:
# query string
# subgraph endpoint
#
# outputs: all the results in json

def subgraphRequest (inputQueryString, graphURL):
    import re
    import requests

    def replace_skip_number(query_string, new_skip_number):
        # Use regular expression to find and replace the number after 'skip:'
        return re.sub(r'(skip:\s*)\d+', rf'\g<1>{new_skip_number}', query_string)

    tempData = []

    moreToGo = True

    counter = 0

    while moreToGo:

        print('Counter: ', counter)
        query = replace_skip_number(inputQueryString, (counter * 1000))

        data = {
            "query" : query
        }
        # puts the query into a usable data thingy for making a web request

        headers = {
            "Content-Type": "application/json"
        }
        #api call request headers

        print('Getting data')
        queryResponse = requests.post(graphURL, json=data, headers=headers)

        print('Turning into JSON')
        queryData = queryResponse.json()

        #print(queryData)
        print('-----')

        # Get the name of the first field under 'data'
        print('getting field name')
        first_field_name = list(queryData['data'].keys())[0]
        print(first_field_name)

        try:
            tempData.extend(queryData['data'][first_field_name])
            numberOfResponses = len(queryData['data'][first_field_name])
            if numberOfResponses < 1000:
                moreToGo = False
        except Exception as e:
            print('Error time yall')
            print(e)
            print(queryData)
            moreToGo = False

        counter = counter + 1

    return(tempData)

#testStr = '''
'''{
    alchemistDepositEvents(
        orderBy: timestamp
        orderDirection: asc
        first: 1000
        skip: 0
    ) {
        amount
        transaction {
            id
        }
        timestamp
        recipient
        sender
        yieldToken
        }
}
'''

'''graphURL = "https://api.goldsky.com/api/public/project_cltwyhnfyl4z001x17t5odo5x/subgraphs/alchemix-arb/1.0.0/gn"


subgraphRequest(testStr, graphURL)'''
