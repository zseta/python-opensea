# History

## 0.1.6 (2022-02-25)
* Fix /events endpoint pagination (`events_backfill()` function) by
passing only *the cursor hash* and not the full URL to the next request.

## 0.1.5 (2022-02-17)

* Ability to override base_url with any other URL
* Support for cursor-based pagination for /events endpoint (and removed deprecated arguments)
* New function to help paginate the /events endpoint
* Introducing a temporary function to fix the `next` url problem until OpenSea addresses this issue
* Minor docs updates and cleanup


## 0.1.3 (2021-12-03)

* Ability to reach all endpoints from one `OpenseaAPI` object
* API key support (Opensea requires it from now on)

## 0.1.0 (2021-11-07)

* First release on PyPI.
