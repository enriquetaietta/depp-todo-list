import { useNuxtApp } from '#app'

export const useAppToast = () => {
  const nuxtApp = useNuxtApp()
  const toast = nuxtApp.$toast

  const showError = (message: string) => {
    toast.error(message, {
      timeout: 8000, // Durata più lunga per gli errori
      icon: '❌'
    })
  }

  const showSuccess = (message: string) => {
    toast.success(message, {
      timeout: 3000,
      icon: '✅'
    })
  }

  const showInfo = (message: string) => {
    toast.info(message, {
      timeout: 5000,
      icon: 'ℹ️'
    })
  }

  const clearToast = () => {
    toast.clear()
  }
  return { showError, showSuccess, showInfo, clearToast }
}