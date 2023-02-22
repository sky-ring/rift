import functools
import json
import random

import requests

EDGE_ENDPOINT = "https://ton.access.orbs.network"
VESRION = 1


@functools.cache
def get_nodes():
    nodes_api = f"{EDGE_ENDPOINT}/nodes"
    body = requests.get(nodes_api).content
    nodes = json.loads(body)
    # Filter out unhealthy
    nodes = filter(lambda x: x["Healthy"] == "1", nodes)
    return list(nodes)


def route(protocol="toncenter-api-v2", testnet=False):
    return endpoint(protocol=protocol, testnet=testnet, node_id="route")


def endpoint(protocol="toncenter-api-v2", testnet=False, node_id=None):
    if node_id is None:
        nodes = get_nodes()
        i = random.randint(0, len(nodes) - 1)
        node_id = nodes[i]["Name"]
    network = "testnet" if testnet else "mainnet"
    suffix = ""
    return (
        f"{EDGE_ENDPOINT}/{node_id}/{VESRION}/{network}/{protocol}/{suffix}"
    )
