"""Top-level package for OpenSea API Python wrapper."""

__author__ = """Attila Toth"""
__email__ = "hello@attilatoth.dev"
__version__ = "0.1.2"
__all__ = ["Events", "Asset", "Assets", "Contract", "Collection",
           "CollectionStats", "Collections", "Bundles", "utils"]

from opensea.opensea import Events, Asset, Assets, Contract, Collection, \
    CollectionStats, Collections, Bundles

from opensea import utils