# hass-elgordo

[![Static Badge](https://img.shields.io/badge/HACS-Custom-41BDF5?style=for-the-badge&logo=homeassistantcommunitystore&logoColor=white)](https://github.com/hacs/integration)
![GitHub Downloads (all assets, all releases)](https://img.shields.io/github/downloads/miggi92/hass-elgordo/total?style=for-the-badge)
![GitHub Release](https://img.shields.io/github/v/release/miggi92/hass-elgordo?style=for-the-badge)
![GitHub License](https://img.shields.io/github/license/miggi92/hass-elgordo?style=for-the-badge)
![GitHub Repo stars](https://img.shields.io/github/stars/miggi92/hass-elgordo?style=for-the-badge)

El Gordo Home Assistant Component

## Result fallback

The integration normally displays the current draw reported by the El Pais
lottery endpoint. Outside the draw period, the endpoint may respond without any
results. Every complete draw summary is stored by Home Assistant. In that case,
the three main prize sensors continue to display the most recently stored draw
and expose `data_source: stored_results` and its `draw_year` as state attributes.
The verified 2025 results are used only until the integration has stored its
first complete API response.

Ticket prize sensors are generally unavailable while the fallback is active.
The built-in 2025 fallback includes the verified result for ticket `27133`, so
that sensor reports `0 EUR`. Other tickets remain unavailable because reporting
`0 EUR` without checking the complete prize list would be misleading.

## Installation

[![Open your Home Assistant instance and open a repository inside the Home Assistant Community Store.](https://my.home-assistant.io/badges/hacs_repository.svg)](https://my.home-assistant.io/redirect/hacs_repository/?owner=miggi92&repository=hass-elgordo&category=Integration)

### HACS (recommended)

1. Open HACS
2. add this repository as a custom repository
3. search for "El Gordo" in the HACS store
4. install the integration
5. restart Home Assistant

### Manual

Copy the `custom_components/elgordo` folder to your Home Assistant `custom_components` folder. Then restart Home Assistant.