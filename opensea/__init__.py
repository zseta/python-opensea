"""Top-level package for OpenSea API Python wrapper."""

__author__ = """Attila Toth"""
__email__ = "hello@attilatoth.dev"
__version__ = '0.1.7'
__all__ = ["Events", "Asset", "Assets", "Contract", "Collection",
           "CollectionStats", "Collections", "Bundles", "utils",
           "OpenseaAPI"]

from opensea.opensea import Events, Asset, Assets, Contract, Collection, \
    CollectionStats, Collections, Bundles
from opensea.opensea_api import OpenseaAPI
from opensea import utils
