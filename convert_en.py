import os
import re

site_dir = r"C:\Users\opc\source\repos\recyclebin-website"

# Comprehensive Chinese-to-English replacements for ALL visible text
replacements = {
    # Nav items
    '首頁': 'Home',
    '指南': 'Guides',
    '據點': 'Centers',
    '活動': 'Events',
    '教學': 'How-To',
    # Common UI
    '返回指南': 'Back to Guides',
    '返回活動列表': 'Back to Events',
    '返回列表': 'Back to List',
    '我要參加': 'Join Now',
    '與我們一起清理海岸線垃圾，恢復沙灘與海洋的美麗。': 'Join us to remove coastal litter and restore the shoreline and ocean.',
    '二十八天回收挑戰，累積積分換取獎品與公益徽章。': '28-day recycling challenge with points, prizes, and impact badges.',
    '以個人或家庭為單位報名，每周記錄回收投放量、累積積分，並解鎖徽章。最終積分最高者將在園遊會接受表揚。': 'Sign up as an individual or household. Track weekly recycling drops, earn points, and unlock badges. Top collectors will receive prizes and recognition at the community fair.',
    '攜帶舊手機、筆電、平板與電池到場。認證回收商現場收件，並提供備份與資料安全抹除協助。': 'Bring old laptops, phones, tablets, and batteries. Certified recyclers will collect on-site, and volunteers will help you back up and wipe sensitive data before drop-off.',
    '現場將示範堆肥箱設置、綠材與棕材比例、異味問題排查，以及如何收成果堆。參加者可免費領取入門套件。': 'A hands-on workshop covering bin setup, greens vs browns, troubleshooting odors, and harvesting finished compost. Take home a starter kit.',
    '請攜帶舊襯衫或枕頭套，學習基礎縫紉技巧，將它改造成可重複使用的購物袋。本活動歡迎初學者，現場備完整工具與模板，完成即可帶回家。': 'Bring an old shirt or pillowcase and learn basic sewing to turn it into a reusable tote. Beginners welcome. All tools and templates provided. Finished bags can be taken home the same day.',
    '由環境教育團隊分享中小學與大學的實務案例，主題涵蓋廢棄物稽核、學生主導的再生商店，以及將永續觀念融入課程。': 'A panel of environmental educators will present case studies from primary, secondary, and university campuses. Topics include waste audits, student-led reuse shops, and curriculum integration.',
    '這是一場開放報名的社群活動，所有人皆可報名參加。現場備有清潔工具，並會有專人進行活動說明。請穿著適合戶外活動的衣鞋，並自備飲用水。': 'This is an open community event. All are welcome. Supplies and a short safety briefing will be provided. Wear outdoor-friendly clothing and bring a water bottle.',
    '這是一場.open 的社群活動。所有人都能自由參加。現場將提供手套、垃圾袋與基礎說明。請穿著適合戶外活动的衣物與鞋子，並自備水壺。活動結束後將頒發感謝狀給所有參與者。': 'This is an open community event. All are welcome. On-site gloves, bags, and a brief orientation will be provided. Please wear suitable outdoor clothing and shoes, and bring your own water bottle. Certificates of appreciation will be given to all participants at the end.',
    '這是一場開放報名的社群活動，所有人皆可報名參加。現場將提供手套、垃圾袋與基礎說明。請穿著適合戶外活動的衣物與鞋子，並自備水壺。活動結束後將頒發感謝狀給所有參與者。': 'This is an open community event. All are welcome. On-site gloves, bags, and a brief orientation will be provided. Please wear suitable outdoor clothing and shoes, and bring your own water bottle. Certificates of appreciation will be given to all participants at the end.',
    # Guides list
    '塑膠': 'Plastic',
    '塑膠分類入門': 'Plastic Sorting 101',
    '認識 1-7 號塑膠分類標示，了解哪些塑膠可回收、如何清潔準備。': 'Learn resin codes 1-7, what\'s recyclable, and how to prepare plastics for collection.',
    '紙類': 'Paper',
    '紙類回收完整指南': 'Paper Recycling Guide',
    '報紙、紙箱、雜誌、衛生紙——哪些能回收？油漬紙張怎麼辦？': 'Newspaper, cardboard, magazines, tissue — what can be recycled and how to handle soiled paper.',
    '玻璃': 'Glass',
    '玻璃回收須知': 'Glass Recycling Essentials',
    '玻璃可無限回收而不損品質，但顏色要分開。了解完整流程。': 'Glass can be endlessly recycled without quality loss, but colors must be separated. Learn the full process.',
    '金屬': 'Metal',
    '金屬與鋁罐回收': 'Metal & Aluminum Cans',
    '回收鋁節省 94% 能源。了解鐵罐、鋁罐、拆解注意事項。': 'Recycling aluminum saves 94% energy. Learn about steel, aluminum, cans, and prep tips.',
    '電子垃圾': 'E-Waste',
    '電子垃圾正確回收': 'E-Waste Recycling',
    '手機、筆電、電池不能丟一般垃圾。認識合格回收通道與資料安全。': 'Phones, laptops, and batteries never go in regular trash. Find certified channels and data safety tips.',
    '有害廢棄物': 'Hazardous',
    '有害廢棄物處理': 'Hazardous Waste Handling',
    '油漆、清潔劑、燈管、藥品——特殊回收管道與注意事項。': 'Paint, cleaners, bulbs, and medicine — special collection and precautions.',
    # Guide detail pages
    '紙類回收重點': 'Paper Recycling Guide',
    '報紙與紙箱可回收；但油污紙、衛生紙、烘焙紙通常不適合回收。紙類應保持乾燥，避免混入其他垃圾。回收紙可減少 7,000 加侖用水。': 'Newspaper and cardboard are recyclable. Soiled paper, tissues, and wax paper are usually not. Keep paper dry and separate from other waste.',
    '玻璃回收重點': 'Glass Recycling Essentials',
    '透明、棕色、綠色玻璃需分開收集。回收前請沖洗乾淨並移除瓶蓋。碎玻璃應以厚紙袋包裝並標示，避免清理人員受傷。': 'Separate clear, brown, and green glass. Rinse and remove caps before recycling. Wrap broken glass in thick paper and label it.',
    '金屬回收重點': 'Metal & Aluminum Cans',
    '鋁罐與鐵罐可分開回收；壓扁可節省空間。請勿將含有食物殘餘的罐頭直接投入回收箱，應先沖洗乾淨。': 'Separate aluminum and steel cans when possible. Rinse food residue to avoid odors. Crush cans to save space.',
    '電子垃圾回收重點': 'E-Waste Recycling',
    '舊手機與筆電應送至認證回收點，避免有害物質污染環境。丟棄前請備份並刪除個人資料，或使用資料抹除工具。': 'Take old devices to certified recyclers to avoid toxic pollution. Back up your data and wipe storage before drop-off.',
    '有害廢棄物處理重點': 'Hazardous Waste Handling',
    '油漆、清潔劑、燈管、藥品等有害廢棄物需送至指定收集點。容器應保持原裝並加蓋，避免洩漏。切勿與一般垃圾混放。': 'Keep hazardous items in original containers with lids sealed. Use designated collection points. Never mix with regular trash.',
    # Index / Home
    '廢棄物是設計缺陷。我們相信每一種材料都有第二次生命，讓回收成為日常生活的一部分。': 'Waste is a design flaw. We believe every material deserves a second life, making recycling part of daily life.',
    '什麼該回收、怎麼分類': 'What to recycle, and how',
    '查找附近的回收站': 'Find drop-off locations near you',
    '社區回收活動': 'Community recycling activities',
    '一步步跟著做': 'Step-by-step tutorials',
    '了解材料的生命週期，是邁向循環經濟的第一步。': 'Understanding the lifecycle of materials is the first step toward a circular economy.',
    '可 infinitely 回收': 'Infinitely recyclable',
    '玻璃可以無窮次回收而不影響品質。': 'Glass can be recycled endlessly without losing purity or quality.',
    '約 75% 的廢棄物其實是可以回收的。': 'About 75% of waste is actually recyclable.',
    '全球每年可回收電子垃圾價值超過 620 億美元。': 'Over $62B in recoverable e-waste value per year worldwide.',
    '回收鋁比生產新鋁節省 94% 能源。': 'Recycling aluminum uses 94% less energy than producing new aluminum.',
    '每一個回收行動，都能為地球帶來實際改變。': 'Every recycling action creates measurable change for the planet.',
    '精選影片帶你深入了解回收、永續發展與循環經濟。': 'Curated videos explaining recycling, sustainability, and circular economy concepts.',
    '深入解析回收系統的運作方式。': 'A deep dive into how recycling really works and what happens to your waste.',
    '正確分類與準備可回收物的步驟。': 'Step-by-step guide to sorting and preparing your recyclables correctly.',
    '認識電子垃圾危機與正確回收方式。': 'Understanding the electronic waste crisis and how to responsibly recycle devices.',
    '一起加入循環經濟，讓廢棄物不再是問題。': 'Join the circular economy movement and make waste part of the solution.',
    '重新定義廢棄物為潛在資源。你通往物質無限循環的完整指南。': 'Redefining waste as latent resource. Your complete guide to the infinite return of matter.',
    # Guides page
    '全面了解如何正確分類與回收各類材料。': 'Learn how to sort and recycle each material correctly.',
    '認識 1-7 號塑膠分類標示，了解哪些塑膠可回收、如何清潔準備。': 'Learn resin codes 1-7, what\'s recyclable, and how to prepare plastics for collection.',
    '報紙、紙箱、雜誌、衛生紙——哪些能回收？油漬紙張怎麼辦？': 'Newspaper, cardboard, magazines, tissue — what can be recycled and how to handle soiled paper.',
    '玻璃可無限回收而不損品質，但顏色要分開。了解完整流程。': 'Glass can be endlessly recycled without quality loss, but colors must be separated. Learn the full process.',
    '回收鋁節省 94% 能源。了解鐵罐、鋁罐、拆解注意事項。': 'Recycling aluminum saves 94% energy. Learn about steel, aluminum, cans, and prep tips.',
    '手機、筆電、電池不能丟一般垃圾。認識合格回收通道與資料安全。': 'Phones, laptops, and batteries never go in regular trash. Find certified channels and data safety tips.',
    '油漆、清潔劑、燈管、藥品——特殊回收管道與注意事項。': 'Paint, cleaners, bulbs, and medicine — special collection and precautions.',
    # Events page
    '近期活動': 'Upcoming Events',
    '參與社區淨灘、回收挑戰與環境教育活動。': 'Join clean-ups, challenges, and sustainability workshops.',
    '2025-06-15': '2025-06-15',
    '海灘淨灘總動員': 'Beach Cleanup Rally',
    '2025-07-02': '2025-07-02',
    '社區回收挑戰賽': 'Community Recycling Challenge',
    '2025-07-20': '2025-07-20',
    '家庭 composting 工作坊': 'Home Composting Workshop',
    '學習如何在家堆肥，減少廚餘並肥沃你的花園。': 'Learn to compost at home, reduce food scraps, and enrich your garden.',
    '2025-08-05': '2025-08-05',
    '電子產品回收日': 'E-Waste Recycling Day',
    '免費回收舊手機、筆電、電池，並提供資料抹除教學。': 'Free drop-off for devices and batteries, plus secure data wipe guidance.',
    '2025-08-22': '2025-08-22',
    '校園永續講座': 'Campus Sustainability Talk',
    '邀請環境教育講者分享循環經濟在學校的實踐案例。': 'Environmental educators share real circular economy projects in schools.',
    '2025-09-10': '2025-09-10',
    '週末拼布購物袋 DIY': 'Weekend Tote Bag DIY',
    '利用回收布料製作專屬購物袋，減少一次性塑膠袋。': 'Upcycle fabric into a custom tote bag to cut single-use plastic.',
    '活動詳情': 'Event Details',
    '這是一場開放報名的社群活動，所有人都能自由參加。現場備有清潔工具，並會有專人進行活動說明。請穿著適合戶外活動的衣鞋，並自備飲用水。': 'This is an open community event. All are welcome. Supplies and a short safety briefing will be provided. Wear outdoor-friendly clothing and bring a water bottle.',
    # Centers page
    '尋找回收據點': 'Find a Recycling Center',
    '根據你的位置，顯示最近的回收站與據點。': 'Find the nearest recycling drop-off locations.',
    '無法取得位置，顯示所有據點。': 'Unable to detect location. Showing all centers.',
    '此瀏覽器不支援定位，顯示所有據點。': 'This browser does not support geolocation. Showing all centers.',
    '正在偵測位置...': 'Detecting location...',
    '位置未知': 'Location unknown',
    '— 點擊按鈕以偵測': '— tap Detect to find nearby centers',
    '偵測我的位置': 'Detect My Location',
    '位置偵測失敗': 'Location detection failed',
    '顯示全部': 'Show All',
    '台中回收中心': 'Taichung Recycling Center',
    '台中市西屯區文心路三段 100 號': 'No. 100, Wenxin Rd. Sec. 3, Xitun, Taichung',
    '台北資源回收站': 'Taipei Resource Station',
    '台北市中山區南京東路二段 88 號': 'No. 88, Nanjing E. Rd. Sec. 2, Zhongshan, Taipei',
    '高雄環保園區': 'Kaohsiung Eco Park',
    '高雄市苓雅區三多一路 150 號': 'No. 150, Sanduo 1st Rd., Lingya, Kaohsiung',
    '台南資源分類站': 'Tainan Sort Center',
    '台南市東區中華路二段 75 號': 'No. 75, Zhonghua Rd. Sec. 2, East, Tainan',
    '新北回收廣場': 'New Taipei Recycle Plaza',
    '新北市板橋區文化路一段 200 號': 'No. 200, Wenhua Rd. Sec. 1, Banqiao, New Taipei',
    '桃園循環中心': 'Taoyuan Loop Center',
    '桃園市中壢區環北路 50 號': 'No. 50, Huanbei Rd., Zhongli, Taoyuan',
    '09:00 - 18:00': '09:00 - 18:00',
    '08:30 - 17:30': '08:30 - 17:30',
    '09:00 - 20:00': '09:00 - 20:00',
    '10:00 - 18:00': '10:00 - 18:00',
    '08:00 - 17:00': '08:00 - 17:00',
    '09:30 - 18:30': '09:30 - 18:30',
    '營業時間': 'Hours',
    '— 顯示最近的據點': '— showing nearest centers',
    '— 約略位置': '— approximate location',
    # How-to page
    '一步一步學回收': 'Step-by-Step Recycling',
    '實用圖文教學，讓回收變得簡單又正確。': 'Practical tutorials to make recycling simple and correct.',
    '準備回收物': 'Prep Your Materials',
    '清潔容器、去除食物殘渣、分門別類。這是提高回收率的第一步。': 'Clean containers, remove food residue, and sort. The first step to higher recycling rates.',
    '了解本地規則': 'Know Your Local Rules',
    '每個地區回收規範不同，查看當地可回收清單與時間。': 'Recycling rules vary by area. Check your curbside guide and schedule.',
    '正確分類': 'Sort Correctly',
    '紙、塑膠、玻璃、金屬——學會快速辨識並分裝。': 'Paper, plastic, glass, and metal — learn to identify and separate quickly.',
    '安全處理有害物品': 'Handle Hazardous Items Safely',
    '電池、燈管、清潔劑——正確收納並送至指定地點。': 'Batteries, bulbs, and chemicals — store and deliver to collection sites.',
    '在家開始堆肥': 'Start Composting at Home',
    '用廚房廢料製成有機肥料，減少垃圾量並肥沃土壤。': 'Turn kitchen scraps into soil food and cut your trash footprint.',
    '追蹤你的影響': 'Track Your Impact',
    '記錄回收數量、計算碳減排，讓成果看得見。': 'Record collections, estimate carbon savings, and celebrate progress.',
    # Index specific
    '開始學習': 'Start Learning',
    '尋找回收點': 'Find a Center',
    # Footer
    '資源': 'Resources',
    '分類': 'Categories',
    '社群': 'Community',
    '回收指南': 'Recycling Guides',
    '回收據點': 'Local Centers',
    '近期活動': 'Upcoming Events',
    '家用廢棄物': 'Household',
    '有害廢棄物': 'Hazardous Waste',
    '堆肥': 'Composting',
    '校園永續講座': 'Campus Sustainability Talk',
    # Events event-specific
    '家庭 composting 工作坊': 'Home Composting Workshop',
    'Composting': 'Composting',
    'How-To': 'How-To',
    # Misc
    '2025-06-15': '2025-06-15',
    '2025-07-02': '2025-07-02',
    '2025-07-20': '2025-07-20',
    '2025-08-05': '2025-08-05',
    '2025-08-22': '2025-08-22',
    '2025-09-10': '2025-09-10',
    'Less Energy<br>回收鋁節省 94% 能源': 'Less Energy<br>Recycling aluminum uses 94% less energy',
    'Gallons Saved<br>回收一噸紙省 7,000 加侖水': 'Gallons Saved<br>Recycling one ton of paper saves 7,000 gallons of water',
    'Trees Preserved<br>回收一噸紙挽救 17 棵樹': 'Trees Preserved<br>Recycling one ton of paper saves 17 trees',
    'CO₂ Reduced<br>每戶每年減少 1.5 噸碳排放': 'CO₂ Reduced<br>1.5 tons of CO₂ reduced per household per year',
    'Waste is a <em>design flaw.</em>': 'Waste is a <em>design flaw.</em>',
}

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

    # 1. Change html lang
    content = content.replace('<html lang="zh-Hant">', '<html lang="en">')

    # 2. Remove language toggle buttons
    content = re.sub(r'\s*<button class="lang-toggle"[^>]*>.*?</button>\s*\n?\s*', '', content, flags=re.DOTALL)

    # 3. Remove zh-Hant i18n block
    content = re.sub(r"'zh-Hant':\s*\{[^}]*\},?\s*\n?\s*", "", content)

    # 4. Apply all Chinese-to-English replacements
    for zh, en in replacements.items():
        content = content.replace(zh, en)

    # 5. Fix zh-Hant fallback in JS
    content = re.sub(r"i18n\['zh-Hant'\]", "i18n['en']", content)
    content = re.sub(r'i18n\["zh-Hant"\]', "i18n['en']", content)
    content = re.sub(r"\|\| i18n\['zh-Hant'\]", "|| i18n['en']", content)
    content = re.sub(r"currentLang === 'zh-Hant'", "currentLang === 'en'", content)
    content = re.sub(r"currentLang==='zh-Hant'", "currentLang==='en'", content)
    content = re.sub(r"s === 'zh-Hant'", "s === 'en'", content)
    content = re.sub(r"s==='zh-Hant'", "s==='en'", content)
    content = re.sub(r"== 'zh-Hant'", "== 'en'", content)
    content = re.sub(r"==='zh-Hant'", "==='en'", content)

    # 6. Fix init functions
    content = re.sub(
        r"\(function init\(\)\{\s*const saved = localStorage\.getItem\('recyclebin-lang'\);\s*if\s*\(saved && \(saved === 'en' \|\| saved === 'zh-Hant'\)\) \{\s*setLanguage\(saved\);\s*\}\s*\}\)\(\)",
        "(function(){ setLanguage('en'); })()",
        content
    )
    content = re.sub(
        r"\(function\(\)\{\s*const s=localStorage\.getItem\('recyclebin-lang'\);\s*if\s*\(s&&\(s==='en'\|\|s==='zh-Hant'\)\)\s*setLanguage\(s\);\s*\}\)\(\)",
        "(function(){ setLanguage('en'); })()",
        content
    )

    # 7. Make toggleLanguage a no-op
    content = re.sub(
        r"function toggleLanguage\(\)[^\{]*\{[^}]+\}",
        "function toggleLanguage(){ /* English-only mode */ }",
        content
    )

    # 8. Remove showError Chinese fallback
    content = re.sub(r"showError\(currentLang==='en'\?[^:]+:[^)]+\)", "showError('Location detection failed.')", content)
    content = re.sub(r'showError\(currentLang==="en"\?[^:]+:[^)]+\)', 'showError("Location detection failed.")', content)

    # 9. Remove getLabel zh-Hant fallback
    content = re.sub(r"\(i18n\[currentLang\] \|\| i18n\['en'\]\)", "(i18n[currentLang] || i18n['en'])", content)

    if content != original:
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(content)
        changed.append(os.path.relpath(filepath, site_dir))

print(f"Updated {len(changed)} files:")
for f in changed:
    print(' ', f)
