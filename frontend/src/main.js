import { createApp } from 'vue'
import App from './pages/App.vue'
import router from './router'
import '@fortawesome/fontawesome-free/css/all.css';
import './assets/styles.css'

const app = createApp(App)
app.use(router);
app.mount('#app')
