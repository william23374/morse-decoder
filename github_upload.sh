#!/bin/bash
# GitHub 上传脚本
# 使用说明：
# 1. 先创建 GitHub 个人访问令牌 (PAT): https://github.com/settings/tokens
# 2. 创建 GitHub 仓库: https://github.com/new
# 3. 运行此脚本: bash github_upload.sh <你的PAT>

set -e  # 遇到错误立即退出

# 颜色定义
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m' # No Color

echo "=========================================="
echo "摩尔斯电码解码器 - GitHub 上传工具"
echo "=========================================="
echo ""

# 检查参数
if [ -z "$1" ]; then
    echo -e "${YELLOW}使用方法:${NC}"
    echo "  bash github_upload.sh <你的个人访问令牌(PAT)>"
    echo ""
    echo -e "${YELLOW}如何创建 PAT:${NC}"
    echo "  1. 访问: https://github.com/settings/tokens"
    echo "  2. 点击 'Generate new token (classic)'"
    echo "  3. 设置权限: 勾选 'repo'"
    echo "  4. 复制生成的令牌"
    echo ""
    echo -e "${YELLOW}如何创建仓库:${NC}"
    echo "  1. 访问: https://github.com/new"
    echo "  2. 仓库名称: morse-decoder"
    echo "  3. 点击 'Create repository'"
    echo ""
    exit 1
fi

GITHUB_TOKEN="$1"
REPO_NAME="morse-decoder"
USERNAME="william23374"
GITHUB_REPO_URL="https://${GITHUB_TOKEN}@github.com/${USERNAME}/${REPO_NAME}.git"

echo -e "${GREEN}✓ 检查 Git 状态...${NC}"
if ! git rev-parse --git-dir > /dev/null 2>&1; then
    echo -e "${RED}✗ 错误: 当前目录不是 Git 仓库${NC}"
    exit 1
fi

echo -e "${GREEN}✓ 检查远程仓库...${NC}"
if git remote get-url origin > /dev/null 2>&1; then
    echo "远程仓库已存在:"
    git remote get-url origin
    echo ""
    read -p "是否更新远程仓库 URL? (y/N): " -n 1 -r
    echo
    if [[ $REPLY =~ ^[Yy]$ ]]; then
        git remote set-url origin "$GITHUB_REPO_URL"
        echo -e "${GREEN}✓ 远程仓库 URL 已更新${NC}"
    fi
else
    echo -e "${GREEN}✓ 添加远程仓库...${NC}"
    git remote add origin "$GITHUB_REPO_URL"
fi

echo ""
echo -e "${YELLOW}⚠️  即将推送到:${NC}"
echo "  URL: https://github.com/${USERNAME}/${REPO_NAME}"
echo "  分支: main"
echo ""

read -p "确认推送? (y/N): " -n 1 -r
echo
if [[ ! $REPLY =~ ^[Yy]$ ]]; then
    echo "已取消推送"
    exit 0
fi

echo ""
echo -e "${GREEN}✓ 开始推送...${NC}"

# 推送到 GitHub
if git push -u origin main; then
    echo ""
    echo -e "${GREEN}==========================================${NC}"
    echo -e "${GREEN}✓ 上传成功！${NC}"
    echo -e "${GREEN}==========================================${NC}"
    echo ""
    echo "📦 仓库地址: https://github.com/${USERNAME}/${REPO_NAME}"
    echo ""
    echo "📝 下一步操作:"
    echo "  1. 访问仓库确认文件已上传"
    echo "  2. 更新仓库描述和标签"
    echo "  3. 设置 GitHub Pages (如果需要)"
    echo "  4. 配置 GitHub Actions (如果需要)"
    echo ""
else
    echo ""
    echo -e "${RED}==========================================${NC}"
    echo -e "${RED}✗ 推送失败${NC}"
    echo -e "${RED}==========================================${NC}"
    echo ""
    echo "可能的原因:"
    echo "  1. 个人访问令牌 (PAT) 无效或过期"
    echo "  2. 仓库不存在或仓库名称错误"
    echo "  3. PAT 权限不足 (需要 repo 权限)"
    echo "  4. 网络连接问题"
    echo ""
    echo "解决方法:"
    echo "  1. 检查 PAT 是否正确复制"
    echo "  2. 确认仓库已创建: https://github.com/new"
    echo "  3. 重新生成 PAT: https://github.com/settings/tokens"
    echo ""
    exit 1
fi
