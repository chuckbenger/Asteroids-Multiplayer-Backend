import logging
from typing import Optional, Dict
from server.packets.player_position import PlayerPositionPacket
from server.packets.game_left import GameLeftPacket
from server.packets.game_join import GameJoinPacket
from server.packets.player_blaster import PlayerBlasterPacket
from server.packets.asteroid_killed import AsteroidKilledPacket
from server.packets.packet import Packet

decoders = {}
decoders[PlayerPositionPacket.get_type()] = PlayerPositionPacket.decode
decoders[GameLeftPacket.get_type()] = GameLeftPacket.decode
decoders[GameJoinPacket.get_type()] = GameJoinPacket.decode
decoders[PlayerBlasterPacket.get_type()] = PlayerBlasterPacket.decode
decoders[AsteroidKilledPacket.get_type()] = AsteroidKilledPacket.decode


def decode_packet(data: Dict) -> Optional[Packet]:
    packet_type = data.get('packet_type')
    if packet_type:
        return _decode_packet_type(packet_type, data)
    else:
        logging.error(f"Invalid packet {data}")
        return None


def _decode_packet_type(packet_type: str, data: Dict) -> Optional[Packet]:
    decoder = decoders.get(packet_type)

    if decoder:
        return decoder(data)
    else:
        logging.error(f"No packet decoder for {packet_type} {data}")
        return None
