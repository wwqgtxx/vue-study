import Vue from 'vue'
import Router from 'vue-router'
import NotFoundComponent from '../components/NotFoundComponent.vue'
import Index from '../components/Index.vue'
import TextShow from '../components/TextShow.vue'
import FallBack from '../components/FallBack.vue'
import Login from '../components/Login.vue'
import Register from '../components/Register.vue'
import UserSettings from '../components/UserSettings.vue'
Vue.use(Router)

export default new Router({
  mode: 'history',
  routes: [
    {
      path: '/',
      // name: 'Index',
      component: Index,
      children: [
        {
          path: 'page/6',
          component: FallBack
        },
        {
          path: 'page/:id',
          component: TextShow
        },
        {
          path: '',
          component: TextShow
        }
      ]
    },
    {
      path: '/login',
      name: 'Login',
      component: Login
    },
    {
      path: '/register',
      name: 'Register',
      component: Register
    },
    {
      path: '/user_settings',
      name: 'UserSettings',
      component: UserSettings
    },
    {
      path: '/1',
      name: 'Hello',
      component: Index
    },
    {
      path: '/2',
      name: 'Hello2',
      component: Index
    },
    {
      path: '/3',
      name: 'Hello3',
      component: Index
    },
    {
      path: '*',
      component: NotFoundComponent
    }
  ],
  linkActiveClass: "active"
})
