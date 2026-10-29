# SSL open Zoho Projects map
Static site: `index.html` loads `projects.json` (re-checked every 30 min, cache-busted).
Live refresh: regenerate `projects.json` from Zoho Projects (get_projects_list, portal 699799171) + CompanyCam (list_projects) with `build_data.py <zoho_list_dump>` and push; the page picks up the new file on its next refresh. No credentials live in this repo.

## Refresh
Run `python3 build_data.py` (needs Zoho/CompanyCam access on the box; no secrets are stored in this repo), then commit and push the updated `projects.json`. Pages redeploys automatically.

## Privacy
This site is PUBLIC. It intentionally includes customer addresses and phone numbers (approved by Luke). Anyone with the link can see them.

## Update button
Owner-only (cosmetic, client-side): the page asks for a GitHub token once (Issues: write on this repo, kept in the browser's localStorage), looks up the login, and shows **Update** only if the login is in `ALLOW` in `index.html` (currently `xlukex15`; add lowercase logins to that array to allow more people). Pressing it opens an issue titled "Update request"; the owner's assistant checks for those on weekdays 7am-7pm Mountain (about every 15 minutes), rebuilds `projects.json`, pushes it, and closes the issue. The page polls for the new data and reloads. There is no server-side check on the button; the assistant only acts on issues opened by allowlisted logins.
