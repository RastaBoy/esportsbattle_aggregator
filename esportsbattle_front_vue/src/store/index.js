import Vue from 'vue'
import Vuex from 'vuex'

import api from './modules/api'
import matches from './modules/matches'

Vue.use(Vuex)

export default new Vuex.Store({
  state: {
  },
  getters: {
  },
  mutations: {
  },
  actions: {
  },
  modules: {
    api,
    matches,
  }
})
