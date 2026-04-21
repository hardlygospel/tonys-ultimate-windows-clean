# 🪟⚡ Tony's Ultimate Windows Clean

[![Stars](https://img.shields.io/github/stars/hardlygospel/tonys-ultimate-windows-clean?style=for-the-badge&color=yellow)](https://github.com/hardlygospel/tonys-ultimate-windows-clean/stargazers) [![Forks](https://img.shields.io/github/forks/hardlygospel/tonys-ultimate-windows-clean?style=for-the-badge&color=blue)](https://github.com/hardlygospel/tonys-ultimate-windows-clean/network/members) [![Last Commit](https://img.shields.io/github/last-commit/hardlygospel/tonys-ultimate-windows-clean?style=for-the-badge&color=green)](https://github.com/hardlygospel/tonys-ultimate-windows-clean/commits) [![License](https://img.shields.io/github/license/hardlygospel/tonys-ultimate-windows-clean?style=for-the-badge)](https://github.com/hardlygospel/tonys-ultimate-windows-clean/blob/main/LICENSE)
### *For Discord Users & Gamers*

> One command. No intervention. Walk away with a faster, cleaner Windows PC.

---

## ⚡ Quick Start

Right-click `windows_clean.py` → **Run as administrator**, or in a terminal:

```cmd
python windows_clean.py
```

```cmd
# Nuclear mode — also cleans Docker
python windows_clean.py --full
```

> Run as Administrator for the full clean. It works without, but some steps will be skipped.

---

## 🧹 What Gets Cleaned

| | What | Result |
|---|---|---|
| 📸 | **Screenshots** | Sorted into `Desktop\Screenshots\YYYY\MM` |
| 🖥️ | **Desktop** | Loose files moved to `Desktop\Misc` (shortcuts kept) |
| 📥 | **Downloads** | Files 30+ days old archived automatically |
| 🗑️ | **Recycle Bin** | Emptied |
| 🧹 | **Temp Files** | `%TEMP%`, `%TMP%` and `C:\Windows\Temp` cleared |
| 🪟 | **Windows Update Cache** | `SoftwareDistribution\Download` cleared |
| ⚡ | **Prefetch** | Prefetch files cleared |
| 🧹 | **App Caches** | IE/Edge WebCache, CrashDumps, Explorer cache |
| 🌍 | **Browsers** | Chrome, Firefox, Edge, Brave, Opera, Vivaldi caches cleared |
| 💬 | **Discord** | Cache, Code Cache, GPU Cache cleared |
| 🎮 | **Games** | Steam shader cache, Epic, GOG, Battle.net, EA App caches cleared |
| 👁️ | **Thumbnails** | `thumbcache_*.db` files cleared |
| 🪵 | **Event Logs** | All Windows Event Logs wiped |
| 📦 | **npm** | Cache purged |
| 🐍 | **pip** | Cache purged |
| 🌐 | **DNS** | `ipconfig /flushdns` |
| 🧽 | **Disk Cleanup** | Windows built-in cleanmgr run on C: |
| 📊 | **HTML Report** | Beautiful report auto-opens on Desktop |

**With `--full` also cleans:**

| | What | Result |
|---|---|---|
| 🐳 | **Docker** | All unused images, containers & volumes |

---

## 📊 Report

After every run a slick dark-mode HTML report pops open on your Desktop showing total space freed, every task result, and how long it took.

---

## 🎮 Why This Exists

Discord and games chew through cache, logs and temp files fast. Windows doesn't clean these up automatically. Screenshots pile up on the Desktop. Downloads folder becomes a graveyard. This script fixes all of that in one go — including Steam shader caches, Epic Games leftovers and Discord's notorious cache bloat.

---

## 🔒 Safe by Default

- Files are **moved**, not deleted (Desktop → Misc, Downloads → Archive)
- Desktop **shortcuts (.lnk) are never touched**
- Browser **passwords and history are never touched** — only cache
- `--full` Docker cleanup is **opt-in only**
- Steps needing Admin are **skipped gracefully** if not available

---

## 💻 Requirements

### Required
| What | Why | Get It |
|---|---|---|
| **Windows 10 or later** | Needed for ANSI colour support in terminal | Already have it |
| **Python 3.8+** | Runs the script | [python.org/downloads](https://www.python.org/downloads/) — tick **"Add Python to PATH"** during install |

### Optional — script skips these gracefully if not installed
| What | Why you'd want it | Get It |
|---|---|---|
| **Git** | Push changes to GitHub | [git-scm.com](https://git-scm.com/download/win) |
| **Node.js / npm** | Cleans npm cache | [nodejs.org](https://nodejs.org/en/download/) |
| **pip** | Cleans Python package cache | Comes with Python 3 |
| **Docker Desktop** | `--full` mode prunes unused images & containers | [docker.com/products/docker-desktop](https://www.docker.com/products/docker-desktop/) |
| **Steam** | Cleans shader cache automatically if installed | [store.steampowered.com](https://store.steampowered.com/about/) |
| **Epic Games Launcher** | Cache cleared automatically if installed | [epicgames.com](https://store.epicgames.com/en-US/download) |

### Running as Administrator
Some steps need Admin rights (Windows Update cache, Prefetch, Event Logs, Disk Cleanup). Three ways:

**Option A — Command Prompt:**
```cmd
# Right-click "Command Prompt" → Run as administrator, then:
python windows_clean.py
```

**Option B — PowerShell:**
```powershell
# Right-click "PowerShell" → Run as administrator, then:
python windows_clean.py
```

**Option C — File Explorer:**
Right-click `windows_clean.py` → **Run as administrator**

---

## 📄 Licence

MIT — do whatever you like with it.

---

*Made with ☕ and too many hours in Discord.*
