import sys; sys.stdout.reconfigure(encoding='utf-8')
bd = [
(1741,"estate","n.","/I'steIt/","房地产；庄园","He inherited a large estate from his grandfather."),
(1742,"esteem","n./v.","/I'sti:m/","尊重","She is held in high esteem by her colleagues."),
(1743,"eternal","adj.","/I't3:rn@l/","永恒的","The debate about nature versus nurture seems eternal."),
(1744,"ethic","n.","/'eTIk/","伦理","The medical profession has a strict code of ethics."),
(1745,"ethnic","adj.","/'eTnIk/","民族的","The city is known for its diverse ethnic communities."),
(1746,"evacuate","v.","/I'vAkjueIt/","疏散","Residents were evacuated ahead of the hurricane."),
(1747,"evade","v.","/I'veId/","逃避","The company was accused of evading taxes offshore."),
(1748,"evaluate","v.","/I'vAljueIt/","评估","The program will be evaluated after the first year."),
(1749,"evaporate","v.","/I'vAp@reIt/","蒸发","Their savings evaporated within months of losing jobs."),
(1750,"eve","n.","/i:v/","前夕","They arrived on the eve of the festival."),
(1751,"eventually","adv.","/I'ventSu@li/","最终","After months of talks they eventually reached an agreement."),
(1752,"evoke","v.","/I'vouk/","唤起","The photograph evokes memories of a simpler time."),
(1753,"evolution","n.","/ev@'lu:S@n/","进化","Evolution is supported by a vast body of evidence."),
(1754,"exceed","v.","/Ik'si:d/","超过","The final cost exceeded the original estimate by 50 percent."),
(1755,"excel","v.","/Ik'sel/","擅长","She excels in mathematics and plans to study engineering."),
(1756,"exceptional","adj.","/Ik'sepS@n@l/","例外的","The company achieved exceptional growth during the downturn."),
(1757,"excerpt","n.","/'eks3:rpt/","摘录","The magazine published an excerpt from her novel."),
(1758,"excessive","adj.","/Ik'sesIv/","过度的","Excessive drinking can lead to serious health problems."),
(1759,"exclude","v.","/Ik'sklu:d/","排除","The policy excludes part-time workers from certain benefits."),
(1760,"exclusive","adj.","/Ik'sklu:sIv/","独有的；高档的","The journalist got an exclusive interview with the prime minister."),
(1761,"execute","v.","/'eksIkju:t/","执行","The plan was poorly executed and failed to achieve its goals."),
(1762,"exemplify","v.","/Ig'zemplIfaI/","举例说明","Her career exemplifies the value of persistence and hard work."),
(1763,"exempt","adj./v.","/Ig'zempt/","免除的；免除","Charities are exempt from paying income tax."),
(1764,"exert","v.","/Ig'z3:rt/","施加","The new CEO has exerted a strong influence on the company."),
(1765,"exhaust","v.","/Ig'zO:st/","耗尽","The long journey had completely exhausted the driver."),
(1766,"exhibit","v.","/Ig'zIbIt/","展示","The patient exhibited all the classic symptoms of the disease."),
(1767,"exile","n./v.","/'eksaIl/","流放；流放","The former dictator has been living in exile for a decade."),
(1768,"exotic","adj.","/Ig'zA:tIk/","异国情调的","The market sells exotic fruits imported from Southeast Asia."),
(1769,"expedition","n.","/eksp@'dIS@n/","远征","The expedition to the South Pole took over three months."),
(1770,"expel","v.","/Ik'spel/","驱逐","The student was expelled from school for repeated misconduct."),
(1771,"expenditure","n.","/Ik'spendItS@r/","支出","Government expenditure on health has doubled in a decade."),
(1772,"expertise","n.","/eksp@r'ti:z/","专业知识","Her expertise in law made her the ideal candidate."),
(1773,"expire","v.","/Ik'spaI@r/","到期","My passport expires next month so I need to renew it."),
(1774,"explicit","adj.","/Ik'splIsIt/","明确的","The instructions were explicit about emergency procedures."),
(1775,"exploit","n.","/'eksplOIt/","功绩","His wartime exploits were celebrated in books and films."),
(1776,"explosive","adj./n.","/Ik'splousIv/","爆炸的；炸药","The situation in the region remains highly explosive."),
(1777,"exponential","adj.","/eksp@'nenS@l/","指数的","The company has seen exponential growth in users this year."),
(1778,"exquisite","adj.","/Ik'skwIzIt/","精致的","The museum houses an exquisite collection of Chinese porcelain."),
(1779,"extend","v.","/Ik'stend/","延伸","The deadline has been extended by two weeks."),
(1780,"extent","n.","/Ik'stent/","程度","To what extent does the government control the media?"),
(1781,"external","adj.","/Ik'st3:rn@l/","外部的","The company hired an external auditor to review its finances."),
(1782,"extinct","adj.","/Ik'stINkt/","灭绝的","The dodo bird has been extinct for over 300 years."),
(1783,"extinguish","v.","/Ik'stINgwIS/","熄灭","Firefighters worked through the night to extinguish the blaze."),
(1784,"extract","n.","/'ekstrAkt/","摘录","The article contains extracts from the private diary."),
(1785,"extravagant","adj.","/Ik'strAv@g@nt/","奢侈的","The wedding was an extravagant affair costing over a million."),
(1786,"extreme","adj.","/Ik'stri:m/","极端的","The region experiences extreme temperatures in summer."),
(1787,"fabric","n.","/'fAbrIk/","织物；★结构","Corruption threatens the very fabric of democratic society."),
(1788,"fabulous","adj.","/'fAbj@l@s/","极好的","The hotel offers fabulous views of the surrounding mountains."),
(1789,"facet","n.","/'fAsIt/","方面","The problem has many facets that need careful consideration."),
(1790,"facilitate","v.","/f@'sIlIteIt/","促进","The new tunnel will facilitate the flow of traffic between cities."),
]
lines = []
lines.append("## Big Day 11（词汇 1741-1920）")
lines.append("")
lines.append("| # | 单词 | 词性 | 音标 | 释义 | 例句 |")
lines.append("|---|------|------|------|------|------|")
for n,w,p,ph,d,e in bd:
    lines.append(f"| {n} | **{w}** | {p} | {ph} | {d} | {e} |")
with open(r"C:\Users\方向容\Documents\408学习\408-学习管理\英语\考研词汇_词库.md","a",encoding="utf-8") as f:
    f.write("\n".join(lines))
print(f"OK: appended BD11 first half ({len(bd)} words)")
