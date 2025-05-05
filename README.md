# ✈️ AviBot - Discord Aviation Bot

AviBot is a simple Discord bot that provides airport and aircraft information.

## Features
- `!airport <ICAO_CODE>` – Fetches airport details using the AviationStack API.
- `!aircraft <CODE>` – Displays aircraft data from a JSON file.

## Quick Setup
1. Install dependencies:
   ```
   pip install discord.py requests
   ```
2. Add your Discord Bot Token and AviationStack API key into `avibot.py`.
3. Create `aircraft_data.json` with aircraft info.
4. Run the bot:
   ```
   python avibot.py
   ```

## Example Commands
```
!airport KATL
!aircraft A320
```


