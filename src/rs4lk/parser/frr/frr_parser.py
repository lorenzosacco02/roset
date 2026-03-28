from ...foundation.parser.grammar_parser import Parser

import re

from ...model.bgp_session import BgpSession


# BGP Regex
BGP_SECTION: re.Pattern = re.compile(r"^router bgp (\d+)\n(.*?)^\!", re.MULTILINE | re.DOTALL)
NEIGHBOR_REMOTE_AS: re.Pattern = re.compile(r"^\s+neighbor (\S+) remote-as (\d+)", re.MULTILINE)
# NEIGHBOR_DESCRIPTION: re.Pattern = re.compile(r"^\s+neighbor (\S+) description (.+)", re.MULTILINE)


class FrrParser(Parser):

    def _parse_interfaces(self, content: str) -> None:
        # Per ora non implementato
        pass

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

