# Dispatch on GitHub — setup guide

Your site will live at **https://amyevd.github.io/dispatch/**

Takes about 20–30 minutes, once. Four parts: put the files on GitHub, switch on the website, get a Google sign-in key, then set Chrome to open it.

---

## 1. Put the files on GitHub

1. Go to **github.com/new** (signed in as amyevd).
2. Repository name: `dispatch`. Leave it **Public** (free GitHub Pages needs this — your tasks and calendar are still private, see the note at the end). Click **Create repository**.
3. On the next page, click the link **uploading an existing file**.
4. Drag in these four files from the zip: `index.html`, `build_news.py`, `feeds.txt`, `news.json`. Click **Commit changes**.
5. The automation file lives in a hidden folder, so add it by hand:
   - Click **Add file → Create new file**.
   - In the name box type exactly: `.github/workflows/news.yml` (the slashes create the folders).
   - Open `news.yml` from the zip (it's in `.github/workflows/`; on a Mac press **Cmd+Shift+.** in Finder to show hidden folders), copy everything, paste it in.
   - Click **Commit changes**.

## 2. Switch on the website

1. In the repository, go to **Settings → Pages**.
2. Under **Build and deployment**, Source: **Deploy from a branch**. Branch: **main**, folder **/ (root)**. Click **Save**.
3. Wait a minute or two, then open **https://amyevd.github.io/dispatch/** — you should see the headlines and a "sign in" box.
4. Test the headline automation: go to the **Actions** tab. If it asks, click the button to enable workflows. Click **Refresh headlines → Run workflow**. After a minute or so it goes green, and from then on it refreshes the news every 2 hours during the day.

## 3. Get your Google sign-in key

This lets the page read your calendar and tasks. It's free.

1. Go to **console.cloud.google.com** and sign in with amyedyrmishi@gmail.com. Accept the terms if asked.
2. At the top, click the project picker → **New project**. Name it `Dispatch` → **Create**. Make sure it's selected at the top.
3. Turn on the two Google services:
   - Search the top bar for **Google Tasks API** → open it → **Enable**.
   - Search for **Google Calendar API** → open it → **Enable**.
4. Set up the sign-in screen: search the top bar for **Google Auth Platform** (it may also be called **OAuth consent screen**) → **Get started**.
   - App name: `Dispatch`. User support email: your Gmail. **Next**.
   - Audience: **External**. **Next**.
   - Contact email: your Gmail. **Next** → tick the agreement → **Create**.
5. Add yourself as a tester: in the left menu go to **Audience** → under **Test users** click **Add users** → enter `amyedyrmishi@gmail.com` → **Save**.
6. Create the key: in the left menu go to **Clients** → **Create client**.
   - Application type: **Web application**. Name: `Dispatch`.
   - Under **Authorized JavaScript origins** click **Add URI** and enter exactly: `https://amyevd.github.io` (no slash or `/dispatch` at the end).
   - Click **Create**. Copy the **Client ID** (it ends in `.apps.googleusercontent.com`).
7. Put the key in the page: back on GitHub, open `index.html` → click the pencil (Edit). Press Ctrl+F / Cmd+F and find `PASTE-YOUR-CLIENT-ID-HERE.apps.googleusercontent.com`. Replace that whole text inside the quotes with your Client ID. **Commit changes**.
8. Wait a minute, reload your site and click **Sign in with Google**. You'll see "Google hasn't verified this app" — that's expected for your own personal app: click **Continue**, then allow access to Tasks and Calendar.

## 4. Open it when Chrome starts

- **Computer:** Chrome menu (⋮) → **Settings → On startup → Open a specific page or set of pages → Add a new page** → `https://amyevd.github.io/dispatch/`. For a Home button too: **Settings → Appearance → Show home button** → enter the same address.
- **Android:** Chrome ⋮ → **Settings → Homepage** → enter the address.
- **iPhone:** open the page in Chrome → **Share → Add to Home Screen**.

---

## How it works day to day

- **Google Tasks:** your incomplete tasks, overdue first, then due today, then undated, then upcoming. Ticking one completes it in Google Tasks. Anything unticked just stays — tomorrow it shows as overdue. "Add a task" adds to your default Google Tasks list.
- **Schedule:** today's Google Calendar events. Ticks here are saved in the browser you ticked them in (Google Calendar events have no "done" state). Unticked one-off events from the last 7 days show under **Carried over**; repeating events don't.
- **Sign-in:** Google's sign-in on a site like this lasts about an hour. When it runs out, the page asks you to sign in again — one tap.
- **Headlines:** refresh automatically every 2 hours, roughly 6am–10pm. To add or remove a news source, edit `feeds.txt` on GitHub (one per line: `Section|Language|Source name|RSS link`).

**Privacy:** the page itself is public, like any website, but it holds no personal data. Your tasks and calendar are fetched straight from Google by your browser, only after you sign in, and are never saved to GitHub. Anyone else visiting sees only the headlines. The line `noindex` keeps it out of search results.

**Troubleshooting**

- *"Error 400: redirect_uri_mismatch" or "origin not allowed"* — the JavaScript origin in step 3.6 must be exactly `https://amyevd.github.io`.
- *"Access blocked: Dispatch has not completed verification"* — add your Gmail as a test user (step 3.5).
- *"access is off" message in a panel* — the matching API isn't enabled (step 3.3).
- *Headlines stop updating* — check the **Actions** tab; if GitHub paused the schedule, click **Enable workflow**.
