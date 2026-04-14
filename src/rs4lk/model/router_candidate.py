from ..foundation.configuration.vendor_configuration import VendorConfiguration
from .topology import BgpRouter


class RouterCandidate(BgpRouter):
    __slots__ = ['router_name', 'vendor', 'config_path', 'vendor_config']

    def __init__(self, router_name: str, vendor: str, config_path: str, local_as: int,
                 vendor_config: VendorConfiguration | None = None) -> None:
        super().__init__(local_as, None)
        self.router_name: str = router_name
        self.vendor: str = vendor
        self.config_path: str = config_path
        self.vendor_config: VendorConfiguration | None = vendor_config

    @property
    def machine_name(self) -> str:
        return f"as{self.identifier}_{self.router_name}"

    def __repr__(self) -> str:
        return f"RouterCandidate {self.router_name} (as{self.identifier}, vendor={self.vendor})"
