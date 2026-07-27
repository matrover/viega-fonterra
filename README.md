# Viega Fonterra Smart Control

[Add to Home Assistant](https://my.home-assistant.io/redirect/hacsrepo/?owner=matrover&repository=viega-fonterra&category=integration)
[HACS](https://hacs.xyz/docs/panel/custom_repositories)

**Home Assistant custom integration for Viega Fonterra Smart Control floor heating via Modbus TCP.**

Built based on the extensive community thread:  
https://community.home-assistant.io/t/viega-floorheating-fonterra-smart-control/284753

---

## Features

- One `climate` entity per heating zone (current temperature, target temperature, on/off)
- Additional sensors (outdoor temperature, pump status, error codes, etc.)
- Full Modbus register mapping based on Viega manual and community contributions
- Configurable via the UI (Config Flow)
- Robust error handling and automatic reconnection

---

## Installation

Click the **Add to Home Assistant** button above or add this repository manually in HACS:

- **Repository**: `matrover/viega-fonterra`
- **Category**: `Integration`

After installation, go to **Settings → Devices & Services → Add Integration** and search for **Viega Fonterra**.

---

## Configuration

The integration is configured through the UI. You will be asked for:
- Modbus Host (IP address of the Fonterra WiFi module)
- Port (default 502)
- Your heating zones

---

## Register Map (summary)

| Register | Type   | Description                  | Scaling |
|----------|--------|------------------------------|---------|
| 50+x     | Input  | Current temperature zone x   | ×0.1    |
| 51+x     | Holding| Target temperature zone x    | ×0.1    |
| 100      | Input  | Outdoor temperature          | ×0.1    |
| 200+     | Holding| Pump status, errors, etc.    | -       |

Full mapping is implemented in the code (`climate.py` and `sensor.py`).

---

## Support

Report issues on [GitHub Issues](https://github.com/matrover/viega-fonterra/issues).

This integration has **not yet been tested on live hardware** — testing feedback is very welcome.

---

**Repository:** https://github.com/matrover/viega-fonterra
