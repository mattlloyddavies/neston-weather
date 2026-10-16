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
- **No paywall, no phone app**: it's a personal web build, so everything's unlocked (`const DEMO = true` in `index.html`)
  and the iOS/Android wrapper, store assets and push server have been removed
- **Radar** shows RainViewer's free tiles, which stop at zoom 7, so the map stretches them past that.
  The **Clouds** layer is an Open-Meteo cloud-cover grid, because RainViewer dropped its free satellite feed.
- **Warnings**: the Met Office and MeteoAlarm feeds block browser access, so the app
  links to the Met Office North West warnings page instead of showing alerts in-app.

## Sources
- Forecast, humidity, air quality, pressure, UV, sun and tides: [Open-Meteo](https://open-meteo.com)
- Postcodes: [postcodes.io](https://postcodes.io) · Fixtures: ESPN public API · Radar: RainViewer

## Run it
Open `index.html` in any browser, or visit the live site. The 📍 location button needs
HTTPS (the live site); town and postcode search work anywhere. Every push to `main`
redeploys GitHub Pages automatically.
