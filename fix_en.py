import os
import re

site_dir = r'C:\Users\opc\source\repos\recyclebin-website'

# Direct Chinese -> English replacements for body text not covered by i18n keys
# These are the most common ones that appear as static text (not in i18n blocks)
direct_replacements = [
    # index.html
    ('廢棄物是設計缺陷。我們相信每一種材料都有第二次生命，讓回收成為日常生活的一部分。',
     'Waste is a design flaw. We believe every material deserves a second life, making recycling part of daily life.'),
    ('什麼該回收、怎麼分類', 'What to recycle, and how'),
    ('查找附近的回收站', 'Find drop-off locations near you'),
    ('社區回收活動', 'Community recycling activities'),
    ('一步步跟著做', 'Step-by-step tutorials'),
    ('了解材料的生命週期，是邁向循環經濟的第一步。', 'Understanding the lifecycle of materials is the first step toward a circular economy.'),
    ('可 infinitely 回收', 'Infinitely recyclable'),
    ('玻璃可以無窮次回收而不影響品質。', 'Glass can be recycled endlessly without losing purity or quality.'),
    ('約 75% 的廢棄物其實是可以回收的。', 'About 75% of waste is actually recyclable.'),
    ('全球每年可回收電子垃圾價值超過 620 億美元。', 'Over $62B in recoverable e-waste value per year worldwide.'),
    ('回收鋁比生產新鋁節省 94% 能源。', 'Recycling aluminum uses 94% less energy than producing new aluminum.'),
    ('每一個回收行動，都能為地球帶來實際改變。', 'Every recycling action creates measurable change for the planet.'),
    ('精選影片帶你深入了解回收、永續發展與循環經濟。', 'Curated videos explaining recycling, sustainability, and circular economy concepts.'),
    ('深入解析回收系統的運作方式。', 'A deep dive into how recycling really works and what happens to your waste.'),
    ('正確分類與準備可回收物的步驟。', 'Step-by-step guide to sorting and preparing your recyclables correctly.'),
    ('認識電子垃圾危機與正確回收方式。', 'Understanding the electronic waste crisis and how to responsibly recycle devices.'),
    ('一起加入循環經濟，讓廢棄物不再是問題。', 'Join the circular economy movement and make waste part of the solution.'),
    ('重新定義廢棄物為潛在資源。你通往物質無限循環的完整指南。', 'Redefining waste as latent resource. Your complete guide to the infinite return of matter.'),
    # events
    ('參與社區淨灘、回收挑戰與環境教育活動。', 'Join clean-ups, challenges, and sustainability workshops.'),
    ('與我們一起清理海岸線垃圾，恢復沙灘與海洋的美麗。', 'Join us to remove coastal litter and restore the shoreline and ocean.'),
    ('二十八天回收挑戰，累積積分換取獎品與公益徽章。', '28-day recycling challenge with points, prizes, and impact badges.'),
    ('學習如何在家堆肥，減少廚餘並肥沃你的花園。', 'Learn to compost at home, reduce food scraps, and enrich your garden.'),
    ('免費回收舊手機、筆電、電池，並提供資料抹除教學。', 'Free drop-off for devices and batteries, plus secure data wipe guidance.'),
    ('邀請環境教育講者分享循環經濟在學校的實踐案例。', 'Environmental educators share real circular economy projects in schools.'),
    ('利用回收布料製作專屬購物袋，減少一次性塑膠袋。', 'Upcycle fabric into a custom tote bag to cut single-use plastic.'),
    # centers
    ('根據你的位置，顯示最近的回收站與據點。', 'Find the nearest recycling drop-off locations.'),
    ('尋找回收據點', 'Find a Recycling Center'),
    ('無法取得位置，顯示所有據點。', 'Unable to detect location. Showing all centers.'),
    ('此瀏覽器不支援定位，顯示所有據點。', 'This browser does not support geolocation. Showing all centers.'),
    ('顯示全部', 'Show All'),
    ('正在偵測位置...', 'Detecting location...'),
    ('位置偵測失敗', 'Location detection failed'),
    ('位置未知', 'Location unknown'),
    ('台中回收中心', 'Taichung Recycling Center'),
    ('台中市西屯區文心路三段 100 號', 'No. 100, Wenxin Rd. Sec. 3, Xitun, Taichung'),
    ('台北資源回收站', 'Taipei Resource Station'),
    ('台北市中山區南京東路二段 88 號', 'No. 88, Nanjing E. Rd. Sec. 2, Zhongshan, Taipei'),
    ('高雄環保園區', 'Kaohsiung Eco Park'),
    ('高雄市苓雅區三多一路 150 號', 'No. 150, Sanduo 1st Rd., Lingya, Kaohsiung'),
    ('台南資源分類站', 'Tainan Sort Center'),
    ('台南市東區中華路二段 75 號', 'No. 75, Zhonghua Rd. Sec. 2, East, Tainan'),
    ('新北回收廣場', 'New Taipei Recycle Plaza'),
    ('新北市板橋區文化路一段 200 號', 'No. 200, Wenhua Rd. Sec. 1, Banqiao, New Taipei'),
    ('桃園循環中心', 'Taoyuan Loop Center'),
    ('桃園市中壢區環北路 50 號', 'No. 50, Huanbei Rd., Zhongli, Taoyuan'),
    ('營業時間', 'Hours'),
    # howto
    ('一步一步學回收', 'Step-by-Step Recycling'),
    ('實用圖文教學，讓回收變得簡單又正確。', 'Practical tutorials to make recycling simple and correct.'),
    ('準備回收物', 'Prep Your Materials'),
    ('清潔容器、去除食物殘渣、分門別類。這是提高回收率的第一步。', 'Clean containers, remove food residue, and sort. The first step to higher recycling rates.'),
    ('了解本地規則', 'Know Your Local Rules'),
    ('每個地區回收規範不同，查看當地可回收清單與時間。', 'Recycling rules vary by area. Check your curbside guide and schedule.'),
    ('正確分類', 'Sort Correctly'),
    ('紙、塑膠、玻璃、金屬——學會快速辨識並分裝。', 'Paper, plastic, glass, and metal — learn to identify and separate quickly.'),
    ('安全處理有害物品', 'Handle Hazardous Items Safely'),
    ('電池、燈管、清潔劑——正確收納並送至指定地點。', 'Batteries, bulbs, and chemicals — store and deliver to collection sites.'),
    ('在家開始堆肥', 'Start Composting at Home'),
    ('用廚房廢料製成有機肥料，減少垃圾量並肥沃土壤。', 'Turn kitchen scraps into soil food and cut your trash footprint.'),
    ('追蹤你的影響', 'Track Your Impact'),
    ('記錄回收數量、計算碳減排，讓成果看得見。', 'Record collections, estimate carbon savings, and celebrate progress.'),
    # guides detail pages
    ('塑膠分類入門', 'Plastic Sorting 101'),
    ('認識 1-7 號塑膠分類標示，了解哪些塑膠可回收、如何清潔準備。', 'Learn resin codes 1-7, what\'s recyclable, and how to prepare plastics for collection.'),
    ('PET（1號）常用於飲料瓶；HDPE（2號）常见於洗髮乳瓶；PVC（3號）通常不建議回收；LDPE（4號）常见於塑膠袋；PP（5號）常見於優格杯；PS（6號）保麗龍難回收；Other（7號）多為複合材料。建議先查詢當地回收規範。',
     'PET (1) is used for drink bottles. HDPE (2) is common in detergent bottles. PVC (3) is usually not accepted. LDPE (4) is used in plastic bags. PP (5) is common in yogurt cups. PS (6) is hard to recycle. Other (7) is mixed-material. Check your local rules first.'),
    ('紙類回收完整指南', 'Paper Recycling Guide'),
    ('報紙、紙箱、雜誌、衛生紙——哪些能回收？油漬紙張怎麼辦？', 'Newspaper, cardboard, magazines, tissue — what can be recycled and how to handle soiled paper.'),
    ('報紙與紙箱可回收；但油污紙、衛生紙、烘焙紙通常不適合回收。紙類應保持乾燥，避免混入其他垃圾。回收紙可減少 7,000 加侖用水。',
     'Newspaper and cardboard are recyclable. Soiled paper, tissues, and wax paper are usually not. Keep paper dry and separate from other waste.'),
    ('玻璃回收須知', 'Glass Recycling Essentials'),
    ('玻璃可無限回收而不損品質，但顏色要分開。了解完整流程。', 'Glass can be endlessly recycled without quality loss, but colors must be separated. Learn the full process.'),
    ('透明、棕色、綠色玻璃需分開收集。回收前請沖洗乾淨並移除瓶蓋。碎玻璃應以厚紙袋包裝並標示，避免清理人員受傷。',
     'Separate clear, brown, and green glass. Rinse and remove caps before recycling. Wrap broken glass in thick paper and label it.'),
    ('金屬與鋁罐回收', 'Metal & Aluminum Cans'),
    ('回收鋁節省 94% 能源。了解鐵罐、鋁罐、拆解注意事項。', 'Recycling aluminum saves 94% energy. Learn about steel, aluminum, cans, and prep tips.'),
    ('鋁罐與鐵罐可分開回收；壓扁可節省空間。請勿將含有食物殘餘的罐頭直接投入回收箱，應先沖洗乾淨。',
     'Separate aluminum and steel cans when possible. Rinse food residue to avoid odors. Crush cans to save space.'),
    ('電子垃圾正確回收', 'E-Waste Recycling'),
    ('手機、筆電、電池不能丟一般垃圾。認識合格回收通道與資料安全。', 'Phones, laptops, and batteries never go in regular trash. Find certified channels and data safety tips.'),
    ('舊手機與筆電應送至認證回收點，避免有害物質污染環境。丟棄前請備份並刪除個人資料，或使用資料抹除工具。',
     'Take old devices to certified recyclers to avoid toxic pollution. Back up your data and wipe storage before drop-off.'),
    ('有害廢棄物處理', 'Hazardous Waste Handling'),
    ('油漆、清潔劑、燈管、藥品——特殊回收管道與注意事項。', 'Paint, cleaners, bulbs, and medicine — special collection and precautions.'),
    ('油漆、清潔劑、燈管、藥品等有害廢棄物需送至指定收集點。容器應保持原裝並加蓋，避免洩漏。切勿與一般垃圾混放。',
     'Keep hazardous items in original containers with lids sealed. Use designated collection points. Never mix with regular trash.'),
    # events detail bodies
    ('活動詳情', 'Event Details'),
    ('這是一場開放報名的社群活動，所有人皆可報名參加。現場備有清潔工具，並會有專人進行活動說明。請穿著適合戶外活動的衣鞋，並自備飲用水。',
     'This is an open community event. All are welcome. Supplies and a short safety briefing will be provided. Wear outdoor-friendly clothing and bring a water bottle.'),
    ('我們將於上午 8:00 在沙灘主入口集合。現場提供手套、垃圾袋與安全說明，歡迎所有年齡參加。請自備防曬、飲用水與滿滿熱情。',
     'We\'ll meet at the main beach entrance at 8:00 AM. Gloves, bags, and a quick safety briefing will be provided. All ages welcome. Bring sunscreen, water, and your enthusiasm.'),
    ('以个人或家庭为单位報名，每周记录回收投放量、累積积分，並解鎖徽章。最終积分最高者將在園遊會接受表揚。',
     'Sign up as an individual or household. Track weekly recycling drops, earn points, and unlock badges. Top collectors will receive prizes and recognition at the community fair.'),
    ('攜帶舊手機、筆電、平板與電池到場。認證回收商現場收件，並提供備份與資料安全抹除協助。',
     'Bring old laptops, phones, tablets, and batteries. Certified recyclers will collect on-site, and volunteers will help you back up and wipe sensitive data before drop-off.'),
    ('現場將示範堆肥箱設置、綠材與棕材比例、味覺問題排查，以及如何收成果堆。參加者可免費領取入門套件。',
     'A hands-on workshop covering bin setup, greens vs browns, troubleshooting odors, and harvesting finished compost. Take home a starter kit.'),
    ('請攜帶舊襯衫或枕頭套，學習基礎縫紉技巧，將它改造成可重複使用的購物袋。本活動歡迎初學者，現場備完整工具與模板，完成即可帶回家。',
     'Bring an old shirt or pillowcase and learn basic sewing to turn it into a reusable tote. Beginners welcome. All tools and templates provided. Finished bags can be taken home the same day.'),
    ('由環境教育團隊分享中小學與大學的實務案例，主題涵蓋廢棄物稽核、學生主導的再生商店，以及將永續觀念融入課程。',
     'A panel of environmental educators will present case studies from primary, secondary, and university campuses. Topics include waste audits, student-led reuse shops, and curriculum integration.'),
    ('— 點擊按鈕以偵測', '— tap Detect to find nearby centers'),
    ('— 顯示最近的據點', '— showing nearest centers'),
    ('— 約略位置', '— approximate location'),
]

# Pattern replacements (regex based)
pattern_replacements = [
    (r'活動結束後將頒發感謝狀給所有參與者。',
     'Certificates of appreciation will be given to all participants at the end.'),
    (r'這是一場\.open 的[^<]+', 'This is an open community event. All are welcome.'),
    (r'根據你的位置，顯示最近的回收站與據點。', 'Find the nearest recycling drop-off locations.'),
]

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

    # Direct replacements
    for zh, en in direct_replacements:
        content = content.replace(zh, en)

    # Pattern replacements
    for pattern, replacement in pattern_replacements:
        content = re.sub(pattern, replacement, content)

    # Fix i18n references that leaked Chinese defaults
    # Replace any remaining zh-Hant references in JS
    content = re.sub(r"i18n\['zh-Hant'\]", "i18n['en']", content)
    content = re.sub(r"i18n\[\"zh-Hant\"\]", "i18n['en']", content)
    content = re.sub(r"\|\| i18n\['zh-Hant'\]", "|| i18n['en']", content)
    content = re.sub(r"currentLang === 'zh-Hant'", "currentLang === 'en'", content)
    content = re.sub(r"currentLang==='zh-Hant'", "currentLang==='en'", content)
    content = re.sub(r"== 'zh-Hant'", "== 'en'", content)
    content = re.sub(r"=== 'zh-Hant'", "=== 'en'", content)
    content = re.sub(r"s === 'zh-Hant'", "s === 'en'", content)
    content = re.sub(r"s==='zh-Hant'", "s==='en'", content)

    # Remove lang-toggle CSS styles (keep class for backward compat but hide it)
    # Actually just remove the button tag entirely (already done but may have missed)
    content = re.sub(r'\s*<button class="lang-toggle"[^>]*>.*?</button>\s*\n?\s*', '', content, flags=re.DOTALL)

    # Remove localStorage lang persistence, force English
    content = re.sub(
        r"localStorage\.getItem\('recyclebin-lang'\);[^;]+",
        "'en'",
        content
    )
    content = re.sub(
        r"localStorage\.setItem\('recyclebin-lang',[^)]+\)",
        "localStorage.setItem('recyclebin-lang','en')",
        content
    )

    # Fix remaining CSS class .lang-toggle references (keep class but no button to click)
    # No action needed

    if content != original:
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(content)
        changed.append(os.path.relpath(filepath, site_dir))

print(f"Third pass updated {len(changed)} files:")
for f in changed:
    print(' ', f)
