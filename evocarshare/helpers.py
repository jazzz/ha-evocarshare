from base64 import b64decode, b64encode
from zlib import compress, decompress

from homeassistant.core import HomeAssistant

from .const import LATITUDE, LONGITUDE


def get_zone_config(hass: HomeAssistant):
    zones = {}

    # Create and append a default 'Home' zone.
    zones["home"] = {
        "id": "home",
        "name": hass.config.location_name,
        LATITUDE: hass.config.latitude,
        LONGITUDE: hass.config.longitude,
    }

    return zones | hass.data["zone"].data


def get_zone_by_name(hass: HomeAssistant, name: str):
    for v in get_zone_config(hass).values():
        if v["name"] == name:
            return v
    raise KeyError(name)


def obscure(s: str) -> str:
    return b64encode(compress(bytes(s, "utf8")))


def deobscure(s: str) -> str:
    return decompress(b64decode(s)).decode("utf-8")
