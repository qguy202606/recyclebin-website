import os, re

site_dir = r"C:\Users\opc\source\repos\recyclebin-website"

file_fixes = {
    'plastic.html': {
        '認識Plastic 1-7 號CATEGORIES標示，了解哪些可回收、如何清潔準備。':
            'Learn resin codes 1-7, what\'s recyclable, and how to prepare plastics for collection.',
        'PlasticCATEGORIES重點': 'Plastic Sorting 101',
        'PET（1號）常用於飲料瓶；HDPE（2號）常见於洗髮乳瓶；PVC（3號）通常不建議回收；LDPE（4號）常见於Plastic袋；PP（5號）常見於優格杯；PS（6號）保麗龍難回收；Other（7號）多為複合材料。建議先查詢當地回收規範。':
            'PET (1) is used for drink bottles. HDPE (2) is common in detergent bottles. PVC (3) is not accepted. LDPE (4) is for plastic bags. PP (5) is for yogurt cups. PS (6) is hard to recycle. Other (7) is mixed. Check your local rules.',
    },
    'paper.html': {
        'Paper回收完整Guides': 'Paper Recycling Guide',
        'Paper回收重點': 'Paper Recycling 101',
        '報紙與紙箱可回收；但油汙紙、衛生紙、烘焙紙通常不適合回收。Paper應保持乾燥，避免混入其他垃圾。回收紙可減少 7,000 加侖用水。':
            'Newspaper and cardboard are recyclable. Soiled paper, tissues, and wax paper are usually not. Keep paper dry. Recycling paper saves 7,000 gallons of water per ton.',
    },
    'metal.html': {
        'Metal回收重點': 'Metal & Aluminum Cans',
        'Aluminum Cans與鐵罐可分開回收；壓扁可節省空間。請勿將含有食物殘餘的罐頭直接投入回收箱，應先沖洗乾淨。':
            'Separate aluminum and steel cans. Rinse food residue. Crush cans to save space.',
    },
    'glass.html': {
        'Glass回收重點': 'Glass Recycling Essentials',
        '透明、棕色、綠色Glass需分開收集。回收前請沖洗乾淨並移除瓶蓋。碎璃應以厚紙袋包裝並標示，避免清理人員受傷。':
            'Separate clear, brown, and green glass. Rinse and remove caps. Wrap broken glass in thick paper and label it.',
    },
    'ewaste.html': {
        '手機、筆電、電池不能丟一般垃圾，認識合格回收管道與資料安全。':
            'Phones, laptops, and batteries never go in regular trash. Find certified channels and data safety tips.',
        'E-Waste回收重點': 'E-Waste Recycling',
        '舊手機與筆電應送至認證回收點，避免有害物質污染環境。丟棄前請備份並刪除個人資料，或使用資料抹除工具。':
            'Take old devices to certified recyclers to avoid toxic pollution. Back up your data and wipe storage before drop-off.',
    },
    'index.html': {
        '🗓️ Events資訊': '🗓️ Upcoming Events',
        '社區回收Events': 'Community recycling activities',
        '什麼該回收、怎麼CATEGORIES': 'What to recycle, and how',
    },
    'guides.html': {
        '全面了解如何Sort Correctly與回收各類材料。': 'Learn how to sort and recycle each material correctly.',
        'Paper回收完整Guides': 'Paper Recycling Guide',
    },
}

for filename, fixes in file_fixes.items():
    rels = [os.path.join('guides', filename), os.path.join('events', filename), filename]
    target = None
    for rel in rels:
        p = os.path.join(site_dir, rel)
        if os.path.isfile(p):
            target = p
            break
    if not target:
        continue
    txt = open(target, 'r', encoding='utf-8').read()
    orig = txt
    for zh, en in fixes.items():
        txt = txt.replace(zh, en)
    if txt != orig:
        open(target, 'w', encoding='utf-8').write(txt)
        print(f'Patched {rel}')
    else:
        print(f'No change {rel}')
