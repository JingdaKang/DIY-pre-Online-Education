import { post } from '../network/http';
import urls from '../network/urls';
import Cookies from 'js-cookie';
import store from '../store';
export var UserService = {
  login (name,pw,type,t = function () {}) {

    var data = {'username':name,'password':pw,'type':type}
    post(urls.login, data).then(res => {
      console.log(res);
      res = res.data;

      if (res.code === 1) {
        let id = res.id;
        let name = res.username;
        let user = {id,name};
        sessionStorage.setItem('username', res.username);
        sessionStorage.setItem('user_id', res.id);
        store.commit('user', user);
        //console.log(this.$cookies.get('user_id'));
        //console.log(this.$store);
        console.log('登录成功');
        t();
        // Cookies.set('user_token', res.data.cn_user_token);
      }
    }, err => {
      console.log(err);
    });
  },
  register (data, success, error) {
    post(urls.register, data).then(res => {
      res = res.data;
      if (res.code === 'ok') {
        success();
      } else {
        error();
      }
    }, err => {
      console.log(err);
      error('请求错误！');
    });
  },
  checkUsername (data, success, error) {
    post(urls.checkUsername, data).then(res => {
      res = res.data;
      if (res.code === 'ok') {
        success();
      } else {
        error();
      }
    });
  },
  updatePassword (data, success, error) {
    let id = Cookies.get('user_id');
    let token = Cookies.get('user_token');
    let data2 = {
      id, token, ...data
    };
    console.log(data2);
    post(urls.updatePassword, data2).then(res => {
      res = res.data;
      if (res.status === 0) {
        success();
      } else {
        error(res.message);
      }
    }, err => {
      console.log(err);
      error('请求错误！');
    });
  },
  logout (store, callback = () => {},error = function () {}) {
    //Cookies.remove('user_id');
    //Cookies.remove('user_name');
    // Cookies.remove('user_token');
    sessionStorage.removeItem('user_id');
    sessionStorage.removeItem('username');
    post(urls.logout).then(res => {
      res = res.data;
      if (res.code === 1) {
        console.log(store.state.uesr);
        store.commit('user', null);
        callback();
      } else {
        error();
      }
    });
  }
};
