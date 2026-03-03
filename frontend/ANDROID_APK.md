# Android APK 打包说明（Docker 架构保持不变）

本方案不会改动现有后端与 Docker 部署方式。  
APK 只是一个 Android 壳应用，启动后访问你现有的 HTTPS 服务地址。

## 1. 前置条件

- 后端和前端已按原方式部署（Docker Compose 不变）
- 对外可访问的 `HTTPS` 域名（例如 `https://soniox.example.com`）
- 已安装 Android Studio（含 Android SDK）
- Node.js 20+

## 2. 同步 Android 工程

在 `frontend` 目录执行：

### Windows PowerShell

```powershell
$env:CAP_SERVER_URL="https://soniox.example.com"
npm run android:sync
```

### macOS / Linux

```bash
CAP_SERVER_URL="https://soniox.example.com" npm run android:sync
```

说明：

- `CAP_SERVER_URL` 必须是 `https://`，否则登录 Cookie（`Secure`）无法工作
- 每次修改前端代码或服务地址后，都要重新执行 `npm run android:sync`

## 3. 打开 Android Studio 并打包

```bash
npm run android:open
```

然后在 Android Studio 中：

1. 等待 Gradle 同步完成
2. 菜单 `Build` -> `Build APK(s)`
3. 产物默认在 `android/app/build/outputs/apk/debug/app-debug.apk`

## 4. 命令行打包（可选）

### Windows

```powershell
cd android
.\gradlew.bat assembleDebug
```

### macOS / Linux

```bash
cd android
./gradlew assembleDebug
```

## 5. 已处理的功能兼容点

- 保持所有 API 与 WebSocket 路径不变（`/api`、`/ws`）
- Android 已声明麦克风权限（`RECORD_AUDIO`）
- 保持现有登录、历史记录、实时转录、AI 功能逻辑不变

