/* eslint-disable */
<template>
  <div class="login-box">
    <!-- 通过:rules="loginFormRules"来绑定输入内容的校验规则 -->
    <!-- label-width="auto"-->
    <el-form
      :rules="loginFormRules"
      ref="loginForm"
      :model="loginForm"
      label-position="right"
      show-message>
      <span class="login-title">欢迎登录<br>在线作业管理系统</span>
      <div style="margin-top: 5px"></div>
      <el-form-item label="用户名" prop="username">
        <el-col :span="24">
          <el-input
            placeholder="请输入用户名"
            prefix-icon="el-icon-user"
            type="username"
            v-model="loginForm.username"
            clearable>
          </el-input>
        </el-col>
      </el-form-item>

      <el-form-item label="密码" prop="password">
        <el-col :span="24">
          <el-input
            placeholder="请输入密码"
            prefix-icon="el-icon-lock"
            type="password"
            v-model="loginForm.password"
            show-password>
          </el-input>
        </el-col>
      </el-form-item>

      <el-form-item label="账号类型">
        <el-col :span="18">
          <el-radio-group v-model="loginForm.Radio">
            <el-radio label="1" border>学生</el-radio>
            <el-radio label="2" border>教师</el-radio>
          </el-radio-group>
        </el-col>
      </el-form-item>

      <el-form-item>
        <el-button type="text" @click="changepassword">忘记密码</el-button>
      </el-form-item>

      <el-form-item>
        <el-col :span="24">
          <el-button type="primary" @click="loginSubmit('loginForm')" round>登录</el-button>
          <el-button @click="registerSubmit()" round>注册</el-button>
        </el-col>
      </el-form-item>
    </el-form>
  </div>
</template>

<script>
  export default {
    name: "login",
    data() {
      return {
        delivery: false,
        loginForm: {
          username: '',
          password: '',
          Radio: '1',
        },
        // 表单验证，需要在 el-form-item 元素中增加 prop 属性
        loginFormRules: {
          username: [
            {required: true, message: '账号不可为空！', trigger: 'blur'}
          ],
          password: [
            {required: true, message: '密码不可为空！', trigger: 'blur'}
          ]
        }
      }
    },
    methods: {
      loginSubmit: function (loginForm) {
        this.$refs[loginForm].validate((valid) => {
          if (valid) {
            // 为表单绑定验证功能
            this.$axios.post('/api/Login',
              {
                username: this.loginForm.username,
                password: this.loginForm.password
              })
              .then((response) => {
                if (response.data.status === 0) {
                  // 使用 vue-router 路由到指定页面
                  var temp = this.loginForm.Radio;
                  if (temp === '1' && unescape(response.data.type) === 'S') {
                    this.$notify({
                      title: '登录学生系统成功',
                      message: response.data.username + ',欢迎您！',
                      type: 'success'
                    });
                    this.$cookies.set('username', response.data.username);
                    console.log("to Student");
                    this.$router.replace("/Student");
                  } else if (temp === '2' && unescape(response.data.type) === 'T') {
                    this.$notify({
                      title: '登录教师系统成功',
                      message: response.data.username + ',欢迎您！',
                      type: 'success'
                    });
                    this.$cookies.set('username', response.data.username);
                    console.log("to Teacher")
                    this.$router.replace("/Teacher");
                  } else {
                    this.$notify({
                      title: '登录失败',
                      message: '账号类型错误！',
                      type: 'error'
                    })
                  }
                } else {
                  this.$notify({
                    title: '登录失败',
                    message: response.data.message,
                    type: 'error'
                  })
                }

              });
          } else {
            return false;
          }
        })
      },

      registerSubmit() {
        this.$router.replace("/Register");
      },

      /*querySearch(queryString, cb) {
        var users = this.users;
        var results = queryString ? users.filter(this.createFilter(queryString)) : users;
        // 调用 callback 返回建议列表的数据
        cb(results);
      },
      createFilter(queryString) {
        return (user) => {
          return (user.value.toLowerCase().indexOf(queryString.toLowerCase()) !== -1);
        };
      },
      loadAll() {
        this.$axios.post('/api/GetUsers')
          .then((response) =>{
            //alert(response.data.userlist);
            this.userslist = [];
            this.userslist.push({ "value": "123"});
            //alert(response.data.userlist[0])
            //alert(this.userslist)
            for(let i=0;i<response.data.userlist.length;i++){
              this.userslist.push({'value':response.data.userlist[i].username});
              //alert(i+response.data.userlist[i].username);
            }

          })
        return this.userslist;
      },
      handleSelect(item) {
        console.log(item);
      }*/

    }
    /*mounted() {
      this.users = this.loadAll();
    },*/
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
