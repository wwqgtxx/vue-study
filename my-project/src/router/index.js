import Vue from 'vue'
import Router from 'vue-router'
import store from '../store'
import NotFoundComponent from '../components/NotFoundComponent.vue'
import Index from '../components/Index.vue'
import TestSocketio from '../components/TestSocketio.vue'
import TextShow from '../components/TextShow.vue'
import FallBack from '../components/FallBack.vue'
import Login from '../components/Login.vue'
import Register from '../components/Register.vue'
import UserSettings from '../components/UserSettings.vue'
Vue.use(Router)

const router = new Router({
  mode: 'history',
  routes: [
    {
      path: '/',
      // name: 'Index',
      component: Index,
      meta: {
        requireAuth: true,  // 添加该字段，表示进入这个路由是需要登录的
      },
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
      meta: {
        requireAuth: true,  // 添加该字段，表示进入这个路由是需要登录的
      },
      component: UserSettings
    },
    {
      path: '/1',
      name: 'TestSocketio',
      component: TestSocketio
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

export default router

router.beforeEach((to, from, next) => {
  if (to.meta.requireAuth) {  // 判断该路由是否需要登录权限
    if (store.state.username) {  // 通过vuex state获取当前的username是否存在
      next();
    }
    else {
      next({
        path: '/login',
        query: {redirect: to.fullPath}  // 将跳转的路由path作为参数，登录成功后跳转到该路由
      })
    }
  }
  else {
    next();
  }
})
