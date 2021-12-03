# OpenSea NFT API Python 3 wrapper
This an API wrapper library for the [OpenSea API](https://docs.opensea.io/reference/api-overview) written in Python 3.

The library provides a simplified interface to fetch a diverse set of NFT data points from OpenSea. 

## Supported endpoints
The wrapper covers **all** of the OpenSea API endpoints (as of 2021-12-02, NOT including the Orderbook and Rinkeby API):

* [Single asset](###get-data-about-a-single-asset) ([/asset](https://docs.opensea.io/reference/retrieving-a-single-asset))
* [Single asset contract](###get-data-about-a-single-asset-contract) ([/asset_contract](https://docs.opensea.io/reference/retrieving-a-single-contract))
* [Single collection](###Get-data-about-a-single-collection) ([/collection](https://docs.opensea.io/reference/retrieving-a-single-collection))
* [Collection stats](###Get-collection-stats) ([/collection/{slug}/stats](https://docs.opensea.io/reference/retrieving-collection-stats))
* [Multiple assets](###Get-data-about-multiple-assets) ([/assets](https://docs.opensea.io/reference/getting-assets))
* [Multiple collections](###Get-data-about-multiple-collections) ([/collections](https://docs.opensea.io/reference/retrieving-collections))
* [Multiple events](###Get-data-about-multiple-events) ([/events](https://docs.opensea.io/reference/retrieving-asset-events))
* [Multiple bundles](###Get-data-about-multiple-bundles) ([/bundles](https://docs.opensea.io/reference/retrieving-bundles))


## Prerequisite
As of Dec 2, 2021 you need to have an API key to use the OpenSea API, and thus 
you need one to use this wrapper too. [You can request a key here.](https://docs.opensea.io/reference/request-an-api-key)

## Installation
Install with pip:
```bash
virtualenv env && source env/bin/activate
pip install opensea-api
```

## Usage examples

### Get data about a single asset
```python
from opensea import OpenseaAPI

api = OpenseaAPI(apikey="<APIKEY>")
result = api.asset(asset_contract_address="0x495f947276749Ce646f68AC8c248420045cb7b5e",
                   token_id="66406747123743156841746366950152533278033835913591691491127082341586364792833")
print(result)
```

### Get data about a single asset contract
```python
from opensea import OpenseaAPI

api = OpenseaAPI(apikey="<APIKEY>")
result = api.contract(asset_contract_address="0x495f947276749Ce646f68AC8c248420045cb7b5e")
print(result)
```

### Get data about a single collection
```python
from opensea import OpenseaAPI

api = OpenseaAPI(apikey="<APIKEY>")
result = api.collection(collection_slug="cryptopunks")
print(result)
```

### Get collection stats
```python
from opensea import OpenseaAPI

api = OpenseaAPI(apikey="<APIKEY>")
result = api.collection_stats(collection_slug="cryptopunks")
print(result)
```

### Get data about multiple assets 
This example fetches three NFTs that Snoop Dogg owns:
```python
from opensea import OpenseaAPI

api = OpenseaAPI(apikey="<APIKEY>")
result = api.assets(owner="0xce90a7949bb78892f159f428d0dc23a8e3584d75",
                    limit=3)
print(result)
```

### Get data about multiple collections
This example creates a JSON file with 3 collections where Snoop Dogg is an owner:
```python
from opensea import OpenseaAPI

api = OpenseaAPI(apikey="<APIKEY>")
result = api.collections(asset_owner="0xce90a7949bb78892f159f428d0dc23a8e3584d75",
                         limit=3,
                         export_file_name='snoop_collections.json')
print(result)
```
     
### Get data about multiple events
This example creates a JSON file with 10 events that happened between the 
defined time period (UTC timezone) between `2021-11-06 14:25` and `2021-11-06 14:30`
```python
from opensea import OpenseaAPI
from opensea import utils

api = OpenseaAPI(apikey="<APIKEY>")
period_start = utils.datetime_utc(2021, 11, 6, 14, 25)
period_end = utils.datetime_utc(2021, 11, 6, 14, 30)
result = api.events(occurred_after=period_start,
                    occurred_before=period_end,
                    limit=10,
                    export_file_name='events.json')
print(result)
```

### Get data about multiple bundles    
```python
from opensea import OpenseaAPI

api = OpenseaAPI(apikey="<APIKEY>")
result = api.bundles(limit=3)
print(result)
```

## Documentation
* [Wrapper documentation](https://opensea-api.attilatoth.dev) (work in progress)
* [OpenSea API documentation](https://docs.opensea.io/reference/api-overview)

