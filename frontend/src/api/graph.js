import service, { requestWithRetry } from './index'

/**
 * 生成本体（上传文档和模拟需求）
 * @param {Object} data - 包含files, simulation_requirement, project_name等
 * @returns {Promise}
 */
export function generateOntology(formData) {
  return requestWithRetry(() => 
    service({
      url: '/api/graph/ontology/generate',
      method: 'post',
      data: formData,
      headers: {
        'Content-Type': 'multipart/form-data'
      }
    })
  )
}

/**
 * 构建图谱
 * @param {Object} data - 包含project_id, graph_name等
 * @returns {Promise}
 */
export function buildGraph(data) {
  return requestWithRetry(() =>
    service({
      url: '/api/graph/build',
      method: 'post',
      data
    })
  )
}

/**
 * 查询任务状态
 * @param {String} taskId - 任务ID
 * @returns {Promise}
 */
export function getTaskStatus(taskId) {
  return service({
    url: `/api/graph/task/${taskId}`,
    method: 'get'
  })
}

/**
 * 获取图谱数据
 * @param {String} graphId - 图谱ID
 * @returns {Promise}
 */
export function getGraphData(graphId) {
  return service({
    url: `/api/graph/data/${graphId}`,
    method: 'get'
  })
}

/**
 * 获取项目信息
 * @param {String} projectId - 项目ID
 * @returns {Promise}
 */
export function getProject(projectId) {
  return service({
    url: `/api/graph/project/${projectId}`,
    method: 'get'
  })
}

/**
 * Search OpenAlex for papers (works) or researchers (authors) via backend proxy.
 * @param {String} type - 'works' | 'authors'
 * @param {String} q - search query
 * @returns {Promise}
 */
export function searchOpenAlex(type, q) {
  return service({
    url: '/api/graph/openalex/search',
    method: 'get',
    params: { type, q }
  })
}

/**
 * Fetch top-cited works for a given OpenAlex author id.
 * @param {String} authorId
 * @param {Number} perPage
 * @returns {Promise}
 */
export function getAuthorWorks(authorId, perPage = 3) {
  return service({
    url: '/api/graph/openalex/author_works',
    method: 'get',
    params: { author_id: authorId, per_page: perPage }
  })
}
