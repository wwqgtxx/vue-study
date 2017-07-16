// The Vue build version to load with the `import` command
// (runtime-only or standalone) has been set in webpack.base.conf with an alias.
import Vue from 'vue'
import App from './App.vue'
import router from './router'
import store from './store'
import './common/axios_config'

// import $ from "jquery";
import 'jquery-confirm/dist/jquery-confirm.min.css'
import 'jquery-confirm/dist/jquery-confirm.min.js'
// import 'jquery.cookie'
import 'bootstrap/dist/css/bootstrap.min.css'
import 'bootstrap/dist/js/bootstrap.min.js'

import vmodal from 'vue-js-modal'

Vue.use(vmodal)

// import {Alert, Confirm, Toast, Prompt} from 'wc-messagebox'
// import 'wc-messagebox/style.css'
//
// let options = {
//   title: '',  // 默认标题为 '提示'
//   btn: {
//     text: '',
//     style: {} // 可以通过 style 来修改按钮的样式, 比如说粗细, 颜色
//   }
// }
// Vue.use(Alert)
// Vue.use(Confirm)
// Vue.use(Toast)
// Vue.use(Prompt)

Vue.config.productionTip = false

/* eslint-disable no-new */
new Vue({
  el: '#app',
  store,
  router,
  template: '<App/>',
  components: {App}
})
