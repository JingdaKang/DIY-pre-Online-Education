<template>
  <div id="ClassManage" style="background: #FFFFFF">
    <el-container>
      <el-header style="height: 90px;width:100%;background-color:#FFFFFF;border-bottom:1px solid lightgray">
        <el-row style="text-align:center;margin:0;">
          <p style="float:left;width:auto;font-size:30px">在线教育平台</p>
          <p style="margin-left:4px;color:red;float:left;width:auto;font-size:30px">课程管理系统</p>
          <el-button style="float:right;margin-right:15px;margin-top:30px" type="danger" @click="logOut()">退出
          </el-button>
          <label style="float:right;margin-right:15px;margin-top:20px"> {{user.username}}</label>
          <el-avatar :size="40" src="api/avatar/"
                     style="float:right;margin-right:20px;margin-top:30px"></el-avatar>
        </el-row>
      </el-header>

      <el-container>
        <el-aside style="height: auto;width:280px;background-color:#FFFFFF;border-right:1px solid lightgray;border-top:0">
          <h3 style="color: black;font-size:20px" v-if="user.type=='S'">学生端</h3>
          <h3 style="color: black;font-size:20px" v-if="user.type=='T'">教师端</h3>
          <el-menu
            style="border-right:0"
            background-color="#FFFFFF"
            text-color="#000000"
            active-text-color="#FFFFFF"
            active-font-size="20px"
            active-background-color="#3370ff"
            default-active="/AllClass"
            router
          >
            <el-menu-item index="/AllClass">
              <i class="el-icon-news"></i>
              <span slot="title">全部课程</span>
            </el-menu-item>
            <el-menu-item v-if="user.type=='T'" index="/ReleaseClass">
              <i class="el-icon-edit"></i>
              <span slot="title">发布课程</span>
            </el-menu-item>
            <el-menu-item v-if="user.type=='T'" index="/MyClass">
              <i class="el-icon-folder"></i>
              <span slot="title">我的课程</span>
            </el-menu-item>
            <el-menu-item v-if="user.type=='S'" index="/SelectedClass">
              <i class="el-icon-tickets"></i>
              <span slot="title">已选课程</span>
            </el-menu-item>
          </el-menu>
        </el-aside>
        <el-main>
         <router-view v-if="!this.$route.meta.keepAlive"/>
          <keep-alive>
            <router-view v-if="this.$route.meta.keepAlive"/>
          </keep-alive>
        </el-main>
      </el-container>
    </el-container>

  </div>
</template>

<script>
  export default {
    name: "ClassManage",
    data() {
      return {
        user: [],
      }
    },
    created() {
      this.getUrl();
    },
    mounted: function () {
      if (this.$cookies.get('username')) {
        this.getUser()
      } else {
        this.$router.push('/Login')
      }
    },
    methods: {
      getUrl() {
        let self = this;
        let currentUrl = window.location.href;
        self.activeIndex = currentUrl.split('#')[1];
      },
      logOut() {
        this.$router.push('/Login')
      },
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
    }
  }
</script>

<style scoped>
 .el-menu-item.is-active {
    background-color: #3370ff !important;
    color: #fff;
  }

  .logo {
    float: left;
    margin-left: 20px;
    margin-top: 0;
    text-align: center;
    width: 260px
  }

  .logo img {
    width: 80px;
    height: 80px;
  }
</style>
