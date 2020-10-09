<template>
  <div class="page">
    <div class="white"></div>
    <div class="register">
      <h2>注册账户</h2>
      <el-col>
        <el-form :model="FormData" status-icon ref="FormData" :rules="rules">
          <el-form-item label="用户名" prop="username">
            <el-input type="text" v-model="FormData.username" placeholder="请输入用户名"></el-input>
          </el-form-item>
          <el-form-item label="密码" prop="password">
            <el-input type="password" v-model="FormData.password" placeholder="请输入密码"></el-input>
          </el-form-item>
          <el-form-item label="再次输入密码" prop="repassword">
            <el-input type="password" v-model="FormData.repassword" placeholder="请再次输入密码"></el-input>
          </el-form-item>
          <el-form-item>
            <el-button type="primary" @click="submitd('FormData')">提交</el-button>
            <el-button @click="resetForm('FormData')">重置</el-button>
          </el-form-item>
        </el-form>
        已有帐号?
        <router-link to="/forum/login" style="color: black">点击登录</router-link>
      </el-col>
    </div>
  </div>

</template>

<script>
  export default {
    name: 'Register',
    data() {
      // 检测第二次输入的密码
      var checkPassword = (rule, value, callback) => {
        if (value === '') {
          callback(new Error('请再次输入密码'))
        } else if (value !== this.FormData.password) {
          callback(new Error('两次输入的密码不一致.'))
        } else {
          callback()
        }
      }
      // 检测用户名是否已经被注册
      var dulaUsername = (rule, value, callback) => {
        // 验证用户名是否存在
        if (value.length < 3) {
          callback(new Error('你的用户名太短了！'))
        } else if (value.length > 18) {
          callback(new Error('你的用户名太长了！'))
        } else {
          this.axios.post('/forum/register?check=1', {
            check_username: value
          })
            .then(response => {
              if (response.data.is_indb === 1) {
                callback(new Error('该用户名已经被注册'))
              } else {
                callback();
              }
            })
        }
      }
      // 检测密码的长度
      var checkLen = (rule, value, callback) => {
        if (value.length < 6) {
          callback(new Error('密码长度不能小于6位'))
        } else if (value.length > 18) {
          callback(new Error('密码长度不能超过18位'))
        } else {
          callback()
        }
      }
      return {
        FormData: {
          username: "",
          password: "",
          repassword: "",
        },
        rules: {
          username: [{required: true, message: '这是必填项', trigger: 'blur'}, {validator: dulaUsername, trigger: 'blur'}],
          password: [{required: true, message: "这是必填项", trigger: 'blur'}, {validator: checkLen, trigger: 'blur'}],
          repassword: [{required: true, message: '这是必填项', trigger: 'blur'}, {validator: checkPassword, trigger: 'blur'}],
        }
      }
    },
    methods: {
      submitd: function (formdata) {
        this.$refs[formdata].validate((valid) => {
          if (valid) {
            // 成功.
            this.axios.post('/forum/register', {
              username: this.FormData.username,
              password: this.FormData.password,
            })
              .then(response => {
                if (response.data.status === 0) {
                  this.$store.commit('hasLogin', this.FormData.username)
                  window.localStorage.setItem('username', this.FormData.username)
                  this.$router.push({path: '/forum'})
                  window.location.reload()
                } else {
                  return false
                }
              })
          } else {
            return false;
          }
        });
      },
      resetForm: function (formdata) {
        this.$refs[formdata].resetFields()
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
    .register{
      margin-top: 20px;
      width: 400px;

    }
  }
</style>

