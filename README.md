# Viega Fonterra Smart Control - Home Assistant Integration

**HACS Custom Integration** voor de Viega Fonterra Smart Control vloerverwarming via **Modbus TCP**.

Deze integratie creëert nette `climate` entities per zone + bijbehorende sensoren (huidige temperatuur, setpoint, status, etc.).

---

## Functies

- Volledige Modbus register mapping gebaseerd op het officiële Viega document (p. 105+)
- Een `climate` entity per verwarmingszone (met target temperature, current temperature, HVAC mode)
- Extra sensor entities (pompstatus, foutmeldingen, buitentemperatuur, etc.)
- Auto-discovery van zones (configureerbaar aantal)
- Goede error handling en reconnect logica
- Logo's en nette branding

---

## Installatie via HACS

1. Ga naar **HACS** → **Integrations**
2. Klik op de 3 puntjes rechtsboven → **Custom repositories**
3. Vul in:
   - **Repository**: `https://github.com/MarijnRoverts/viega-fonterra`
   - **Category**: `Integration`
4. Klik op **Add**
5. Zoek naar **"Viega Fonterra"** en installeer het
6. Herstart Home Assistant

### Configuratie (configuration.yaml)

```yaml
modbus:
  - name: viega_fonterra
    type: tcp
    host: 192.168.1.XXX          # IP van de Fonterra Wifi module
    port: 502
    sensors:
      - name: "Fonterra Buiten Temperatuur"
        slave: 1
        address: 100
        input_type: input
        data_type: int16
        scale: 0.1
        precision: 1
        unit_of_measurement: "°C"

viega_fonterra:
  modbus_hub: viega_fonterra
  zones:
    - name: "Woonkamer"
      zone_id: 1
    - name: "Slaapkamer"
      zone_id: 2
    - name: "Badkamer"
      zone_id: 3
    # Voeg hier al je zones toe
```

---

## Register Map (samenvatting uit Viega handleiding + community)

| Register | Type | Beschrijving | Scaling |
|----------|------|--------------|---------|
| 50       | Input | Huidige temperatuur zone 1 | ×0.1 |
| 51       | Holding | Target temperatuur zone 1 | ×0.1 |
| 100      | Input | Buitentemperatuur | ×0.1 |
| 200+     | Holding | Pompstatus, foutcodes, etc. | - |

Volledige mapping staat in `modbus_map.py` in de repo.

---

## Status

- **Versie**: 1.0.0 (eerste release)
- **Teststatus**: Nog niet getest op live hardware (zoals je aangaf)
- **Gemaakt voor**: Marijn Roverts

---

## Bijdragen

Pull requests zijn welkom. Vooral testen op echte hardware is zeer gewenst.

---

**Gemaakt met ❤️ voor de Home Assistant community**

Repo: https://github.com/MarijnRoverts/viega-fonterra
