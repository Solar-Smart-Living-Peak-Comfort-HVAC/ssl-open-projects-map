# SSL open Zoho Projects map
Static site: `index.html` loads `projects.json` (re-fetched every 5 min, cache-busted).
Live refresh: regenerate `projects.json` from Zoho Projects (get_projects_list, portal 699799171) + CompanyCam (list_projects) with `build_data.py <zoho_list_dump>` and push; the page picks up the new file on its next refresh. No credentials live in this repo.

## Refresh
Run `python3 build_data.py` (needs Zoho/CompanyCam access on the box; no secrets are stored in this repo), then commit and push the updated `projects.json`. Pages redeploys automatically.

## Privacy
This site is PUBLIC. It intentionally includes customer addresses and phone numbers (approved by Luke). Anyone with the link can see them.
