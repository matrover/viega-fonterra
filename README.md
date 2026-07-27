# Viega Fonterra Smart Control

[![HACS](https://img.shields.io/badge/HACS-Custom-41BDF5.svg)](https://github.com/hacs/integration)
[![GitHub Release](https://img.shields.io/github/v/release/MarijnRoverts/viega-fonterra)](https://github.com/MarijnRoverts/viega-fonterra/releases)
[![License](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)

**Home Assistant custom integration for Viega Fonterra Smart Control floor heating via Modbus TCP.**

Built based on the extensive community thread:  
https://community.home-assistant.io/t/viega-floorheating-fonterra-smart-control/284753

---

## Features

- One `climate` entity per heating zone (current temperature, target temperature, on/off)
- Additional sensors (outdoor temperature, pump status, error codes, etc.)
- Full Modbus register mapping based on Viega manual and community contributions
- Robust error handling and automatic reconnection
- HACS compatible with branding and documentation

---

## Installation

### Via HACS (recommended)

1. Go to **HACS** → **Integrations**
2. Click the three dots in the top right → **Custom repositories**
3. Add the following:
   - **Repository**: `MarijnRoverts/viega-fonterra`
   - **Category**: `Integration`
4. Click **Add**
5. Search for **"Viega Fonterra"** and install it
6. Restart Home Assistant

### Manual installation

Copy the `custom_components/viega_fonterra` folder to your Home Assistant `config/custom_components/` directory and restart.

---

## Configuration (`configuration.yaml`)

```yaml
modbus:
  - name: fonterra
    type: tcp
    host: 192.168.1.50          # IP address of the Fonterra WiFi module
    port: 502
    delay: 0.1

viega_fonterra:
  modbus_hub: fonterra
  zones:
    - name: "Living Room"
      zone_id: 1
    - name: "Bedroom"
      zone_id: 2
    - name: "Bathroom"
      zone_id: 3
    # Add all your zones here
```

---

## Register Map (summary)

| Register | Type   | Description                  | Scaling |
|----------|--------|------------------------------|---------|
| 50+x     | Input  | Current temperature zone x   | ×0.1    |
| 51+x     | Holding| Target temperature zone x    | ×0.1    |
| 100      | Input  | Outdoor temperature          | ×0.1    |
| 200+     | Holding| Pump status, errors, etc.    | -       |

Full mapping is implemented in `climate.py` and `sensor.py`.

---

## Support & Contributing

- Created for **Marijn Roverts**
- Report issues or improvements on [GitHub Issues](https://github.com/MarijnRoverts/viega-fonterra/issues)
- This integration has not yet been tested on live hardware — testing feedback is very welcome.

---

**Thank you to all contributors in the original community thread!**

[Open your Home Assistant instance and show the integrations](https://my.home-assistant.io/redirect/integrations)

[Open your Home Assistant instance and show the dashboard](https://my.home-assistant.io/redirect/dashboard)
