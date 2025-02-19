from enum import IntEnum


class EntrySubType(IntEnum):
    # FIND_SERVICE (0x00)
    # OFFER_SERVICE (0x01)
    # STOP_OFFER_SERVICE (0x02)

    # SUBSCRIBE_EVENT (0x03)
    INITIAL_EVENTS = 0x00
    EVENTGROUP_ADDED = 0x01

    # STOP_SUBSCRIBE_EVENT (0x04)

    # SUBSCRIBE_ACK (0x05)
    ACK = 0x00
    NACK = 0x01

    # SUBSCRIBE_NACK (0x06)
