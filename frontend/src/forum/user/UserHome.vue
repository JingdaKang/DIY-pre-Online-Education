<template>
  <div class="userhome">
    <div class="sidebar">
      <el-row class="tac">
        <el-col :span="12" class="el-col">
          <h1 class="pagetitle">我的论坛</h1>
          <el-menu
            default-active=""
            class="el-menu-vertical-demo"
            @open="handleOpen"
            @close="handleClose"
            active-text-color="#FFFFFF"
            router >
            <!--
            el-menu-item index="/forum/userhome/info">
              <i class="el-icon-albb-businesscard"></i>
              <span slot="title">我的信息</span>
            </el-menu-item
            -->
            <el-menu-item index="/forum/userhome/topic">
              <i class="el-icon-albb-createtask"></i>
              <span slot="title">我的主题</span>
            </el-menu-item>
            <el-menu-item index="/forum/userhome/reply">
              <i class="el-icon-albb-barrage"></i>
              <span slot="title">我的回复</span>
            </el-menu-item>
            <el-menu-item index="/forum/userhome/collect">
              <i class="el-icon-albb-accessory"></i>
              <span slot="title">我的收藏</span>
            </el-menu-item>
            <el-menu-item index="/forum/userhome/discuss">
              <i class="el-icon-albb-group"></i>
              <span slot="title">我的小组讨论</span>
            </el-menu-item>
            <el-menu-item index="/forum/userhome/discussreply">
              <i class="el-icon-albb-interactive"></i>
              <span slot="title">我参与的小组讨论</span>
            </el-menu-item>
            <el-menu-item index="/forum/userhome/focus">
              <i class="el-icon-albb-task"></i>
              <span slot="title">我关注的小组讨论</span>
            </el-menu-item>
            <el-menu-item index="/forum/userhome/apply">
              <i class="el-icon-albb-remind"></i>
              <span slot="title">小组加入申请</span>
            </el-menu-item>
            <el-menu-item index="/forum/userhome/following">
              <i class="el-icon-albb-people_fill"></i>
              <span slot="title">我的关注</span>
            </el-menu-item>
            <el-menu-item index="/forum/userhome/follower">
              <i class="el-icon-albb-people"></i>
              <span slot="title">我的粉丝</span>
            </el-menu-item>
            <el-menu-item index="/forum/userhome/message">
              <i class="el-icon-albb-message"></i>
              <span slot="title">我的消息</span>
            </el-menu-item>

          </el-menu>
        </el-col>
      </el-row>
    </div>
    <div class="main">
      <router-view></router-view>
    </div>
  </div>
</template>

<script>
    export default {
      name: "UserHome",
      data() {
        return {
          user: window.localStorage.getItem('username'),
        }
      },
      methods: {
        handleOpen(key, keyPath) {
          console.log(key, keyPath);
        },
        handleClose(key, keyPath) {
          console.log(key, keyPath);
        }
      },
      created(){
        if(!this.user){
          this.$router.push("/forum/login")
        }
      },
    }
</script>

<style scoped lang="scss">
.userhome{
  display: flex;
  margin-left: 6%;
  .sidebar{
    width: 15%;

    .tac{
      .el-col{
        width: 100%;
        .pagetitle{
          margin-left: 10px;
        }
        .el-menu-item{
          border-radius: 6px;
        }
        .el-menu-item.is-active {
          background-color: #409EFF !important;
          color: #ffffff;
          span {
            color: #ffffff !important;
          }
        }
      }
    }
  }
  .main{
    margin-left: 30px;
    margin-top: 75px;
    width: 70%;
  }
}

</style>
