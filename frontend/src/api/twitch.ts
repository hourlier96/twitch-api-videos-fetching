import api from '@/helpers/axios-wrapper.ts'
import { VIDEOS_PREFIX, CATEGORIES_PREFIX } from '@/api/config.ts'

export async function getCategories(params: object) {
  return await api.get(`${CATEGORIES_PREFIX}`, params)
}

export async function getVideos(params: object) {
    return await api.get(`${VIDEOS_PREFIX}`, params)
  }