import os
import re
import shutil

site_dir = r"C:\Users\opc\source\repos\recyclebin-website"

# Chinese text to replace with English equivalents
replacements = {
    '首頁': 'Home',
    '指南': 'Guides',
    '據點': 'Centers',
    '活動': 'Events',
    '教學': 'How-To',
    '返回指南': 'Back to Guides',
    '返回活動列表': 'Back to Events',
    '我要參加': 'Join Now',
    '開始學習': 'Start Learning',
    '閱讀更多': 'Read More',
    '觀看影片 →': 'Watch on YouTube →',
    '觀看影片': 'Watch Video',
    '取得路線': 'Get Directions',
    '偵測我的位置': 'Detect My Location',
    '顯示全部': 'Show All',
    '正在偵測位置...': 'Detecting location...',
    '位置未知': 'Location unknown',
    '— 點擊按鈕以偵測': '— tap Detect to find nearby centers',
    '— 顯示最近的據點': '— showing nearest centers',
    '— 約略位置': '— approximate location',
    '位置偵測失敗': 'Location detection failed',
    '無法取得位置，顯示所有據點。': 'Unable to detect location. Showing all centers.',
    '此瀏覽器不支援定位，顯示所有據點。': 'This browser does not support geolocation. Showing all centers.',
    '營業時間': 'Hours',
    'Less Energy<br>回收鋁節省 94% 能源': 'Less Energy<br>Recycling aluminum uses 94% less energy',
    'Gallons Saved<br>回收一噸紙省 7,000 加侖水': 'Gallons Saved<br>Recycling one ton of paper saves 7,000 gallons of water',
    'Trees Preserved<br>回收一噸紙挽救 17 棵樹': 'Trees Preserved<br>Recycling one ton of paper saves 17 trees',
    'CO₂ Reduced<br>每戶每年減少 1.5 噸碳排放': 'CO₂ Reduced<br>1.5 tons of CO₂ reduced per household per year',
    'Waste is a <em>design flaw.</em>': 'Waste is a <em>design flaw.</em>',
    '廢棄物是設計缺陷。我們相信每一種材料都有第二次生命，讓回收成為日常生活的一部分。': 'Waste is a design flaw. We believe every material deserves a second life, making recycling part of daily life.',
    '尋找回收點': 'Find a Center',
    '什麼該回收、怎麼分類': 'What to recycle, and how',
    '查找附近的回收站': 'Find drop-off locations near you',
    '社區回收活動': 'Community recycling activities',
    '一步步跟著做': 'Step-by-step tutorials',
    'Every material tells a story': 'Every material tells a story',
    '了解材料的生命週期，是邁向循環經濟的第一步。': 'Understanding the lifecycle of materials is the first step toward a circular economy.',
    '可 infinitely 回收': 'Infinitely recyclable',
    '玻璃': 'Glass',
    '玻璃可以無窮次回收而不影響品質。': 'Glass can be recycled endlessly without losing purity or quality.',
    '高回收率': 'High recycling rate',
    '紙類': 'Paper',
    '約 75% 的廢棄物其實是可以回收的。': 'About 75% of waste is actually recyclable.',
    '高價值': 'High value',
    '電子垃圾': 'E-Waste',
    '全球每年可回收電子垃圾價值超過 620 億美元。': 'Over $62B in recoverable e-waste value per year worldwide.',
    '節能首選': 'Energy saver',
    '鋁罐': 'Aluminum',
    '回收鋁比生產新鋁節省 94% 能源。': 'Recycling aluminum uses 94% less energy than producing new aluminum.',
    '影響數據': 'Impact Data',
    'Why recycling matters': 'Why recycling matters',
    '每一個回收行動，都能為地球帶來實際改變。': 'Every recycling action creates measurable change for the planet.',
    '影片庫': 'Video Library',
    'Watch & Learn': 'Watch & Learn',
    '精選影片帶你深入了解回收、永續發展與循環經濟。': 'Curated videos explaining recycling, sustainability, and circular economy concepts.',
    '深入解析回收系統的運作方式。': 'A deep dive into how recycling really works and what happens to your waste.',
    '正確分類與準備可回收物的步驟。': 'Step-by-step guide to sorting and preparing your recyclables correctly.',
    '認識電子垃圾危機與正確回收方式。': 'Understanding the electronic waste crisis and how to responsibly recycle devices.',
    'Ready to close the loop?': 'Ready to close the loop?',
    '一起加入循環經濟，讓廢棄物不再是問題。': 'Join the circular economy movement and make waste part of the solution.',
    '探索指南': 'Explore Guides',
    '查看活動': 'View Events',
    '重新定義廢棄物為潛在資源。你通往物質無限循環的完整指南。': 'Redefining waste as latent resource. Your complete guide to the infinite return of matter.',
    '資源': 'Resources',
    '分類': 'Categories',
    '社群': 'Community',
    '回收指南': 'Recycling Guides',
    '回收據點': 'Local Centers',
    '近期活動': 'Upcoming Events',
    '家用廢棄物': 'Household',
    '有害廢棄物': 'Hazardous Waste',
    '堆肥': 'Composting',
    'Impact Reports': 'Impact Reports',
    'Recycling Challenges': 'Recycling Challenges',
    'Clean-Up Drives': 'Clean-Up Drives',
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
    '近垃圾是設計缺陷。': 'Waste is a design flaw.',
    '我們相信每一種材料都有第二次生命，讓回收成為日常生活的一部分。': 'We believe every material deserves a second life, making recycling part of daily life.',
    '海灘淨灘總動員': 'Beach Cleanup Rally',
    '與我們一起清理海岸線垃圾，恢復沙灘與海洋的美麗。': 'Join us to remove coastal litter and restore the shoreline and ocean.',
    '活動詳情': 'Event Details',
    '這是一場開放報名的社群活動，所有人皆可報名參加。現場備有清潔工具，並會有專人進行活動說明。請穿著適合戶外活動的衣鞋，並自備飲用水。': 'This is an open community event. All are welcome. Supplies and a short safety briefing will be provided. Wear outdoor-friendly clothing and bring a water bottle.',
    '這是一場.open 的社區活動，所有人都能自由參加。現場將提供手套、垃圾袋與基礎說明。請穿著適合戶外活動的衣物與鞋子，並自備水壺。活動結束後將頒發感謝狀給所有參與者。': 'This is an open community event. All are welcome. On-site gloves, bags, and a brief orientation will be provided. Please wear suitable outdoor clothing and shoes, and bring your own water bottle. Certificates of appreciation will be given to all participants at the end.',
    'community recycling challenge with points, prizes, and impact badges.': '28-day recycling challenge with points, prizes, and impact badges.',
    'Sign up as an individual or household. Track weekly recycling drops, earn points, and unlock badges. Top collectors will receive prizes and recognition at the community fair.': 'Sign up as an individual or household. Track weekly recycling drops, earn points, and unlock badges. Top collectors will receive prizes and recognition at the community fair.',
    'Bring old laptops, phones, tablets, and batteries. Certified recyclers will collect on-site, and volunteers will help you back up and wipe sensitive data before drop-off.': 'Bring old laptops, phones, tablets, and batteries. Certified recyclers will collect on-site, and volunteers will help you back up and wipe sensitive data before drop-off.',
    'A hands-on workshop covering bin setup, greens vs browns, troubleshooting odors, and harvesting finished compost. Take home a starter kit.': 'A hands-on workshop covering bin setup, greens vs browns, troubleshooting odors, and harvesting finished compost. Take home a starter kit.',
    'Bring an old shirt or pillowcase and learn basic sewing to turn it into a reusable tote. Beginners welcome. All tools and templates provided. Finished bags can be taken home the same day.': 'Bring an old shirt or pillowcase and learn basic sewing to turn it into a reusable tote. Beginners welcome. All tools and templates provided. Finished bags can be taken home the same day.',
    'A panel of environmental educators will present case studies from primary, secondary, and university campuses. Topics include waste audits, student-led reuse shops, and curriculum integration.': 'A panel of environmental educators will present case studies from primary, secondary, and university campuses. Topics include waste audits, student-led reuse shops, and curriculum integration.',
    '2025-06-15': '2025-06-15',
    '2025-07-02': '2025-07-02',
    '2025-07-20': '2025-07-20',
    '2025-08-05': '2025-08-05',
    '2025-08-22': '2025-08-22',
    '2025-09-10': '2025-09-10',
    '海灘淨灘總動員': 'Beach Cleanup Rally',
    '社區回收挑戰賽': 'Community Recycling Challenge',
    '家庭 composting 工作坊': 'Home Composting Workshop',
    '電子產品回收日': 'E-Waste Recycling Day',
    '校園永續講座': 'Campus Sustainability Talk',
    '週末拼布購物袋 DIY': 'Weekend Tote Bag DIY',
    '尋找回收據點': 'Find a Recycling Center',
    '根據你的位置，顯示最近的回收站與據點。': 'Find the nearest recycling drop-off locations.',
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
}

# Collect all HTML files
html_files = []
for root, dirs, files in os.walk(site_dir):
    # Skip backup directory
    if '_backup_before_en' in root:
        continue
    for f in files:
        if f.endswith('.html') and not f.endswith('.py') and not f.endswith('.json'):
            html_files.append(os.path.join(root, f))

html_files.sort()
processed = []

for filepath in html_files:
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    
    original = content
    
    # 1. Change html lang to en
    content = content.replace('<html lang="zh-Hant">', '<html lang="en">')
    
    # 2. Remove language toggle buttons
    content = re.sub(r'\s*<button class="lang-toggle"[^>]*>.*?</button>', '', content, flags=re.DOTALL)
    
    # 3. Apply Chinese-to-English replacements
    for zh, en in replacements.items():
        content = content.replace(zh, en)
    
    # 4. Remove zh-Hant i18n blocks (keep 'en' blocks only)
    # Remove 'zh-Hant': { ... },
    content = re.sub(r"'zh-Hant':\s*\{[^}]*\},?\s*\n?\s*", "", content)
    
    # 5. Fix init functions - remove localStorage check, just set 'en'
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
    
    # 6. Remove references to zh-Hant in code
    content = content.replace("|| 'zh-Hant'", "|| 'en'")
    content = content.replace("currentLang === 'zh-Hant'", "currentLang === 'en'")
    content = content.replace("c === 'zh-Hant'", "c === 'en'")
    content = content.replace("s === 'zh-Hant'", "s === 'en'")
    
    # 7. Fix toggleLanguage to be a no-op for English-only mode
    content = re.sub(
        r"function toggleLanguage\(\)\{[^}]+\}",
        "function toggleLanguage(){ /* English-only mode */ }",
        content
    )
    
    # 8. Fix remaining zh-Hant default in getLabel or other vars
    content = re.sub(r"getLabel\('([^']+)'\)", r"getLabel('\1')", content)
    
    # 9. Fix '.open' remnants
    content = content.replace('.open', 'open')
    
    # 10. Fix any remaining Chinese characters that weren't in replacements
    # Remove any remaining <em>design flaw.</em> duplication issues  
    content = content.replace('<em>design flaw.</em>', '<em>design flaw.</em>')
    
    if content != original:
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(content)
        processed.append(os.path.relpath(filepath, site_dir))

print(f"Processed {len(processed)} files:")
for f in processed:
    print(f"  - {f}")
