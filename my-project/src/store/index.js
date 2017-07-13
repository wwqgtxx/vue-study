import Vue from 'vue'
import Vuex from 'vuex'
import createPersistedState from 'vuex-persistedstate'

Vue.use(Vuex)

const store = new Vuex.Store({
  state: {
    count: 0
  },
  getters: {
    double_count(state){
      return state.count * 2;
    }
  },
  mutations: {
    increment (state) {
      state.count++
    }
  },
  actions: {
    increment (context) {
      setTimeout(() => {
        context.commit('increment')
      }, 1000)

    }
  },
  plugins: [createPersistedState()]
})

export default store
