/* eslint-disable */
<template>
  <div class="login-box">
    <el-form
      :model="FormData"
      status-icon
      ref="FormData"
      :rules="rules"
      label-position="right"
      show-message>

      <span class="login-title">注册账号</span>
      <div style="margin-top: 5px"></div>
        <el-form-item label="用户名" prop="username">
          <el-input
            type="text"
            prefix-icon="el-icon-user"
            v-model="FormData.username"
            placeholder="请输入用户名"
            clearable></el-input>
        </el-form-item>
        <el-form-item label="输入密码" prop="password">
          <el-input
            type="password"
            prefix-icon="el-icon-lock"
            v-model="FormData.password"
            placeholder="请输入密码"
            show-password></el-input>
        </el-form-item>
        <el-form-item label="再次输入密码" prop="repassword">
          <el-input
            type="password"
            prefix-icon="el-icon-lock"
            v-model="FormData.repassword"
            placeholder="请再次输入密码"
            show-password></el-input>
        </el-form-item>
        <el-form-item label="邮箱" prop="email">
          <el-input
            v-model="FormData.email"
            prefix-icon="el-icon-message"
            placeholder="请输入邮箱"
            clearable></el-input>
        </el-form-item>
        <el-form-item label="账号类型">
          <el-col :span="18">
            <el-radio-group v-model="FormData.Radio">
              <el-radio label="1" border>学生</el-radio>
              <el-radio label="2" border>教师</el-radio>
            </el-radio-group>
          </el-col>
        </el-form-item>
        <el-form-item>
          <el-button type="primary" @click="submitd('FormData')" round>提交</el-button>
          <el-button @click="resetForm('FormData')" round>重置</el-button>
          <el-button @click="back" type="text" >返回
            <i class="el-icon-back"></i></el-button>
        </el-form-item>
    </el-form>

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
        // 验证用户名是否存在.  一会再写
        if (value.length < 3) {
          callback(new Error('你的用户名太短了！'))
        } else if (value.length > 18) {
          callback(new Error('你的用户名太长了！'))
        } else {
          this.$axios.post('/api/Register?select=1', {
            select_username: value
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
          email: "",
          Radio: '1',
        },
        rules: {
          username: [{required: true, message: '这是必填项！', trigger: 'blur'}, {validator: dulaUsername, trigger: 'blur'}],
          password: [{required: true, message: "这是必填项！", trigger: 'blur'}, {validator: checkLen, trigger: 'blur'}],
          repassword: [{required: true, message: '这是必填项！', trigger: 'blur'}, {validator: checkPassword, trigger: 'blur'}],
          email: [{required: true, message: "请输入邮箱地址！", trigger: 'blur'}, {type: 'email', message: '请输入正确的邮箱地址', trigger: ['blur', 'change']}]
        }
      }
    },
    methods: {
      submitd: function (formdata) {
        this.$refs[formdata].validate((valid) => {
          if (valid) {
            // 成功.
            this.$axios.post('/api/Register', {
              username: this.FormData.username,
              password: this.FormData.password,
              email: this.FormData.email,
              type: this.FormData.Radio
            })
              .then(response => {
                if (response.data.status === 0) {
                  this.$router.push({path: '/'})
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
      },
      back(){
        this.$router.push({path:'/'})
      }
    }
  }
</script>

<style scoped>
  .login-box {
    border: 1px solid #DCDFE6;
    width: 300px;
    margin: 180px auto;
    padding: 35px 35px 15px 35px;
    border-radius: 5px;
    -webkit-border-radius: 5px;
    -moz-border-radius: 5px;
    box-shadow: 0 0 25px palegreen;
  }
  .login-title {
    text-align: center;
    margin: 0 auto 40px auto;
    color: #66CD00;
    font-size: 30px;
    font-weight: bold;
  }
</style>
