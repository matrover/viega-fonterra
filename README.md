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
- Configurable via the UI (Config Flow)
- HACS compatible

---

## Installation

### Via HACS (recommended)

1. Go to **HACS** → **Integrations**
2. Click the three dots in the top right → **Custom repositories**
3. Add the following:
   - **Repository**: `matrover/viega-fonterra`
   - **Category**: `Integration`
4. Click **Add**
5. Search for **"Viega Fonterra"** and install it
6. Restart Home Assistant

### Manual installation

Copy the `custom_components/viega_fonterra` folder to your Home Assistant `config/custom_components/` directory and restart.

---

## Configuration

After installation, go to **Settings → Devices & Services → Add Integration** and search for **Viega Fonterra**.

You can configure the Modbus host, port and your heating zones through the UI.

---

## Register Map (summary)

| Register | Type   | Description                  | Scaling |
|----------|--------|------------------------------|---------|
| 50+x     | Input  | Current temperature zone x   | ×0.1    |
| 51+x     | Holding| Target temperature zone x    | ×0.1    |
| 100      | Input  | Outdoor temperature          | ×0.1    |
| 200+     | Holding| Pump status, errors, etc.    | -       |

Full mapping is implemented in the code.

---

## Support

Created for **Marijn Roverts**.  
Report issues on [GitHub Issues](https://github.com/matrover/viega-fonterra/issues).

This integration has not yet been tested on live hardware — testing feedback is welcome.

---

**Quick links:**

[Open your Home Assistant instance and show the integrations](https://my.home-assistant.io/redirect/integrations)

[Open your Home Assistant instance and show the dashboard](https://my.home-assistant.io/redirect/dashboard)
