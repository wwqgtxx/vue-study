import Vue from 'vue'
import Vuex from 'vuex'
import createPersistedState from 'vuex-persistedstate'
import axios from 'axios'
import route from '../router'

Vue.use(Vuex)

const store = new Vuex.Store({
  state: {
    // count: 0,
    username: null,
    is_admin: false,
    role: "",
  },
  // getters: {
  //   double_count(state){
  //     return state.count * 2;
  //   }
  // },
  mutations: {
    // increment (state) {
    //   state.count++
    // },
    login(state, info){
      state.username = info.username
      state.is_admin = info.is_admin
      state.role = info.role
    },
    logout(state){
      state.username = null
      state.is_admin = false
    },
    change_name(state,username){
      state.username = username
    }
  },
  actions: {
    // increment (context) {
    //   setTimeout(() => {
    //     context.commit('increment')
    //   }, 1000)
    //
    // },
    async logout(context){
      try {
        let response = await axios({
          method: "post",
          url: "/api/logout/"
        })
        console.log(response.data)
        if(response.data.status === "ok"){
          context.commit('logout')
          route.push("/")
        }
      }catch(err) {
        console.log(err)
      }
    }
  },
  plugins: [createPersistedState()]
})

export default store
