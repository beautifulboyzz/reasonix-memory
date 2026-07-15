# -*- coding: utf-8 -*-
"""生成最详细的日常规划PDF"""
from fpdf import FPDF
import os

FONT_PATH = "C:\\Windows\\Fonts\\msyh.ttc"

class PDF(FPDF):
    def footer(self):
        self.set_y(-12)
        self.set_font('zh', '', 6)
        self.set_text_color(160,160,160)
        self.cell(0, 8, f'Reasonix 生成  |  2026-07  |  {self.page_no()}/{{nb}}', align='C')

pdf = PDF('P', 'mm', 'A4')
pdf.alias_nb_pages()
pdf.add_font('zh', '', FONT_PATH)

def section(title, color=(30,30,50)):
    pdf.set_fill_color(*color)
    pdf.rect(12, pdf.get_y(), 186, 8, 'F')
    pdf.set_text_color(255,255,255)
    pdf.set_font('zh', '', 11)
    pdf.set_xy(15, pdf.get_y()+0.5)
    pdf.cell(0, 7, title)
    pdf.ln(11)

def row(time, icon, activity, detail, color=(80,80,90)):
    c = color
    pdf.set_fill_color(248,249,250)
    # time
    pdf.set_font('zh', '', 9)
    pdf.set_text_color(*c)
    pdf.set_xy(14, pdf.get_y())
    pdf.cell(25, 6.5, time)
    # icon+activity
    pdf.set_font('zh', '', 10)
    pdf.set_text_color(30,30,40)
    pdf.cell(40, 6.5, f'{icon} {activity}')
    # detail
    pdf.set_font('zh', '', 7.5)
    pdf.set_text_color(100,100,110)
    pdf.multi_cell(0, 6.5, detail)
    pdf.ln(0.5)

pdf.add_page()

# ═══════════════════════ 标题页 ═══════════════════════
pdf.set_fill_color(20, 28, 48)
pdf.rect(0, 0, 210, 55, 'F')
pdf.set_text_color(255,255,255)
pdf.set_font('zh', '', 26)
pdf.set_y(12)
pdf.cell(0, 14, 'DAILY ROUTINE', align='C')
pdf.ln(16)
pdf.set_font('zh', '', 11)
pdf.set_text_color(180,200,225)
pdf.cell(0, 8, '24岁 · 期货交易员 · 广东御澜 · 深圳南光村', align='C')
pdf.ln(8)
pdf.set_font('zh', '', 8)
pdf.cell(0, 6, '减脂期：1,400~1,550 kcal / 蛋白150g / 碳水100~125g / 脂肪45g  |  16:8间歇断食  |  每日训练', align='C')

pdf.set_y(62)

# ═══════════════════════ 个人底线 ═══════════════════════
pdf.set_fill_color(245,245,245)
pdf.rect(12, 62, 186, 28, 'F')
y0 = pdf.get_y() + 2
pdf.set_xy(14, y0)
stats = [
    ('173cm', '74kg', '~24%BF', '目标 ~70kg'),
    ('BMR 1,706', 'TDEE 2,100~2,600', '缺口 800~1,000', '蛋白 150g 底线'),
]
pdf.set_text_color(50,55,65)
pdf.set_font('zh', '', 8)
for row_data in stats:
    pdf.set_xy(14, y0)
    for s in row_data:
        pdf.cell(44, 5.5, s, align='C')
    y0 += 5.5

pdf.set_y(95)

# ═══════════════════════ 时间线 ═══════════════════════
section('☀️ 上午', (45, 70, 40))

row('10:45', '🌅', '起床', '醒来先关空调，开窗通风，喝 300ml 水')
row('10:50', '🧘', '晨间拉伸', '弹力带绕肩 1min → 胸椎猫牛式 1min → 全身动态拉伸 2min')
row('10:55', '🍌', '练前加餐', '香蕉 1 根 + 黑咖啡 1 杯 + 肌酸 5g + 甜菜根粉 + 巴西莓粉 + 枸杞原浆 30ml')
row('11:05', '🏋️', '居家训练', '👇 见下方「每日训练模板」')
row('11:30', '🚿', '冷水澡', '训练完立刻洗，如果太热就先回空调房缓 5min 再洗')
row('11:40', '🥩', '练后第一餐', '方糕 70g + 豆乳 200ml + 蛋白粉 1 勺 + 水 500ml')
row('12:00', '🎯', '自由时间', '刷手机 / 研究策略 / 休息')
row('12:30', '🚇', '通勤', '南光村 → 福田站，25min 地铁')
row('13:00', '💼', '上班', '广东御澜 · 研究策略 + 随身笔记本每 30min 记录')

section('🌆 下午+傍晚', (50, 60, 90))

row('18:00', '🚇', '下班回家', '福田 → 南光村，25min 地铁')
row('18:30', '🍳', '做晚饭', '电饭煲 400W 2L 焖饭：茉莉米 100g + 0 水 + 番茄 150g + 肉 + 蔬菜包 + 腊肠 20g，盖盖煮')

# 天气分支
pdf.set_fill_color(250, 245, 235)
pdf.rect(14, pdf.get_y(), 182, 22, 'F')
pdf.set_text_color(120, 80, 30)
pdf.set_font('zh', '', 9)
pdf.set_xy(16, pdf.get_y()+1.5)
pdf.cell(0, 6, '🌤️  天气分支：晴天 vs 下雨')
pdf.set_xy(16, pdf.get_y()+8)
pdf.set_font('zh', '', 7.5)
pdf.set_text_color(110, 90, 50)
pdf.cell(88, 5, '☀️  晴天：19:00~19:40 打篮球 40min', align='C')
pdf.cell(0, 5, '🌧️  下雨：居家拉伸+泡沫轴+体态纠正 20min', align='C')
pdf.ln(14)

row('~20:00', '🥚', '加菜焖蛋', '到家（或拉伸完）→ 开盖加西兰花/绿叶菜 + 鸡蛋 2 个 + 橄榄油喷 → 盖盖焖 5~10min → 全熟蛋')
row('20:10', '🚿', '冷水澡', '打完球或拉伸完洗一次')
row('20:20', '🥩', '晚餐+补剂', '吃焖饭 + 所有脂溶性补剂（维D+Q10+叶黄素+姜黄素+番茄红素+鱼油+善存）')
row('20:40', '🧹', '洗碗收尾', '收拾厨房，准备明日食材')

section('🌙 夜间', (30, 30, 50))

row('21:00', '🎮', '个人时间', '打游戏 / 追剧 / 学习（7月：基金从业科目二+英语教培刷卷）')
row('01:30', '', '夜盘收尾准备', '调暗灯光，减少蓝光暴露')
row('01:40', '💊', '温水+睡前补剂', '复合镁 NovaFun + L-茶氨酸 NOW 200mg + （如有短时入睡困难则加褪黑素）')
row('01:50', '🛏️', '上床+关手机', '关手机放远，闭眼。不刷任何屏幕。')
row('02:00', '😴', '入睡目标', '如果 02:00 睡 → 10:30 起 = 8.5h ✅  如果 03:00 睡 → 10:30 起 = 7.5h ✅')
pdf.ln(2)
pdf.set_fill_color(245, 240, 255)
pdf.rect(14, pdf.get_y(), 182, 8, 'F')
pdf.set_text_color(80, 60, 120)
pdf.set_font('zh', '', 7.5)
pdf.set_xy(16, pdf.get_y()+1)
pdf.cell(0, 6, '⏰ 睡眠核心纪律：固定起床时间 10:30，入睡时间浮动但保证 ≥7.5h。褪黑素只在连续入睡困难时用。')

pdf.ln(12)

# ═══════════════════════ 每日训练模板 ═══════════════════════
section('🏋️ 每日训练模板（A/B/C 循环）', (140, 70, 30))

pdf.set_font('zh', '', 8)
pdf.set_text_color(50,50,60)
pdf.cell(0, 5, '每天必做（不分日）：弹力带绕肩 1min + 胸椎猫牛式 1min → 主训练 20~25min → 收尾拉伸 2min')
pdf.ln(6)

# A日
pdf.set_fill_color(252, 240, 235)
pdf.rect(14, pdf.get_y(), 182, 28, 'F')
pdf.set_text_color(180, 80, 40)
pdf.set_font('zh', '', 9)
pdf.set_xy(16, pdf.get_y()+1)
pdf.cell(0, 5, 'A日 · 上肢推+拉（一周2~3次）')
pdf.set_text_color(60,60,70)
pdf.set_font('zh', '', 7.5)
pdf.set_xy(16, pdf.get_y()+6)
row_text = '① 哑铃卧推 3×10~12  ② 哑铃划船 3×10~12  ③ 哑铃推举 3×10~12  ④ 俯卧撑 2×力竭'
pdf.cell(0, 4.5, row_text)
pdf.set_xy(16, pdf.get_y()+5)
row_text2 = '⑤ 靠墙天使 2×15  ⑥ 死虫 2×12/侧  ⑦ 胸椎旋转拉伸收尾'
pdf.cell(0, 4.5, row_text2)
pdf.ln(30)

# B日
pdf.set_fill_color(235, 245, 240)
pdf.rect(14, pdf.get_y(), 182, 33, 'F')
pdf.set_text_color(30, 120, 70)
pdf.set_font('zh', '', 9)
pdf.set_xy(16, pdf.get_y()+1)
pdf.cell(0, 5, 'B日 · 下肢+弹跳（一周1~2次）')
pdf.set_text_color(60,60,70)
pdf.set_font('zh', '', 7.5)
pdf.set_xy(16, pdf.get_y()+6)
pdf.cell(0, 4.5, '① 哑铃深蹲/高脚杯深蹲 3×10~12  ② 哑铃罗马尼亚硬拉 3×10~12')
pdf.set_xy(16, pdf.get_y()+5)
pdf.cell(0, 4.5, '③ 保加利亚分腿蹲/箭步蹲 3×8~10/腿  ④ 臀桥 3×15')
pdf.set_xy(16, pdf.get_y()+5)
pdf.cell(0, 4.5, '⑤ 弹跳训练（原地纵跳/连续跳）3×5次  ⑥ 平板支撑 2×30~45s')
pdf.set_xy(16, pdf.get_y()+5)
pdf.cell(0, 4.5, '⑦ 大腿前侧+后侧拉伸收尾')
pdf.ln(35)

# C日
pdf.set_fill_color(240, 235, 250)
pdf.rect(14, pdf.get_y(), 182, 28, 'F')
pdf.set_text_color(90, 60, 140)
pdf.set_font('zh', '', 9)
pdf.set_xy(16, pdf.get_y()+1)
pdf.cell(0, 5, 'C日 · 体态纠正+灵活度（主动恢复日，一周1~2次）')
pdf.set_text_color(60,60,70)
pdf.set_font('zh', '', 7.5)
pdf.set_xy(16, pdf.get_y()+6)
pdf.cell(0, 4.5, '① 靠墙天使 3×15  ② 胸椎猫牛式+旋转各10次  ③ 臀桥 3×15')
pdf.set_xy(16, pdf.get_y()+5)
pdf.cell(0, 4.5, '④ 死虫 3×10/侧  ⑤ 弹跳训练 5×3次  ⑥ 全身拉伸 5min')
pdf.ln(30)

pdf.ln(3)

# ═══════════════════════ 饮食模板 ═══════════════════════
section('🥩 每日饮食模板', (170, 60, 50))

pdf.set_font('zh', '', 8)
pdf.set_text_color(40,40,50)
pdf.cell(0, 5, '热量底线：≤1,550 kcal ｜ 蛋白150g ｜ 碳水≤125g ｜ 脂肪≤50g')
pdf.ln(7)

meals = [
    ('晨间', '10:50', '香蕉1根 + 黑咖啡 + 肌酸5g + 甜菜根+巴西莓+枸杞', '~165', '2g', '37g', '~0g'),
    ('练后', '11:40', '方糕70g + 豆乳200ml + 蛋白粉1勺', '~330', '31g', '32g', '9g'),
    ('晚餐基底', '20:20', '茉莉米100g + 番茄150g + 蔬菜包 + 腊肠20g + 西兰花 + 蛋2个 + 橄榄油喷', '~530', '22g', '61g', '21g'),
]

pdf.set_fill_color(248,248,248)
for meal in meals:
    pdf.rect(14, pdf.get_y(), 182, 16, 'F')
    pdf.set_font('zh', '', 9)
    pdf.set_text_color(170, 60, 50)
    pdf.set_xy(16, pdf.get_y()+1)
    pdf.cell(20, 6, meal[0])
    pdf.set_font('zh', '', 8)
    pdf.set_text_color(80,80,90)
    pdf.cell(20, 6, meal[1])
    pdf.set_font('zh', '', 7.5)
    pdf.set_text_color(40,40,50)
    pdf.cell(70, 6, meal[2])
    pdf.set_text_color(170,80,60)
    pdf.set_font('zh', '', 8)
    pdf.cell(15, 6, meal[3], align='C')
    pdf.cell(15, 6, meal[4], align='C')
    pdf.cell(15, 6, meal[5], align='C')
    pdf.cell(15, 6, meal[6], align='C')
    pdf.ln(16)

pdf.ln(2)

# 肉类轮换表
pdf.set_fill_color(250,245,240)
pdf.rect(14, pdf.get_y(), 182, 42, 'F')
pdf.set_text_color(140,100,50)
pdf.set_font('zh', '', 8)
pdf.set_xy(16, pdf.get_y()+1)
pdf.cell(0, 5, '🥩 晚餐肉类轮换（建议吃足 200~250g）')
pdf.set_text_color(60,60,70)
pdf.set_font('zh', '', 7)
pdf.set_xy(16, pdf.get_y()+6)
pdf.cell(0, 4.5, '🥇 鸡腿肉丁 200g（240kcal / 40g蛋白） ← 主力，建议每周4~5次')
pdf.set_xy(16, pdf.get_y()+4.5)
pdf.cell(0, 4.5, '🥇 黄牛牛肉丝 150g（240kcal / 33g蛋白） ← 补铁，每周2次')
pdf.set_xy(16, pdf.get_y()+4.5)
pdf.cell(0, 4.5, '✅ 巴沙鱼片/黑鱼片 200g（160~180kcal / 30~36g蛋白）← 轮换')
pdf.set_xy(16, pdf.get_y()+4.5)
pdf.cell(0, 4.5, '✅ 牡蛎/生蚝 200g（120kcal / 20g蛋白）← 补锌，一次替代锌片')
pdf.set_xy(16, pdf.get_y()+4.5)
pdf.cell(0, 4.5, '⚠️ 鲭鱼/猪肉馅/梅花肉/牛肉丸 ← 偶尔吃，脂肪偏高需控量')
pdf.ln(44)

pdf.ln(2)

# 补剂
section('💊 补剂时间表', (70, 70, 100))

sups = [
    ('☀️ 晨间练前', '肌酸 Foyes 5g + 甜菜根 Onlytree + 巴西莓 Onlytree + 枸杞宁之春'),
    ('🥩 练后第一餐', '葡萄糖酸锌 1片'),
    ('🥩 晚餐后', '维生素D NOW 1000IU + 辅酶Q10 Doctor`s Best 100mg + 叶黄素 Doppelherz 20mg'),
    ('', '+ 姜黄素 Naturewise 500mg + 番茄红素 Timeless + 鱼油 N29 EPA600/DHA330 + 善存蓝瓶'),
    ('😴 睡前', '复合镁 NovaFun 420mg + L-茶氨酸 NOW 200mg +（必要时褪黑素）'),
]
pdf.set_font('zh', '', 7.5)
for when, what in sups:
    pdf.set_text_color(80, 70, 90 if '睡前' not in when else 130)
    pdf.set_x(14)
    pdf.set_font('zh', '', 8)
    pdf.cell(30, 5.5, when)
    pdf.set_font('zh', '', 7)
    pdf.set_text_color(60,60,70)
    pdf.cell(0, 5.5, what)
    pdf.ln(5.5)

pdf.ln(5)

# ═══════════════════════ 雨天特别版 ═══════════════════════
section('🌧️ 雨天版（不下雨则跳过）', (60, 80, 100))

pdf.set_font('zh', '', 8)
pdf.set_text_color(50,50,60)
items = [
    '✅ 晨间举铁照常（拉伸 → 力量 → 弹跳 → 冷水澡 → 练后餐）',
    '✅ 上班照常',
    '❌ 傍晚不打球，改为居家主动恢复：',
    '   ① 泡沫轴滚压（大腿/背部/臀部）各 1min',
    '   ② C日体态纠偏训练（靠墙天使+臀桥+死虫+胸椎灵活度）',
    '   ③ 额外拉伸 5~8min',
    '🍽️ 饮食：与晴天完全一致，不需要减量。恢复日消耗略低，但缺口仍在 ~700 kcal',
]
for item in items:
    pdf.set_x(16)
    pdf.cell(0, 5.5, item)
    pdf.ln(5.5)

pdf.ln(4)

# ═══════════════════════ 财务目标 ═══════════════════════
section('💰 财务底线', (50, 60, 40))

pdf.set_font('zh', '', 7.5)
pdf.set_text_color(40,40,50)
items2 = [
    '🎯 年底目标：存款 5 万 ｜ 当前 2,000 ｜ 距年底 ~5.5 个月',
    '💳 网贷：每月 ~1,000 最低还款，优先清掉中行信用卡 3,360',
    '💵 8月底目标：底薪 7,000 → 谈到底薪 10,000（策略实盘+满一年筹码）',
    '📊 分红预估：期货组~8~10万 + 御澜币~5k~8k + 策略提成~2~4万',
    '🏠 刚性支出：房租水电 2,000 + 交通 220 + 朴朴 ~1,200 + 娱乐 300 + 网话 100 = ~3,820',
    '📈 月结余：9,500 - 3,820 - 1,000(网贷) = ~4,680 ｜ 加薪后目标 ~7,000',
]
for item in items2:
    pdf.set_x(14)
    pdf.cell(0, 5, item)
    pdf.ln(5)

# 底部
pdf.ln(5)
pdf.set_text_color(140,140,150)
pdf.set_font('zh', '', 6)
pdf.cell(0, 6, '由 Reasonix 根据用户个人数据生成 ｜ 2026-07 ｜ 如有变化随时更新', align='C')

out = os.path.join(os.environ['USERPROFILE'], 'Desktop', 'Reasonix_详细日常规划.pdf')
pdf.output(out)
print(f'OK -> {out}')
