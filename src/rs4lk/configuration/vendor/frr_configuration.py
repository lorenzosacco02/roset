from ...foundation.configuration.vendor_configuration import VendorConfiguration
from ...model.interface import Interface, VlanInterface



class FrrConfiguration(VendorConfiguration):
    
    def get_image(self) -> str:
        return 'frrouting/frr:9'

    def _remap_interfaces(self) -> None:
        idx = 0
        # Prima passa: assegna indici alle interfacce fisiche
        for iface in self.interfaces.values():
            if not isinstance(iface, VlanInterface):
                self.iface_to_iface_idx[iface.name] = idx
                idx += 1

        # Seconda passa: le VLAN ereditano l'indice della phy padre
        for iface in self.interfaces.values():
            if isinstance(iface, VlanInterface):
                phy_idx = self.iface_to_iface_idx[iface.phy.name]
                self.iface_to_iface_idx[iface.name] = phy_idx

    def check_health(self, result):
        raise NotImplementedError

    def check_file_existence(self, result):
        raise NotImplementedError

    def check_configuration_validity(self, result):
        raise NotImplementedError

    def check_bgp_state(self, result):
        raise NotImplementedError

    def parse_bgp_routes(self, result):
        raise NotImplementedError

    def command_healthcheck(self):
        raise NotImplementedError

    def command_list_file(self):
        raise NotImplementedError

    def command_test_configuration(self):
        raise NotImplementedError

    def command_get_neighbour_bgp_networks(self, neighbour_ip):
        raise NotImplementedError

    def command_set_iface_ip(self, num, ip):
        raise NotImplementedError

    def command_unset_iface_ip(self, num, ip):
        raise NotImplementedError

    def apply_to_network_scenario(self, net_scenario):
        raise NotImplementedError
