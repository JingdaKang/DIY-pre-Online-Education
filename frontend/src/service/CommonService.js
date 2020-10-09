import { post } from '../network/http';
import urls from '../network/urls';
import Cookies from 'js-cookie';

export let CommonService = {
  isLogin (store, t = function () {}, f = function () {}, e = function () {}) {
    let user = store.state.user;
    if (user === null) {
      let id = Cookies.get('user_id');
      let name = Cookies.get('username');
      // let token = Cookies.get('user_token');
      //let id = sessionStorage.getItem('user_id');
      //let name = sessionStorage.getItem('username');
      console.log(id);
      console.log(name);
      if (id != null) {
        user = {id, name};
        post(urls.validator).then(res => {
          console.log(res);
          res = res.data;
          if (res.code === 'ok') {
            store.commit('user', user);
            t();
          } else {
            store.commit('user', null);
            //Cookies.remove('user_id');
            //Cookies.remove('user_name');
            f();
          }
        }, err => {
          e(err);
        });
      } else {
        f();
      }
    } else {
      f();
    }
  }
};
