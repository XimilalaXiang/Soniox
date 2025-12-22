/**
 * 发言人工具函数
 * 提供发言人相关的辅助函数，包括颜色映射和时间格式化
 */

/**
 * 发言人颜色映射表
 * 为不同发言人分配不同的颜色
 */
const speakerColors = [
  '#000000',  // Speaker 0 - 黑色
  '#333333',  // Speaker 1 - 深灰
  '#666666',  // Speaker 2 - 中灰
  '#999999',  // Speaker 3 - 浅灰
  '#1a1a1a',  // Speaker 4 - 近黑
  '#4d4d4d',  // Speaker 5 - 暗灰
  '#737373',  // Speaker 6 - 灰色
  '#a6a6a6'   // Speaker 7 - 亮灰
]

/**
 * 获取发言人的颜色
 * 
 * @param {string} speaker - 发言人标识符（如 "Speaker 0"）
 * @returns {string} 颜色十六进制代码
 */
export function getSpeakerColor(speaker) {
  if (!speaker) return speakerColors[0]
  
  // 提取发言人编号
  const speakerNum = parseInt(speaker.replace(/\D/g, '')) || 0
  
  // 循环使用颜色
  return speakerColors[speakerNum % speakerColors.length]
}

/**
 * 格式化时间戳（毫秒）为 MM:SS 格式
 * 
 * @param {number} ms - 毫秒时间戳
 * @returns {string} 格式化的时间字符串
 */
export function formatTime(ms) {
  if (ms === undefined || ms === null) return '0:00'
  
  const totalSeconds = Math.floor(ms / 1000)
  const minutes = Math.floor(totalSeconds / 60)
  const seconds = totalSeconds % 60
  
  return `${minutes}:${seconds.toString().padStart(2, '0')}`
}

/**
 * 格式化秒数为 MM:SS 格式
 * 
 * @param {number} seconds - 秒数
 * @returns {string} 格式化的时间字符串
 */
export function formatDuration(seconds) {
  if (seconds === undefined || seconds === null) return '0:00'
  
  const mins = Math.floor(seconds / 60)
  const secs = Math.floor(seconds % 60)
  
  return `${mins}:${secs.toString().padStart(2, '0')}`
}

/**
 * 格式化日期为本地化字符串
 * 
 * @param {string} dateString - ISO 日期字符串
 * @returns {string} 格式化的日期时间字符串
 */
export function formatDate(dateString) {
  if (!dateString) return ''
  
  const date = new Date(dateString)
  return date.toLocaleString('zh-CN', {
    year: 'numeric',
    month: '2-digit',
    day: '2-digit',
    hour: '2-digit',
    minute: '2-digit'
  })
}

export default {
  getSpeakerColor,
  formatTime,
  formatDuration,
  formatDate
}

