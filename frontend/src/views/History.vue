<template>
  <div class="min-h-screen bg-white">
    <!-- 头部 -->
    <header class="border-b-4 border-black bg-white">
      <div class="container mx-auto px-4 py-6">
        <div class="flex items-center justify-between">
          <div>
            <h1 class="text-3xl font-bold">历史记录</h1>
            <p class="text-sm text-gray-600 mt-1">查看和管理所有转录会话</p>
          </div>
          <button @click="$router.push('/')" class="btn-secondary">
            <svg class="w-5 h-5 inline mr-2" fill="currentColor" viewBox="0 0 20 20">
              <path fill-rule="evenodd" d="M9.707 16.707a1 1 0 01-1.414 0l-6-6a1 1 0 010-1.414l6-6a1 1 0 011.414 1.414L5.414 9H17a1 1 0 110 2H5.414l4.293 4.293a1 1 0 010 1.414z" clip-rule="evenodd"/>
            </svg>
            返回
          </button>
        </div>
      </div>
    </header>

    <!-- 主内容 -->
    <main class="container mx-auto px-4 py-8">
      <!-- 搜索和过滤 -->
      <div class="card mb-6">
        <div class="flex items-center space-x-4">
          <div class="flex-1">
            <input
              v-model="searchQuery"
              @keyup.enter="loadSessions"
              type="text"
              placeholder="搜索会话标题或内容..."
              class="input w-full"
            />
          </div>
          <button @click="loadSessions" class="btn-primary">
            <svg class="w-5 h-5 inline mr-2" fill="currentColor" viewBox="0 0 20 20">
              <path fill-rule="evenodd" d="M8 4a4 4 0 100 8 4 4 0 000-8zM2 8a6 6 0 1110.89 3.476l4.817 4.817a1 1 0 01-1.414 1.414l-4.816-4.816A6 6 0 012 8z" clip-rule="evenodd"/>
            </svg>
            搜索
          </button>
          <button
            v-if="searchQuery"
            @click="clearSearch"
            class="btn-secondary"
          >
            清除
          </button>
        </div>

        <div class="mt-4 text-sm text-gray-600">
          共 {{ total }} 个会话
        </div>
      </div>

      <!-- 加载中 -->
      <div v-if="loading" class="text-center py-12">
        <div class="loading-dots inline-block">
          <span></span>
          <span></span>
          <span></span>
        </div>
        <p class="text-gray-600 mt-4">加载中...</p>
      </div>

      <!-- 会话列表 -->
      <div v-else-if="sessions.length > 0" class="space-y-4">
        <div
          v-for="session in sessions"
          :key="session.session_id"
          class="card hover:shadow-xl transition-shadow duration-200"
        >
          <div class="flex items-start justify-between">
            <div class="flex-1">
              <!-- 标题 -->
              <div class="flex items-center mb-2">
                <h3
                  v-if="!editingSessionId || editingSessionId !== session.session_id"
                  class="text-xl font-bold cursor-pointer hover:underline"
                  @click="viewSession(session.session_id)"
                >
                  {{ session.title }}
                </h3>
                <input
                  v-else
                  v-model="editingTitle"
                  @keyup.enter="saveTitle(session.session_id)"
                  @keyup.esc="cancelEdit"
                  type="text"
                  class="input flex-1 mr-2"
                  ref="titleInput"
                />
                <button
                  v-if="!editingSessionId || editingSessionId !== session.session_id"
                  @click="startEdit(session.session_id, session.title)"
                  class="ml-2 text-gray-500 hover:text-black"
                  title="编辑标题"
                >
                  <svg class="w-5 h-5" fill="currentColor" viewBox="0 0 20 20">
                    <path d="M13.586 3.586a2 2 0 112.828 2.828l-.793.793-2.828-2.828.793-.793zM11.379 5.793L3 14.172V17h2.828l8.38-8.379-2.83-2.828z"/>
                  </svg>
                </button>
                <button
                  v-else
                  @click="saveTitle(session.session_id)"
                  class="ml-2 text-green-600 hover:text-green-800"
                  title="保存"
                >
                  <svg class="w-5 h-5" fill="currentColor" viewBox="0 0 20 20">
                    <path fill-rule="evenodd" d="M16.707 5.293a1 1 0 010 1.414l-8 8a1 1 0 01-1.414 0l-4-4a1 1 0 011.414-1.414L8 12.586l7.293-7.293a1 1 0 011.414 0z" clip-rule="evenodd"/>
                  </svg>
                </button>
              </div>

              <!-- 元数据 -->
              <div class="flex items-center space-x-4 text-sm text-gray-600 mb-3">
                <span>📅 {{ formatDate(session.created_at) }}</span>
                <span>⏱️ {{ formatDuration(session.duration_seconds) }}</span>
                <span>👥 {{ session.speaker_count }} 位发言人</span>
                <span>📝 {{ session.word_count }} 字</span>
                <span
                  :class="{
                    'text-green-600': session.status === 'completed',
                    'text-yellow-600': session.status === 'active',
                    'text-gray-600': session.status === 'stopped'
                  }"
                >
                  {{ getStatusText(session.status) }}
                </span>
              </div>

              <!-- 操作按钮 -->
              <div class="flex items-center space-x-2">
                <button
                  @click="viewSession(session.session_id)"
                  class="btn-primary text-sm"
                >
                  查看详情
                </button>
                <button
                  @click="showExportMenu(session.session_id)"
                  class="btn-secondary text-sm"
                >
                  导出
                </button>
                <button
                  @click="deleteSessionConfirm(session.session_id)"
                  class="btn-danger text-sm"
                >
                  删除
                </button>
              </div>
            </div>
          </div>

          <!-- 导出菜单 -->
          <div
            v-if="exportMenuSessionId === session.session_id"
            class="mt-4 p-4 border-2 border-black rounded-md bg-gray-50"
          >
            <p class="text-sm font-semibold mb-2">选择导出格式：</p>
            <div class="flex space-x-2">
              <button
                @click="exportSessionFile(session.session_id, 'txt')"
                class="btn-secondary text-sm"
              >
                📄 TXT
              </button>
              <button
                @click="exportSessionFile(session.session_id, 'json')"
                class="btn-secondary text-sm"
              >
                📋 JSON
              </button>
              <button
                @click="exportSessionFile(session.session_id, 'markdown')"
                class="btn-secondary text-sm"
              >
                📝 Markdown
              </button>
              <button
                @click="exportMenuSessionId = null"
                class="btn-secondary text-sm"
              >
                取消
              </button>
            </div>
          </div>
        </div>

        <!-- 分页 -->
        <div class="flex items-center justify-center space-x-4 mt-8">
          <button
            @click="previousPage"
            :disabled="currentPage === 1"
            class="btn-secondary disabled:opacity-50 disabled:cursor-not-allowed"
          >
            上一页
          </button>
          <span class="text-sm">
            第 {{ currentPage }} 页 / 共 {{ totalPages }} 页
          </span>
          <button
            @click="nextPage"
            :disabled="currentPage >= totalPages"
            class="btn-secondary disabled:opacity-50 disabled:cursor-not-allowed"
          >
            下一页
          </button>
        </div>
      </div>

      <!-- 空状态 -->
      <div v-else class="text-center py-12">
        <svg class="w-24 h-24 mx-auto text-gray-300" fill="currentColor" viewBox="0 0 20 20">
          <path fill-rule="evenodd" d="M4 3a2 2 0 00-2 2v10a2 2 0 002 2h12a2 2 0 002-2V5a2 2 0 00-2-2H4zm12 12H4l4-8 3 6 2-4 3 6z" clip-rule="evenodd"/>
        </svg>
        <p class="text-gray-600 mt-4">暂无历史记录</p>
        <button @click="$router.push('/')" class="btn-primary mt-4">
          开始新的转录
        </button>
      </div>
    </main>
  </div>
</template>

<script setup>
import { ref, computed, onMounted, nextTick } from 'vue'
import { useRouter } from 'vue-router'
import { getSessions, deleteSession, updateSessionTitle, exportSession } from '@/services/api'

const router = useRouter()

const sessions = ref([])
const loading = ref(false)
const searchQuery = ref('')
const currentPage = ref(1)
const pageSize = ref(10)
const total = ref(0)

const editingSessionId = ref(null)
const editingTitle = ref('')
const titleInput = ref(null)

const exportMenuSessionId = ref(null)

const totalPages = computed(() => Math.ceil(total.value / pageSize.value))

async function loadSessions() {
  loading.value = true
  try {
    const params = {
      skip: (currentPage.value - 1) * pageSize.value,
      limit: pageSize.value
    }

    if (searchQuery.value) {
      params.search = searchQuery.value
    }

    const data = await getSessions(params)
    sessions.value = data.sessions
    total.value = data.total
  } catch (error) {
    console.error('Failed to load sessions:', error)
    alert('加载会话失败: ' + error.message)
  } finally {
    loading.value = false
  }
}

function clearSearch() {
  searchQuery.value = ''
  currentPage.value = 1
  loadSessions()
}

function previousPage() {
  if (currentPage.value > 1) {
    currentPage.value--
    loadSessions()
  }
}

function nextPage() {
  if (currentPage.value < totalPages.value) {
    currentPage.value++
    loadSessions()
  }
}

function viewSession(sessionId) {
  router.push(`/session/${sessionId}`)
}

async function deleteSessionConfirm(sessionId) {
  if (confirm('确定要删除这个会话吗？此操作无法撤销。')) {
    try {
      await deleteSession(sessionId)
      await loadSessions()
    } catch (error) {
      console.error('Failed to delete session:', error)
      alert('删除失败: ' + error.message)
    }
  }
}

async function startEdit(sessionId, title) {
  editingSessionId.value = sessionId
  editingTitle.value = title
  await nextTick()
  if (titleInput.value) {
    titleInput.value.focus()
  }
}

function cancelEdit() {
  editingSessionId.value = null
  editingTitle.value = ''
}

async function saveTitle(sessionId) {
  if (!editingTitle.value.trim()) {
    alert('标题不能为空')
    return
  }

  try {
    await updateSessionTitle(sessionId, editingTitle.value)
    await loadSessions()
    cancelEdit()
  } catch (error) {
    console.error('Failed to update title:', error)
    alert('更新标题失败: ' + error.message)
  }
}

function showExportMenu(sessionId) {
  exportMenuSessionId.value = exportMenuSessionId.value === sessionId ? null : sessionId
}

function exportSessionFile(sessionId, format) {
  exportSession(sessionId, format)
  exportMenuSessionId.value = null
}

function formatDate(dateString) {
  const date = new Date(dateString)
  return date.toLocaleString('zh-CN', {
    year: 'numeric',
    month: '2-digit',
    day: '2-digit',
    hour: '2-digit',
    minute: '2-digit'
  })
}

function formatDuration(seconds) {
  const mins = Math.floor(seconds / 60)
  const secs = Math.floor(seconds % 60)
  return `${mins}:${secs.toString().padStart(2, '0')}`
}

function getStatusText(status) {
  const statusMap = {
    active: '进行中',
    stopped: '已停止',
    completed: '已完成'
  }
  return statusMap[status] || status
}

onMounted(() => {
  loadSessions()
})
</script>

