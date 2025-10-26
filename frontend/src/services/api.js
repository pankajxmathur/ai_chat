import axios from 'axios'

const BASE_URL = '/api'

const apiService = {
  call: async (config) => {
    try {
      const response = await axios.post(`${BASE_URL}/method/${config.method}`,
        config.args || {}
      )
      return response.data
    } catch (error) {
      console.error('API Error:', error)
      throw error
    }
  },

  get: async (endpoint, params = {}) => {
    const response = await axios.get(`${BASE_URL}${endpoint}`, { params })
    return response.data
  },

  post: async (endpoint, data = {}) => {
    const response = await axios.post(`${BASE_URL}${endpoint}`, data)
    return response.data
  }
}

export default apiService
