<template>
  <div class="user-tool">
    <!-- 未登录显示 -->
    <div v-if="user!=null" class="login">
      <span>欢迎，{{user}}</span>
      &nbsp
      <span><router-link to="/forum/userhome/message"
                         style="text-decoration: none;color: #409EFF">新消息({{unreadCount}})</router-link></span>
      <span class="bt-registered" @click="logout2" >退出</span>
    </div>
    <!-- div v-else class="login">
      <a class="bt-login"><router-link to="/forum/login"
                                       style="text-decoration: none; color: black">立即登录</router-link></a>
      <a class="bt-registered"><router-link to="/forum/register"
                                            style="text-decoration: none;color: white">注册</router-link></a>
    </div -->
    <!-- 登录后显示 -->

  </div>
</template>

<script>

export default {
  name: 'UserNav',
  components: {
  },
  data () {
    return{
      user: window.localStorage.getItem('username'),
      unreadCount:0,

    }
  },
  created(){
    console.log("user", typeof(window.localStorage.getItem('username')));
    if(typeof(window.localStorage.getItem('username')) != "string"  ){
      console.log("type of username", typeof(this.$cookies.get('username')))
      console.log("cookies-username", this.$cookies.get('username'))
      if(typeof(this.$cookies.get('username')) == "string"){
        console.log("已登录")
        const login_username = this.$cookies.get('username')
        const login_pw = this.$cookies.get('pw')
        this.login(login_username, login_pw)
      }
    }else{
      if(typeof(this.$cookies.get('username')) != "string"){
        window.localStorage.removeItem('username');
      }
    }

    this.getUserInfo();
  },
  methods: {
    getUserInfo() {
      console.log('name', this.user)
      this.axios.get('/forum/userinfo',{
        params: {
          user: this.user,
        }
      })
        .then((response) => {
          if (response.data.status === 0) {
            console.log('userinfo', response)
            this.unreadCount = response.data.data.user_unread_count
          }

        })
        .catch((error) => {
          console.error('获取用户信息异常', error)
        })
    },
    logout() {
      this.axios.post('/forum/logout')
        .then(response =>{
          if (response.data.status === 0) {
            this.$message({
              showClose: true,
              message: response.data.message,
              type: response.success === 0 ? 'success' : 'error',
              duration: 2000
            })
          }
        })
      window.localStorage.removeItem('username');
      this.$store.commit('hasLogout');
      this.$cookies.remove('user_id')
      this.$cookies.remove('username')
      this.$cookies.remove('type')
      this.$router.push('/Login')
      //this.$router.go(0);
    },
    logout2() {
      this.axios.post('/forum/logout')
        .then(response =>{
          if (response.data.status === 0) {
            this.$message({
              showClose: true,
              message: response.data.message,
              type: response.success === 0 ? 'success' : 'error',
              duration: 2000
            })
          }
        })
      window.localStorage.removeItem('username');
      this.$store.commit('hasLogout');
      this.$router.push('/Home')
      //this.$router.go(0);
    },
    login(login_user, login_pw){
      console.log("login_user",login_user)
      console.log("login_pw",login_pw)
      this.axios.post("/forum/login", {
        username: login_user,
        password: login_pw,
      })
        .then(response => {
          if (response.data.status === 0) {
            console.log("login")
            this.$store.commit('hasLogin', login_user)
            window.localStorage.setItem('username', login_user)
            //this.$router.push({path: "/forum"});
            window.location.reload();
          }
        })
    }
  }
}
</script>

<style scoped lang="scss">
  @import '@/common/style/base.scss';
  @import '@/common/style/mixin.scss';
  .user-tool{
    display: flex;
    justify-content: flex-end;
    width: 25%;
    padding: 0 15px;
    .login{
      font-size: 13px;
      .bt-login, .bt-registered{
        display: inline-block;
        padding: 0 12px;
        cursor: pointer;
        height: 34px;
        line-height: 34px;
        font-weight: 500;
        border-radius: 5px;
      }
      .bt-login{
        color: $theme;
        &:hover{
          background: #F3F3F3;
        }
      }
      .bt-registered{
        margin-left: 10px;
        background: $theme;
        color: white;
        transition: all .2s linear;
        &:hover{
          background: rgb(205,92,92);
        }
      }
    }
  }
</style>
