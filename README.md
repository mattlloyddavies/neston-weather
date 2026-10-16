# Neston Weather Desk

A personal weather app for **Neston, Cheshire** and the Dee estuary, with a strong opinion
about whether you should light the BBQ. It's a fork of
[Heartland Weather Desk](https://github.com/teskemj/ai) by Michael Teske, converted from the
US Midwest to the UK. It's still a single self-contained HTML page: no build step, no
dependencies, no API keys.

**Live site:** https://mattlloyddavies.github.io/neston-weather/ *(after Pages is enabled)*

## What's different from the Heartland original
- **°C and mph**, UK date and time formats, **UK postcode search** (full or outward code, via postcodes.io)
- **BBQ forecast** re-tuned for British weather. 13° and dry counts as a go. It also has a
  **best BBQ day this week** strip and the gazebo-grilling verdict.
- **Terrace Report**: football, rugby, cricket and pub-garden lines. Live fixtures for
  Liverpool, Everton, Tranmere and Wrexham, or the Manchester clubs if you look at Manchester.
- **Shore & Fairway**: golf, sea fishing, and **Parkgate marsh birding** with a model
  high-water time and spring-tide flag (the daytime spring tides are the big event)
- **European AQI**, England & Wales holidays (bank holidays, Bonfire Night, St David's Day)
- **No paywall**: it's a personal build, so everything's unlocked (`const DEMO = true` in `index.html`)
- **Warnings**: the Met Office and MeteoAlarm feeds block browser access, so the app
  links to the Met Office North West warnings page instead of showing alerts in-app.

## Sources
- Forecast, humidity, air quality, pressure, UV, sun and tides: [Open-Meteo](https://open-meteo.com)
- Postcodes: [postcodes.io](https://postcodes.io) · Fixtures: ESPN public API · Radar: RainViewer

---
*The rest of this README is from the original project and still applies to the app wrapper and store tooling.*

## Run it (web)
Open `index.html` in any browser, or visit the live site. The 📍 location button needs
HTTPS (the hosted site); city/ZIP search works anywhere.

**Free vs. Premium:** new visitors get a 14-day full-access trial, then the free tier
(weather + local sports); Premium unlocks BBQ, Golf, Field & Stream and team themes.

**Paywall-free demo:** `demo.html` (e.g. `https://teskemj.github.io/ai/demo.html`) shows
everything unlocked with no paywall UI — for demos, investors, or store review. Adding
`?demo` to the normal URL does the same. `demo.html` is generated from `index.html` by
`npm run sync:web`, so keep editing `index.html` only.

## Mobile apps (iOS + Android)
The same `index.html` is wrapped with Capacitor. See **[CAPACITOR.md](CAPACITOR.md)**
to build and run, **[STORE_LAUNCH.md](STORE_LAUNCH.md)** for the data-licensing
requirements and the full App Store / Google Play submission checklist, and
**[PUSH.md](PUSH.md)** for severe-weather push alerts (client + `server/weather-alerts/`),
and **[REVENUECAT.md](REVENUECAT.md)** for in-app purchases (Premium subscription).

> `index.html` at the repo root is the single source of truth (web + app).
> Run `npm run sync:web` to copy it into `www/` before a Capacitor build.
