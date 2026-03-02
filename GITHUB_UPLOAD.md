# GitHub 上传指南

## 🚨 重要提示：密码认证已停用

GitHub 不再支持使用密码进行 Git 操作。您需要使用个人访问令牌 (Personal Access Token)。

## 步骤 1：创建个人访问令牌 (PAT)

1. 登录 GitHub (https://github.com)
2. 点击右上角头像 → Settings
3. 左侧菜单 → Developer settings
4. Personal access tokens → Tokens (classic)
5. Generate new token → Generate new token (classic)
6. 设置令牌信息：
   - Note: `morse-decoder-upload`
   - Expiration: 选择过期时间（建议 90 天）
   - 勾选权限：
     - ✅ `repo` (完整仓库访问权限)
     - ✅ `workflow` (如果需要 GitHub Actions)
7. 点击 "Generate token"
8. **⚠️ 重要**：复制生成的令牌（只会显示一次）

## 步骤 2：创建 GitHub 仓库

1. 访问 https://github.com/new
2. 填写仓库信息：
   - Repository name: `morse-decoder`
   - Description: `高性能摩尔斯电码解码器，支持 V2/V3 解码器和命令行工具`
   - 选择 Public 或 Private
   - **不要**勾选 "Initialize this repository with a README"
3. 点击 "Create repository"

## 步骤 3：配置 Git 并推送代码

```bash
cd /workspace/projects/release

# 配置用户信息
git config user.name "william23374"
git config user.email "your-email@example.com"  # 替换为您的 GitHub 邮箱

# 添加所有文件
git add .

# 创建初始提交
git commit -m "feat: 摩尔斯电码解码器 v1.0.0

实现功能：
- V2 解码器：高性能解码器（1200x 实时）
- V3 解码器：先进算法解码器（高噪声环境）
- 命令行工具：支持文件、麦克风、流模式
- 完整文档：CLI、API、快速入门指南
- 单元测试：8/8 通过"

# 添加远程仓库（替换为您的令牌）
git remote add origin https://YOUR_TOKEN@github.com/william23374/morse-decoder.git

# 推送到 GitHub
git push -u origin master
```

## 步骤 4：验证上传

1. 访问 https://github.com/william23374/morse-decoder
2. 确认所有文件已上传
3. 检查 README.md 显示是否正常

## 🛡️ 安全建议

1. **不要共享您的令牌**：像密码一样保护它
2. **定期轮换令牌**：建议每 90 天更新一次
3. **使用环境变量**：在脚本中使用环境变量存储令牌
4. **最小权限原则**：只授予必要的权限

## 🔧 故障排除

### 错误：Authentication failed

**原因**：令牌无效或过期

**解决**：
1. 检查令牌是否正确复制
2. 确认令牌权限包含 `repo`
3. 生成新的令牌

### 错误：Repository not found

**原因**：仓库名称或用户名错误

**解决**：
1. 检查仓库 URL 是否正确
2. 确认仓库已创建

### 错误：Connection refused

**原因**：网络问题

**解决**：
1. 检查网络连接
2. 尝试使用代理
3. 检查防火墙设置

## 📝 命令速查

```bash
# 查看远程仓库
git remote -v

# 修改远程仓库 URL
git remote set-url origin https://YOUR_TOKEN@github.com/william23374/morse-decoder.git

# 推送更改
git push origin master

# 拉取更改
git pull origin master

# 查看状态
git status

# 查看提交历史
git log --oneline
```

## 🎯 下一步

上传成功后，您可以：

1. **发布到 PyPI**：
   ```bash
   cd /workspace/projects/release
   python -m build
   twine upload dist/*
   ```

2. **添加 GitHub Actions**：
   - 自动化测试
   - 自动构建
   - 自动发布

3. **添加贡献指南**：
   - `CONTRIBUTING.md`
   - `CHANGELOG.md`

4. **添加许可证**：
   - 已包含 MIT 许可证

## 📞 获取帮助

- GitHub 文档: https://docs.github.com
- PAT 创建指南: https://docs.github.com/authentication/keeping-your-account-and-data-secure/creating-a-personal-access-token
