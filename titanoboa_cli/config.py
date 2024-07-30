from dataclasses import dataclass, astuple
from boa.network import NetworkEnv, EthereumRPC
from boa.environment import Env
import boa


@dataclass
class Network:
    alias: str
    url: str | None

    def _create_env(self) -> NetworkEnv:
        return NetworkEnv(EthereumRPC(self.url))

    def __eq__(self, other: str | "Network") -> bool:
        if isinstance(other, str):
            return self.alias == other
        if isinstance(other, self.__class__):
            return astuple(self) == astuple(other)
        return False


class _Networks:
    _networks: dict[str, Network]

    def __init__(self):
        # call setattr a bunch in here
        # for network in toml_data: `networks.zksync`
        # for k, s in toml_data["networks"].items():
        # n = Network(url=s["url"], name=k)
        # setattr(self, k, n)
        pass

    def get_active_network(self) -> Network:
        return Network(boa.env.nickname)

    def get_network_by_name(self, alias: str) -> Network:
        # what to do with pyevm / throw exception
        return self._networks[alias]

    def __getattr__(self, name):
        # TODO
        pass


class Config:
    networks: _Networks

    def __init__(self):
        pass

    def get_active_network(self):
        return self.networks.get_active_network()
