from typing import OrderedDict

from .router_candidate import RouterCandidate


class AsCandidate:
    __slots__ = ['local_as', 'routers', '_routers_by_name']

    def __init__(self, local_as: int) -> None:
        self.local_as: int = local_as
        self.routers: list[RouterCandidate] = []
        self._routers_by_name: dict[str, RouterCandidate] = {}

    def add_router(self, router: RouterCandidate) -> None:
        if router.identifier != self.local_as:
            raise ValueError(f"Router {router.router_name} has AS {router.identifier}, expected {self.local_as}")
        
        if router.router_name in self._routers_by_name:
            raise ValueError(f"Router with name {router.router_name} already exists in AS {self.local_as}")
        
        self.routers.append(router)
        self._routers_by_name[router.router_name] = router

    def get_router(self, name: str) -> RouterCandidate | None:
        return self._routers_by_name.get(name)

    def __repr__(self) -> str:
        return f"AsCandidate AS{self.local_as} ({len(self.routers)} routers: {[r.router_name for r in self.routers]})"
