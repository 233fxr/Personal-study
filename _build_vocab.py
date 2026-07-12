# -*- coding: utf-8 -*-
"""Build vocab website from word bank, supporting Big Day format."""
import sys, os, re, json
sys.stdout.reconfigure(encoding='utf-8')

ROOT = r"C:\Users\方向容\Documents\408"
WORD_BANK = r"C:\Users\方向容\Documents\408学习\408-学习管理\英语\考研词汇_词库.md"
VOCAB_DIR = os.path.join(ROOT, "英语")

with open(WORD_BANK, "r", encoding="utf-8") as f:
    content = f.read()

all_words = []
sections = re.split(r'\n## (?:Big Day|Day) \d+.*?\n', content)
for sec in sections[1:]:
    for line in sec.split('\n'):
        line = line.strip()
        if not line.startswith('|') or line.startswith('|---') or line.startswith('| #'):
            continue
        cols = [c.strip() for c in line.split('|')]
        cols = [c for c in cols if c]
        if len(cols) < 4:
            continue
        n = int(cols[0]) if cols[0].isdigit() else 0
        word = cols[1].replace('**','')
        pos = cols[2]
        if len(cols) >= 6:
            phon = cols[3]; defin = cols[4]; example = cols[5]
        else:
            defin = cols[3]; example = cols[4] if len(cols)>4 else ""; phon = ""
        all_words.append({"num": n, "word": word, "pos": pos, "phon": phon, "definition": defin, "example": example})

all_words.sort(key=lambda w: w["num"])
print(f"Parsed {len(all_words)} words")

if not all_words:
    print("No words found, cannot continue")
    sys.exit(1)

WORDS_PER = 180
big_days = []
for i in range(0, len(all_words), WORDS_PER):
    chunk = all_words[i:i+WORDS_PER]
    big_days.append({"day": len(big_days)+1, "start": chunk[0]["num"], "end": chunk[-1]["num"], "words": chunk})

# Clear old vocab dirs
if os.path.exists(VOCAB_DIR):
    for root_dir, dirs, files in os.walk(VOCAB_DIR, topdown=False):
        for fname in files:
            if fname.endswith('.md'):
                try: os.remove(os.path.join(root_dir, fname))
                except: pass
        for d in dirs:
            try: os.rmdir(os.path.join(root_dir, d))
            except: pass

os.makedirs(VOCAB_DIR, exist_ok=True)

# Load review data
review_path = os.path.join(VOCAB_DIR, "vocab-review.json")
review_data = {"updated": "2026-07-02", "focusWords": {
    "extract":    {"day": 4, "bigDay": None, "reason": "记成额外", "since": "2026-06-08"},
    "exaggerate": {"day": 4, "bigDay": None, "reason": "记成形容词", "since": "2026-06-08"},
    "forge":      {"day": 6, "bigDay": None, "reason": "只答锻造，漏建立", "since": "2026-06-16"},
    "manifest":   {"day": 6, "bigDay": None, "reason": "完全不会", "since": "2026-06-16"},
    "appliance":  {"day": 5, "bigDay": None, "reason": "记错", "since": "2026-06-10"},
    "dispose":    {"day": 3, "bigDay": None, "reason": "不会", "since": "2026-06-07"},
}, "studyLog": []}

# Map focus word day -> bigDay
for bd in big_days:
    for w in bd["words"]:
        if w["word"] in review_data["focusWords"]:
            review_data["focusWords"][w["word"]]["bigDay"] = bd["day"]

with open(review_path, "w", encoding="utf-8") as f:
    json.dump(review_data, f, ensure_ascii=False, indent=2)

# Create chapter structure
chapters_data = []
for i in range(0, len(big_days), 4):
    ch_bds = big_days[i:i+4]
    if not ch_bds: continue
    ch_name = f"{ch_bds[0]['day']:02d}-BD{ch_bds[0]['day']}-{ch_bds[-1]['day']}"
    ch_path = os.path.join(VOCAB_DIR, ch_name)
    os.makedirs(ch_path, exist_ok=True)
    ch_info = {"name": ch_name, "path": f"英语/{ch_name}", "notes": []}

    for bd in ch_bds:
        first = bd["words"][0]["word"]
        last = bd["words"][-1]["word"]
        fname = f"BD{bd['day']}-{first}-{last}.md"
        fpath = os.path.join(ch_path, fname)

        focus = {}
        for wn, info in review_data["focusWords"].items():
            if info.get("bigDay") == bd["day"]:
                focus[wn] = info

        md = []
        md.append(f"# Big Day {bd['day']}（{bd['start']}-{bd['end']}）")
        md.append(f"> {first} ~ {last} · {len(bd['words'])} 词")
        md.append("")
        if focus:
            md.append("## ⚠️ 需重点复习")
            md.append("| 单词 | 原因 |")
            md.append("|------|------|")
            for wn, info in focus.items():
                md.append(f"| **{wn}** | {info['reason']} |")
            md.append("")

        md.append("| # | 单词 | 词性 | 释义 | 例句 |")
        md.append("|---|------|------|------|------|")
        for w in bd["words"]:
            md.append(f"| {w['num']} | **{w['word']}** | {w['pos']} | {w['definition']} | {w['example']} |")
        md.append("")

        with open(fpath, "w", encoding="utf-8") as f:
            f.write("\n".join(md))

        rel = f"英语/{ch_name}/{fname}"
        ch_info["notes"].append({"id": len(ch_info["notes"])+1, "title": f"BD{bd['day']} · {first}~{last}", "path": rel})
    chapters_data.append(ch_info)

# Update manifest
manifest_path = os.path.join(ROOT, "manifest.json")
with open(manifest_path, "r", encoding="utf-8") as f:
    manifest = json.load(f)

eng_chapters = [{"name": c["name"], "path": c["path"], "notes": c["notes"]} for c in chapters_data]
found = False
for s in manifest.get("subjects", []):
    if s["name"] == "英语":
        s["chapters"] = eng_chapters; found = True; break
if not found:
    manifest["subjects"].insert(0, {"name": "英语", "path": "英语", "chapters": eng_chapters})
with open(manifest_path, "w", encoding="utf-8") as f:
    json.dump(manifest, f, ensure_ascii=False, indent=2)

# Update search index
search_path = os.path.join(ROOT, "search-index.json")
with open(search_path, "r", encoding="utf-8") as f:
    s_idx = json.load(f)
s_idx = [e for e in s_idx if not (e.get("path","").startswith("英语/"))]
for c in chapters_data:
    for n in c["notes"]:
        s_idx.append({"title": n["title"], "path": n["path"], "content": f"考研英语词汇 {n['title']}"})
with open(search_path, "w", encoding="utf-8") as f:
    json.dump(s_idx, f, ensure_ascii=False, indent=2)

print(f"Built: {len(big_days)} big days, {len(chapters_data)} chapters, {sum(len(c['notes']) for c in chapters_data)} pages")
