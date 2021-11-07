# Python 3 wrapper for the OpenSea NFT API
This an API wrapper library for the [OpenSea API](https://docs.opensea.io/reference/api-overview) written in Python 3.

The library provides a simplified interface to fetch a diverse set of NFT data points from OpenSea. 

## Supported endpoints
The wrapper covers **all** of the OpenSea API endpoints (as of 2021-10-07, NOT including the Orderbook and Rinkeby API):

* Single asset ([/asset](https://docs.opensea.io/reference/retrieving-a-single-asset))
* Single asset contract ([/asset_contract](https://docs.opensea.io/reference/retrieving-a-single-contract))
* Single collection ([/collection](https://docs.opensea.io/reference/retrieving-a-single-collection))
* Collection stats ([/collection/{slug}/stats](https://docs.opensea.io/reference/retrieving-collection-stats))
* Multiple assets ([/assets](https://docs.opensea.io/reference/getting-assets))
* Multiple collections ([/collections](https://docs.opensea.io/reference/retrieving-collections))
* Multiple events ([/events](https://docs.opensea.io/reference/retrieving-asset-events))
* Multiple bundles ([/bundles](https://docs.opensea.io/reference/retrieving-bundles))

## Installation
Install with pip:
```bash
pip install opensea-api
```

## Usage

### Get data about a single asset
```python
from opensea import Asset
api = Asset(asset_contract_address="0x495f947276749Ce646f68AC8c248420045cb7b5e",
            token_id="66406747123743156841746366950152533278033835913591691491127082341586364792833")
print(api.fetch())
```

### Get data about a single asset contract
```python
from opensea import Contract
api = Contract(asset_contract_address="0x495f947276749Ce646f68AC8c248420045cb7b5e")
print(api.fetch())
```

### Get data about a single collection
```python
from opensea import Collection
api = Collection(collection_slug="cryptopunks")
print(api.fetch())
```

### Get collection stats
```python
from opensea import CollectionStats
api = CollectionStats(collection_slug="cryptopunks")
print(api.fetch())
```

### Get data about multiple assets 
This example fetches three NFTs that Snoop Dogg owns:
```python
from opensea import Assets
api = Assets()
print(api.fetch(owner="0xce90a7949bb78892f159f428d0dc23a8e3584d75",
                limit=3))
```

### Get data about multiple collections
This example creates a JSON file with 3 collections where Snoop Dogg is an owner:
```python
from opensea import Collections
api = Collections()
print(api.fetch(asset_owner="0xce90a7949bb78892f159f428d0dc23a8e3584d75",
                limit=3,
                export_file_name='snoop_collections.json'))
```
     
### Get data about multiple events
This example creates a JSON file with 10 events that happened between the defined time period (UTC timezone)
between 2021-11-06 14:25 and 2021-11-06 14:30
```python
from opensea import Events
from opensea import utils
api = Events()
period_start = utils.datetime_utc(2021, 11, 6, 14, 25)
period_end = utils.datetime_utc(2021, 11, 6, 14, 30)
print(api.fetch(occurred_after=period_start,
                occurred_before=period_end,
                export_file_name='events.json'))
```

### Get data about multiple bundles    
```python
from opensea import Bundles
api = Bundles()
print(api.fetch(limit=3))
```


## Documentation
* [Wrapper documentation](https://opensea-api.attilatoth.dev) (work in progress)
* [OpenSea API documentation](https://docs.opensea.io/reference/api-overview)

