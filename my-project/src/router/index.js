import Vue from 'vue'
import Router from 'vue-router'
import Hello from '../components/Hello.vue'
import Hello2 from '../components/Hello2.vue'
import Hello3 from '../components/Hello3.vue'

Vue.use(Router)

export default new Router({
  routes: [
    {
      path: '/',
      name: 'Hello',
      component: Hello
    },
    {
      path: '/2',
      name: 'Hello2',
      component: Hello2
    },
    {
      path: '/3',
      name: 'Hello3',
      component: Hello3
    }
  ]
})
