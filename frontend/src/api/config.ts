export const APISettings = {
    baseURL: import.meta.env.VITE_BASE_URL || 'http://127.0.0.1:8000',
    headers: {
      'Content-Type': 'application/json',
      Accept: 'application/json'
    }
  }
  
  export const CATEGORIES_PREFIX = '/categories'
  export const VIDEOS_PREFIX = '/videos'