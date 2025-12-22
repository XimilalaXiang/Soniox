<template>
  <div class="min-h-screen bg-white">
    <!-- 头部 -->
    <header class="border-b-4 border-black bg-white">
      <div class="container mx-auto px-4 py-6">
        <div class="flex items-center justify-between">
          <div class="flex-1">
            <button @click="$router.back()" class="text-gray-600 hover:text-black mb-2">
              <svg class="w-5 h-5 inline mr-1" fill="currentColor" viewBox="0 0 20 20">
                <path fill-rule="evenodd" d="M9.707 16.707a1 1 0 01-1.414 0l-6-6a1 1 0 010-1.414l6-6a1 1 0 011.414 1.414L5.414 9H17a1 1 0 110 2H5.414l4.293 4.293a1 1 0 010 1.414z" clip-rule="evenodd"/>
              </svg>
              返回
            </button>
            <h1 class="text-3xl font-bold">{{ session?.title || '加载中...' }}</h1>
          </div>
        </div>
      </div>
    </header>

    <!-- 加载中 -->
    <div v-if="loading" class="container mx-auto px-4 py-12 text-center">
      <div class="loading-dots inline-block">
        <span></span>
        <span></span>
        <span></span>
      </div>
      <p class="text-gray-600 mt-4">加载中...</p>
    </div>

    <!-- 主内容 -->
    <main v-else-if="session" class="container mx-auto px-4 py-8">
      <div class="grid grid-cols-1 lg:grid-cols-3 gap-6">
        <!-- 左侧：转录内容 -->
        <div class="lg:col-span-2">
          <div class="card">
            <div class="flex items-center justify-between mb-4">
              <h2 class="text-2xl font-bold">转录内容</h2>
              <div class="flex space-x-2">
                <button @click="showExportMenu = !showExportMenu" class="btn-secondary text-sm">
                  导出
                </button>
              </div>
            </div>

            <!-- 导出菜单 -->
            <div v-if="showExportMenu" class="mb-4 p-4 border-2 border-black rounded-md bg-gray-50">
              <p class="text-sm font-semibold mb-2">选择导出格式：</p>
              <div class="flex space-x-2">
                <button @click="exportFile('txt')" class="btn-secondary text-sm">
                  📄 TXT
                </button>
                <button @click="exportFile('json')" class="btn-secondary text-sm">
                  📋 JSON
                </button>
                <button @click="exportFile('markdown')" class="btn-secondary text-sm">
                  📝 Markdown
                </button>
              </div>
            </div>

            <!-- 元数据 -->
            <div class="flex items-center space-x-4 text-sm text-gray-600 mb-6 pb-4 border-b-2 border-gray-200">
              <span>📅 {{ formatDate(session.created_at) }}</span>
              <span>⏱️ {{ formatDuration(session.duration_seconds) }}</span>
              <span>👥 {{ session.speaker_count }} 位发言人</span>
              <span>📝 {{ session.word_count }} 字</span>
            </div>

            <!-- 转录片段 -->
            <div class="space-y-4">
              <div
                v-for="(segment, index) in session.segments"
                :key="index"
                class="transcript-segment fade-in"
                :style="{ borderLeftColor: getSpeakerColor(segment.speaker) }"
              >
                <div class="speaker-label" :style="{ color: getSpeakerColor(segment.speaker) }">
                  {{ segment.speaker }}
                </div>
                <div class="transcript-text">{{ segment.text }}</div>
                <div class="text-xs text-gray-400 mt-1">
                  {{ formatTime(segment.start_time) }} - {{ formatTime(segment.end_time) }}
                </div>
              </div>
            </div>
          </div>
        </div>

        <!-- 右侧：AI 分析 -->
        <div class="lg:col-span-1 space-y-6">
          <!-- AI 总结 -->
          <div v-if="session.ai_summary" class="card">
            <h3 class="text-lg font-bold mb-3">📝 AI 总结</h3>
            <div class="text-sm" v-html="aiSummaryHtml"></div>
          </div>

          <!-- AI 待办事项 -->
          <div v-if="session.ai_action_items" class="card">
            <h3 class="text-lg font-bold mb-3">✅ 待办事项</h3>
            <div class="text-sm" v-html="aiActionItemsHtml"></div>
          </div>

          <!-- AI 助手 -->
          <div class="card">
            <h3 class="text-lg font-bold mb-3">🤖 AI 助手</h3>

            <!-- 快捷操作 -->
            <div class="mb-4">
              <p class="text-sm font-semibold mb-2">快捷操作：</p>
              <div class="space-y-2">
                <button
                  @click="summarize"
                  :disabled="isProcessing"
                  class="btn-secondary text-sm w-full"
                >
                  📝 总结要点
                </button>
                <button
                  @click="extractActionItems"
                  :disabled="isProcessing"
                  class="btn-secondary text-sm w-full"
                >
                  ✅ 提取待办事项
                </button>
              </div>
            </div>

            <!-- 自定义提问 -->
            <div class="mb-4">
              <p class="text-sm font-semibold mb-2">自定义提问：</p>
              <textarea
                v-model="customQuestion"
                placeholder="输入你的问题..."
                class="input w-full h-20 resize-none"
                :disabled="isProcessing"
              ></textarea>
              <button
                @click="askCustomQuestion"
                :disabled="isProcessing || !customQuestion"
                class="btn-primary text-sm w-full mt-2"
              >
                提问
              </button>
            </div>

            <!-- AI 响应 -->
            <div v-if="aiResponse || isProcessing" class="mt-4">
              <p class="text-sm font-semibold mb-2">AI 回复：</p>
              <div class="border-2 border-black rounded-md p-3 bg-gray-50 max-h-64 overflow-y-auto text-sm">
                <div v-if="isProcessing && !aiResponse" class="flex items-center text-gray-500">
                  <div class="loading-dots mr-2">
                    <span></span>
                    <span></span>
                    <span></span>
                  </div>
                  思考中...
                </div>
                <div v-else v-html="aiHtml"></div>
                <div v-if="isProcessing" class="inline-block">
                  <span class="animate-pulse">▋</span>
                </div>
              </div>
            </div>
          </div>

          <!-- 统计信息 -->
          <div class="card">
            <h3 class="text-lg font-bold mb-3">📊 统计信息</h3>
            <div class="space-y-2 text-sm">
              <div class="flex justify-between">
                <span class="text-gray-600">会话 ID:</span>
                <span class="font-mono text-xs">{{ session.session_id.substring(0, 8) }}...</span>
              </div>
              <div class="flex justify-between">
                <span class="text-gray-600">状态:</span>
                <span :class="{
                  'text-green-600': session.status === 'completed',
                  'text-yellow-600': session.status === 'active',
                  'text-gray-600': session.status === 'stopped'
                }">
                  {{ getStatusText(session.status) }}
                </span>
              </div>
              <div class="flex justify-between">
                <span class="text-gray-600">持续时间:</span>
                <span>{{ formatDuration(session.duration_seconds) }}</span>
              </div>
              <div class="flex justify-between">
                <span class="text-gray-600">发言人数:</span>
                <span>{{ session.speaker_count }}</span>
              </div>
              <div class="flex justify-between">
                <span class="text-gray-600">字数:</span>
                <span>{{ session.word_count }}</span>
              </div>
              <div class="flex justify-between">
                <span class="text-gray-600">片段数:</span>
                <span>{{ session.segments?.length || 0 }}</span>
              </div>
            </div>
          </div>
        </div>
      </div>
    </main>

    <!-- 错误状态 -->
    <div v-else class="container mx-auto px-4 py-12 text-center">
      <p class="text-red-600">加载失败</p>
      <button @click="loadSession" class="btn-primary mt-4">重试</button>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted, computed } from 'vue'
import { useRoute } from 'vue-router'
import { useTranscriptionStore } from '@/stores/transcription'
import { getSession, exportSession, summarizeSession } from '@/services/api'
import { renderMarkdown } from '@/utils/markdown'
import { getSpeakerColor, formatDate, formatDuration, formatTime } from '@/utils/speaker'

const route = useRoute()
const store = useTranscriptionStore()

const session = ref(null)
const loading = ref(false)
const showExportMenu = ref(false)

const isProcessing = ref(false)
const aiResponse = ref('')
const customQuestion = ref('')

// Markdown 渲染
const aiHtml = computed(() => renderMarkdown(aiResponse.value))
const aiSummaryHtml = computed(() => renderMarkdown(session.value?.ai_summary || ''))
const aiActionItemsHtml = computed(() => renderMarkdown(session.value?.ai_action_items || ''))

async function loadSession() {
  loading.value = true
  try {
    const sessionId = route.params.id
    session.value = await getSession(sessionId)
  } catch (error) {
    console.error('Failed to load session:', error)
    alert('加载会话失败: ' + error.message)
  } finally {
    loading.value = false
  }
}

function exportFile(format) {
  exportSession(session.value.session_id, format)
  showExportMenu.value = false
}

function getStatusText(status) {
  const statusMap = {
    active: '进行中',
    stopped: '已停止',
    completed: '已完成'
  }
  return statusMap[status] || status
}

async function summarize() {
  await processRequest('请总结以下会议内容的要点，以清晰的列表形式呈现：')
}

async function extractActionItems() {
  await processRequest('请从以下会议内容中提取所有的待办事项、行动项和决策：')
}

async function askCustomQuestion() {
  if (!customQuestion.value.trim()) return
  await processRequest(customQuestion.value)
  customQuestion.value = ''
}

async function processRequest(prompt) {
  if (!store.openaiConfig.api_key) {
    alert('请先在主页配置 OpenAI API')
    return
  }

  isProcessing.value = true
  aiResponse.value = ''

  try {
    const generator = summarizeSession(
      session.value.session_id,
      store.openaiConfig,
      prompt
    )

    for await (const chunk of generator) {
      aiResponse.value += chunk
    }
  } catch (error) {
    console.error('AI processing error:', error)
    aiResponse.value = `错误: ${error.message}`
  } finally {
    isProcessing.value = false
  }
}

onMounted(() => {
  loadSession()
})
</script>
