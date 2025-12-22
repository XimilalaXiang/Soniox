/**
 * Markdown 渲染工具
 * 提供统一的 Markdown 渲染和消毒处理
 */

import MarkdownIt from 'markdown-it'
import DOMPurify from 'dompurify'

/**
 * 创建 MarkdownIt 实例
 */
const md = new MarkdownIt({
  html: false,
  linkify: true,
  breaks: true
})

/**
 * 渲染 Markdown 文本为 HTML
 * 
 * @param {string} text - 原始 Markdown 文本
 * @returns {string} 渲染后的 HTML 字符串
 */
export function renderMarkdown(text) {
  if (!text) return ''
  
  try {
    const html = md.render(text)
    return DOMPurify.sanitize(html)
  } catch (e) {
    // 降级处理：转义 HTML 特殊字符
    return String(text).replace(/</g, '&lt;').replace(/>/g, '&gt;')
  }
}

export default renderMarkdown

