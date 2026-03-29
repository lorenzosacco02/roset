import re
import ipaddress


from ...foundation.parser.grammar_parser import Parser
from ...model.bgp_session import BgpSession
from ...model.interface import Interface, VlanInterface



# BGP Regex
BGP_SECTION: re.Pattern = re.compile(r"^router bgp (\d+)\n(.*?)^\!", re.MULTILINE | re.DOTALL)
NEIGHBOR_REMOTE_AS: re.Pattern = re.compile(r"^\s+neighbor (\S+) remote-as (\d+)", re.MULTILINE)
# NEIGHBOR_DESCRIPTION: re.Pattern = re.compile(r"^\s+neighbor (\S+) description (.+)", re.MULTILINE)

# Interface Regex
IFACE_SECTION: re.Pattern = re.compile(r"^interface (\S+)\n(.*?)^!", re.MULTILINE | re.DOTALL)
IFACE_ADDRESS: re.Pattern = re.compile(r"^\s+ip(?:v6)? address (\S+)", re.MULTILINE)
VLAN_IFACE: re.Pattern = re.compile(r"^(.+)\.(\d+)$")



class FrrParser(Parser):

    def _parse_interfaces(self, content: str) -> None:
        for name, body in IFACE_SECTION.findall(content):
            addresses = [ipaddress.ip_interface(a) for a in IFACE_ADDRESS.findall(body)]
 
            vlan_match = VLAN_IFACE.match(name)
            if vlan_match:
                phy_name = vlan_match.group(1)
                vlan_id = int(vlan_match.group(2))
                if phy_name not in self._configuration.interfaces:
                    self._configuration.interfaces[phy_name] = Interface(phy_name)
                iface = VlanInterface(name, self._configuration.interfaces[phy_name], vlan_id)
            else:
                iface = Interface(name)
 
            for addr in addresses:
                iface.add_address(addr)
 
            self._configuration.interfaces[name] = iface

    def _parse_bgp(self, content: str) -> None:
        match = BGP_SECTION.search(content)
        if not match:
            return

        local_as = int(match.group(1))
        self._configuration.local_as = local_as

        bgp_body = match.group(2)

        # Creiamo sessioni e peering
        for remote_ip, remote_as_str in NEIGHBOR_REMOTE_AS.findall(bgp_body):
            remote_as = int(remote_as_str)

            if remote_as not in self._configuration.sessions:
                self._configuration.sessions[remote_as] = BgpSession(local_as, remote_as)

            self._configuration.sessions[remote_as].add_peering(
                local_ip=None,       # In FRR non è esplicito, viene inferito dopo
                remote_ip=remote_ip,
            )

