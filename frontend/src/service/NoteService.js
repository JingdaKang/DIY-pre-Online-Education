import Cookies from 'js-cookie';
import { post } from '../network/http';
import urls from '../network/urls';

export var NoteService = {
  findAll (success, error) {
    let id = Cookies.get('user_id');
    let token = Cookies.get('user_token');
    let data = {id, token};
    post(urls.n_findAll, data).then(res => {
      res = res.data;
      if (res.status === 0) {
        success(res.data);
      } else {
        error(res.message);
      }
    }, err => {
      console.log(err);
      error('请求错误！');
    });
  },
  create (data, success, error) {
    let id = Cookies.get('user_id');
    let token = Cookies.get('user_token');
    let data2 = {id, token, ...data};
    post(urls.n_add, data2).then(res => {
      res = res.data;
      if (res.status === 0) {
        success(res.data);
      } else {
        error(res.message);
      }
    }, err => {
      console.log(err);
      error('请求错误！');
    });
  },
  update (data, success, error) {
    let id = Cookies.get('user_id');
    let token = Cookies.get('user_token');
    let data2 = {id, token, ...data};
    console.log(data2);
    post(urls.nb_update, data2).then(res => {
      res = res.data;
      if (res.status === 0) {
        success(res.data);
      } else {
        error(res.message);
      }
    }, err => {
      console.log(err);
      error('请求错误！');
    });
  },
  delete (data, success, error) {
    let id = Cookies.get('user_id');
    let token = Cookies.get('user_token');
    let data2 = {id, token, ...data};
    post(urls.nb_delete, data2).then(res => {
      res = res.data;
      if (res.status === 0) {
        success(res.data);
      } else {
        error(res.message);
      }
    }, err => {
      console.log(err);
      error('请求错误！');
    });
  }
};
