---
name: 修复小程序API地址配置
overview: 将小程序的API请求地址从 http://10.61.0.2:8000 改为 http://localhost:8000，解决本地开发时的网络连接问题
todos:
  - id: search-all-ip-references
    content: 搜索 miniprogram 目录下所有 10.61.0.2 引用（已完成，共8处）
    status: completed
  - id: update-parse-js
    content: 修改 parse.js 第142行API地址和第245行错误信息中的IP为 localhost
    status: completed
    dependencies:
      - search-all-ip-references
  - id: update-profile-js
    content: 修改 profile.js 中全部6处API地址为 localhost:8000
    status: completed
    dependencies:
      - search-all-ip-references
  - id: verify-and-test
    content: 验证修改结果，重启开发者工具并测试解析功能是否正常
    status: completed
    dependencies:
      - update-parse-js
      - update-profile-js
---

## 用户需求

修复小程序本地开发环境下API请求失败的问题。用户已勾选微信开发者工具的"不校验合法域名、web-view、TLS版本以及HTTPS证书"选项，后端服务已启动在 0.0.0.0:8000，但小程序代码中使用的是 `http://10.61.0.2:8000`（非活跃网络接口IP），导致 API 请求报 500 错误和 timeout。需要将 API 地址统一修改为 `http://localhost:8000`。

## 核心功能

- 将小程序中所有引用 `10.61.0.2:8000` 的 API 请求地址修改为 `localhost:8000`
- 更新相关错误信息中的 IP 地址提示
- 确保本地开发环境下小程序能正常调用后端解析接口

## 技术栈

- 小程序平台：微信小程序（Windows 模拟器，lib: 3.16.1）
- 后端：FastAPI（运行在 localhost:8000）
- 开发模式：本地开发测试（不校验域名）

## 实施方案

### 修改范围

共涉及 **2 个文件，8 处引用**：

**文件1：miniprogram/pages/parse/parse.js**

- 第142行：`url: 'http://10.61.0.2:8000/api/parse'` → `url: 'http://localhost:8000/api/parse'`
- 第245行：错误信息中的 `'请检查服务是否运行在 10.61.0.2:8000'` → `'请检查服务是否运行在 localhost:8000'`

**文件2：miniprogram/pages/profile/profile.js**（共6处）

- 第69行：`url: 'http://10.61.0.2:8000/api/config'`
- 第185行：`url: 'http://10.61.0.2:8000/api/config'`
- 第214行：`url: 'http://10.61.0.2:8000/api/config'`
- 第246行：`url: 'http://10.61.0.2:8000/api/cookie/simplify'`
- 第261行：`url: 'http://10.61.0.2:8000/api/config'`
- 第290行：`url: 'http://10.61.0.2:8000/api/config'`

以上所有地址均需修改为对应的 `localhost:8000` 地址。

### 实施策略

1. 直接字符串替换，将 `10.61.0.2:8000` 统一替换为 `localhost:8000`
2. 修改后验证小程序能正常发起 POST 请求到 `/api/parse` 接口
3. 确保后端服务正常运行在 localhost:8000

## 注意事项

- 此修改仅适用于本地开发测试场景，上线前需更换为正式域名
- 用户已勾选"不校验合法域名"选项，localhost 在微信开发者工具中可正常访问
- 修改后需重启微信开发者工具使变更生效

## 使用的扩展

### SubAgent

- **code-explorer**
- 用途：在前期调研阶段搜索 miniprogram 目录下所有包含 `10.61.0.2` 的文件，精确定位需要修改的位置
- 预期结果：已完整定位到 2 个文件、8 处引用，为实施计划提供准确依据