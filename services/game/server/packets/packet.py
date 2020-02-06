from typing import Dict


class Packet:

    def encode(self) -> Dict:
        return {
            "packet_type": self.__class__.get_type()
        }

    @staticmethod
    def decode():
        pass

    @staticmethod
    def get_type() -> str:
        pass
