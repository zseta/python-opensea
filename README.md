# OpenSea NFT API Python 3 wrapper
This an API wrapper library for the [OpenSea API](https://docs.opensea.io/reference/api-overview) written in Python 3.

The library provides a simplified interface to fetch a diverse set of NFT data points from OpenSea. 

## Supported endpoints
The wrapper covers **all** of the OpenSea API endpoints (as of 2021-12-02, NOT including the Orderbook and Rinkeby API):

* [Single asset](#get-data-about-a-single-asset) ([/asset](https://docs.opensea.io/reference/retrieving-a-single-asset))
* [Single asset contract](#get-data-about-a-single-asset-contract) ([/asset_contract](https://docs.opensea.io/reference/retrieving-a-single-contract))
* [Single collection](#get-data-about-a-single-collection) ([/collection](https://docs.opensea.io/reference/retrieving-a-single-collection))
* [Collection stats](#get-collection-stats) ([/collection/{slug}/stats](https://docs.opensea.io/reference/retrieving-collection-stats))
* [Multiple assets](#get-data-about-multiple-assets) ([/assets](https://docs.opensea.io/reference/getting-assets))
* [Multiple collections](#get-data-about-multiple-collections) ([/collections](https://docs.opensea.io/reference/retrieving-collections))
* [Multiple events](#get-data-about-multiple-events) ([/events](https://docs.opensea.io/reference/retrieving-asset-events))
* [Multiple bundles](#get-data-about-multiple-bundles) ([/bundles](https://docs.opensea.io/reference/retrieving-bundles))


## Prerequisite
As of Dec 2, 2021 you need to have an **API key** to use the OpenSea API, and thus 
you need one to use this wrapper too. [You can request a key here.](https://docs.opensea.io/reference/request-an-api-key). The API key can take over 4-7 days to recieve and requires you to show the project you are working on. 

## Installation
Install with pip:
```bash
virtualenv env && source env/bin/activate
pip install opensea-api
```

## Usage examples

```python
# import the OpenseaAPI object from the opensea module
from opensea import OpenseaAPI

# create an object to interact with the Opensea API (need an api key)
api = OpenseaAPI(apikey="YOUR APIKEY")

# fetch a single asset
contract_address = "0x495f947276749Ce646f68AC8c248420045cb7b5e"
token_id = "66406747123743156841746366950152533278033835913591691491127082341586364792833"
result = api.asset(asset_contract_address=contract_address, token_id=token_id)

# fetch multiple assets
result = api.assets(owner="0xce90a7949bb78892f159f428d0dc23a8e3584d75", limit=3)

# fetch a single contract
result = api.contract(asset_contract_address="0x495f947276749Ce646f68AC8c248420045cb7b5e")

# fetch a single collection
result = api.collection(collection_slug="cryptopunks")

# fetch multiple collections
result = api.collections(asset_owner="0xce90a7949bb78892f159f428d0dc23a8e3584d75", limit=3)

# fetch collection stats
result = api.collection_stats(collection_slug="cryptopunks")

# fetch multiple events
from opensea import utils as opensea_utils

period_start = opensea_utils.datetime_utc(2021, 11, 6, 14, 25)
period_end = opensea_utils.datetime_utc(2021, 11, 6, 14, 30)
result = api.events(
    occurred_after=period_start,
    occurred_before=period_end,
    limit=10,
    export_file_name="events.json",
)

# fetch multiple bundles
result = api.bundles(limit=2)
```

[Here's a demo video showcasing the basics.](https://www.youtube.com/watch?v=ga4hTqNRjfw)

## Documentation
* [Wrapper documentation](https://opensea-api.attilatoth.dev) (work in progress)
* [OpenSea API documentation](https://docs.opensea.io/reference/api-overview)

