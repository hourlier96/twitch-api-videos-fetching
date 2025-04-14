import { APISettings } from '@/api/config.ts'
import { ApiError } from '@/types/errors.ts'
import axios from 'axios'

const axiosInstance = axios.create(APISettings)

export default {
  axiosInstance,
  async get(path: string, params: {}, headers: Headers | null = null) {
    const config = {
      method: 'GET',
      url: `${path}`,
      params: params
    }
    if (headers) {
      config['headers'] = headers
    }
    return await call(config, path)
  }
}

async function call(config: object, path: string) {
  try {
    return await axiosInstance(config)
  } catch (error) {
    throw new ApiError(error.message, `${APISettings.baseURL}${path}`)
  }
}