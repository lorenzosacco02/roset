from ...foundation.parser.grammar_parser import Parser

class FrrParser(Parser):
    __slots__ = ['_bgp_groups', '_vlan_interfaces']

    def __init__(self) -> None:
        super().__init__()

        self._bgp_groups = {}
        self._vlan_interfaces: dict[str, dict] = {}

    def _parse_bgp(self, content: str) -> None:
        return

    def _parse_interfaces(self, content: str) -> None:
        return