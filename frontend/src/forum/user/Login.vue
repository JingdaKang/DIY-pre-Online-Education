<template>
  <div class="page">
    <div class="white"></div>
    <div class="panel">
      <div class="login" v-loading="false">
        <h2>登录</h2>
        <el-col>
          <el-form ref="loginform" :model="loginform" label-width="80px" :rules="rules">
            <el-form-item label="用户名" prop="username">
              <el-input type="text" v-model="loginform.username" autocomplete="off" placeholder="请输入用户名"></el-input>
            </el-form-item>
            <el-form-item label="密码" prop="password">
              <el-input type="password" v-model="loginform.password" autocomplete="off" placeholder="请输入密码"></el-input>
            </el-form-item>
            <el-form-item>
              <el-button class="loginButton" type="primary" @click="submitLogin('loginform')">登录</el-button>
              &nbsp;&nbsp;没有帐号?
              <router-link to="/forum/register" style="color: black">点我注册</router-link>
            </el-form-item>
          </el-form>
        </el-col>
      </div>
    </div>
  </div>


</template>

<script>
  export default {
    name: 'login',
    data() {
      return {
        loginform: {
          username: '',
          password: ''
        },
        rules: {
          username: [
            {required: true, message: '请输入用户名!', trigger: 'blur'}
          ],
          password: [
            {required: true, message: '请输入密码!', trigger: 'blur'}
          ]
        }
      }
    },
    methods: {
      submitLogin: function (Dataset) {
        this.$refs[Dataset].validate((valid) => {
          if (valid) {
            // 成功
            this.axios.post("/forum/login", {
              username: this.loginform.username,
              password: this.loginform.password,
            })
              .then(response => {
                if (response.data.status === 0) {
                  this.$store.commit('hasLogin', this.loginform.username)
                  window.localStorage.setItem('username', this.loginform.username)
                  this.$router.push({path: "/forum"});
                  window.location.reload();
                } else {
                  this.$notify({
                    title: '登录失败',
                    message: response.data.message,
                    type: 'error'
                  })
                }
              })
          } else {
            return false;
          }
        })
      }
    }
  }
</script>

<style lang="scss" scoped>
  .page{
    display: flex;
    height: 700px;
    .white{
      width: 30%;
    }
    .login{
      margin-top: 20px;
      width: 400px;

    }
  }
</style>
