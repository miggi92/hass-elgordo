# Repository Guidelines

## Project Overview

This repository contains `hass-elgordo`, a HACS-compatible custom integration for Home Assistant. It polls the El Pais Spanish Christmas Lottery API, exposes the first three winning numbers, and creates one prize sensor for each configured ticket number.

- Integration domain: `elgordo`
- Integration path: `custom_components/elgordo/`
- Distribution: HACS custom integration and release ZIP
- Home Assistant integration type: config entry with cloud polling
- Runtime language: Python

Keep source code, identifiers, comments, docstrings, documentation, commit messages, and agent instructions in English. User-facing strings may be localized through the translation JSON files; preserve supported translations when changing UI text.

## Current Architecture

- `custom_components/elgordo/__init__.py` sets up and unloads config entries, stores the coordinator in `hass.data[DOMAIN][entry.entry_id]`, forwards the sensor platform, and reloads the entry after option changes.
- `custom_components/elgordo/config_flow.py` allows one config entry. The `tickets` field is a comma-separated string and can be changed through the options flow.
- `custom_components/elgordo/coordinator.py` owns API polling. It refreshes every 30 minutes, loads the draw summary once, and requests prize data once per configured ticket.
- `custom_components/elgordo/sensor.py` creates a ticket prize sensor for every configured ticket and three global sensors for the first, second, and third winning numbers.
- `custom_components/elgordo/const.py` owns the domain, API base URL, and manufacturer constants.
- `custom_components/elgordo/translations/` contains localized UI strings.
- `custom_components/elgordo/manifest.json` contains Home Assistant and HACS metadata, runtime requirements, and the integration version.

Do not add services, storage, yearly rollover, ticket fractions, archival behavior, or total-winnings entities unless the requested feature explicitly requires them. They are not part of the current implementation.

## Data Flow and Contracts

1. The config flow stores `tickets` in `ConfigEntry.data`; the options flow overrides it in `ConfigEntry.options`.
2. Ticket strings are split on commas and trimmed. Ticket numbers must remain strings so leading zeroes are preserved.
3. `ElGordoCoordinator` calls `${BASE_API_URL}?n=resumen` for summary data and `${BASE_API_URL}?n=<ticket>` for each ticket.
4. The API may prefix its response with non-JSON text. `_fetch_data` finds the first `{` and parses from there.
5. Coordinator data has this shape:

   ```python
   {
       "summary": {"numero1": "...", "numero2": "...", "numero3": "..."},
       "tickets": {"27133": {"premio": 0}},
   }
   ```

6. Ticket sensors expose the API's `premio` value in euros. Main prize sensors expose `numero1`, `numero2`, and `numero3`.
7. Updating options reloads the config entry so that sensors are recreated for the new ticket list.

Treat the coordinator data shape, config key names, unique IDs, and domain as compatibility contracts. If one changes, update all producers, consumers, migrations or compatibility handling, and tests together.

## Home Assistant Conventions

- Keep network I/O out of entity properties. Fetch shared data in the coordinator and let entities read `coordinator.data`.
- Never block Home Assistant's event loop. The current `requests` calls must remain in `hass.async_add_executor_job`, or be replaced completely with Home Assistant's async HTTP client.
- Convert transport errors, timeouts, HTTP errors, and malformed responses into `UpdateFailed` so Home Assistant marks updates unavailable without crashing the integration.
- Use config-entry lifecycle methods for setup, reload, and unload. Clean up data and listeners during unload.
- Give every entity a stable unique ID and shared device information.
- Prefer typed Home Assistant APIs and entity descriptions when extending the integration.
- Add config-flow validation for new user input and expose errors through translated flow strings.
- Keep secrets, credentials, and personal ticket data out of logs.

## Change Guidelines

- Make the smallest change that solves the requested behavior and follow existing module boundaries.
- **When implementing or modifying prize evaluation, you must strictly use the lottery logic defined in the `LOTERY_LOGIC.md` file.**
- Preserve leading zeroes in five-digit lottery numbers.
- Avoid duplicating ticket parsing or API interpretation when adding behavior; introduce a focused helper only when it removes actual duplication.
- Update both `en.json` and `de.json` when adding or changing user-facing translation keys.
- Keep `README.md`, `hacs.json`, `manifest.json`, and release behavior consistent with the integration directory and domain.
- Do not manually change the manifest version for ordinary code changes. The publish workflow derives it from the release tag.
- Do not add synchronous network calls directly to async functions.
- Do not silently substitute zero for communication or parsing failures; distinguish a confirmed zero prize from unavailable data.

## Validation

Install development dependencies with:

```bash
python -m pip install -r requirements.txt
```

Run the narrowest relevant checks first. The repository currently has no committed test suite, so at minimum run:

```bash
python -m compileall custom_components/elgordo
ruff check custom_components/elgordo
python -m json.tool custom_components/elgordo/manifest.json > /dev/null
python -m json.tool custom_components/elgordo/translations/en.json > /dev/null
python -m json.tool custom_components/elgordo/translations/de.json > /dev/null
```

When behavior changes, add focused pytest coverage under `tests/` for the config flow, coordinator, or sensors as appropriate. Mock external API responses; tests must not depend on the live lottery API.

Pull requests are also validated by:

- Home Assistant hassfest through `.github/workflows/hassfest.yaml`
- HACS validation through `.github/workflows/hacs_validate.yaml`

## Release Notes

GitHub releases trigger `.github/workflows/publish.yaml`. The workflow removes an optional `v` prefix from the release tag, writes that version to `manifest.json`, creates `elgordo.zip` from the integration directory, and uploads the archive to the release.