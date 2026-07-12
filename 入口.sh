#!/usr/bin/env bash
set -euo pipefail

# ─── 408 课程笔记本 macOS / Linux 启动脚本 ───

# 自动定位到脚本所在目录（不依赖硬编码路径）
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$SCRIPT_DIR"

echo "========================================"
echo "  408 考研复习笔记本"
echo "========================================"

# 1. 生成搜索索引和清单
echo "[1/2] 生成索引 & 清单..."
python3 生成索引.py

# 2. 打开浏览器
echo "[2/2] 启动服务 & 打开浏览器..."
if command -v open &>/dev/null; then
    # macOS
    open "http://localhost:8765" &
elif command -v xdg-open &>/dev/null; then
    # Linux
    xdg-open "http://localhost:8765" &
elif command -v start &>/dev/null; then
    # Windows (fallback)
    start "http://localhost:8765" &
fi

# 3. 启动 HTTP 服务器（阻塞，Ctrl+C 退出）
python3 server.py
echo "服务已关闭。"