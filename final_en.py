import os
import re

site_dir = r"C:\Users\opc\source\repos\recyclebin-website"

replacements = [
    # guides.html
    ('回收Guides', 'Recycling Guides'),
    ('PlasticCategories入門', 'Plastic Sorting 101'),
    ('認識 1-7 號PlasticCategories標示，了解哪些Plastic可回收、如何清潔準備。', 'Learn resin codes 1-7, what\'s recyclable, and how to prepare plastics for collection.'),
    ('Paper回收完整Guides', 'Paper Recycling Guide'),
    ('Glass回收須知', 'Glass Recycling Essentials'),
    ('Glass可無限回收而不損品質，但顏色要分開。了解完整流程。', 'Glass can be endlessly recycled without quality loss, but colors must be separated. Learn the full process.'),
    ('Metal與鋁罐回收', 'Metal & Aluminum Cans'),
    ('回收鋁節省 94% 能源。了解鐵罐、鋁罐、拆解注意事項。', 'Recycling aluminum saves 94% energy. Learn about steel, aluminum, cans, and prep tips.'),
    ('E-Waste正確回收', 'E-Waste Recycling'),
    ('Hazardous Waste處理', 'Hazardous Waste Handling'),
    ('閱讀更多', 'Read More'),
    # events.html
    ('近期Events', 'Upcoming Events'),
    ('參與社區淨灘、回收挑戰與環境教育Events。', 'Join clean-ups, challenges, and sustainability workshops.'),
    # centers.html
    ('尋找回收Centers', 'Find a Recycling Center'),
    ('根據你的位置，顯示最近的回收站與Centers。', 'Find the nearest recycling drop-off locations.'),
    ('無法取得位置，顯示所有Centers。', 'Unable to detect location. Showing all centers.'),
    ('取得路線', 'Directions'),
    # howto.html
    ('實用圖文How-To，讓回收變得簡單又正確。', 'Practical tutorials to make recycling simple and correct.'),
    ('紙、Plastic、Glass、Metal——學會快速辨識並分裝。', 'Paper, plastic, glass, and metal — learn to identify and separate quickly.'),
    (' compost 在家開始', 'Start Composting at Home'),
    # events-detail.html
    ('Events詳情', 'Event Details'),
    ('這是一場.open 的社區Events，所有人都能自由參加。現場將提供手套、垃圾袋與基礎說明。請穿著適合戶外Events的衣物與鞋子，並自備水壺。Events結束後將頒發感謝狀給所有參與者。', 'This is an open community event. All are welcome. On-site gloves, bags, and a brief orientation will be provided. Please wear suitable outdoor clothing and shoes, and bring your own water bottle. Certificates of appreciation will be given to all participants at the end.'),
    ('返回Events列表', 'Back to Events'),
    # index.html
    ('📚 回收Guides', '📚 Recycling Guides'),
    ('📍 回收Centers', '📍 Find Centers'),
    ('🗓️ Events資訊', '🗓️ Upcoming Events'),
    ('社區回收Events', 'Community recycling activities'),
    ('材料智能', 'Material Intelligence'),
    ('Glass可以無窮次回收而不影響品質。', 'Glass can be recycled endlessly without losing purity or quality.'),
    ('高回收率', 'High Recovery'),
    ('高價值', 'High Value'),
    ('全球每年可回收E-Waste價值超過 620 億美元。', 'Over $62B in recoverable e-waste value per year worldwide.'),
    ('節能首選', 'Energy Saver'),
    ('鋁罐', 'Aluminum Cans'),
    ('影響數據', 'Impact Stats'),
    ('影片庫', 'Video Library'),
    ('觀看影片 →', 'Watch Video →'),
    ('認識E-Waste危機與正確回收方式。', 'Understanding the electronic waste crisis and how to responsibly recycle devices.'),
    ('探索Guides', 'Explore Guides'),
    ('查看Events', 'View Events'),
    ('重新定義廢棄物為潛在Resources。你通往物質無限循環的完整Guides。', 'Redefining waste as latent resource. Your complete guide to the infinite return of matter.'),
    ('回收Guides', 'Recycling Guides'),
    ('回收Centers', 'Local Centers'),
    ('近期Events', 'Upcoming Events'),
    ('淨灘行動', 'Beach Cleanup'),
    ('回收挑戰', 'Recycling Challenge'),
    ('影響報告', 'Impact Report'),
    # guides detail pages
    ('PlasticCategories重點', 'Plastic Sorting 101'),
    ('PET（1號）常用於飲料瓶；HDPE（2號）常见於洗髮乳瓶；PVC（3號）通常不建議回收；LDPE（4號）常见於Plastic袋；PP（5號）常見於優格杯；PS（6號）保麗龍難回收；Other（7號）多為複合材料。建議先查詢當地回收規範。', 'PET (1) is used for drink bottles. HDPE (2) is common in detergent bottles. PVC (3) is usually not accepted. LDPE (4) is used in plastic bags. PP (5) is common in yogurt cups. PS (6) is hard to recycle. Other (7) is mixed-material. Check your local rules first.'),
    ('Paper回收重點', 'Paper Recycling 101'),
    ('報紙與紙箱可回收；但油汙紙、衛生紙、烘焙紙通常不適合回收。Paper應保持乾燥，避免混入其他垃圾。回收紙可減少 7,000 加侖用水。', 'Newspaper and cardboard are recyclable. Soiled paper, tissues, and wax paper are usually not. Keep paper dry and separate from other waste.'),
    ('Glass回收重點', 'Glass Recycling Essentials'),
    ('透明、棕色、綠色Glass需分開收集。回收前請沖洗乾淨並移除瓶蓋。碎璃應以厚紙袋包裝並標示，避免清理人員受傷。', 'Separate clear, brown, and green glass. Rinse and remove caps before recycling. Wrap broken glass in thick paper and label it.'),
    ('Metal回收重點', 'Metal & Aluminum Cans'),
    ('Aluminum與鐵罐可分開回收；壓扁可節省空間。請勿將含有食物殘餘的罐頭直接投入回收箱，應先沖洗乾淨。', 'Separate aluminum and steel cans when possible. Rinse food residue to avoid odors. Crush cans to save space.'),
    ('E-Waste回收重點', 'E-Waste Recycling'),
    ('Hazardous處理重點', 'Hazardous Waste 101'),
    ('油漆、清潔劑、燈管、藥品等Hazardous需送至指定收集點。容器應保持原裝並加蓋，避免洩漏。切勿與一般垃圾混放。', 'Keep hazardous items in original containers with lids sealed. Use designated collection points. Never mix with regular trash.'),
    ('顯示最近的Centers', 'showing nearest centers'),
    ('取得路線', 'Directions'),
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
    for zh, en in replacements:
        content = content.replace(zh, en)
    # JS Chinese defaults
    content = re.sub(r"\?\s*'[^']*'", ": 'Location detection failed.'", content)
    if content != original:
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(content)
        changed.append(os.path.relpath(filepath, site_dir))
print(f'Final pass updated {len(changed)} files:')
for f in changed:
    print(' ', f)
