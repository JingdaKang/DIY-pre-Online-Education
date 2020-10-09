<template>
  <div class="app">
    <el-container>
      <el-aside class="app-side app-side-left"
                :class="isCollapse ? 'app-side-collapsed' : 'app-side-expanded'"
                width="200px"
                style="position: relative">
        <div class="app-side-logo" style="text-align: center">
          <img src="@/assets/logo.png"
               :width="isCollapse ? '60' : '60'"
               height="60" />
        </div>
        <div>
          <!-- 我是样例菜单 -->
          <el-menu class="el-menu-vertical-demo"
                   :default-active="$route.path"
                   router
                   active-text-color="#ffffff"
                   :collapse="isCollapse">
            <el-submenu index="1">
              <template slot="title">
                <i class="el-icon-menu"></i>
                <span slot="title">发布考试</span>
              </template>
              <el-menu-item-group>
                <el-menu-item index="/addQuestion">试题添加</el-menu-item>
                <el-menu-item index="/selectQuestion">试题查询</el-menu-item>
                <el-menu-item index="/addPaper">试卷组合</el-menu-item>
                <el-menu-item index="/selectPaper">试卷预览</el-menu-item>
                <el-menu-item index="/addExam">考试发布</el-menu-item>
                <el-menu-item index="/findExam">我的考试</el-menu-item>
              </el-menu-item-group>
            </el-submenu>
            <el-submenu index="2">
              <template slot="title">
                <i class="el-icon-menu"></i>
                <span slot="title">考试处理</span>
              </template>
              <el-menu-item-group>
                <el-menu-item index="/selectScore">试卷批阅</el-menu-item>
                <el-menu-item index="/showScore">成绩查询</el-menu-item>
                <el-menu-item index="/showGrade">成绩可视化</el-menu-item>
              </el-menu-item-group>
            </el-submenu>
<!--            <el-menu-item index="/setCourse">-->
<!--              <i class="el-icon-setting"></i>-->
<!--              <span slot="title">课程相关</span>-->
<!--            </el-menu-item>-->
          </el-menu>
        </div>
      </el-aside>

      <el-container>
        <el-header class="app-header" style="line-height: 60px;background: #fafafa;border-top: 3px solid #ff0000;box-shadow: 0px 2px 10px 0px rgba(0,0,0,0.1), 0 1px rgba(0,0,0,0.1);">
          <el-row>
            <el-col :span="12">
              <div style="text-align: left">
                <span style="font-size: x-large;">在线考试管理系统</span>
                <span style="font-size: x-large;color: #ff0000">教师端</span>
              </div>
            </el-col>
            <el-col :span="12">
              <div style="text-align: right">
                <el-dropdown trigger="hover"
                             :hide-on-click="false">
                  <span class="el-dropdown-link">
                    {{ username }}
                    <i class="el-icon-arrow-down el-icon--right"></i>
                  </span>
                  <el-dropdown-menu slot="dropdown">
                    <el-dropdown-item>我的消息</el-dropdown-item>
                    <el-dropdown-item>设置</el-dropdown-item>
                    <el-dropdown-item divided
                                      @click.native="logout">退出登录</el-dropdown-item>
                  </el-dropdown-menu>
                </el-dropdown>
                <el-button type="danger" v-on:click="logout">退出</el-button>
              </div>
            </el-col>
          </el-row>
        </el-header>
        <router-view/>
      </el-container>
    </el-container>
  </div>
</template>

<script>
export default {
  name: 'Teacher',
  data () {
    return {
      username: '',
      isCollapse: false,
      avatar: ''
    }
  },
  methods: {
    toggleSideBar () {
      this.isCollapse = !this.isCollapse
    },
    logout: function () {
      this.$confirm('确认退出?', '提示', {})
        .then(() => {
          sessionStorage.removeItem('user')
          this.$router.push('/Login')
        })
        .catch(() => { })
    },
    getAvatar () {
      this.axios.post('/exam/getavatar', {username: this.username})
        .then(response => {
          this.avatar = '/media/' + response.data.img
        })
    }
  },
  mounted: function () {
    let user = this.$cookies.get('username')
    if (user) {
      sessionStorage.setItem('username', user)
      this.username = user
    }
    this.getAvatar()
  }
}
</script>

<style scoped>
.el-menu-item.is-active{
  background-color: #20B2AA !important;
  font-weight: bold;
}
</style>
