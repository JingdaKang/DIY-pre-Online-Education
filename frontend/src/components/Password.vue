<template>
  <el-card class="box-card" style="width:60%;text-align: center;margin-top:100px;margin-left: 20%" v-loading="loading">
    <p style="font-size:20px;font-weight:bold">
      修改密码
    </p>
    <el-form ref="password" :rules="rules" :model="user" label-width="100px" style="margin-left:10%;margin-top:80px;width:80%;padding-bottom: 15px">
      <el-form-item label="当前密码" prop="password" style="margin-top: 20px">
        <el-input type="password" v-model="user.password" show-password></el-input>
      </el-form-item>
      <el-form-item label="新密码" prop="new_password1" style="margin-top: 20px">
        <el-input type="password" v-model="user.new_password1" show-password></el-input>
      </el-form-item>
      <el-form-item label="重复新密码" prop="new_password2" style="margin-top: 20px">
        <el-input type="password" v-model="user.new_password2" show-password></el-input>
      </el-form-item>
      <el-row style="text-align: center;margin-top: 20px">
        <el-button type="success" round @click="submit()">修改密码</el-button>
        <el-button type="info" round @click="cancel()">返回</el-button>
      </el-row>
    </el-form>
  </el-card>
</template>

<script>
  export default {
    name: "Password",
    data() {
    return{
        loading: false,
        user: [],
        rules: {
          password: [
            {
              required: true,
             message:'请输入原密码',
              trigger: 'blur'
            }
          ],
          new_password1: [
            {
              required: true,
             message:'请输入新密码',
              trigger: 'blur'
            }
          ],
          new_password2: [
            {
              required: true,
             message:'请重复新密码',
              trigger: 'blur'
            }
          ],
        },
      }
    },
    mounted: function () {
      if (this.$cookies.get('user_id')) {
      } else {
        this.$router.push('/Login')
      }
    },
    methods: {
      submit() {
        let password = this.user.password
        let new_password1 = this.user.new_password1
        let new_password2 = this.user.new_password2
        if (new_password1 === new_password2) {
          let that = this
          let param = new URLSearchParams()
          param.append('password', password)
          param.append('new_password1', new_password1)
          param.append('user_id', that.$cookies.get('user_id'))
          that.loading = true
          that.axios({
            method: 'post',
            url: '/api/password/',
            data: param
          })
            .then(function (res) {
              if (res.data.code === 0) {
                that.loading = false
                that.$message.error(res.data.msg)
              } else if (res.data.code === 1) {
                that.loading = false
                that.$message({
                  message: res.data.msg,
                  type: 'success'
                });
                setTimeout(function () {
                  that.password = ''
                  that.new_password1 = ''
                  that.new_password2 = ''
                  that.$router.push('/User')
                }.bind(that), 1000)
              }
            })
        } else {
          this.new_password2 = ''
          this.$message('请输入相同的新密码')
        }
      },
      cancel() {
        this.password = ''
        this.new_password1 = ''
        this.new_password2 = ''
        this.$router.push('/User')
      }
    }

  }
</script>

<style scoped>

</style>
