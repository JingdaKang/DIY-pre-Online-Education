//var base = 'http://localhost:8222/api'; nb!
var base = 'http://127.0.0.1:8888/api';
//var suffix = '.api';

function join (url) {
  return base + url;
}

function noteBook (url) {
  return join('/book' + url);
}

function note (url) {
  return join('/note' + url);
}

export default {
  login: join('/login/'),
  logout:join('/logout/'),
  register: join('/register/'),
  checkUsername: join('/checkUsername/'),
  validator: join('/validator/'),
  updatePassword: join('/updatePassword'),
  nb_findAll: noteBook('/findAll'),
  nb_create: noteBook('/create'),
  nb_update: noteBook('/update'),
  nb_delete: noteBook('/delete'),
  n_findAll: note('/findAll'),
  n_add: join('/note/')
};
