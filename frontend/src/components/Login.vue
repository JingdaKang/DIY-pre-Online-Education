<template>
  <div id="Login" v-loading="loading">
    <el-card style="margin-top: 50px;width: 70%;margin-left: 15%">
      <el-aside style="float:left;width: 50%;border-top:0;height:500px;margin: 0;">
        <el-form label-width="80px"
                 style="text-align: center;margin-top: 10px">
          <h1>在线教育管理系统</h1>
          <h3>欢迎登录</h3>
          <el-form-item label="用户名:" prop="username" style="margin-left: 10px;margin-top: 35px">
            <el-input style="width: 75%" type="text" placeholder="请输入用户名" v-model="username"/>
          </el-form-item>
          <el-form-item label="密码:" prop="password" style="margin-left: 10px;margin-top: 35px">
            <el-input style="width: 75%" type="password" placeholder="请输入密码" v-model="password" show-password/>
          </el-form-item>
          <el-form-item label="类型:" prop="type" style="margin-left: 10px;margin-top: 35px">
            <el-select style="width: 75%" v-model="type" default-first-option>
              <el-option label="学生" value="S"></el-option>
              <el-option label="教师" value="T"></el-option>
              <el-option label="管理员" value="A"></el-option>
            </el-select>
          </el-form-item>
          <el-row style="text-align: center;margin-top: 35px">
            <el-button type="primary" v-on:click="login()">登录</el-button>
            <el-button type="success" v-on:click="goto_register()">注册</el-button>
          </el-row>
          <el-row style="text-align: center;margin-top:20px">
            <a @click="reset_password()">忘记密码</a>
          </el-row>
        </el-form>
      </el-aside>
      <el-main style="overflow:hidden;float:left;width: 50%;height:480px;margin: 0;padding: 0">
        <img src="@/assets/background.jpg" style="overflow: hidden">
      </el-main>
    </el-card>
  </div>
</template>

<script>
import store from '@/store';
  export default {
    name: "Login",
    data() {
      return {
        loading: false,
        username: '',
        password: '',
        type: ''
      }
    },
    mounted: function () {
      if (this.$cookies.get('username')) {
        this.$router.push('/Home')
      }
    },
    methods: {
      login() {
        if (this.username === "" || this.password === "" || this.type === "") {
          this.$message("请输入用户名或密码并选择用户类型")
        } else {
          let that = this
          let param = new URLSearchParams()
          param.append('username', that.username)
          param.append('password', that.password)
          param.append('type', that.type)
          that.loading = true
          that.axios({
            method: 'post',
            url: '/api/login/',
            data: param
          })
            .then(function (res) {
              if (res.data.code === 1) {
                that.$message({
                  message: '登录成功',
                  type: 'success'
                });
                that.$cookies.set('user_id', res.data.id)
                that.$cookies.set('username', res.data.username)
                that.$cookies.set('pw', that.password)
                that.$cookies.set('type', res.data.type)
                localStorage.username = res.data.username
                sessionStorage.setItem('user_id', res.data.id);
                sessionStorage.setItem('username', res.data.username)
                that.loading = false
                setTimeout(function () {
                  that.$router.push('/Home')
                }.bind(that), 1000)
              } else if (res.data.code === 2) {
                that.loading = false
                that.$message.error('密码错误')
              } else if (res.data.code === 3) {
                that.loading = false
                that.$message.error('不存在该用户')
              }else if (res.data.code === 4) {
                that.loading = false
                that.$message.info('该用户已停用,请联系管理员激活')
              }
            })
        }
      },
      goto_register() {
        this.$router.push('/Register')
      },
      reset_password() {
        this.$router.push('/ForgetPassword')
      }
    }
  }
</script>

<style scoped>

</style>
