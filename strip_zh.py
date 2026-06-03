import os
import re

site_dir = r"C:\Users\opc\source\repos\recyclebin-website"

html_files = []
for root, dirs, files in os.walk(site_dir):
    if '_backup_before_en' in root:
        continue
    for f in files:
        if f.endswith('.html'):
            html_files.append(os.path.join(root, f))

html_files.sort()
changed = []

for filepath in html_files:
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    original = content

    # 1. Set html lang to en
    content = content.replace('<html lang="zh-Hant">', '<html lang="en">')

    # 2. Remove language toggle buttons (match various forms)
    content = re.sub(r'\s*<button class="lang-toggle"[^>]*>.*?</button>\s*\n?\s*', '', content, flags=re.DOTALL)

    # 3. Remove zh-Hant i18n block entirely
    # Pattern: 'zh-Hant': { ... },  (with possible trailing comma)
    content = re.sub(
        r"'zh-Hant':\s*\{[^}]*\},?\s*\n?\s*",
        "",
        content
    )

    # 4. Fix zh-Hant fallback in JS to en
    content = re.sub(r"i18n\['zh-Hant'\]", "i18n['en']", content)
    content = re.sub(r'i18n\["zh-Hant"\]', "i18n['en']", content)
    content = re.sub(r"\|\| i18n\['zh-Hant'\]", "|| i18n['en']", content)
    content = re.sub(r"currentLang === 'zh-Hant'", "currentLang === 'en'", content)
    content = re.sub(r"currentLang==='zh-Hant'", "currentLang==='en'", content)
    content = re.sub(r"== 'zh-Hant'", "== 'en'", content)
    content = re.sub(r"==='zh-Hant'", "==='en'", content)

    # 5. Fix init functions - remove localStorage check, default to 'en'
    # Variant 1: (function(){ const s=...; if(...) setLanguage(s); })();
    content = re.sub(
        r"\(function\(\)\{\s*const s=localStorage\.getItem\('recyclebin-lang'\);\s*if\s*\(s&&\(s==='en'\|\|s==='zh-Hant'\)\)\s*setLanguage\(s\);\s*\}\)\(\)",
        "(function(){ setLanguage('en'); })()",
        content
    )
    # Variant 2: (function init(){ const saved = ...; if(...) { setLanguage(saved); } })();
    content = re.sub(
        r"\(function init\(\)\{\s*const saved = localStorage\.getItem\('recyclebin-lang'\);\s*if\s*\(saved && \(saved === 'en' \|\| saved === 'zh-Hant'\)\) \{\s*setLanguage\(saved\);\s*\}\s*\}\)\(\)",
        "(function(){ setLanguage('en'); })()",
        content
    )
    # Variant 3: detectLocation ternary with Chinese fallback
    content = re.sub(
        r"showError\(currentLang==='en'\?'[^']+':'[^']+'\)",
        "showError('Location detection failed.')",
        content
    )
    content = re.sub(
        r"showError\(currentLang==='en'\?\"[^\"]+\":\"[^\"]+\"\)",
        'showError("Location detection failed.")',
        content
    )

    # 6. Remove the toggleLanguage function body
    content = re.sub(
        r"function toggleLanguage\(\)\{[^}]+\}",
        "function toggleLanguage(){ /* English-only mode */ }",
        content
    )

    if content != original:
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(content)
        changed.append(os.path.relpath(filepath, site_dir))

print(f"Updated {len(changed)} files:")
for f in changed:
    print(' ', f)
