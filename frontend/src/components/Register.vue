<template>
  <div id="register" v-loading="loading">
    <el-card class="box-card" style="width: 60%;margin-left:20%;margin-top:30px;">
      <div slot="header" class="clearfix" style="font-size: large">
        <span><h3 class="login-title">欢迎注册</h3></span>
      </div>
      <div style="width: 60%;margin-left: 20%">
        <el-form label-width="90px"
                 class="login-box"
                 :rules="rules"
                 :model="user">
          <el-form-item label="用户名:" prop="username" style="margin-top: 35px">
            <el-input type="text" placeholder="请输入用户名" v-model="user.username"/>
          </el-form-item>
          <el-form-item label="账户类型" prop="type">
            <el-select style="float: left" v-model="user.type">
              <el-option label="学生" value="S"></el-option>
              <el-option label="教师" value="T"></el-option>
            </el-select>
          </el-form-item>
          <el-form-item label="邮箱" prop="email">
            <el-input v-model="user.email"></el-input>
          </el-form-item>
          <el-form-item label="密码:" prop="new_password1" style="margin-top: 35px">
            <el-input type="password" placeholder="请输入密码" v-model="user.new_password1" show-password/>
          </el-form-item>
          <el-form-item label="确认密码:" prop="new_password2" style="margin-top: 35px">
            <el-input type="password" placeholder="请输入密码" v-model="user.new_password2" show-password/>
          </el-form-item>
          <el-row style="text-align: center;margin-top: 35px">
            <el-button type="primary" v-on:click="register()">注册</el-button>
            <el-button type="danger" @click="cancel()">取消</el-button>
          </el-row>
          <el-row style="margin-top:20px;text-align:center">
            <a @click="goto_login()">已有账号，前往登陆</a>
          </el-row>
        </el-form>
      </div>
    </el-card>
  </div>
</template>

<script>
  export default {
    name: "Register",
    data() {
      const checkUsername = (rule, value, callback) => {
        const mailReg = /^[\u4E00-\u9FA5a-zA-Z0-9_-]{4,10}$/
        if (!value) {
          return callback(new Error('用户名不能为空'))
        }
        setTimeout(() => {
          if (mailReg.test(value)) {
            callback()
          } else {
            callback(new Error('请输入4-10位用户名'))
          }
        }, 100)
      }
      const checkPassword = (rule, value, callback) => {
        const mailReg = /^.*(?=.{6,})(?=.*\d)(?=.*[A-Z])(?=.*[a-z])(?=.*[!@#$%^&*?_ ]).*$/
        if (!value) {
          return callback(new Error('密码不能为空'))
        }
        setTimeout(() => {
          if (mailReg.test(value)) {
            callback()
          } else {
            callback(new Error('6位以上密码,至少包括一个大写字母，一个小写字母，1个数字，1个特殊字符'))
          }
        }, 100)
      }
      const checkEmail = (rule, value, callback) => {
        const mailReg = /^([a-zA-Z0-9_-])+@([a-zA-Z0-9_-])+(.[a-zA-Z0-9_-])+/
        if (!value) {
          return callback(new Error('邮箱不能为空'))
        }
        setTimeout(() => {
          if (mailReg.test(value)) {
            callback()
          } else {
            callback(new Error('请输入正确的邮箱格式'))
          }
        }, 100)
      }
      return {
        loading: false,
        user: [],
        rules: {
          username: [
            {
              required: true,
              validator: checkUsername,
              trigger: 'blur'
            }
          ],
          type: [
            {
              required: true,
              message: '请选择账户类型',
              trigger: 'blur'
            }
          ],
          email: [
            {
              required: true,
              validator: checkEmail,
              trigger: 'blur'
            }
          ],
          new_password1: [
            {
              required: true,
              validator: checkPassword,
              trigger: 'blur'
            }
          ],
          new_password2: [
            {
              required: true,
              validator: checkPassword,
              trigger: 'blur'
            }
          ]
        }
      }
    },
    mounted: function () {
      if (this.$cookies.get('username')) {
        this.$router.push('/Home')
      }
    },
    methods: {
      register() {
        let that = this
        let new_password1 = that.user.new_password1
        let new_password2 = that.user.new_password2
        if (new_password1 === new_password2) {
          that.loading = true
          let param = new URLSearchParams()
          param.append('username', that.user.username)
          param.append('type', that.user.type)
          param.append('gender', that.user.gender)
          param.append('email', that.user.email)
          param.append('password', new_password1)
          that.axios({
            method: 'post',
            url: '/api/register/',
            data: param
          })
            .then(function (res) {
              if (res.data.code === 0) {
                that.loading = false
                that.$message.error('注册失败')
              } else if (res.data.code === 1) {
                that.loading = false
                that.$message({
                  message: '注册成功',
                  type: 'success'
                });
                setTimeout(function () {
                  that.$router.push('/Login')
                }.bind(that), 1000)
              } else if (res.data.code === 2) {
                that.loading = false
                that.$message.error('该用户名已存在')
              } else if (res.data.code === 3) {
                that.loading = false
                that.$message.error('该邮箱已被注册')
              }
            })
        } else {
          that.user.new_password2 = ''
          that.$message('请输入相同的新密码')
        }
      },
      goto_login() {
        this.$router.push('/Login')
      },
      cancel() {
        this.user = []
      }
    }

  }
</script>

<style scoped>

</style>
