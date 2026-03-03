import { execSync } from 'node:child_process'

const serverUrl = process.env.CAP_SERVER_URL?.trim()

if (!serverUrl) {
  console.error('Missing CAP_SERVER_URL. Example: https://soniox.example.com')
  process.exit(1)
}

if (!/^https:\/\//i.test(serverUrl)) {
  console.error('CAP_SERVER_URL must use https:// because auth cookie is Secure.')
  process.exit(1)
}

console.log(`[android] using CAP_SERVER_URL=${serverUrl}`)
execSync('npm run build', { stdio: 'inherit', shell: true })
execSync('npx cap sync android', { stdio: 'inherit', shell: true })
