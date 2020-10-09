<template>
  <div id="home" v-loading="loading">
    <el-card style="margin-top: 50px;width: 80%;margin-left: 10%">
      <el-aside style="float:left;width: 50%;height:520px;margin: 0;border-top:0;border-right: 2px solid #EBEEF5;background-color:#FFFFFF ">
        <h3 >欢迎登录</h3>
        <el-divider></el-divider>
        <el-row style="height: 100px;margin-top: 10px;text-align: center">
          <div class="avatar_box" style="text-align: center">
            <img src="api/avatar/" class="avatar" id="user_avatar">
          </div>
        </el-row>
        <el-row style="margin-top: 30px;margin-left: 20px">
          <label style="width:80px;text-align:right;float: left;margin-left: 10px">用户名:</label>
          <label style="float: left;margin-left: 25px">{{user.username}}</label>
        </el-row>
        <el-row style="margin-top: 30px;margin-left: 20px">
          <label style="width:80px;text-align:right;float: left;margin-left: 10px">账户类型:</label>
          <label style="float:left;margin-left:25px" v-if="user.type==='A'">管理员</label>
          <label style="float:left;margin-left:25px" v-if="user.type==='T'">老师</label>
          <label style="float:left;margin-left:25px" v-if="user.type==='S'">学生</label>
        </el-row>
        <el-row style="margin-top: 30px;margin-left: 20px">
          <label style="width:80px;text-align:right;float: left;margin-left: 10px">邮箱:</label>
          <label style="float: left;margin-left: 25px">{{user.email}}</label>
        </el-row>
        <el-row style="margin-top: 30px;margin-left: 20px">
          <label style="width:80px;text-align:right;float: left;margin-left: 10px">账户状态:</label>
          <button style="float:left;margin-left:25px" v-if="user.is_active===true" type="button"
                  class="el-button el-button--small el-button--success is-circle"><i class="el-icon-check"></i></button>
          <button style="float:left;margin-left:25px" v-if="user.is_active===false" type="button"
                  class="el-button el-button--small el-button--danger is-circle"><i class="el-icon-close"></i></button>
        </el-row>
        <el-row style="text-align: center;margin-top: 35px">
          <el-button type="success" @click="userCenter()">个人中心</el-button>
          <el-button type="danger" @click="logout()">退出登录</el-button>
        </el-row>
      </el-aside>
      <el-main style="overflow:hidden;float:left;width: 48%;height:520px;margin: 0;padding: 0">
        <h3 >选择子系统</h3>
        <el-divider></el-divider>
        <div v-if="user.type==='A'">
          <el-row style="margin-left: 20px;margin-top: 30px">
            <el-button style="width: 150px" type="primary" @click="gotoAdminSystem">后台管理系统</el-button>
          </el-row>
        </div>
        <div v-if="user.type!='A'">
          <el-row v-if="user.type==='S'" style="margin-left: 20px;margin-top: 30px">
            <el-button style="width: 150px" type="warning" @click="gotoSelectSystem">选课系统</el-button>
          </el-row>
          <el-row v-if="user.type==='T'" style="margin-left: 20px;margin-top: 30px">
            <el-button style="width: 150px" type="warning" @click="gotoReleaseSystem">课程系统</el-button>
          </el-row>
          <el-row style="margin-left: 20px;margin-top: 30px">
            <el-button style="width: 150px" type="primary" @click="gotoHomeworkSystem">作业系统</el-button>
          </el-row>
          <el-row style="margin-left: 20px;margin-top: 30px">
            <el-button style="width: 150px" type="success" @click="goExamSystem">考试系统</el-button>
          </el-row>
          <el-row style="margin-left: 20px;margin-top: 30px">
            <el-button style="width: 150px" type="info" @click="gotoNoteSystem">云笔记系统</el-button>
          </el-row>
          <el-row style="margin-left: 20px;margin-top: 30px">
            <el-button style="width: 150px" type="warning" @click="gotoForumSystem">论坛系统</el-button>
          </el-row>
          <el-row style="margin-left: 20px;margin-top: 30px">
            <el-button style="width: 150px" type="danger" @click="gotoIASystem">智能问答系统</el-button>
          </el-row>
        </div>
      </el-main>
    </el-card>
  </div>
</template>

<script>
  export default {
    name: "Login",
    data() {
      return {
        loading: false,
        user: [],
      }
    },
    mounted: function () {
      if (this.$cookies.get('username')) {
        this.getUser()
      } else {
        this.$router.push('/Login')
      }
    },
    methods: {
      getUser() {
        let that = this
        let param = new URLSearchParams()
        let user_id = that.$cookies.get('user_id')
        param.append('user_id', user_id)
        that.axios({
          method: 'post',
          url: '/api/user/',
          data: param
        })
          .then(function (res) {
            if (res.data.code === 1) {
              that.user = res.data.user[0]
              that.loading = false
            } else if (res.data.code === 0) {
              that.$message.error('查询失败')
              console.log(res.data.msg)
            }
          })
      },
      userCenter() {
        this.$router.push('/User')
      },
      logout() {
        this.$cookies.remove('user_id')
        this.$cookies.remove('username')
        this.$cookies.remove('type')
        this.$router.push('/Login')
      },
      gotoSelectSystem() {
        this.$router.push('/ClassManage')
      },
      gotoReleaseSystem() {
        this.$router.push('/ClassManage')
      },
      gotoAdminSystem() {
        this.$router.push('/Admin')
      },
      gotoIASystem() {
        this.$router.push('/IAsystem')

      },
      gotoForumSystem() {
        this.$router.push('/forum_home')
      },
      goExamSystem() {
        if (this.$cookies.get('type') == 'S') {
          this.$router.push('/exam/student')
        } else {
          //考试教师用户账户登录跳转
          this.$router.push('/exam/teacher')
        }
      },
      gotoNoteSystem() {
        //window.location.href = "http://127.0.0.1:8888/#/cloudnote"
        this.$router.push('/cloudnote')
      },
      gotoHomeworkSystem() {
        if (this.$cookies.get('type') == 'S')
          this.$router.push('/work/Student')
        else
          this.$router.push('/work/Teacher')
      }
    }
  }
</script>

<style scoped>
  .avatar_box {
    height: 100px;
    margin-left: 45px;
    float: left;
    display: block;
  }

  .avatar {
    width: 100px;
    height: 100px;
    border-radius: 50%;
    display: block;
  }

  .login-box {
    border-radius: 4px;
    border: 1px solid #EBEEF5;
    background-color: #FFF;
    overflow: hidden;
    color: #303133;
    -webkit-transition: .3s;
    transition: .3s
  }
</style>

