import os, re

site_dir = r"C:\Users\opc\source\repos\recyclebin-website"
targets = []
for root, dirs, files in os.walk(site_dir):
    if '_backup_before_en' in root:
        continue
    for f in files:
        if f.endswith('.html'):
            targets.append(os.path.join(root, f))

cjk = re.compile(r'[\u4e00-\u9fff\u3000-\u303f\uff00-\uffef]')
changed = []
for path in targets:
    with open(path, 'r', encoding='utf-8') as f:
        txt = f.read()
    original = txt

    txt = cjk.sub('', txt)
    txt = re.sub(r'\s*<button class="lang-toggle"[^>]*>\s*EN\s*/\s*中文\s*</button>\s*\n?\s*', '', txt)
    txt = re.sub(r"'zh-Hant':\s*\{[^}]*\},?\s*\n?\s*", "", txt)
    txt = txt.replace("'zh-Hant'", "'en'")
    txt = txt.replace('"zh-Hant"', '"en"')
    txt = re.sub(r'function\s+toggleLanguage\s*\([^)]*\)\s*\{[^}]*\}', 'function toggleLanguage() {}', txt)

    with open(path, 'w', encoding='utf-8') as f:
        f.write(txt)
    if txt != original:
        changed.append(os.path.relpath(path, site_dir))

print(f'Updated {len(changed)} files')
for c in changed:
    print(' ', c)
