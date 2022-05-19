import time
import requests
from datetime import datetime
from opensea import utils


class OpenseaAPI:

    MAX_EVENT_ITEMS = 300
    MAX_ASSET_ITEMS = 50
    MAX_COLLECTION_ITEMS = 300
    MAX_BUNDLE_ITEMS = 50
    MAX_LISTING_ITEMS = 50
    MAX_OFFER_ITEMS = 50

    def __init__(self, base_url="https://api.opensea.io/api", apikey=None,
                 version="v1"):
        """Base class to interact with the OpenSea API and fetch NFT data.

        Args:
            base_url (str): OpenSea API base URL. Defaults to
            "https://api.opensea.io/api".
            apikey (str): OpenSea API key (you need to request one)
            version (str, optional): API version. Defaults to "v1".
        """
        self.api_url = f"{base_url}/{version}"
        self.apikey = apikey

    def _make_request(self, endpoint=None, params=None, export_file_name="",
                      return_response=False):
        """Makes a request to the OpenSea API and returns either a response
        object or dictionary.

        Args:
            endpoint (str, optional): API endpoint to use for the request.
            params (dict, optional): Query parameters to include in the
            request. Defaults to None.
            export_file_name (str, optional): In case you want to download the
            data into a file,
            specify the filename here. Eg. 'export.json'. Be default, no file
            is created.
            return_response (bool, optional): Set it True if you want it to
            return the actual response object.
            By default, it's False, which means a dictionary will be returned.
            next_url (str, optional): If you want to paginate, provide the
            `next` value here (this is a URL) OpenSea provides in the response.
            If this argument is provided, `endpoint` will be ignored.

        Raises:
            ValueError: returns the error message from the API in case one
            (or more) of your request parameters are incorrect.
            HTTPError: Unauthorized access. Try using an API key.
            ConnectionError: your request got blocked by the server (try
            using an API key if you keep getting this error)
            TimeoutError: your request timed out (try rate limiting)

        Returns:
            Data sent back from the API. Either a response or dict object
            depending on the `return_response` argument.
        """
        if endpoint is None:
            raise ValueError(
                """You need to define an `endpoint` when
                             making a request!"""
            )

        headers = {"X-API-KEY": self.apikey}
        url = f"{self.api_url}/{endpoint}"
        response = requests.get(url, headers=headers, params=params)
        if response.status_code == 400:
            raise ValueError(response.text)
        elif response.status_code == 401:
            raise requests.exceptions.HTTPError(response.text)
        elif response.status_code == 403:
            raise ConnectionError("The server blocked access.")
        elif response.status_code == 495:
            raise requests.exceptions.SSLError("SSL certificate error")
        elif response.status_code == 504:
            raise TimeoutError("The server reported a gateway time-out error.")

        if export_file_name != "":
            utils.export_file(response.content, export_file_name)
        if return_response:
            return response
        return response.json()

    def events(
        self,
        asset_contract_address=None,
        collection_slug=None,
        token_id=None,
        account_address=None,
        event_type=None,
        only_opensea=False,
        auction_type=None,
        limit=None,
        occurred_before=None,
        occurred_after=None,
        collection_editor=None,
        export_file_name="",
    ):
        """Fetches Events data from the API. Function arguments will be passed
        as API query parameters.

        OpenSea API Events query parameters:
        https://docs.opensea.io/reference/retrieving-asset-events

        All arguments will be passed without modification, except
        *occurred_before* and *occurred_after*. For these two args, you need
        to use datetime objects when calling this function.

        There's one extra optional argument:
        export_file_name (str, optional): Exports the JSON data into the
        specified file.

        Returns:
            [dict]: Events data
        """
        if occurred_before is not None and not isinstance(occurred_before,
                                                          datetime):
            raise ValueError("`occurred_before` must be a datetime object")

        if occurred_after is not None and not isinstance(occurred_after,
                                                         datetime):
            raise ValueError("`occurred_after` must be a datetime object")

        query_params = {
            "asset_contract_address": asset_contract_address,
            "collection_slug": collection_slug,
            "token_id": token_id,
            "account_address": account_address,
            "event_type": event_type,
            "only_opensea": only_opensea,
            "auction_type": auction_type,
            "collection_editor": collection_editor,
            "limit": self.MAX_EVENT_ITEMS if limit is None else limit,
        }
        if occurred_before is not None:
            query_params["occurred_before"] = occurred_before.timestamp()

        if occurred_after is not None:
            query_params["occurred_after"] = occurred_after.timestamp()
        return self._make_request("events", query_params, export_file_name)

    def events_backfill(
        self,
        start,
        until,
        rate_limiting=2,
        asset_contract_address=None,
        collection_slug=None,
        token_id=None,
        account_address=None,
        event_type=None,
        only_opensea=False,
        auction_type=None,
        limit=None,
        collection_editor=None,
    ):
        """
        EXPERIMENTAL FUNCTION!

        Expected behaviour:

        Download events and paginate over multiple pages until the given
        time is reached. Pagination happens **backwards** (so you can use this
        function to **backfill** events data eg. into a database) from `start`
        until `until`.

        The function returns a generator.

        Args:
            start (datetime): A point in time where you want to start
            downloading data from.
            until (datetime): How much data do you want?
            How much do you want to go back in time? This datetime value will
            provide that threshold.
            rate_limiting (int, optional): Seconds to wait between requests.
            Defaults to 2.

            Other parameters are available (all of the `events` endpoint
            parameters) and they are documented in the OpenSea docs
            https://docs.opensea.io/reference/retrieving-asset-events

        Yields:
            dictionary: event data
        """
        if not isinstance(until, datetime) or not isinstance(start, datetime):
            raise ValueError("`until` and `start` must be datetime objects")

        if until > start:
            raise ValueError(
                """`start` must be a later point in time
                             than `until`"""
            )

        query_params = {
            "asset_contract_address": asset_contract_address,
            "collection_slug": collection_slug,
            "token_id": token_id,
            "account_address": account_address,
            "event_type": event_type,
            "only_opensea": only_opensea,
            "auction_type": auction_type,
            "limit": self.MAX_EVENT_ITEMS if limit is None else limit,
            "occurred_before": start,
            "collection_editor": collection_editor,
        }

        # make the first request to get the `next` cursor value
        first_request = self._make_request("events", query_params)
        yield first_request
        query_params["cursor"] = first_request["next"]

        # paginate
        while True:
            time.sleep(rate_limiting)
            data = self._make_request("events", query_params)

            # update the `next` parameter for the upcoming request
            query_params["cursor"] = data["next"]

            time_field = data["asset_events"][0]["created_date"]
            current_time = utils.str_to_datetime_utc(time_field)
            if current_time >= until:
                yield data
            else:
                break
        yield None

    def asset(
        self,
        asset_contract_address,
        token_id,
        account_address=None,
        export_file_name="",
    ):
        """Fetches Asset data from the API.

        Args:
            asset_contract_address (str): Contract address of the NFT.
            token_id (str): Token ID of the NFT.
            account_address (str, optional). Defaults to None.
            export_file_name (str, optional): Exports the JSON data into a the
            specified file.

        Returns:
            [dict]: Single asset data
        """
        endpoint = f"asset/{asset_contract_address}/{token_id}"
        query_params = {"account_address": account_address}
        return self._make_request(endpoint, query_params, export_file_name)

    def assets(
        self,
        owner=None,
        token_ids=[],
        asset_contract_address=None,
        asset_contract_addresses=None,
        order_by=None,
        order_direction=None,
        offset=None,
        limit=None,
        collection=None,
        include_orders=False,
        pagination=False,
        rate_limiting=2,
        export_file_name="",
    ):
        """Fetches assets data from the API. Function arguments will be passed
        as API query parameters, without modification.

        OpenSea API Assets query parameters:
        https://docs.opensea.io/reference/getting-assets

        There are extra optional arguments:
        pagination (boolean, optional): Whether you want to get only the first
        page of assets, or all of them. If it's `True` it will use the
        cursor-based pagination provided by OpenSea. Defaults to False.
        rate_limiting (int, optional): Only relevant if pagination is `True`.
        It applies a rate limitation in-between requests. Defaults to 2 seconds.
        export_file_name (str, optional): Exports the JSON data into the
        specified file. If pagination is `True` this argument is ignored.

        Returns:
            [dict]: Assets data
        """
        query_params = {
            "owner": owner,
            "token_ids": token_ids,
            "asset_contract_address": asset_contract_address,
            "asset_contract_addresses": asset_contract_addresses,
            "order_by": order_by,
            "order_direction": order_direction,
            "offset": offset,
            "limit": self.MAX_ASSET_ITEMS if limit is None else limit,
            "collection": collection,
            "include_orders": include_orders
        }
        if pagination:
            # make the first request to get the `next` cursor value
            first_request = self._make_request("assets", query_params)
            yield first_request
            query_params["cursor"] = first_request.get("next")
            
            # paginate
            while True:
                time.sleep(rate_limiting)
                if query_params["cursor"] is not None:
                    response = self._make_request("assets", query_params)
                    yield response
                    query_params["cursor"] = response.get("next")
                else:
                    break # stop pagination if there is no next page
        else:
            return self._make_request("assets", query_params, export_file_name)

    def contract(self, asset_contract_address, export_file_name=""):
        """Fetches asset contract data from the API.

        OpenSea API Asset Contract query parameters:
        https://docs.opensea.io/reference/retrieving-a-single-contract

        Args:
            asset_contract_address (str): Contract address of the NFT.
            export_file_name (str, optional): Exports the JSON data into a the
            specified file.

        Returns:
            [dict]: Single asset contract data
        """
        endpoint = f"asset_contract/{asset_contract_address}"
        return self._make_request(endpoint, export_file_name=export_file_name)

    def collection(self, collection_slug, export_file_name=""):
        """Fetches collection data from the API.

        OpenSea API Collection query parameters:
        https://docs.opensea.io/reference/retrieving-a-single-collection

        Args:
            collection_slug (str): Collection slug (unique identifer)
            export_file_name (str, optional): Exports the JSON data into a the
            specified file.

        Returns:
            [dict]: Single collection data
        """
        endpoint = f"collection/{collection_slug}"
        return self._make_request(endpoint, export_file_name=export_file_name)

    def collection_stats(self, collection_slug, export_file_name=""):
        """Fetches collection stats data from the API.

        OpenSea API Collection Stats query parameters:
        https://docs.opensea.io/reference/retrieving-collection-stats

        Args:
            export_file_name (str, optional): Exports the JSON data into the
            specified file.

        Returns:
            [dict]: Collection stats
        """
        endpoint = f"collection/{collection_slug}/stats"
        return self._make_request(endpoint, export_file_name=export_file_name)

    def collections(
        self, asset_owner=None, offset=None, limit=None, export_file_name=""
    ):
        """Fetches Collections data from the API. Function arguments will be
        passed as API query parameters,
        without modification.

        OpenSea API Collections query parameters:
        https://docs.opensea.io/reference/retrieving-collections

        There's one extra optional argument:
        export_file_name (str, optional): Exports the JSON data into a the
        specified file.

        Returns:
            [dict]: Collections data
        """
        query_params = {
            "asset_owner": asset_owner,
            "offset": offset,
            "limit": self.MAX_COLLECTION_ITEMS if limit is None else limit,
        }
        return self._make_request("collections", query_params,
                                  export_file_name)

    def bundles(
        self,
        on_sale=None,
        owner=None,
        asset_contract_address=None,
        asset_contract_addresses=[],
        token_ids=[],
        limit=None,
        export_file_name="",
        offset=None,
    ):
        """Fetches Bundles data from the API. Function arguments will be
        passed as API query parameters,
        without modification.

        OpenSea API Bundles query parameters:
        https://docs.opensea.io/reference/retrieving-bundles

        There's one extra optional argument:
        export_file_name (str, optional): Exports the JSON data into a the
        specified file.

        Returns:
            [dict]: Bundles data
        """
        query_params = {
            "on_sale": on_sale,
            "owner": owner,
            "asset_contract_address": asset_contract_address,
            "asset_contract_addresses": asset_contract_addresses,
            "token_ids": token_ids,
            "limit": self.MAX_BUNDLE_ITEMS if limit is None else limit,
            "offset": offset,
        }
        return self._make_request("bundles", query_params, export_file_name)

    def listings(
        self, asset_contract_address, token_id, limit=None, export_file_name=""
    ):
        """Fetches Listings data for an asset from the API. Function arguments
        will be passed as API query parameters, without modification.

        OpenSea API Listings query parameters:
        https://docs.opensea.io/reference/asset-listings

        There's one extra optional argument:
        export_file_name (str, optional): Exports the JSON data into a the
        specified file.

        Returns:
            [dict]: Listings data
        """
        query_params = {
            "limit": self.MAX_LISTING_ITEMS if limit is None else limit
        }
        endpoint = f"asset/{asset_contract_address}/{token_id}/listings"
        return self._make_request(endpoint, query_params, export_file_name)

    def offers(self, asset_contract_address, token_id, limit=None,
               export_file_name=""):
        """Fetches Offers data for an asset from the API. Function arguments
        will be passed as API query parameters, without modification.

        OpenSea API Listings query parameters:
        https://docs.opensea.io/reference/asset-offers

        There's one extra optional argument:
        export_file_name (str, optional): Exports the JSON data into a the
        specified file.

        Returns:
            [dict]: Offers data
        """
        query_params = {
            "limit": self.MAX_OFFER_ITEMS if limit is None else limit
        }
        endpoint = f"asset/{asset_contract_address}/{token_id}/offers"
        return self._make_request(endpoint, query_params, export_file_name)
