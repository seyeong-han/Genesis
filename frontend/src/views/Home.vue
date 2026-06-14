<template>
  <div class="home-container">
    <!-- 顶部导航栏 -->
    <nav class="navbar">
      <div class="nav-brand">GENESIS</div>
      <div class="nav-links">
        <span class="nav-tagline">{{ $t('home.tagline') }}</span>
        <a href="https://github.com/seyeong-han/Genesis" target="_blank" class="github-link">
          {{ $t('nav.visitGithub') }} <span class="arrow">↗</span>
        </a>
      </div>
    </nav>

    <div class="main-content">
      <!-- 上半部分：Hero 区域 -->
      <section class="hero-section">
        <div class="hero-left">
          <div class="tag-row">
            <span class="orange-tag">{{ $t('home.tagline') }}</span>
            <span class="version-text">{{ $t('home.version') }}</span>
          </div>
          
          <h1 class="main-title">
            {{ $t('home.heroTitle1') }}<br>
            <span class="gradient-text">{{ $t('home.heroTitle2') }}</span>
          </h1>
          
          <div class="hero-desc">
            <p>
              <i18n-t keypath="home.heroDesc" tag="span">
                <template #brand><span class="highlight-bold">{{ $t('home.heroDescBrand') }}</span></template>
                <template #agentScale><span class="highlight-orange">{{ $t('home.heroDescAgentScale') }}</span></template>
                <template #optimalSolution><span class="highlight-code">{{ $t('home.heroDescOptimalSolution') }}</span></template>
              </i18n-t>
            </p>
            <p class="slogan-text">
              {{ $t('home.slogan') }}<span class="blinking-cursor">_</span>
            </p>
          </div>
           
          <div class="decoration-square"></div>
        </div>
        
        <div class="hero-right">
          <!-- Logo 区域 -->
          <div class="logo-container">
            <img src="../assets/logo/genesis_logo.png" alt="Genesis" class="hero-logo" />
          </div>
          
          <button class="scroll-down-btn" @click="scrollToBottom">
            ↓
          </button>
        </div>
      </section>

      <!-- 下半部分：双栏布局 -->
      <section class="dashboard-section">
        <!-- 左栏：状态与步骤 -->
        <div class="left-panel">
          <div class="panel-header">
            <span class="status-dot">■</span> {{ $t('home.systemStatus') }}
          </div>
          
          <h2 class="section-title">{{ $t('home.systemReady') }}</h2>
          <p class="section-desc">
            {{ $t('home.systemReadyDesc') }}
          </p>
          
          <!-- 数据指标卡片 -->
          <div class="metrics-row">
            <div class="metric-card">
              <div class="metric-value">{{ $t('home.metricLowCost') }}</div>
              <div class="metric-label">{{ $t('home.metricLowCostDesc') }}</div>
            </div>
            <div class="metric-card">
              <div class="metric-value">{{ $t('home.metricHighAvail') }}</div>
              <div class="metric-label">{{ $t('home.metricHighAvailDesc') }}</div>
            </div>
          </div>

          <!-- 项目模拟步骤介绍 (新增区域) -->
          <div class="steps-container">
            <div class="steps-header">
               <span class="diamond-icon">◇</span> {{ $t('home.workflowSequence') }}
            </div>
            <div class="workflow-list">
              <div class="workflow-item">
                <span class="step-num">01</span>
                <div class="step-info">
                  <div class="step-title">{{ $t('home.step01Title') }}</div>
                  <div class="step-desc">{{ $t('home.step01Desc') }}</div>
                </div>
              </div>
              <div class="workflow-item">
                <span class="step-num">02</span>
                <div class="step-info">
                  <div class="step-title">{{ $t('home.step02Title') }}</div>
                  <div class="step-desc">{{ $t('home.step02Desc') }}</div>
                </div>
              </div>
              <div class="workflow-item">
                <span class="step-num">03</span>
                <div class="step-info">
                  <div class="step-title">{{ $t('home.step03Title') }}</div>
                  <div class="step-desc">{{ $t('home.step03Desc') }}</div>
                </div>
              </div>
              <div class="workflow-item">
                <span class="step-num">04</span>
                <div class="step-info">
                  <div class="step-title">{{ $t('home.step04Title') }}</div>
                  <div class="step-desc">{{ $t('home.step04Desc') }}</div>
                </div>
              </div>
              <div class="workflow-item">
                <span class="step-num">05</span>
                <div class="step-info">
                  <div class="step-title">{{ $t('home.step05Title') }}</div>
                  <div class="step-desc">{{ $t('home.step05Desc') }}</div>
                </div>
              </div>
            </div>
          </div>
        </div>

        <!-- 右栏：交互控制台 -->
        <div class="right-panel">
          <div class="console-box">
            <!-- One-click example -->
            <div class="example-banner">
              <div class="example-text">
                <span class="example-tag">EXAMPLE</span>
                <span class="example-desc">Engineering CRISPR-Cas — biology × transformers × cosmology × philosophy</span>
              </div>
              <button
                class="example-btn"
                @click="loadExample"
                :disabled="loadingExample || loading"
              >
                {{ loadingExample ? 'Loading…' : 'Try this →' }}
              </button>
            </div>

            <!-- Seed source -->
            <div class="console-section">
              <div class="console-header">
                <span class="console-label">{{ $t('home.realitySeed') }}</span>
                <span class="console-meta">{{ $t('home.supportedFormats') }}</span>
              </div>

              <!-- Seed mode tabs -->
              <div class="seed-tabs">
                <button
                  v-for="m in ['upload', 'paper', 'author']"
                  :key="m"
                  class="seed-tab"
                  :class="{ active: seedMode === m }"
                  @click="seedMode = m"
                >
                  {{ { upload: $t('home.seedModeUpload'), paper: $t('home.seedModePaper'), author: $t('home.seedModeAuthor') }[m] }}
                </button>
              </div>

              <!-- Upload mode -->
              <div
                v-if="seedMode === 'upload'"
                class="upload-zone"
                :class="{ 'drag-over': isDragOver, 'has-files': files.length > 0 }"
                @dragover.prevent="handleDragOver"
                @dragleave.prevent="handleDragLeave"
                @drop.prevent="handleDrop"
                @click="triggerFileInput"
              >
                <input
                  ref="fileInput"
                  type="file"
                  multiple
                  accept=".pdf,.md,.txt"
                  @change="handleFileSelect"
                  style="display: none"
                  :disabled="loading"
                />

                <div v-if="files.length === 0" class="upload-placeholder">
                  <div class="upload-icon">↑</div>
                  <div class="upload-title">{{ $t('home.dragToUpload') }}</div>
                  <div class="upload-hint">{{ $t('home.orBrowse') }}</div>
                </div>

                <div v-else class="file-list">
                  <div v-for="(file, index) in files" :key="index" class="file-item">
                    <span class="file-icon">📄</span>
                    <span class="file-name">{{ file.name }}</span>
                    <button @click.stop="removeFile(index)" class="remove-btn">×</button>
                  </div>
                </div>
              </div>

              <!-- OpenAlex search mode (paper / author) -->
              <div v-else class="search-zone">
                <div class="search-bar">
                  <input
                    v-model="searchQuery"
                    class="search-input"
                    :placeholder="seedMode === 'paper' ? $t('home.searchPapersPlaceholder') : $t('home.searchAuthorsPlaceholder')"
                    @keyup.enter="runSearch"
                    :disabled="searching"
                  />
                  <button class="search-btn" @click="runSearch" :disabled="searching || !searchQuery.trim()">
                    {{ searching ? $t('home.searching') : $t('home.searchBtn') }}
                  </button>
                </div>

                <div class="search-results">
                  <div v-if="searchError" class="search-empty">{{ searchError }}</div>
                  <div v-else-if="!searching && searchResults.length === 0 && hasSearched" class="search-empty">
                    {{ $t('home.noResults') }}
                  </div>

                  <!-- Paper results -->
                  <template v-if="seedMode === 'paper'">
                    <div v-for="r in searchResults" :key="r.id" class="result-item">
                      <div class="result-main">
                        <div class="result-title">{{ r.title }}</div>
                        <div class="result-meta">
                          {{ r.lead_author }} · {{ r.year || '—' }} · {{ $t('home.citedBy', { count: r.cited_by_count }) }}
                        </div>
                      </div>
                      <button class="add-btn" :disabled="isSeedAdded(r.id)" @click="addPaperSeed(r)">
                        {{ isSeedAdded(r.id) ? $t('home.added') : $t('home.addSeed') }}
                      </button>
                    </div>
                  </template>

                  <!-- Author results -->
                  <template v-else>
                    <div v-for="r in searchResults" :key="r.id" class="result-item">
                      <div class="result-main">
                        <div class="result-title">{{ r.name }}</div>
                        <div class="result-meta">
                          {{ r.institution || '—' }} · {{ $t('home.worksCount', { count: r.works_count }) }} · {{ $t('home.citedBy', { count: r.cited_by_count }) }}
                        </div>
                      </div>
                      <button class="add-btn" :disabled="isSeedAdded(r.id) || addingAuthor === r.id" @click="addAuthorSeed(r)">
                        {{ isSeedAdded(r.id) ? $t('home.added') : (addingAuthor === r.id ? $t('home.searching') : $t('home.viewWorks')) }}
                      </button>
                    </div>
                  </template>
                </div>

                <!-- Selected seeds -->
                <div v-if="seeds.length > 0" class="selected-seeds">
                  <div class="selected-label">{{ $t('home.selectedSeeds') }} ({{ seeds.length }})</div>
                  <div v-for="(s, i) in seeds" :key="s.id" class="file-item seed-item">
                    <span class="file-icon">{{ s.kind === 'author' ? '🧠' : '📄' }}</span>
                    <span class="file-name">{{ s.label }}</span>
                    <button @click.stop="removeSeed(i)" class="remove-btn">×</button>
                  </div>
                </div>
              </div>
            </div>

            <!-- 分割线 -->
            <div class="console-divider">
              <span>{{ $t('home.inputParams') }}</span>
            </div>

            <!-- 输入区域 -->
            <div class="console-section">
              <div class="console-header">
                <span class="console-label">{{ $t('home.simulationPrompt') }}</span>
              </div>
              <div class="input-wrapper">
                <textarea
                  v-model="formData.simulationRequirement"
                  class="code-input"
                  :placeholder="$t('home.promptPlaceholder')"
                  rows="6"
                  :disabled="loading"
                ></textarea>
                <div class="model-badge">{{ $t('home.engineBadge') }}</div>
              </div>
            </div>

            <!-- 启动按钮 -->
            <div class="console-section btn-section">
              <button 
                class="start-engine-btn"
                @click="startSimulation"
                :disabled="!canSubmit || loading"
              >
                <span v-if="!loading">{{ $t('home.startEngine') }}</span>
                <span v-else>{{ $t('home.initializing') }}</span>
                <span class="btn-arrow">→</span>
              </button>
            </div>
          </div>
        </div>
      </section>

      <!-- 历史项目数据库 -->
      <HistoryDatabase />
    </div>
  </div>
</template>

<script setup>
import { ref, computed } from 'vue'
import { useRouter } from 'vue-router'
import HistoryDatabase from '../components/HistoryDatabase.vue'
import { searchOpenAlex, getAuthorWorks } from '../api/graph'

const router = useRouter()

// 表单数据
const formData = ref({
  simulationRequirement: ''
})

// 文件列表
const files = ref([])

// 状态
const loading = ref(false)
const error = ref('')
const isDragOver = ref(false)

// 文件输入引用
const fileInput = ref(null)

// --- Seed source mode: upload | paper | author ---
const seedMode = ref('upload')

// OpenAlex search state
const searchQuery = ref('')
const searching = ref(false)
const searchResults = ref([])
const searchError = ref('')
const hasSearched = ref(false)
const addingAuthor = ref(null)

// Selected OpenAlex seeds: { id, kind, label, text }
const seeds = ref([])

// --- One-click demo example: CRISPR-Cas engineering across 4 disciplines ---
const loadingExample = ref(false)
const EXAMPLE = {
  question:
    'What is the most promising strategy for engineering CRISPR-Cas systems with ' +
    'higher precision and programmability? Have a CRISPR biologist, a transformer / ' +
    'sequence-modeling researcher, a cosmologist focused on entropy and the origin of ' +
    'order, and a philosopher of science debate whether better Cas engineering will come ' +
    'primarily from AI-driven sequence design, from thermodynamic and physical ' +
    'constraints, from biological mechanism, or from rethinking what "precision" even ' +
    'means — and converge on one novel, testable hypothesis.',
  // Hardcoded OpenAlex author ids to avoid name-collision at demo time.
  authors: [
    { id: 'A5067184382', name: 'Jennifer A. Doudna', institution: 'UC Berkeley (QB3)', cited_by_count: 118812, works_count: 667 },
    { id: 'A5103024730', name: 'Ashish Vaswani', institution: 'Google', cited_by_count: 12446, works_count: 63 },
    { id: 'A5014894861', name: 'Roger Penrose', institution: 'University of Oxford', cited_by_count: 53918, works_count: 430 },
    { id: 'A5026171189', name: 'Nancy Cartwright', institution: 'Durham University', cited_by_count: 19679, works_count: 296 },
  ],
}

const loadExample = async () => {
  if (loadingExample.value || loading.value) return
  loadingExample.value = true
  searchError.value = ''
  try {
    formData.value.simulationRequirement = EXAMPLE.question
    seedMode.value = 'author'
    for (const a of EXAMPLE.authors) {
      if (isSeedAdded(a.id)) continue
      try {
        const res = await getAuthorWorks(a.id, 3)
        const works = res.results || []
        let text =
          `RESEARCHER SEED\nName: ${a.name}\nInstitution: ${a.institution || 'n/a'}\n` +
          `Total citations: ${a.cited_by_count}\nWorks: ${a.works_count}\nOpenAlex: ${a.id}\n\nTop works:\n`
        works.forEach((w, i) => {
          text += `\n[${i + 1}] ${w.title} (${w.year || 'n/a'}, cited ${w.cited_by_count})\n${w.abstract || '(no abstract)'}\n`
        })
        seeds.value.push({ id: a.id, kind: 'author', label: a.name, text })
      } catch (e) {
        // Skip a failed author but keep the rest of the example usable.
      }
    }
  } finally {
    loadingExample.value = false
  }
}

// 计算属性:是否可以提交
const canSubmit = computed(() => {
  return formData.value.simulationRequirement.trim() !== '' &&
    (files.value.length > 0 || seeds.value.length > 0)
})

const isSeedAdded = (id) => seeds.value.some(s => s.id === id)

const removeSeed = (index) => {
  seeds.value.splice(index, 1)
}

const runSearch = async () => {
  const q = searchQuery.value.trim()
  if (!q || searching.value) return
  searching.value = true
  searchError.value = ''
  hasSearched.value = true
  searchResults.value = []
  try {
    const type = seedMode.value === 'author' ? 'authors' : 'works'
    const res = await searchOpenAlex(type, q)
    searchResults.value = res.results || []
  } catch (e) {
    searchError.value = (e && e.message) ? e.message : 'Search failed'
  } finally {
    searching.value = false
  }
}

const addPaperSeed = (r) => {
  if (isSeedAdded(r.id)) return
  const text =
    `PAPER SEED\nTitle: ${r.title}\nAuthor: ${r.lead_author}\n` +
    `Year: ${r.year || 'n/a'}\nCitations: ${r.cited_by_count}\n` +
    `DOI: ${r.doi || 'n/a'}\nOpenAlex: ${r.id}\n\nAbstract:\n${r.abstract || '(no abstract available)'}\n`
  seeds.value.push({ id: r.id, kind: 'paper', label: r.title, text })
}

const addAuthorSeed = async (r) => {
  if (isSeedAdded(r.id) || addingAuthor.value) return
  addingAuthor.value = r.id
  try {
    const res = await getAuthorWorks(r.id, 3)
    const works = res.results || []
    let text =
      `RESEARCHER SEED\nName: ${r.name}\nInstitution: ${r.institution || 'n/a'}\n` +
      `Total citations: ${r.cited_by_count}\nWorks: ${r.works_count}\nOpenAlex: ${r.id}\n\nTop works:\n`
    works.forEach((w, i) => {
      text += `\n[${i + 1}] ${w.title} (${w.year || 'n/a'}, cited ${w.cited_by_count})\n${w.abstract || '(no abstract)'}\n`
    })
    seeds.value.push({ id: r.id, kind: 'author', label: r.name, text })
  } catch (e) {
    searchError.value = (e && e.message) ? e.message : 'Failed to load works'
  } finally {
    addingAuthor.value = null
  }
}

// Convert selected OpenAlex seeds into in-memory .txt File objects
const seedsToFiles = () => {
  return seeds.value.map((s) => {
    const safe = (s.label || 'seed').replace(/[^\w\- ]+/g, '').slice(0, 50).trim() || 'seed'
    return new File([s.text], `${s.kind}_${safe}.txt`, { type: 'text/plain' })
  })
}

// 触发文件选择
const triggerFileInput = () => {
  if (!loading.value) {
    fileInput.value?.click()
  }
}

// 处理文件选择
const handleFileSelect = (event) => {
  const selectedFiles = Array.from(event.target.files)
  addFiles(selectedFiles)
}

// 处理拖拽相关
const handleDragOver = (e) => {
  if (!loading.value) {
    isDragOver.value = true
  }
}

const handleDragLeave = (e) => {
  isDragOver.value = false
}

const handleDrop = (e) => {
  isDragOver.value = false
  if (loading.value) return
  
  const droppedFiles = Array.from(e.dataTransfer.files)
  addFiles(droppedFiles)
}

// 添加文件
const addFiles = (newFiles) => {
  const validFiles = newFiles.filter(file => {
    const ext = file.name.split('.').pop().toLowerCase()
    return ['pdf', 'md', 'txt'].includes(ext)
  })
  files.value.push(...validFiles)
}

// 移除文件
const removeFile = (index) => {
  files.value.splice(index, 1)
}

// 滚动到底部
const scrollToBottom = () => {
  window.scrollTo({
    top: document.body.scrollHeight,
    behavior: 'smooth'
  })
}

// 开始模拟 - 立即跳转，API调用在Process页面进行
const startSimulation = () => {
  if (!canSubmit.value || loading.value) return
  
  // Combine uploaded files with OpenAlex seed documents
  const combinedFiles = [...files.value, ...seedsToFiles()]

  // 存储待上传的数据
  import('../store/pendingUpload.js').then(({ setPendingUpload }) => {
    setPendingUpload(combinedFiles, formData.value.simulationRequirement)
    
    // 立即跳转到Process页面（使用特殊标识表示新建项目）
    router.push({
      name: 'Process',
      params: { projectId: 'new' }
    })
  })
}
</script>

<style scoped>
/* 全局变量与重置 */
:root {
  --black: #000000;
  --white: #FFFFFF;
  --orange: #FF4500;
  --gray-light: #F5F5F5;
  --gray-text: #666666;
  --border: #E5E5E5;
  /* 
    使用 Space Grotesk 作为主要标题字体，JetBrains Mono 作为代码/标签字体
    确保已在 index.html 引入这些 Google Fonts 
  */
  --font-mono: 'JetBrains Mono', monospace;
  --font-sans: 'Space Grotesk', 'Noto Sans SC', system-ui, sans-serif;
  --font-cn: 'Noto Sans SC', system-ui, sans-serif;
}

.home-container {
  min-height: 100vh;
  background: var(--white);
  font-family: var(--font-sans);
  color: var(--black);
}

/* 顶部导航 */
.navbar {
  height: 60px;
  background: var(--black);
  color: var(--white);
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 0 40px;
}

.nav-brand {
  font-family: var(--font-mono);
  font-weight: 800;
  letter-spacing: 1px;
  font-size: 1.2rem;
}

.nav-links {
  display: flex;
  align-items: center;
  gap: 16px;
}

.github-link {
  color: var(--white);
  text-decoration: none;
  font-family: var(--font-mono);
  font-size: 0.9rem;
  font-weight: 500;
  display: flex;
  align-items: center;
  gap: 8px;
  transition: opacity 0.2s;
}

.github-link:hover {
  opacity: 0.8;
}

.arrow {
  font-family: sans-serif;
}

/* 主要内容区 */
.main-content {
  max-width: 1400px;
  margin: 0 auto;
  padding: 60px 40px;
}

/* Hero 区域 */
.hero-section {
  display: flex;
  justify-content: space-between;
  margin-bottom: 80px;
  position: relative;
}

.hero-left {
  flex: 1;
  padding-right: 60px;
}

.tag-row {
  display: flex;
  align-items: center;
  gap: 15px;
  margin-bottom: 25px;
  font-family: var(--font-mono);
  font-size: 0.8rem;
}

.orange-tag {
  background: var(--orange);
  color: var(--white);
  padding: 4px 10px;
  font-weight: 700;
  letter-spacing: 1px;
  font-size: 0.75rem;
}

.version-text {
  color: #999;
  font-weight: 500;
  letter-spacing: 0.5px;
}

.main-title {
  font-size: 4.5rem;
  line-height: 1.2;
  font-weight: 500;
  margin: 0 0 40px 0;
  letter-spacing: -2px;
  color: var(--black);
}

.gradient-text {
  background: linear-gradient(90deg, #000000 0%, #444444 100%);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  display: inline-block;
}

.hero-desc {
  font-size: 1.05rem;
  line-height: 1.8;
  color: var(--gray-text);
  max-width: 640px;
  margin-bottom: 50px;
  font-weight: 400;
  text-align: justify;
}

.hero-desc p {
  margin-bottom: 1.5rem;
}

.highlight-bold {
  color: var(--black);
  font-weight: 700;
}

.highlight-orange {
  color: var(--orange);
  font-weight: 700;
  font-family: var(--font-mono);
}

.highlight-code {
  background: rgba(0, 0, 0, 0.05);
  padding: 2px 6px;
  border-radius: 2px;
  font-family: var(--font-mono);
  font-size: 0.9em;
  color: var(--black);
  font-weight: 600;
}

.slogan-text {
  font-size: 1.2rem;
  font-weight: 520;
  color: var(--black);
  letter-spacing: 1px;
  border-left: 3px solid var(--orange);
  padding-left: 15px;
  margin-top: 20px;
}

.blinking-cursor {
  color: var(--orange);
  animation: blink 1s step-end infinite;
  font-weight: 700;
}

@keyframes blink {
  0%, 100% { opacity: 1; }
  50% { opacity: 0; }
}

.decoration-square {
  width: 16px;
  height: 16px;
  background: var(--orange);
}

.hero-right {
  flex: 1.1;
  display: flex;
  flex-direction: column;
  justify-content: space-between;
  align-items: flex-end;
}

.logo-container {
  width: 100%;
  display: flex;
  justify-content: flex-end;
  padding-right: 16px;
}

.hero-logo {
  max-width: 720px; /* 调整logo大小 */
  width: 100%;
}

.scroll-down-btn {
  width: 40px;
  height: 40px;
  border: 1px solid var(--border);
  background: transparent;
  display: flex;
  align-items: center;
  justify-content: center;
  cursor: pointer;
  color: var(--orange);
  font-size: 1.2rem;
  transition: all 0.2s;
}

.scroll-down-btn:hover {
  border-color: var(--orange);
}

/* Dashboard 双栏布局 */
.dashboard-section {
  display: flex;
  gap: 60px;
  border-top: 1px solid var(--border);
  padding-top: 60px;
  align-items: flex-start;
}

.dashboard-section .left-panel,
.dashboard-section .right-panel {
  display: flex;
  flex-direction: column;
}

/* 左侧面板 */
.left-panel {
  flex: 0.8;
}

.panel-header {
  font-family: var(--font-mono);
  font-size: 0.8rem;
  color: #999;
  display: flex;
  align-items: center;
  gap: 8px;
  margin-bottom: 20px;
}

.status-dot {
  color: var(--orange);
  font-size: 0.8rem;
}

.section-title {
  font-size: 2rem;
  font-weight: 520;
  margin: 0 0 15px 0;
}

.section-desc {
  color: var(--gray-text);
  margin-bottom: 25px;
  line-height: 1.6;
}

.metrics-row {
  display: flex;
  gap: 20px;
  margin-bottom: 15px;
}

.metric-card {
  border: 1px solid var(--border);
  padding: 20px 30px;
  min-width: 150px;
}

.metric-value {
  font-family: var(--font-mono);
  font-size: 1.8rem;
  font-weight: 520;
  margin-bottom: 5px;
}

.metric-label {
  font-size: 0.85rem;
  color: #999;
}

/* 项目模拟步骤介绍 */
.steps-container {
  border: 1px solid var(--border);
  padding: 30px;
  position: relative;
}

.steps-header {
  font-family: var(--font-mono);
  font-size: 0.8rem;
  color: #999;
  margin-bottom: 25px;
  display: flex;
  align-items: center;
  gap: 8px;
}

.diamond-icon {
  font-size: 1.2rem;
  line-height: 1;
}

.workflow-list {
  display: flex;
  flex-direction: column;
  gap: 20px;
}

.workflow-item {
  display: flex;
  align-items: flex-start;
  gap: 20px;
}

.step-num {
  font-family: var(--font-mono);
  font-weight: 700;
  color: var(--black);
  opacity: 0.3;
}

.step-info {
  flex: 1;
}

.step-title {
  font-weight: 520;
  font-size: 1rem;
  margin-bottom: 4px;
}

.step-desc {
  font-size: 0.85rem;
  color: var(--gray-text);
}

/* 右侧交互控制台 */
.right-panel {
  flex: 1.2;
}

.console-box {
  border: 1px solid #CCC; /* 外部实线 */
  padding: 8px; /* 内边距形成双重边框感 */
}

/* One-click example banner */
.example-banner {
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 14px;
  margin: 12px 12px 0;
  padding: 14px 16px;
  background: #FFF1EA;
  border: 1px solid #FF4500;
}

.example-text {
  display: flex;
  align-items: center;
  gap: 12px;
  min-width: 0;
}

.example-tag {
  flex-shrink: 0;
  background: #FF4500;
  color: #FFFFFF;
  font-family: 'JetBrains Mono', monospace;
  font-size: 0.7rem;
  font-weight: 800;
  letter-spacing: 0.5px;
  padding: 4px 9px;
}

.example-desc {
  font-family: 'JetBrains Mono', monospace;
  font-size: 0.82rem;
  font-weight: 600;
  color: #1A1A1A;
  line-height: 1.4;
}

.example-btn {
  flex-shrink: 0;
  border: 1px solid #FF4500;
  background: #FF4500;
  color: #FFFFFF;
  padding: 10px 18px;
  font-family: 'JetBrains Mono', monospace;
  font-size: 0.85rem;
  font-weight: 800;
  cursor: pointer;
  transition: all 0.2s;
  white-space: nowrap;
}

.example-btn:hover:not(:disabled) {
  background: #1A1A1A;
  border-color: #1A1A1A;
}

.example-btn:disabled {
  background: #E5E5E5;
  border-color: #E5E5E5;
  color: #999;
  cursor: not-allowed;
}

.console-section {
  padding: 20px;
}

.console-section.btn-section {
  padding-top: 0;
}

.console-header {
  display: flex;
  justify-content: space-between;
  margin-bottom: 15px;
  font-family: var(--font-mono);
  font-size: 0.75rem;
  color: #666;
}

/* Seed mode tabs */
.seed-tabs {
  display: flex;
  gap: 4px;
  margin-bottom: 12px;
  background: #F5F5F5;
  padding: 4px;
  border-radius: 6px;
}

.seed-tab {
  flex: 1;
  border: none;
  background: transparent;
  padding: 8px 10px;
  font-family: var(--font-mono);
  font-size: 0.75rem;
  font-weight: 600;
  color: #777;
  border-radius: 4px;
  cursor: pointer;
  transition: all 0.2s;
}

.seed-tab.active {
  background: #FFF;
  color: #000;
  box-shadow: 0 1px 3px rgba(0,0,0,0.08);
}

/* OpenAlex search */
.search-zone {
  display: flex;
  flex-direction: column;
  gap: 12px;
}

.search-bar {
  display: flex;
  gap: 8px;
}

.search-input {
  flex: 1;
  border: 1px solid #DDD;
  background: #FAFAFA;
  padding: 12px 14px;
  font-family: var(--font-mono);
  font-size: 0.85rem;
  outline: none;
}

.search-input:focus {
  border-color: var(--orange);
}

.search-btn {
  border: 1px solid var(--black);
  background: var(--black);
  color: #FFF;
  padding: 0 18px;
  font-family: var(--font-mono);
  font-size: 0.8rem;
  font-weight: 700;
  cursor: pointer;
  transition: all 0.2s;
}

.search-btn:hover:not(:disabled) {
  background: var(--orange);
  border-color: var(--orange);
}

.search-btn:disabled {
  background: #E5E5E5;
  border-color: #E5E5E5;
  color: #999;
  cursor: not-allowed;
}

.search-results {
  max-height: 240px;
  overflow-y: auto;
  display: flex;
  flex-direction: column;
  gap: 8px;
}

.search-empty {
  font-family: var(--font-mono);
  font-size: 0.78rem;
  color: #999;
  padding: 16px 0;
  text-align: center;
}

.result-item {
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 12px;
  border: 1px solid #EEE;
  padding: 10px 12px;
  background: #FFF;
}

.result-main {
  flex: 1;
  min-width: 0;
}

.result-title {
  font-size: 0.85rem;
  font-weight: 600;
  color: var(--black);
  line-height: 1.35;
  margin-bottom: 4px;
}

.result-meta {
  font-family: var(--font-mono);
  font-size: 0.7rem;
  color: #999;
}

.add-btn {
  flex-shrink: 0;
  border: 1px solid var(--black);
  background: transparent;
  color: var(--black);
  padding: 6px 12px;
  font-family: var(--font-mono);
  font-size: 0.72rem;
  font-weight: 700;
  cursor: pointer;
  transition: all 0.2s;
}

.add-btn:hover:not(:disabled) {
  background: var(--black);
  color: #FFF;
}

.add-btn:disabled {
  border-color: #DDD;
  color: #BBB;
  cursor: default;
}

.selected-seeds {
  border-top: 1px solid #EEE;
  padding-top: 12px;
  display: flex;
  flex-direction: column;
  gap: 8px;
}

.selected-label {
  font-family: var(--font-mono);
  font-size: 0.7rem;
  color: var(--orange);
  letter-spacing: 0.5px;
}

.seed-item {
  border-color: #EEE;
}

.nav-tagline {
  font-family: var(--font-mono);
  font-size: 0.75rem;
  color: #BBB;
  letter-spacing: 0.5px;
}

.upload-zone {
  border: 1px dashed #CCC;
  height: 200px;
  overflow-y: auto;
  display: flex;
  align-items: center;
  justify-content: center;
  cursor: pointer;
  transition: all 0.3s;
  background: #FAFAFA;
}

.upload-zone.has-files {
  align-items: flex-start;
}

.upload-zone:hover {
  background: #F0F0F0;
  border-color: #999;
}

.upload-placeholder {
  text-align: center;
}

.upload-icon {
  width: 40px;
  height: 40px;
  border: 1px solid #DDD;
  display: flex;
  align-items: center;
  justify-content: center;
  margin: 0 auto 15px;
  color: #999;
}

.upload-title {
  font-weight: 500;
  font-size: 0.9rem;
  margin-bottom: 5px;
}

.upload-hint {
  font-family: var(--font-mono);
  font-size: 0.75rem;
  color: #999;
}

.file-list {
  width: 100%;
  padding: 15px;
  display: flex;
  flex-direction: column;
  gap: 10px;
}

.file-item {
  display: flex;
  align-items: center;
  background: var(--white);
  padding: 8px 12px;
  border: 1px solid #EEE;
  font-family: var(--font-mono);
  font-size: 0.85rem;
}

.file-name {
  flex: 1;
  margin: 0 10px;
}

.remove-btn {
  background: none;
  border: none;
  cursor: pointer;
  font-size: 1.2rem;
  color: #999;
}

.console-divider {
  display: flex;
  align-items: center;
  margin: 10px 0;
}

.console-divider::before,
.console-divider::after {
  content: '';
  flex: 1;
  height: 1px;
  background: #EEE;
}

.console-divider span {
  padding: 0 15px;
  font-family: var(--font-mono);
  font-size: 0.7rem;
  color: #BBB;
  letter-spacing: 1px;
}

.input-wrapper {
  position: relative;
  border: 1px solid #DDD;
  background: #FAFAFA;
}

.code-input {
  width: 100%;
  border: none;
  background: transparent;
  padding: 20px;
  font-family: var(--font-mono);
  font-size: 0.9rem;
  line-height: 1.6;
  resize: vertical;
  outline: none;
  min-height: 150px;
}

.model-badge {
  position: absolute;
  bottom: 10px;
  right: 15px;
  font-family: var(--font-mono);
  font-size: 0.7rem;
  color: #AAA;
}

.start-engine-btn {
  width: 100%;
  background: var(--black);
  color: var(--white);
  border: none;
  padding: 20px;
  font-family: var(--font-mono);
  font-weight: 700;
  font-size: 1.1rem;
  display: flex;
  justify-content: space-between;
  align-items: center;
  cursor: pointer;
  transition: all 0.3s ease;
  letter-spacing: 1px;
  position: relative;
  overflow: hidden;
}

/* 可点击状态（非禁用） */
.start-engine-btn:not(:disabled) {
  background: var(--black);
  border: 1px solid var(--black);
  animation: pulse-border 2s infinite;
}

.start-engine-btn:hover:not(:disabled) {
  background: var(--orange);
  border-color: var(--orange);
  transform: translateY(-2px);
}

.start-engine-btn:active:not(:disabled) {
  transform: translateY(0);
}

.start-engine-btn:disabled {
  background: #E5E5E5;
  color: #999;
  cursor: not-allowed;
  transform: none;
  border: 1px solid #E5E5E5;
}

/* 引导动画：微妙的边框脉冲 */
@keyframes pulse-border {
  0% { box-shadow: 0 0 0 0 rgba(0, 0, 0, 0.2); }
  70% { box-shadow: 0 0 0 6px rgba(0, 0, 0, 0); }
  100% { box-shadow: 0 0 0 0 rgba(0, 0, 0, 0); }
}

/* 响应式适配 */
@media (max-width: 1024px) {
  .dashboard-section {
    flex-direction: column;
  }
  
  .hero-section {
    flex-direction: column;
  }
  
  .hero-left {
    padding-right: 0;
    margin-bottom: 40px;
  }
  
  .hero-logo {
    max-width: 200px;
    margin-bottom: 20px;
  }
}
</style>

<style>
/* English locale adjustments (unscoped to target html[lang]) */
html[lang="en"] .main-title {
  font-size: 3.5rem;
  font-family: 'Space Grotesk', -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
  letter-spacing: -1px;
}

html[lang="en"] .hero-desc {
  text-align: left;
  font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
  letter-spacing: 0;
}

html[lang="en"] .slogan-text {
  font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
  letter-spacing: 0;
}

html[lang="en"] .tag-row {
  font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
}

html[lang="en"] .navbar .nav-links {
  font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
}

/* Left pane: system status + workflow */
html[lang="en"] .status-section {
  font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
}

html[lang="en"] .status-section .status-ready {
  font-size: 1.6rem;
}

html[lang="en"] .status-section .metric-value {
  font-family: 'Space Grotesk', -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
  font-size: 1.4rem;
}

html[lang="en"] .workflow-list .step-title {
  font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
}

html[lang="en"] .workflow-list .step-desc {
  font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif !important;
  font-size: 0.72rem !important;
  line-height: 1.4 !important;
}

html[lang="en"] .workflow-list {
  font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
}
</style>
