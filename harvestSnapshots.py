# Gets snapshots of harvest events
# including vault balance in the block before harvest

from subgraphRequest import subgraphRequest  #(inputQueryString, graphURL)
from alchemyEndpoint import endpoint #(network)
from dailyUpdateFunctions import getTokenBalance # (blockNumber, tokenAddress, address) convertYieldTokenBalanceToUnderlying (blockNumber, alchemist, yieldToken, balance):
from dailyUpdateFunctions import convertYieldTokenBalanceToUnderlying #(blockNumber, alchemist, yieldToken, balance)

harvestQuery = '''
{
  alchemistHarvestEvents(
    first: 1000
    orderBy: timestamp
    orderDirection: asc
    skip: 0
    where: {timestamp_gt: "0"}
  ) {
    block {
      number
    }
    contract {
      id
    }
    totalHarvested
    yieldToken
    timestamp
    transaction {
      hash
    }
  }
}
'''

graphURL = 'https://api.goldsky.com/api/public/project_cltwyhnfyl4z001x17t5odo5x/subgraphs/alchemix-arb/1.0.0/gn'

harvestEvents = subgraphRequest(harvestQuery, graphURL)

for event in harvestEvents:
#flattening the response, and adding prior block number

    event['block'] = int(event['block']['number'])
    event['contract'] = event['contract']['id']
    event['transaction'] = event['transaction']['hash']
    event['priorBlock'] = hex(event['block'] - 1)
    event['balance'] = getTokenBalance(event['priorBlock'], event['yieldToken'], event['contract'])
    event['underlyingBalance'] = convertYieldTokenBalanceToUnderlying(event['priorBlock'], event['contract'], event['yieldToken'], event['balance'])
    #print(event)

print(harvestEvents)
