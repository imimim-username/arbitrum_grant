# Gets snapshots of harvest events
# including vault balance in the block before harvest

from subgraphRequest import subgraphRequest  #(inputQueryString, graphURL)
from alchemyEndpoint import endpoint #(network)
from dailyUpdateFunctions import getTokenBalance # (blockNumber, tokenAddress, address) convertYieldTokenBalanceToUnderlying (blockNumber, alchemist, yieldToken, balance):
from dailyUpdateFunctions import convertYieldTokenBalanceToUnderlying #(blockNumber, alchemist, yieldToken, balance)
from dailyUpdateFunctions import getHarvestRepaid #(blockNumber, alchemist, harvestTxId)

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

#assume each yieldToken uses a single alchemist
yieldTokens = set()

for event in harvestEvents:
#flattening the response, and adding prior block number, and getting yield token balance and underlying balance for that prior block

    yieldTokens.add(event['yieldToken'])
    event['block'] = int(event['block']['number'])
    event['contract'] = event['contract']['id']
    event['transaction'] = event['transaction']['hash']
    event['priorBlock'] = hex(event['block'] - 1)
    harvestRepaid = getHarvestRepaid(event['block'],event['contract'],event['transaction'])
    event['donation'] = harvestRepaid['donation']
    event['repaid'] = harvestRepaid['yieldRepaid']
    event['balance'] = getTokenBalance(event['priorBlock'], event['yieldToken'], event['contract'])
    event['underlyingBalance'] = convertYieldTokenBalanceToUnderlying(event['priorBlock'], event['contract'], event['yieldToken'], event['balance'])
    #print(event)

for yieldToken in yieldTokens:
    previousHarvest = {}
    for event in harvestEvents:
        if event['yieldToken']!=yieldToken:
            continue
        #skip first harvest, as we need an interval for calculating yield
        if bool(previousHarvest):
            underlyingBalance = event['underlyingBalance']
            if yieldToken=='0x248a431116c6f6fcd5fe1097d16d0597e24100f5': #we actually care more about the underlying token decimals, but this works
                underlyingBalance = underlyingBalance * 1e12 #convert from 1e6 to 1e18 (USDC to alAsset)
            duration = int(event['timestamp'])-int(previousHarvest['timestamp'])
            harvestAPR = (event['repaid']/underlyingBalance)*(365*24*60*60*100)/duration
            donationAPR = (event['donation']/underlyingBalance)*(365*24*60*60*100)/duration
            print(event['timestamp'],yieldToken,harvestAPR,donationAPR)
        previousHarvest = event

print(harvestEvents)
