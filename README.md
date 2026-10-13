# Beckham Hotel Discord Bot

A management Discord Bot built for Beckham Hotel.
Created by Aljay Leodones.

---

## What This Bot Does

This bot provides server management, announcement, onboarding, and member engagement tools for the Beckham Hotel Discord community. It includes a persistent **Mod Panel** summoned with `/summon` that stays active even after bot restarts.

Three systems power it:

| System | What it does |
| --- | --- |
| **Beckham Onboarding** | Opens a private, ticket-style **#handle-onboarding** channel for each new member, walks them through the TikTok Shop questions, the community rules and the Slack-connected questionnaire, then grants the access role that unlocks the rest of the server. |
| **Creator Onboarding** | Tags recently joined members in one post that asks *Are you a TikTok Shop creator?* with **✅ YES / ❌ NO** buttons. Each member gets a private reply based on their answer. |
| **Information Onboarding** | Scans for members who joined recently and were never welcomed, lets you pick **which join days** to include, then posts a tagged welcome and sends each member a warm branded DM. Everyone welcomed is logged so nobody is welcomed twice. |
| **Community Reports** | Daily growth baselines, joins per day, monthly trends and most-active members. Deploy one public report and it refreshes itself in place every few hours. |
| **Engagement Reports** | Ranks every member by messages, reactions and threads for any date range, published as a formal summary plus a full text file. |
| **Engagement Contest** | Start/end contest rounds, score genuine engagement across the contest channels listed in `CONTEST_CHANNEL_IDS` (2 pts per genuine message, 1 pt per reaction, 10 pts per TikTok video post), filter out spam and copy-paste, publish the Top 15 leaderboard, and browse past contests. |

All of it is driven from the Mod Panel — no commands to memorise.

---

## Step-by-Step Installation & Setup Guide

Follow these numbered steps to set up and run the bot.

---

### Phase 1: Discord Developer Portal Setup

#### Step 1: Open the Discord Developer Portal
1. Open your web browser and go to: [https://discord.com/developers/applications](https://discord.com/developers/applications)
2. Log in with your Discord account.

#### Step 2: Select or Create Your Bot Application
1. Click the **"New Application"** button in the top-right corner (or click your existing application if already created).
2. Give your application a name (for example, `Beckham Hotel Bot`) and agree to the Discord Developer terms.
3. Click **Create**.

#### Step 3: Enable Privileged Gateway Intents (Very Important)
1. In the left sidebar, click on **"Bot"**.
2. Scroll down to the section titled **"Privileged Gateway Intents"**.
3. Turn **ON** (check) all three switches:
   - **Presence Intent**
   - **Server Members Intent**
   - **Message Content Intent**
4. Click **"Save Changes"** at the bottom of the page.

#### Step 4: Get Your Bot Token
1. On the same **"Bot"** page, find the **"Token"** section.
2. Click **"Reset Token"** (or **"Copy"** if freshly generated).
3. Copy this token. This is the secret password for your bot.

#### Step 5: Create the Bot Invite Link
1. In the left sidebar, click on **"OAuth2"**, then click on **"URL Generator"**.
2. Under **"Scopes"**, check these two boxes:
   - `bot`
   - `applications.commands` (this enables slash commands like `/summon`)
3. Under **"Bot Permissions"**, check:
   - `Administrator` (or select `Manage Server`, `Send Messages`, `Embed Links`, `Read Message History`, `Use Slash Commands`).
   - For engagement reports without Administrator access, grant `View Channels` and `Read Message History` in every channel that should be analyzed, plus `Send Messages`, `Embed Links`, and `Attach Files` in the report channel.
4. Scroll to the bottom and click **"Copy"** next to the **Generated URL**.

> **Shortcut:** the Beckham Hotel Bot's ready-made invite link (Administrator + slash commands) is:
> `https://discord.com/oauth2/authorize?client_id=1552014826081886300&permissions=8&integration_type=0&scope=bot+applications.commands`

#### Step 6: Invite the Bot to Your Discord Server
1. Paste the copied URL into a new tab in your web browser.
2. Select your Discord server from the dropdown list.
3. Click **"Continue"**, then click **"Authorize"**.
4. Complete the verification check. The bot will now appear in your server member list.

---

### Phase 2: Running the Bot on Your Computer

### Quick Start Launchers (Easiest Way to Run)

- **On Mac:** Simply double-click [`start_bot.command`](start_bot.command). It automatically checks the virtual environment, verifies requirements, and starts the bot.
- **On Windows:** Simply double-click [`start_bot.cmd`](start_bot.cmd).

---

### Manual Terminal Setup (Step-by-Step)

#### Step 7: Open Your Terminal
Open the Terminal application on your computer and navigate to the project directory:
```bash
cd A:\Python\beckham-hotel
```

#### Step 8: Set Up Python Virtual Environment
Create and activate a virtual environment to manage dependencies cleanly:
```bash
python3 -m venv venv
source venv/bin/activate
```

#### Step 9: Install Required Dependencies
Install the required packages (`discord.py` and `python-dotenv`):
```bash
pip install -r requirements.txt
```

#### Step 10: Configure Your `.env` File
1. Make sure you have a `.env` file in the project root directory.
2. Open `.env` and add your bot token:
```env
DISCORD_TOKEN=your_token_here
GUILD_ID=
REPORT_CHANNEL_ID=
REPORT_TIMEZONE=Asia/Manila
```
*(Note: If you want slash commands to appear instantly in a specific test server while developing, paste your Server/Guild ID in `GUILD_ID`)*.

Everything else is optional — see [`.env.example`](.env.example) for the full list:

| Setting | Default | Purpose |
| --- | --- | --- |
| `WELCOME_CHANNEL_ID` | *(blank)* | Starting value for the welcome post channel. |
| `ONBOARDING_CHANNEL_ID` | *(blank)* | The Product Info channel linked in welcomes. |
| `INTRODUCTIONS_CHANNEL_ID` | *(blank)* | The introductions channel linked in welcomes. |
| `ONBOARDING_LOOKBACK_DAYS` | `30` | How far back the onboarding scan looks. |
| `ONBOARDING_EXCLUDED_ROLE_IDS` | *(blank)* | Comma-separated role IDs the onboarding scan always skips. |
| `REPORT_REFRESH_HOURS` | `3` | How often live community reports refresh. |
| `ENABLE_PRESENCE_INTENT` | `true` | Tracks "online now"; the bot starts without it automatically if the portal switch is off. |
| `COMMUNITY_DATABASE_PATH` | `data/community.sqlite3` | Onboarding log, growth snapshots, live reports. |

You never have to edit `.env` for the three onboarding channels — set them in Discord from **Mod Panel → Onboarding → Channel setup**, and those saved choices always win.

#### Step 11: Start the Bot
Run the bot with:
```bash
python3 main.py
```
You will see output indicating that the bot has connected:
```
[INFO] beckham_bot: Registering persistent views...
[INFO] beckham_bot: Loading extensions...
[INFO] beckham_bot.engagement: Engagement tracking database ready at data/engagement.sqlite3
[INFO] beckham_bot.database: Community database ready at data/community.sqlite3
[INFO] beckham_bot.onboarding: Onboarding ready (lookback: 30 days)
[INFO] beckham_bot.memberreport: Community reporting ready (live reports refresh every 3h)
[INFO] beckham_bot: Synced 3 global command(s).
[INFO] beckham_bot: ==========================================
[INFO] beckham_bot: Logged in as: Beckham Hotel Bot (ID: ...)
[INFO] beckham_bot: Bot is active in 1 server(s)
[INFO] beckham_bot: Presence tracking: on
[INFO] beckham_bot: ==========================================
```

---

### Phase 3: Using the Bot

#### Step 12: Summon the Mod Panel
1. Go to any text channel in your Discord server where you have moderator/admin permissions.
2. Type `/summon` and press Enter.
3. The **Beckham Hotel Management Panel** appears with live server info, bot latency, an onboarding snapshot, your live reports, a plain-English guide to every button, and a system health block.
4. Buttons on the panel:

| Button | What it opens |
| --- | --- |
| **🎟️ Beckham Onboarding** | Scan new members and open a private onboarding channel for each. **🧪 Test on myself** opens one for you. |
| **👋 Onboarding** | Creator onboarding: tag new members with the TikTok Shop question (✅ YES / ❌ NO). **🧪 Test message** sends it to any channel. |
| **ℹ️ Information Onboarding** | Scan for new members, pick which join days, send the welcome, set your channels. |
| **📊 Community Reports** | Preview or deploy self-refreshing growth reports. |
| **📈 Engagement Report** | Rank members by messages, reactions and threads. |
| **🏆 Engagement Contest** | Start a new contest, publish the Top 15 leaderboard, end a contest, review past contests, or reset all counts. |
| **📝 Embed Message** | Open the Embed Studio: compose, save reusable templates, and publish to any channel. |
| **💬 Normal Message** | Write a plain message, preview it, edit it, attach up to 4 images, then post it. |
| **🔄 Refresh Dashboard** | Reload the panel with the latest data **and the latest buttons**. |

> Already have an older panel posted? Just click **🔄 Refresh Dashboard** on it once — it upgrades that message to the new button set in place.

Two optional shortcuts post standalone panels for teams that prefer them: `/onboarding` and `/community-report`. Both are persistent, just like `/summon`.

---

#### Step 12a: Beckham Onboarding (private onboarding channels)

**First-time setup:**

1. **👋 Onboarding → ⚙️ Settings** — already points to the **information channel** (`1553106965922578595`, where 🌱 creators are sent) and the **support-ticket channel** (`1549416221995307058`, linked in the community rules). Change them there only if they move. Optionally pick a default test channel or the opportunities channel linked after completion.
2. **🎟️ Beckham Onboarding → ⚙️ Settings** — The **onboarding category** is `1559567789948141710`, and the **Member access role** granted after the questionnaire is `1559568207495303279`. Both are saved for the Beckham server and can be changed here.
3. In *Server Settings → Roles*, put the bot's role **above** the access role, and give the bot **Manage Channels** and **Manage Roles**. The hub lists anything still missing.

**Using it:**

1. Click **🧪 Test on myself**. The bot opens an onboarding channel for you, so you can click through the whole flow. Submitting the questionnaire really saves your answers for Slack and grants the role. Use **🔒 Close onboarding** when you finish. **Test on member** lets you choose someone else; `/test-onboarding [member]` opens the same test flow.
2. Click **🔍 Scan for new members**. Members who joined in the last 30 days, haven't been tagged yet, don't hold an excluded role and don't already have the access role are grouped by join day. Pick the days and press **🎟️ Open N onboarding channels**.
3. Need to tag a group again? Scan, then press **♻️ Clear last tagged group & rescan**. Tagging them again re-uses their existing channels.
4. *(Optional)* **📌 Post Shop 101 checkpoint** posts an *I've finished TikTok Shop 101* button in the TikTok Shop 101 channel.

What each member gets — in **#their-name-onboarding**, visible only to them and your moderators:

```
@member 🔒 This is your private onboarding channel … finish the onboarding below
to unlock all of the server's channels.
👋 Welcome to the Beckham Hotel Creator Community! … Are you a TikTok Shop creator?
  ❌ NO   → how to get started with TikTok Shop
  ✅ YES  → "Where are you in your TikTok Shop journey?"
             🌱 Still learning  → head to TikTok Shop 101
                                  [✅ I've finished TikTok Shop 101] → next step
             🔥 Experienced     → community rules + questionnaire
Questionnaire submitted → answers saved and sent to Slack, access role granted
```

Only the channel's member can answer in it. A category holds at most **50** channels, so delete finished onboarding channels from time to time. The **👋 Onboarding** button also opens one private channel per member. Its **Test message** control can post the questions to a shared channel with private replies. **Close onboarding** asks for confirmation and deletes the channel; only its member or a moderator can close it. Buttons remain registered after a restart.

---

#### Step 13: Welcome New Members (Information Onboarding)

1. On the Mod Panel click **ℹ️ Information Onboarding**.
2. The channels come pre-set from `.env` (welcome post + introductions: `1551941518426771466`, product info: `1552014138333593620`). To change them, click **⚙️ Channel setup**:
   - **Welcome post channel** — where the welcome message is posted.
   - **Product info** — linked in every welcome as `{product_info_channel}`.
   - **Introductions** — linked in every welcome as `{introductions_channel}`.
   Each choice saves instantly and survives restarts.
3. Click **🔍 Scan for new members**. The bot lists everyone who joined in the last 30 days, was never welcomed, and holds none of the `ONBOARDING_EXCLUDED_ROLE_IDS` roles — grouped per join date:
   ```
   ▸ Today · 23 Sep 2026 — 4 member(s)  ✅
   ▸ 1 day ago · 22 Sep 2026 — 2 member(s)  ✅
   ▸ 2 days ago · 21 Sep 2026 — 1 member(s)  ✅
   ...
   ▸ 30 days ago · 24 Aug 2026 — 3 member(s)  ✅
   ```
4. **Tick or untick join days** in the menu (a second menu appears when there are more than 25 days). Every day starts selected; **Select all** / **Clear** reset it.
5. Click **▶️ Preview welcome**. The preview shows the saved welcome message and where it will go. From there:
   - **📣 Post in #channel** — posts one normal message tagging every selected member.
   - **#️⃣ Choose another channel** — post this one somewhere else.
   - **✍️ Edit message** — change the text for this welcome.
   - **💾 Save as default** — keep your edit for every future welcome.
   - **✉️ Warm DM: Off/On** — optionally DM each member a branded welcome too.
6. Everyone welcomed is logged as onboarded so the next scan skips them.

To edit the welcome message without sending anything, click **✍️ Welcome message** on the onboarding hub: **Edit & save** stores your version, **Restore original** brings back the built-in default.

Notes:
- DMs (when switched on) are paced at **one per second** to respect Discord's rate limits. The summary reports how many DMs landed and who has DMs closed.
- **📋 Onboarding stats** shows how many members are waiting, how many were welcomed this week, and the all-time total.
- **♻️ Reset onboarding log** clears the log if you ever want to welcome people again.
- Onboarding panels posted before this update need to be re-posted (`/onboarding` or `/summon`) to show the new **Welcome message** button.

Placeholders you can use in any message (welcome posts, embeds, plain messages):

```
{user_mention}  {user_name}  {server_name}  {member_count}  {date_now}
{time_now}  {brand}  {product_info_channel}  {onboarding_channel}
{introductions_channel}  {welcome_channel}
```

---

#### Step 14: Deploy a Community Report

1. On the Mod Panel click **📊 Community Reports**.
2. **Select which days** the report covers: today, 7 days, 14 days, 30 days, 90 days, or **Custom number of days** (anything from 1 to 365).
3. Then either:
   - **👀 Preview a report** — private, nothing is posted; or
   - **📌 Deploy live report** — pick a channel and the report goes public.
4. A deployed report **refreshes itself in place** every 3 hours (`REPORT_REFRESH_HOURS`) and on every bot start. You never repost it.
5. **🔄 Refresh now** updates every live report immediately. **🗂️ Manage live reports** stops one from refreshing (the posted message stays).

Each report shows:
- **Membership growth** — total, members, bots and online now, each compared to the stored baseline from that many days ago, with the arrow and percentage change.
- **New members per day** — a 14-day bar chart.
- **Joins trend** — monthly totals plus this month versus the same point last month.
- **Most active members** — top contributors for the window, taken from the engagement tracker.
- **Server snapshot** — members, bots, team/admins and online count.

How the numbers stay accurate:
- A baseline snapshot is recorded at **00:05 UTC** every day, on every refresh, and whenever a report is built.
- Join tallies come from live join events **and** are re-derived from every member's join date on each refresh, merged with `MAX()`. Nothing is lost while the bot is offline.
- "Online now" needs the **Presence Intent**. If that switch is off in the Developer Portal the bot notices, starts without it, and hides just that one metric.

---

#### Step 15: Generate an Engagement Report
1. Open the Mod Panel and click **📈 Engagement Report**.
2. Choose **Past 1 day**, **Past 7 days**, **Past 1 month**, or **Custom date range**.
3. For a custom range, enter `YYYY-MM-DD` or `YYYY-MM-DD HH:MM`. Date-only end dates include the complete end day.
4. The bot publishes a formal summary and full ranked text report to `REPORT_CHANNEL_ID`.

The tracker counts each non-bot member's messages, reactions added, and threads created. Each action is one activity point. Reports rank up to 300 members in servers with 300 or fewer members, or up to 1,000 members in larger servers. Before publishing, the bot backfills every readable text channel and active or archived thread for the selected period. Large date ranges can take a few minutes. Discord does not expose historical reaction timestamps, so backfilled reaction totals represent reactions currently visible on messages posted during the selected period; live reaction events use their actual event time.

---

#### Step 15b: Run an Engagement Contest

The contest runs in **rounds**. Starting a contest fixes the starting point of the
count, so nothing posted beforehand can ever score.

1. Open the Mod Panel and click **🏆 Engagement Contest**. The hub shows whether a
   contest is currently running, the scoring rules, and the counted channels.
2. Click **🚀 Start New Contest**, give the round a name (e.g. `September Engagement
   Contest`) and submit. Counting begins at that exact moment. If a contest was
   already running it is closed automatically.
3. While it runs, click **🏆 Publish Leaderboard** at any time to scan the contest
   channels and post the current Top 15 standings to `CONTEST_REPORT_CHANNEL_ID`.
4. Click **🛑 End Contest** to close the round. The final standings are frozen into
   the archive and published as **FINAL RESULTS**.
5. Click **📜 Past Contests** to browse every round on record, view its leaderboard,
   and re-post an archived leaderboard to the report channel.
6. **⚙️ Ad-hoc Report** scores any date range without touching the running contest.
7. **♻️ Reset All Counts** permanently deletes every recorded event and every
   archived contest for the server. Use it only to start the system from scratch —
   to simply begin a new round, use **Start New Contest** instead, which keeps
   old contests archived.

**How points are awarded**

| Action | Points | Conditions |
| --- | --- | --- |
| 💬 Genuine message | **2** | More than two real words. Links, mentions and emoji do not count as words. |
| 🎬 TikTok video post | **10** | Any `tiktok.com`, `vm.`, `vt.` or `m.tiktok.com` link. Each clip scores once per member. |
| ❤️ Reaction | **1** | Every reaction added in a contest channel. |

**What does not score**

- Messages of two words or fewer, and messages that are only a link, mention or emoji.
- The same text repeated by the same member within `CONTEST_SELF_REPEAT_HOURS` (default 24h).
- Text copy-pasted from another member within `CONTEST_CROSS_REPEAT_MINUTES` (default 60m) — only the first person to post it scores.
- Rapid-fire bursts: two scoring messages less than `CONTEST_MESSAGE_COOLDOWN_SECONDS` apart (default 10s).
- Anything from a bot or a member holding an excluded moderator role.

Every filtered item is counted and reported under **Spam / Duplicates Filtered** on
the leaderboard, so the numbers are always auditable.

Raw activity is stored **unscored**; points are calculated at report time by
replaying events in chronological order. That means the leaderboard is fully
reproducible, and the rules above can be re-tuned in `.env` without ever needing
to re-scan Discord.

---

#### Step 16: Compose and Reuse Embeds (Embed Studio)

1. On the Mod Panel click **📝 Embed Message**. The **Embed Studio** opens privately, showing your current draft, the server's template library and the placeholders you can use.
2. Click **✏️ Edit embed** and fill in whatever you need — every field is optional on its own:
   - **Title**
   - **Message** (the embed body)
   - **Text above the embed** — for a ping or a short intro, e.g. `<@&role>`
   - **Image link** — leaving this blank keeps whatever banner is already set; use **🖼️ Banner image** to upload or remove one
   - **Colour hex** — blank for Beckham navy, or e.g. `C8A96A`
3. **🖼️ Banner image** sets the big picture inside the embed. **Upload the file straight from your computer** — that is the reliable way — or paste a link if you prefer. To take the banner off, answer `yes` to **Remove the current banner?**.
4. Save it for next time with **💾 Save as template** and give it a name (up to 60 characters). If that name is already taken the bot shows who last changed it and asks before replacing anything.
6. To reuse a template later, pick it from the **📂 Load a saved template** dropdown. It drops straight into the draft, ready to edit or publish. With more than 25 templates the dropdown pages with **◀️ / ▶️**.
7. While a template is loaded the studio tracks whether the draft still matches it:
   - **✅ saved** — the draft and the template are identical.
   - **⚠️ unsaved changes** — click **🔄 Update "name"** to store your edits back into that template.
8. **🗂️ Manage templates** lists everything saved with how often each one was used, when it changed and who changed it. From there you can **📂 Load**, **✏️ Rename** or **🗑️ Delete** (deleting always asks first, and never touches your draft).
9. **👁️ Preview & publish** shows the finished message with every placeholder filled in, then publishes it to the channel you pick. The studio stays open behind the preview.
10. **🧹 New draft** starts a blank message (saved templates are kept), and **✖️ Close** puts the studio away.

Reliability notes:
- **Your draft is auto-saved after every change.** Close the window, let the panel time out or restart the bot — reopening **📝 Embed Message** brings the same draft back, still linked to its template.
- **Templates are per server and shared with the team.** Anyone with **Manage Server** can load, update or delete them, and the library survives restarts because it lives in `data/community.sqlite3`.
- **Names are unique per server, ignoring case.** `Restock` and `restock` are the same template, and extra spaces are tidied away, so the list never fills up with near-duplicates.
- **Every server keeps up to 100 templates.** Delete one you no longer use to make room.
- **The banner is a picture, never a download card.** Whatever you upload or link is saved with the bot and the embed is pointed at that exact file, so it shows inside the card instead of arriving as an attachment underneath it.
- **Links are copied, not trusted.** A pasted link is downloaded once and kept in `data/banners/`, which is why a banner keeps working after the Discord link it came from expires. If the link cannot be fetched the banner is left alone and the reason is shown.
- **Only PNG, JPG, GIF and WebP are accepted**, up to 8 MB. Anything else — SVG, HEIC from an iPhone, AVIF, a PDF, a web page instead of the picture on it — is refused by name, because Discord would show it as a download rather than a picture.
- Bad data is repaired rather than crashing the composer: an image link Discord would reject is dropped with a warning, an over-long body is trimmed, an invalid colour falls back to Beckham navy, and a template whose stored data cannot be read is flagged with ⚠️ in the list so you can re-save over it.

---

#### Step 16b: Post a Plain Message (Normal Message)

Use this for anything that should read like a normal message instead of a branded card — a quick notice, a photo drop, a short reminder.

1. On the Mod Panel click **💬 Normal Message** and type the message. Placeholders such as `{server_name}` and `{member_count}` work here too, and the box can be left empty if you only want to post pictures.
2. The private composer opens. **The text at the top of that screen is the message** — exactly what the channel will see, with the placeholders already filled in.
3. **✏️ Edit message** reopens the box with your current text still in it. Rewrite it as many times as you like; the preview updates every time.
4. **🖼️ Add images** takes up to **4** pictures. **Upload them straight from your computer** — you can pick several at once — or paste links, one per line, if you prefer.
   - Each picture is fetched and checked as soon as you add it, so a bad one is caught here rather than at publish time.
   - Every picture appears below the composer, showing the exact file the channel will get.
   - **Remove a picture...** appears once you have staged one, and takes several at a time.
5. Pick a channel from **Choose where to publish this message...** and the message goes out.

Reliability notes:
- **Pictures post as pictures, not as downloads.** Each file is re-uploaded under a name built from its actual contents. That matters: Discord decides how to display a file from its extension, so a WebP named `banner.png` — exactly what a `media.discordapp.net` link hands you — used to arrive as a grey download card. Now it does not.
- **Only PNG, JPG, GIF and WebP are accepted**, up to 8 MB each. Anything else is refused by name when you add it.
- **A broken link is caught while you can still fix it.** Nothing is staged that could not be fetched, and the notice names the picture and the reason.
- **A refused publish keeps your work.** Missing permissions or a channel the bot cannot see leaves the draft on screen so you can pick a different channel.
- **`@everyone` and `@here` do not ping from here** — they post as plain text, and the composer says so. Role and member mentions do ping. Use **📣 Beckham Hotel Announcement** for a post that needs to ping the server.
- The composer is private to you and closes itself after 15 minutes of inactivity.

---

#### Step 17: Persistent Controls
- You do **not** need to run `/summon` again when the bot restarts. Every button carries a fixed ID and is re-registered on startup.
- The same is true for the standalone `/onboarding` and `/community-report` panels.
- Clicking **🔄 Refresh Dashboard** on any existing panel refreshes its data and its button set.

---

## Project Structure

```
beckham-hotel/
├── .env                  # Private configuration containing bot token (git ignored)
├── .env.example          # Safe template for configuration
├── .gitignore            # Keeps private files out of Git
├── requirements.txt      # Python dependencies
├── start_bot.command     # 1-Click launcher for macOS
├── start_bot.cmd         # 1-Click launcher for Windows
├── config.py             # Global constants, brand theme and palette
├── main.py               # Launcher, persistent view registration, intent fallback
├── core/
│   ├── __init__.py
│   ├── database.py       # Async SQLite store (onboarding, snapshots, reports, settings, templates)
│   ├── embed_script.py   # Placeholder hydration + broadcast message state
│   ├── embed_templates.py # Saved embed template library and auto-saved drafts
│   └── images.py         # Picture checks, real-format filenames, local asset store
├── utils/
│   ├── __init__.py
│   └── embed_builder.py  # Unified embed design system, deltas, ANSI status blocks
├── cogs/
│   ├── __init__.py
│   ├── engagement.py     # Activity tracking, SQLite ledger, ranked reports
│   ├── memberreport.py   # Growth snapshots, join tallies, self-refreshing reports
│   ├── onboarding.py     # Member scanning, welcome posts, warm DMs, onboarding log
│   └── mod_panel.py      # /summon, /onboarding, /community-report
├── views/
│   ├── __init__.py
│   ├── banner.py                 # Shared banner modal: upload, link or remove
│   ├── broadcast_view.py         # Embed composer and publish preview
│   ├── common.py                 # Permission guards shared by every panel
│   ├── embed_studio_view.py      # Embed Studio: draft, template library, publish
│   ├── engagement_report_view.py # Activity period and custom date controls
│   ├── member_report_view.py     # Day picker, deploy, refresh, manage
│   ├── mod_panel_view.py         # Persistent Mod Panel buttons and embed
│   ├── onboarding_view.py        # Scan, join-day multi-select, composer, delivery
│   └── plain_message_view.py     # Normal Message: preview, edit, image attachments
├── data/                 # Runtime databases and uploaded pictures (git ignored)
└── README.md             # Documentation and guide
```

### Database Tables

`data/community.sqlite3`

| Table | Purpose |
| --- | --- |
| `onboarded_members` | Who was welcomed, when, by which moderator. |
| `member_snapshots` | One growth baseline per server per UTC day. |
| `member_joins` | Join counts per day and per week. |
| `member_reports` | Deployed live reports and their refresh state. |
| `guild_settings` | Channel choices made from the Mod Panel. |
| `embed_templates` | Saved embed templates, one unique name per server. |
| `embed_drafts` | Each moderator's auto-saved Embed Studio draft. |

`data/engagement.sqlite3`

| Table | Purpose |
| --- | --- |
| `activity_events` | One row per message, reaction or thread, de-duplicated. |
| `engagement_metadata` | When live tracking began. |
| `contest_events` | Raw, unscored contest activity with a content fingerprint and word count. |
| `contest_sessions` | One row per contest round, with its frozen final standings. |

---

## Credits

Created by **Aljay Leodones** for **Beckham Hotel**.

## Member questionnaire and Slack responses

Use `/onboarding` or the mod panel Onboarding button to publish the member form in Introduce Yourself. The five questions collect TikTok handle, email, phone number, last 30 days TikTok GMV, and an optional birthday. The member's Discord account is captured automatically. Responses are saved locally and sent to the brand's private Slack channel.

See [SLACK_ONBOARDING_SETUP.md](SLACK_ONBOARDING_SETUP.md) for admin installation steps, private webhook configuration, connection testing, and delivery troubleshooting.


## Role Giver

Open **Role Giver** from `/summon` or `/role-giver`. Choose the target role, optionally exclude other roles, and review the bot/admin filters. The member list refreshes when you select a role or change a filter. **Give Role** shows a confirmation before assigning anything. Progress reports successes and failures, and **Cancel Assignment** stops the remaining work.

When **Give Role** is disabled, the reason appears at the top of the panel. The bot needs Manage Roles or Administrator permission, and its highest role must be above the chosen role. Administrator does not override Discord's role order. If Member or Verified is blocked, move **Beckham Hotel Bot** above the target role to allow assignment. This also applies when onboarding grants Member. Managed integration roles and @everyone cannot be assigned. If no members are eligible, review the exclusions and members who already have the role. An incomplete member scan blocks assignment until it can be retried.

Restart the Beckham bot after updating these files. Open a fresh Role Giver panel after the restart. Run the regression suite with `venv\Scripts\python.exe -m unittest discover -s tests`.


### Onboarding selection recovery

The Open onboarding button now saves the selected member IDs in SQLite and restores them after a panel timeout or bot restart. Each selection can be used once and is restricted to the moderator who created it. Select a member again in a fresh panel after installing this update; panels created by older versions use the old button IDs. Reused onboarding channels move to the configured onboarding category when it changes. Completion is recorded only after the Member role is present or successfully granted. Errors are written to `logs/beckham.log`.
