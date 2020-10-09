import Vue from 'vue'
import Vuex from 'vuex'

Vue.use(Vuex)

export default new Vuex.Store({
  state: {
    username: '',
    isLogin: false,
    //新加的 -zxl
    currentPath: '/',
    user: null,
  },
  getters: {
    getIslogin(state) {
      return state.isLogin
    },
    getUsername(state) {
      return state.username
    },
  },
  mutations: {
    hasLogin(state, loginName) {
      state.username = String(loginName);
      state.isLogin = true;
      console.log("user: " + state.username)
    },
    hasLogout(state) {
      state.isLogin = false;
    },
    //新加 -zxl
    currentPath (state, path) {
      state.currentPath = path;
    },
    user (state, user) {
      state.user = user;
    }
  },
  actions: {
  },
  modules: {
  }
})
