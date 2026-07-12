# -*- coding: utf-8 -*-
import os
root = r'C:\Users\方向容\Documents\408'

notes = {
    '数据结构/01-绪论/01-时间复杂度分析.md': '# 时间复杂度分析\n\n## 定义\n\n时间复杂度 \(n)\$ 描述算法执行时间随输入规模 \\$ 增长的趋势，用 \\$ 记号表示上界。\n\n- \(1)\$：常数阶\n- \(\\log n)\$：对数阶\n- \(n)\$：线性阶\n- \(n\\log n)\$：线性对数阶\n- \(n^2)\$：平方阶\n\n## 核心定理 / 性质\n\n主定理（Master Theorem）：对于 \(n) = aT(n/b) + f(n)\$\n\n| 条件 | \(n)\$ |\n|---|---|\n| \(n)=O(n^{\\log_b a-\\epsilon})\$ | \$\\Theta(n^{\\log_b a})\$ |\n| \(n)=\\Theta(n^{\\log_b a})\$ | \$\\Theta(n^{\\log_b a}\\log n)\$ |\n| \(n)=\\Omega(n^{\\log_b a+\\epsilon})\$ | \$\\Theta(f(n))\$ |\n\n## 计算方法 / 技巧\n\n1. 循环分析：直接计算循环次数\n2. 递推树：画树，每层代价求和\n3. 主定理：匹配三种情况\n\n## 典型例题\n\n分析 for(i=1; i<=n; i*=2) for(j=1; j<=i; j++) 时间复杂度。外层 \\$\\log n\\$ 次，总次数：\n\n\$\ = 1+2+4+\\cdots+n = 2n-1 = O(n)\$\$\n\n## 易错点\n\n1. 多循环直接相乘仅在每层独立时成立\n2. for(i=1;i<n;i*=2) 是 \(\\log n)\$ 而非 \(n)\$\n3. 递归中重复计算子问题会退化为指数\n\n---\n\n归档于 2026-06',
}

for relpath, content in notes.items():
    fullpath = os.path.join(root, relpath.replace('/', os.sep))
    os.makedirs(os.path.dirname(fullpath), exist_ok=True)
    with open(fullpath, 'w', encoding='utf-8') as f:
        f.write(content.lstrip('\n'))

print(f"Created {len(notes)} note files.")
