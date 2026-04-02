"""
windows_clean.py — Tony's Ultimate Windows Clean
For Discord Users & Gamers
Zero-intervention. Run once. Walk away spotless.
Usage: python windows_clean.py [--full]
Run as Administrator for best results.
"""

import os
import sys
import re
import shutil
import subprocess
import time
import json
import ctypes
from pathlib import Path
from datetime import datetime

# ── Config ────────────────────────────────────────────────────
HOME        = Path.home()
DESKTOP     = HOME / "Desktop"
DOWNLOADS   = HOME / "Downloads"
SCREENSHOTS = DESKTOP / "Screenshots"
MISC        = DESKTOP / "Misc"
ARCHIVE     = DOWNLOADS / "Archive"
DAYS_OLD    = 30
FULL_MODE   = "--full" in sys.argv
IS_ADMIN    = ctypes.windll.shell32.IsUserAnAdmin() != 0

# ── Colours (Windows 10+ supports ANSI) ───────────────────────
os.system("color")  # enable ANSI on Windows terminal
G  = "\033[0;32m"
Y  = "\033[1;33m"
B  = "\033[0;36m"
D  = "\033[2m"
NC = "\033[0m"
BD = "\033[1m"

def header(title): print(f"\n{B}{BD}▸ {title}{NC}\n{D}  {'─'*41}{NC}")
def ok(msg):       print(f"  {G}✔{NC}  {msg}")
def info(msg):     print(f"  {B}→{NC}  {msg}")
def warn(msg):     print(f"  {Y}⚠{NC}  {msg}")
def skip(msg):     print(f"  {D}–  {msg} (skipped){NC}")

def human(b):
    if b >= 1_073_741_824: return f"{b/1_073_741_824:.1f} GB"
    if b >= 1_048_576:     return f"{b/1_048_576:.1f} MB"
    if b >= 1_024:         return f"{b/1_024:.1f} KB"
    return f"{b} B"

def dir_size(p):
    total = 0
    try:
        for f in Path(p).rglob("*"):
            try: total += f.stat().st_size
            except: pass
    except: pass
    return total

def run(cmd, **kw):
    return subprocess.run(cmd, shell=True, capture_output=True, text=True, **kw)

def has(cmd):
    return shutil.which(cmd) is not None

report = []
total_freed = 0

def add(emoji, title, detail, freed=0):
    global total_freed
    total_freed += freed
    report.append({"emoji": emoji, "title": title, "detail": detail,
                   "freed": human(freed) if freed > 0 else ""})

start = time.time()

print(f"\n{BD}{B}")
print("  ╔═══════════════════════════════════════╗")
print("  ║  🪟⚡ TONY'S ULTIMATE WINDOWS CLEAN   ║")
print(f"  ║      {datetime.now():%d %b %Y  %H:%M}                  ║")
print("  ╚═══════════════════════════════════════╝")
print(NC)

if not IS_ADMIN:
    warn("Not running as Administrator — some steps will be skipped.")
    warn("Right-click windows_clean.py → Run as administrator for full clean.")
    print()

# ══════════════════════════════════════════════════════════════
# 1. SCREENSHOTS
# ══════════════════════════════════════════════════════════════
header("📸  Screenshots")

moved = 0
pattern = re.compile(r"(\d{4})-(\d{2})-(\d{2})")

# Windows screenshot locations
sources = [
    DESKTOP,
    DOWNLOADS,
    HOME / "Pictures" / "Screenshots",  # default Windows screenshots folder
    HOME / "OneDrive" / "Pictures" / "Screenshots",
]

for source in sources:
    if not source.exists():
        continue
    for f in list(source.iterdir()):
        if not f.is_file():
            continue
        name = f.name.lower()
        if not (name.startswith("screenshot") or name.startswith("screen shot")
                or name.startswith("capture") or "screenshot" in name):
            continue
        m = pattern.search(f.name)
        dest_dir = SCREENSHOTS / (m.group(1) + "/" + m.group(2)) if m else SCREENSHOTS / "Unsorted"
        dest_dir.mkdir(parents=True, exist_ok=True)
        dest = dest_dir / f.name
        if dest.exists():
            dest = dest_dir / f"{f.stem}_dup{f.suffix}"
        try:
            shutil.move(str(f), str(dest))
            moved += 1
        except Exception as e:
            warn(f"Could not move {f.name}: {e}")

if moved:
    ok(f"{moved} screenshot(s) sorted → {SCREENSHOTS}")
    add("📸", "Screenshots sorted", f"{moved} files → Desktop\\Screenshots\\YYYY\\MM")
else:
    info("No screenshots found.")
    add("📸", "Screenshots", "Nothing to sort")

# ══════════════════════════════════════════════════════════════
# 2. DESKTOP TIDY
# ══════════════════════════════════════════════════════════════
header("🖥️   Desktop")

misc_count = 0
skip_names = {"Misc", "Screenshots", "desktop.ini"}

if DESKTOP.exists():
    for f in list(DESKTOP.iterdir()):
        if f.name in skip_names or f.name.startswith("."):
            continue
        if f.is_file() and f.suffix.lower() not in [".lnk", ".url"]:  # keep shortcuts
            MISC.mkdir(exist_ok=True)
            try:
                shutil.move(str(f), str(MISC / f.name))
                misc_count += 1
            except Exception as e:
                warn(f"Could not move {f.name}: {e}")

if misc_count:
    ok(f"{misc_count} loose file(s) → Desktop\\Misc (shortcuts kept in place)")
    add("🖥️", "Desktop tidied", f"{misc_count} files moved to Desktop\\Misc")
else:
    info("Desktop already clean.")
    add("🖥️", "Desktop", "Already tidy")

# ══════════════════════════════════════════════════════════════
# 3. DOWNLOADS ARCHIVE
# ══════════════════════════════════════════════════════════════
header("📥  Downloads")

cutoff = time.time() - (DAYS_OLD * 86400)
old_count = 0

if DOWNLOADS.exists():
    for f in list(DOWNLOADS.iterdir()):
        if f.is_file() and not f.name.startswith("."):
            try:
                if f.stat().st_mtime < cutoff:
                    ARCHIVE.mkdir(exist_ok=True)
                    shutil.move(str(f), str(ARCHIVE / f.name))
                    old_count += 1
            except Exception as e:
                warn(f"Could not archive {f.name}: {e}")

if old_count:
    ok(f"{old_count} file(s) older than {DAYS_OLD} days → Downloads\\Archive")
    add("📥", "Old downloads archived", f"{old_count} files moved to Downloads\\Archive")
else:
    info("No old downloads to archive.")
    add("📥", "Downloads", f"Nothing older than {DAYS_OLD} days")

# ══════════════════════════════════════════════════════════════
# 4. RECYCLE BIN
# ══════════════════════════════════════════════════════════════
header("🗑️   Recycle Bin")

result = run('powershell -Command "Clear-RecycleBin -Force -ErrorAction SilentlyContinue"')
if result.returncode == 0:
    ok("Recycle Bin emptied")
    add("🗑️", "Recycle Bin emptied", "All drives cleared")
else:
    warn("Could not empty Recycle Bin")
    add("🗑️", "Recycle Bin", "Skipped")

# ══════════════════════════════════════════════════════════════
# 5. WINDOWS TEMP FILES
# ══════════════════════════════════════════════════════════════
header("🧹  Temp Files")

temp_dirs = [
    Path(os.environ.get("TEMP", "")),
    Path(os.environ.get("TMP", "")),
    Path("C:/Windows/Temp") if IS_ADMIN else None,
    HOME / "AppData/Local/Temp",
]

temp_freed = 0
for temp in temp_dirs:
    if temp and temp.exists():
        sz = dir_size(temp)
        for item in list(temp.iterdir()):
            try:
                if item.is_dir():
                    shutil.rmtree(str(item), ignore_errors=True)
                else:
                    item.unlink(missing_ok=True)
                temp_freed += sz
            except: pass

ok(f"Temp files cleared (~{human(temp_freed)} freed)")
add("🧹", "Temp files cleared", f"{human(temp_freed)} freed from TEMP directories", temp_freed)

# ══════════════════════════════════════════════════════════════
# 6. WINDOWS UPDATE CACHE
# ══════════════════════════════════════════════════════════════
header("🪟  Windows Update Cache")

if IS_ADMIN:
    wu_cache = Path("C:/Windows/SoftwareDistribution/Download")
    wu_size = dir_size(wu_cache)
    run("net stop wuauserv")
    shutil.rmtree(str(wu_cache), ignore_errors=True)
    wu_cache.mkdir(exist_ok=True)
    run("net start wuauserv")
    ok(f"Windows Update cache cleared (~{human(wu_size)} freed)")
    add("🪟", "Windows Update cache cleared", f"{human(wu_size)} freed", wu_size)
else:
    info("Windows Update cache skipped (needs Admin)")
    add("🪟", "Windows Update cache", "Skipped (run as Admin)")

# ══════════════════════════════════════════════════════════════
# 7. PREFETCH
# ══════════════════════════════════════════════════════════════
header("⚡  Prefetch")

if IS_ADMIN:
    prefetch = Path("C:/Windows/Prefetch")
    pf_size = dir_size(prefetch)
    for f in prefetch.glob("*.pf"):
        try: f.unlink()
        except: pass
    ok(f"Prefetch cleared (~{human(pf_size)} freed)")
    add("⚡", "Prefetch cleared", f"{human(pf_size)} freed", pf_size)
else:
    info("Prefetch skipped (needs Admin)")
    add("⚡", "Prefetch", "Skipped (run as Admin)")

# ══════════════════════════════════════════════════════════════
# 8. USER APP CACHES
# ══════════════════════════════════════════════════════════════
header("🧹  App Caches")

cache_dirs = [
    HOME / "AppData/Local/Microsoft/Windows/INetCache",
    HOME / "AppData/Local/Microsoft/Windows/WebCache",
    HOME / "AppData/Local/CrashDumps",
    HOME / "AppData/Local/Microsoft/Windows/Explorer",
]

cache_freed = 0
for cache in cache_dirs:
    if cache.exists():
        sz = dir_size(cache)
        shutil.rmtree(str(cache), ignore_errors=True)
        cache_freed += sz

ok(f"App caches cleared (~{human(cache_freed)} freed)")
add("🧹", "App caches cleared", f"{human(cache_freed)} freed", cache_freed)

# ══════════════════════════════════════════════════════════════
# 9. BROWSER CACHES
# ══════════════════════════════════════════════════════════════
header("🌍  Browser Caches")

browsers = {
    "Chrome":  HOME / "AppData/Local/Google/Chrome/User Data/Default/Cache",
    "Edge":    HOME / "AppData/Local/Microsoft/Edge/User Data/Default/Cache",
    "Brave":   HOME / "AppData/Local/BraveSoftware/Brave-Browser/User Data/Default/Cache",
    "Opera":   HOME / "AppData/Local/Programs/Opera/cache",
    "Vivaldi": HOME / "AppData/Local/Vivaldi/User Data/Default/Cache",
}

browser_freed = 0
found = []

for name, path in browsers.items():
    if path.exists():
        sz = dir_size(path)
        shutil.rmtree(str(path), ignore_errors=True)
        browser_freed += sz
        found.append(name)

# Firefox
ff_base = HOME / "AppData/Local/Mozilla/Firefox/Profiles"
if ff_base.exists():
    for profile in ff_base.iterdir():
        cache = profile / "cache2"
        if cache.exists():
            sz = dir_size(cache)
            shutil.rmtree(str(cache), ignore_errors=True)
            browser_freed += sz
    found.append("Firefox")

if found:
    ok(f"Browser caches cleared — {human(browser_freed)} freed ({', '.join(found)})")
    add("🌍", "Browser caches cleared", f"{human(browser_freed)} freed — {', '.join(found)}", browser_freed)
else:
    info("No browser caches found.")
    add("🌍", "Browser caches", "None found")

# ══════════════════════════════════════════════════════════════
# 10. DISCORD CACHE
# ══════════════════════════════════════════════════════════════
header("💬  Discord Cache")

discord_caches = [
    HOME / "AppData/Roaming/discord/Cache",
    HOME / "AppData/Roaming/discord/Code Cache",
    HOME / "AppData/Roaming/discord/GPUCache",
]

discord_freed = 0
for cache in discord_caches:
    if cache.exists():
        sz = dir_size(cache)
        shutil.rmtree(str(cache), ignore_errors=True)
        discord_freed += sz

if discord_freed > 0:
    ok(f"Discord cache cleared (~{human(discord_freed)} freed)")
    add("💬", "Discord cache cleared", f"{human(discord_freed)} freed", discord_freed)
else:
    info("No Discord cache found.")
    add("💬", "Discord cache", "None found")

# ══════════════════════════════════════════════════════════════
# 11. GAME CACHES (Steam, Epic, GOG)
# ══════════════════════════════════════════════════════════════
header("🎮  Game Caches")

game_caches = {
    "Steam shader cache": Path("C:/Program Files (x86)/Steam/steamapps/shadercache"),
    "Steam logs":         Path("C:/Program Files (x86)/Steam/logs"),
    "Epic Games cache":   HOME / "AppData/Local/EpicGamesLauncher/Saved/webcache",
    "GOG cache":          HOME / "AppData/Local/GOG.com/Galaxy/webcache",
    "Battle.net cache":   HOME / "AppData/Local/Battle.net/Cache",
    "EA App cache":       HOME / "AppData/Local/Electronic Arts/EA Desktop/Cache",
}

game_freed = 0
found_games = []
for name, path in game_caches.items():
    if path.exists():
        sz = dir_size(path)
        shutil.rmtree(str(path), ignore_errors=True)
        game_freed += sz
        found_games.append(name.split()[0])

if found_games:
    ok(f"Game caches cleared — {human(game_freed)} freed ({', '.join(found_games)})")
    add("🎮", "Game caches cleared", f"{human(game_freed)} freed — {', '.join(found_games)}", game_freed)
else:
    info("No game caches found.")
    add("🎮", "Game caches", "None found")

# ══════════════════════════════════════════════════════════════
# 12. THUMBNAIL CACHE
# ══════════════════════════════════════════════════════════════
header("👁️   Thumbnail Cache")

thumb_cache = HOME / "AppData/Local/Microsoft/Windows/Explorer"
thumb_size = dir_size(thumb_cache)
for f in thumb_cache.glob("thumbcache_*.db") if thumb_cache.exists() else []:
    try: f.unlink()
    except: pass
ok(f"Thumbnail cache cleared (~{human(thumb_size)} freed)")
add("👁️", "Thumbnail cache cleared", f"{human(thumb_size)} freed", thumb_size)

# ══════════════════════════════════════════════════════════════
# 13. EVENT LOGS
# ══════════════════════════════════════════════════════════════
header("🪵  Event Logs")

if IS_ADMIN:
    result = run('powershell -Command "Get-EventLog -List | ForEach-Object { Clear-EventLog $_.Log }" 2>$null')
    ok("Windows Event Logs cleared")
    add("🪵", "Event logs cleared", "All Windows event logs wiped")
else:
    info("Event logs skipped (needs Admin)")
    add("🪵", "Event logs", "Skipped (run as Admin)")

# ══════════════════════════════════════════════════════════════
# 14. NPM
# ══════════════════════════════════════════════════════════════
header("📦  npm")

if has("npm"):
    npm_cache = run("npm config get cache").stdout.strip()
    npm_size = dir_size(npm_cache)
    run("npm cache clean --force")
    ok(f"npm cache cleared (~{human(npm_size)} freed)")
    add("📦", "npm cache cleared", f"{human(npm_size)} freed", npm_size)
else:
    skip("npm not installed")

# ══════════════════════════════════════════════════════════════
# 15. PIP
# ══════════════════════════════════════════════════════════════
header("🐍  pip")

for pip in ["pip3", "pip"]:
    if has(pip):
        pip_dir = run(f"{pip} cache dir").stdout.strip()
        pip_size = dir_size(pip_dir)
        run(f"{pip} cache purge")
        ok(f"pip cache cleared (~{human(pip_size)} freed)")
        add("🐍", "pip cache cleared", f"{human(pip_size)} freed", pip_size)
        break
else:
    skip("pip not installed")

# ══════════════════════════════════════════════════════════════
# 16. DNS FLUSH
# ══════════════════════════════════════════════════════════════
header("🌐  DNS")

result = run("ipconfig /flushdns")
if result.returncode == 0:
    ok("DNS cache flushed")
    add("🌐", "DNS flushed", "ipconfig /flushdns")
else:
    warn("DNS flush failed")
    add("🌐", "DNS", "Failed")

# ══════════════════════════════════════════════════════════════
# 17. DISK CLEANUP (built-in Windows tool)
# ══════════════════════════════════════════════════════════════
header("🧽  Windows Disk Cleanup")

if IS_ADMIN:
    # Run cleanmgr silently with all options
    run("cleanmgr /sagerun:1 /d C:")
    ok("Windows Disk Cleanup run on C: drive")
    add("🧽", "Disk Cleanup run", "Windows built-in cleanup completed on C:")
else:
    info("Disk Cleanup skipped (needs Admin)")
    add("🧽", "Disk Cleanup", "Skipped (run as Admin)")

# ══════════════════════════════════════════════════════════════
# 18. DOCKER (--full only)
# ══════════════════════════════════════════════════════════════
header("🐳  Docker")

if FULL_MODE and has("docker"):
    if run("docker info").returncode == 0:
        run("docker system prune -af --volumes")
        ok("Docker pruned — unused images, containers, volumes removed")
        add("🐳", "Docker pruned", "All unused resources removed")
    else:
        warn("Docker not running")
        add("🐳", "Docker", "Not running")
elif not FULL_MODE:
    info("Docker skipped — use --full to include")
    add("🐳", "Docker", "Skipped (use --full)")
else:
    skip("Docker not installed")

# ══════════════════════════════════════════════════════════════
# 19. HTML REPORT
# ══════════════════════════════════════════════════════════════
header("📊  Report")

elapsed = int(time.time() - start)
report_path = DESKTOP / f"Windows_Clean_Report_{datetime.now():%Y-%m-%d_%H%M}.html"
items_json = json.dumps(report)

html = f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>Windows Clean Report — {datetime.now():%d %b %Y}</title>
<link href="https://fonts.googleapis.com/css2?family=Syne:wght@400;700;800&family=DM+Mono:wght@400;500&display=swap" rel="stylesheet">
<style>
  :root {{ --bg:#0a0a0f; --surface:#13131a; --surface2:#1c1c28; --border:#2a2a3a; --accent:#00b4ff; --text:#e8e8f0; --muted:#6b6b88; }}
  *,*::before,*::after {{ box-sizing:border-box; margin:0; padding:0; }}
  body {{ background:var(--bg); color:var(--text); font-family:'Syne',sans-serif; min-height:100vh; padding:0 0 80px; }}
  .hero {{ position:relative; padding:80px 40px 60px; text-align:center; overflow:hidden; }}
  .hero::before {{ content:''; position:absolute; inset:0; background:radial-gradient(ellipse 60% 50% at 50% -10%, rgba(0,180,255,.15) 0%, transparent 70%); pointer-events:none; }}
  .eyebrow {{ font-family:'DM Mono',monospace; font-size:.75rem; letter-spacing:.2em; text-transform:uppercase; color:var(--accent); margin-bottom:20px; }}
  h1 {{ font-size:clamp(2.8rem,8vw,6rem); font-weight:800; line-height:1; letter-spacing:-.03em; background:linear-gradient(135deg,#fff 30%,var(--accent) 100%); -webkit-background-clip:text; -webkit-text-fill-color:transparent; margin-bottom:12px; }}
  .sub {{ color:var(--muted); font-size:1rem; font-family:'DM Mono',monospace; }}
  .stats {{ display:flex; max-width:700px; margin:40px auto 0; border:1px solid var(--border); border-radius:16px; overflow:hidden; background:var(--surface); }}
  .stat {{ flex:1; padding:28px 24px; text-align:center; border-right:1px solid var(--border); }}
  .stat:last-child {{ border-right:none; }}
  .stat-val {{ font-size:2rem; font-weight:800; color:var(--accent); }}
  .stat-label {{ font-family:'DM Mono',monospace; font-size:.7rem; letter-spacing:.12em; text-transform:uppercase; color:var(--muted); margin-top:6px; }}
  .wrap {{ max-width:1000px; margin:64px auto 0; padding:0 40px; }}
  .section-label {{ font-family:'DM Mono',monospace; font-size:.7rem; letter-spacing:.18em; text-transform:uppercase; color:var(--muted); margin-bottom:20px; }}
  .grid {{ display:grid; grid-template-columns:repeat(auto-fill,minmax(280px,1fr)); gap:12px; }}
  .card {{ background:var(--surface); border:1px solid var(--border); border-radius:14px; padding:22px 24px; display:flex; align-items:flex-start; gap:16px; animation:fadeUp .4s ease both; }}
  @keyframes fadeUp {{ from {{ opacity:0; transform:translateY(16px) }} to {{ opacity:1; transform:translateY(0) }} }}
  .emoji {{ font-size:1.6rem; flex-shrink:0; width:42px; height:42px; display:flex; align-items:center; justify-content:center; background:var(--surface2); border-radius:10px; border:1px solid var(--border); }}
  .card-body {{ flex:1; min-width:0; }}
  .card-title {{ font-weight:700; font-size:.95rem; margin-bottom:4px; }}
  .card-detail {{ font-family:'DM Mono',monospace; font-size:.72rem; color:var(--muted); line-height:1.4; }}
  .card-freed {{ font-family:'DM Mono',monospace; font-size:.75rem; color:var(--accent); margin-top:8px; }}
  footer {{ text-align:center; margin-top:80px; font-family:'DM Mono',monospace; font-size:.72rem; color:var(--muted); }}
</style>
</head>
<body>
<div class="hero">
  <p class="eyebrow">🪟 Windows Deep Clean — {datetime.now():%A, %d %B %Y at %H:%M}</p>
  <h1>All<br>Clean.</h1>
  <p class="sub">Your Windows machine has been scrubbed, sorted &amp; optimised.</p>
  <div class="stats">
    <div class="stat"><div class="stat-val">{human(total_freed)}</div><div class="stat-label">Freed</div></div>
    <div class="stat"><div class="stat-val">{len(report)}</div><div class="stat-label">Tasks</div></div>
    <div class="stat"><div class="stat-val">{elapsed}s</div><div class="stat-label">Duration</div></div>
  </div>
</div>
<div class="wrap">
  <p class="section-label">Detailed Results</p>
  <div class="grid" id="grid"></div>
</div>
<footer><p>Generated by windows_clean.py · {datetime.now():%Y-%m-%d %H:%M:%S}</p></footer>
<script>
const items = {items_json};
const grid = document.getElementById('grid');
items.forEach((item, i) => {{
  const c = document.createElement('div');
  c.className = 'card';
  c.style.animationDelay = (i * 40) + 'ms';
  c.innerHTML = `<div class="emoji">${{item.emoji}}</div>
    <div class="card-body">
      <div class="card-title">${{item.title}}</div>
      <div class="card-detail">${{item.detail}}</div>
      ${{item.freed ? `<div class="card-freed">↓ ${{item.freed}} freed</div>` : ''}}
    </div>`;
  grid.appendChild(c);
}});
</script>
</body>
</html>"""

report_path.write_text(html)
ok(f"Report saved → {report_path}")
os.startfile(str(report_path))

# ══════════════════════════════════════════════════════════════
# DONE
# ══════════════════════════════════════════════════════════════
print(f"\n{BD}{B}")
print("  ╔═══════════════════════════════════════╗")
print("  ║   ✅  DEEP CLEAN COMPLETE             ║")
print(f"  ║   💾  ~{human(total_freed):<32}║")
print(f"  ║   ⏱   Finished in {elapsed} seconds{' '*(21-len(str(elapsed)))}║")
print("  ║   📊  Report opened on Desktop       ║")
print("  ╚═══════════════════════════════════════╝")
print(NC)
print(f"  {D}Tip: run with --full to also clean Docker{NC}\n")
input("  Press Enter to exit...")
