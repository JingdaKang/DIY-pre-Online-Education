<template>
  <el-card class="box-card" style="width:60%;text-align: center;margin-top:100px;margin-left: 20%" v-loading="loading">
    <p style="font-size:20px;font-weight:bold">
      忘记密码
    </p>
    <el-form ref="password" :rules="rules" :model="user" label-width="100px"
             style="margin-left:10%;margin-top:80px;width:80%;padding-bottom: 15px">
      <el-form-item label="用户名" prop="username" style="margin-top: 20px">
        <el-input type="input" v-model="user.username"></el-input>
      </el-form-item>
      <el-form-item label="邮箱" prop="email" style="margin-top: 20px">
        <el-input type="email" v-model="user.email"></el-input>
      </el-form-item>

      <el-row style="text-align: center;margin-top: 20px">
        <el-button type="success" round @click="reset_password()">重置密码</el-button>
        <el-button type="info" round @click="goto_login()">返回</el-button>
      </el-row>
    </el-form>
  </el-card>
</template>

<script>
  export default {
    name: "ForgetPassword",
    data() {
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
              message:'用户名不能为空',
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
        },
      }
    },
    methods: {
      reset_password() {
        let username = this.user.username
        let email = this.user.email
        let that = this
        let param = new URLSearchParams()
        param.append('username', username)
        param.append('email', email)
        that.loading = true
        that.axios({
          method: 'post',
          url: '/api/reset_pass/',
          data: param
        })
          .then(function (res) {
            if (res.data.code === 0) {
              that.loading = false
              that.$message.error('密码重置失败')
            } else if (res.data.code === 1) {
              that.loading = false
              that.$message({
                message: '密码已重置，请前往邮箱查看',
                type: 'success'
              });
              setTimeout(function () {
                that.$router.push('/Login')
              }.bind(that), 1000)
            }
          })

      },
      goto_login(){
        this.$router.push('/Login')
      }
    }

  }
</script>

<style scoped>

</style>
