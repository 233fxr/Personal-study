# -*- coding: utf-8 -*-
import json, os, re

ROOT = os.path.dirname(os.path.abspath(__file__))

def strip_md(text):
    text = re.sub(r'\$\$.*?\$\$', ' ', text, flags=re.DOTALL)
    text = re.sub(r'\$.*?\$', ' ', text)
    text = re.sub(r'#{1,6}\s*', '', text)
    text = re.sub(r'\*\*(.+?)\*\*', r'\1', text)
    text = re.sub(r'\*(.+?)\*', r'\1', text)
    text = re.sub(r'`{1,3}[^`]*`{1,3}', '', text)
    text = re.sub(r'[-*]\s+', '', text)
    text = re.sub(r'---.*', '', text)
    text = re.sub(r'\s+', ' ', text)
    return text.strip()

def read_file(path):
    with open(path, 'r', encoding='utf-8-sig') as f:
        return f.read()

def extract_title(path):
    text = read_file(path)
    first = text.split('\n')[0].strip()
    return re.sub(r'^#\s*', '', first)

manifest = {"subjects": []}
search_entries = []
note_id = 0

for subject in sorted(os.listdir(ROOT)):
    spath = os.path.join(ROOT, subject)
    if not os.path.isdir(spath) or subject.startswith('.') or subject.endswith('.py'):
        continue
    subject_entry = {"name": subject, "path": subject, "chapters": []}
    chapters = sorted([d for d in os.listdir(spath) if os.path.isdir(os.path.join(spath, d))])
    for ch in chapters:
        chpath = os.path.join(spath, ch)
        notes = sorted([f for f in os.listdir(chpath) if f.endswith('.md')])
        chap_entry = {"name": ch, "path": subject + '/' + ch, "notes": []}
        for note in notes:
            note_id += 1
            fpath = os.path.join(chpath, note)
            relpath = (subject + '/' + ch + '/' + note).replace('\\', '/')
            title = extract_title(fpath)
            chap_entry["notes"].append({"id": note_id, "title": title, "path": relpath})
            raw = read_file(fpath)
            clean = strip_md(raw)
            search_entries.append({"id": note_id, "title": title, "path": relpath, "content": clean[:2000]})
        if chap_entry["notes"]:
            subject_entry["chapters"].append(chap_entry)
    if subject_entry["chapters"]:
        manifest["subjects"].append(subject_entry)

with open(os.path.join(ROOT, "manifest.json"), 'w', encoding='utf-8') as f:
    json.dump(manifest, f, ensure_ascii=False, indent=2)

with open(os.path.join(ROOT, "search-index.json"), 'w', encoding='utf-8') as f:
    json.dump(search_entries, f, ensure_ascii=False, indent=2)

print("Done. Subjects:", len(manifest["subjects"]), "Entries:", len(search_entries))
