import os, re

site_dir = r"C:\Users\opc\source\repos\recyclebin-website"
replacements = {
    # Remaining Chinese in index.html
    '廢棄物是設計缺陷。我們相信每一種材料都有第二次生命，讓回收成為日常生活的一部分。':
        'Waste is a design flaw. We believe every material deserves a second life, making recycling part of daily life.',
    '什麼該回收、怎麼CATEGORIES': 'What to recycle, and how',
    '尋找回收Centers': 'Find a Recycling Center',
    '社區回收Events': 'Community recycling activities',
    '玻璃': 'Glass',
    '紙類': 'Paper',
    '鋁罐': 'Aluminum Cans',
    '回收鋁節省 94% 能源': 'Recycling aluminum uses 94% less energy',
    '回收一噸紙省 7,000 加侖水': 'Recycling one ton of paper saves 7,000 gallons of water',
    '回收一噸紙挽救 17 棵樹': 'Recycling one ton of paper saves 17 mature trees',
    '每戶每年減少 1.5 噸碳排放': '1.5 tons of CO₂ reduced per household per year',
    'Sort Correctly與準備可回收物的步驟。': 'Step-by-step guide to sorting and preparing your recyclables correctly.',
    '探索Guides': 'Explore Guides', '查看Events': 'View Events',
    '重新定義廢棄物為潛在RESOURCES。你通往物質無限循環的完整Guides。':
        'Redefining waste as latent resource. Your complete guide to the infinite return of matter.',
    '回收Centers': 'Local Centers', '近期Events': 'Upcoming Events',
    '開始學習': 'Start Learning', '尋找回收點': 'Find a Center',
    '可 infinitely 回收': 'Infinitely recyclable',
    '材料智能': 'MATERIAL INTELLIGENCE',
    '了解材料的生命週期，是邁向循環經濟的第一步。':
        'Understanding the lifecycle of materials is the first step toward a circular economy.',
    '高回收率': 'High recovery rate',
    '高價值': 'High value',
    '節能首選': 'Energy saver',
    '全球每年可回收電子垃圾價值超過 620 億美元。': 'Over $62B in recoverable e-waste value per year worldwide.',
    '影響數據': 'IMPACT DATA',
    '每一個回收行動，都能為地球帶來實際改變。': 'Every recycling action creates measurable change for the planet.',
    '影片庫': 'VIDEO LIBRARY',
    '精選影片帶你深入了解回收、永續發展與循環經濟。':
        'Curated videos explaining recycling, sustainability, and circular economy concepts.',
    '認識電子垃圾危機與正確回收方式。': 'Understanding the electronic waste crisis and how to responsibly recycle devices.',
    '資源': 'RESOURCES', '分類': 'CATEGORIES', '社群': 'COMMUNITY',
    '回收指南': 'Recycling Guides', '教學': 'How-To Tutorials',
    '家用廢棄物': 'Household', '電子垃圾': 'E-Waste',
    '有害廢棄物': 'Hazardous Waste', '堆肥': 'Composting',
    '淨灘行動': 'Clean-Up Drives', '回收挑戰': 'Recycling Challenges',
    '影響報告': 'Impact Reports', '觀看影片': 'Watch Video',

    # Remaining Chinese in guides.html
    '全面了解如何Sort Correctly與回收各類材料。': 'Learn how to sort and recycle each material correctly.',
    '塑膠': 'Plastic', '紙類': 'Paper', '玻璃': 'Glass', '金屬': 'Metal',
    '認識 1-7 號塑膠分類標示，了解哪些塑膠可回收、如何清潔準備。':
        'Learn resin codes 1-7, what\'s recyclable, and how to prepare plastics for collection.',
    '塑膠分類入門': 'Plastic Sorting 101', '紙類回收完整指南': 'Paper Recycling Guide',
    '報紙、紙箱、雜誌、衛生紙——哪些能回收？油漬紙張怎麼辦？':
        'Newspaper, cardboard, magazines, tissue — what can be recycled and how to handle soiled paper.',
    '玻璃回收須知': 'Glass Recycling Essentials',
    '玻璃可無限回收而不損品質，但顏色要分開。了解完整流程。':
        'Glass can be endlessly recycled without quality loss, but colors must be separated. Learn the full process.',
    '金屬與鋁罐回收': 'Metal & Aluminum Cans',
    '回收鋁節省 94% 能源。了解鐵罐、鋁罐、拆解注意事項。':
        'Recycling aluminum saves 94% energy. Learn about steel, aluminum, cans, and prep tips.',
    '電子垃圾正確回收': 'E-Waste Recycling',
    '手機、筆電、電池不能丟一般垃圾。認識合格回收通道與資料安全。':
        'Phones, laptops, and batteries never go in regular trash. Find certified channels and data safety tips.',
    '有害廢棄物處理': 'Hazardous Waste Handling',
    '油漆、清潔劑、燈管、藥品——特殊回收管道與注意事項。':
        'Paint, cleaners, bulbs, and medicine — special collection and precautions.',

    # Remaining Chinese in centers.html
    '根據你的位置，顯示最近的回收站與Centers。': 'Find the nearest recycling drop-off locations.',
    '無法取得位置，顯示所有Centers。': 'Unable to detect location. Showing all centers.',
    '尋找回收Centers': 'Find a Recycling Center',
    '此瀏覽器不支援定位，顯示所有Centers。': 'This browser does not support geolocation. Showing all centers.',
    '約略位置': 'approximate location',

    # Remaining Chinese in events.html
    '近期Events': 'Upcoming Events',
    '參與社區淨灘、Recycling Challenges與環境教育Events。':
        'Join clean-ups, challenges, and sustainability workshops.',
    '免費回收舊手機、筆電、電池，並提供資料抹除How-To Tutorials。':
        'Free drop-off for devices and batteries, plus secure data wipe guidance.',

    # Remaining Chinese in events-detail.html
    'Events詳情': 'Event Details',

    # Remaining Chinese in plastic.html
    '認識塑膠 1-7 號CATEGORIES標示，了解哪些可回收、如何清潔準備。':
        'Learn resin codes 1-7, what\'s recyclable, and how to prepare plastics for collection.',
    '塑膠CATEGORIES重點': 'Plastic Sorting 101',
    'PET（1號）常用於飲料瓶；HDPE（2號）常见於洗髮乳瓶；PVC（3號）通常不建議回收；LDPE（4號）常见於塑膠袋；PP（5號）常見於優格杯；PS（6號）保麗龍難回收；Other（7號）多為複合材料。建議先查詢當地回收規範。':
        'PET (1) is used for drink bottles. HDPE (2) is common in detergent bottles. PVC (3) is not accepted. LDPE (4) is for plastic bags. PP (5) is for yogurt cups. PS (6) is hard to recycle. Other (7) is mixed. Check your local rules.',

    # Remaining Chinese in paper.html
    '紙類回收完整Guides': 'Paper Recycling Guide',
    '紙類回收重點': 'Paper Recycling 101',
    '報紙與紙箱可回收；但油汙紙、衛生紙、烘焙紙通常不適合回收。紙類應保持乾燥，避免混入其他垃圾。回收紙可減少 7,000 加侖用水。':
        'Newspaper and cardboard are recyclable. Soiled paper, tissues, and wax paper are usually not. Keep paper dry. Recycling paper saves 7,000 gallons of water per ton.',

    # Remaining Chinese in metal.html
    '金屬回收重點': 'Metal & Aluminum Cans',
    '鋁罐與鐵罐可分開回收；壓扁可節省空間。請勿將含有食物殘餘的罐頭直接投入回收箱，應先沖洗乾淨。':
        'Separate aluminum and steel cans. Rinse food residue. Crush cans to save space.',

    # Remaining Chinese in glass.html
    '玻璃回收重點': 'Glass Recycling Essentials',
    '透明、棕色、綠色玻璃需分開收集。回收前請沖洗乾淨並移除瓶蓋。碎璃應以厚紙袋包裝並標示，避免清理人員受傷。':
        'Separate clear, brown, and green glass. Rinse and remove caps. Wrap broken glass in thick paper and label it.',

    # Remaining Chinese in ewaste.html
    'E-Waste回收重點': 'E-Waste Recycling',
    '舊手機與筆電應送至認證回收點，避免有害物質污染環境。丟棄前請備份並刪除個人資料，或使用資料抹除工具。':
        'Take old devices to certified recyclers to avoid toxic pollution. Back up your data and wipe storage before drop-off.',

    # Remaining Chinese in hazardous.html
    'Hazardous Waste Handling重點': 'Hazardous Waste 101',
    '油漆、清潔劑、燈管、藥品等Hazardous Waste需送至指定收集點。容器應保持原裝並加蓋，避免洩漏。切勿與一般垃圾混放。':
        'Keep hazardous items in original containers with lids sealed. Use designated collection points. Never mix with regular trash.',

    # Remaining Chinese in howto.html
    '實用圖文How-To Tutorials，讓回收變得簡單又正確。': 'Practical tutorials to make recycling simple and correct.',
    '開始學習': 'Start Learning',
}

for root, dirs, files in os.walk(site_dir):
    if '_backup_before_en' in root:
        continue
    for f in files:
        if not f.endswith('.html'):
            continue
        p = os.path.join(root, f)
        txt = open(p, 'r', encoding='utf-8').read()
        orig = txt
        for zh, en in replacements.items():
            if zh in txt:
                txt = txt.replace(zh, en)
        if txt != orig:
            open(p, 'w', encoding='utf-8').write(txt)

print('Final Chinese cleanup done.')
