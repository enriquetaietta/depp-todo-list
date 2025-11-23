import { defineNuxtPlugin } from '#app'
import Toast, { POSITION, useToast } from 'vue-toastification'
import 'vue-toastification/dist/index.css'

export default defineNuxtPlugin((nuxtApp) => {
  // Configura le opzioni di default
  const options = {
    position: POSITION.TOP_RIGHT,
    timeout: 5000,
    closeOnClick: true,
    pauseOnFocusLoss: true,
    pauseOnHover: true,
    draggable: true,
    draggablePercent: 0.6,
    showCloseButtonOnHover: false,
    hideProgressBar: false,
    closeButton: 'button',
    icon: true,
    rtl: false
  }

  // Installa il plugin
  nuxtApp.vueApp.use(Toast, options)

  // Crea un composable per usare il toast
  const toast = useToast()

  // Espone il toast globalmente
  nuxtApp.provide('toast', toast)
})