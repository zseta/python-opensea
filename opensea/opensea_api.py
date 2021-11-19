import requests
from datetime import datetime
from opensea import utils


class OpenseaAPI:

    BASE_API_URL = "https://api.opensea.io/api"
    MAX_EVENT_ITEMS = 300
    MAX_ASSET_ITEMS = 50
    MAX_COLLECTION_ITEMS = 300
    MAX_BUNDLE_ITEMS = 50

    def __init__(self, apikey=None, version="v1"):
        """Base class to interact with the OpenSea API and fetch NFT data.

        Args:
            apikey (str): OpenSea API key (you need to request one)
            version (str, optional): API version. Defaults to "v1".
        """
        self.api_url = f"{self.BASE_API_URL}/{version}"
        self.apikey = apikey

    def _make_request(
        self, endpoint, params=None, export_file_name="", return_response=False
    ):
        """Makes a request to the OpenSea API and returns either a response
        object or dictionary.

        Args:
            endpoint (str): API endpoint to use for the request.
            params (dict, optional): Query parameters to include in the
            request. Defaults to None.
            export_file_name (str, optional): In case you want to download the
            data into a file,
            specify the filename here. Eg. 'export.json'. Be default, no file
            is created.
            return_response (bool, optional): Set it True if you want it to
            return the actual response object.
            By default, it's False, which means a dictionary will be returned.

        Raises:
            ValueError: returns the error message from the API in case one
            (or more) of your request parameters are incorrect.
            ConnectionError: your request got blocked by the server (try
            using an API key if you keep getting this error)
            TimeoutError: your request timed out (try rate limiting)

        Returns:
            Data sent back from the API. Either a response or dict object
            depending on the *return_response* argument.
        """
        headers = {"X-API-KEY": self.apikey}
        url = f"{self.api_url}/{endpoint}"
        response = requests.get(url, headers=headers, params=params)
        if response.status_code == 400:
            raise ValueError(response.text)
        elif response.status_code == 403:
            raise ConnectionError("The server blocked access.")
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
        offset=0,
        limit=None,
        occurred_before=None,
        occurred_after=None,
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
        export_file_name (str, optional): Exports the JSON data into a the
        specified file.

        Returns:
            [dict]: Events data
        """
        if occurred_after is not None and not isinstance(occurred_after,
                                                         datetime):
            raise ValueError("occurred_after must be a datetime object")

        if occurred_before is not None and not isinstance(occurred_before,
                                                          datetime):
            raise ValueError("occurred_before must be a datetime object")

        query_params = {
            "asset_contract_address": asset_contract_address,
            "collection_slug": collection_slug,
            "token_id": token_id,
            "account_address": account_address,
            "event_type": event_type,
            "only_opensea": only_opensea,
            "auction_type": auction_type,
            "offset": offset,
            "limit": self.MAX_EVENT_ITEMS if limit is None else limit,
        }
        if occurred_before is not None:
            query_params["occurred_before"] = occurred_before.timestamp()
        if occurred_after is not None:
            query_params["occurred_after"] = occurred_after.timestamp()
        return self._make_request("events", query_params, export_file_name)

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
        export_file_name="",
    ):
        """Fetches assets data from the API. Function arguments will be passed
        as API query parameters, without modification.

        OpenSea API Assets query parameters:
        https://docs.opensea.io/reference/getting-assets

        There's one extra optional argument:
        export_file_name (str, optional): Exports the JSON data into a the
        specified file.

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
        }
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
