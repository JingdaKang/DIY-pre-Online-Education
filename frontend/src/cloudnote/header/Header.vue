<template>
  <div class="header">
    <el-menu theme="dark" :default-active="active" mode="horizontal" :router="true">
      <el-menu-item index="/"><i class="el-icon-edit"></i><span style="font-weight: bold">在线教育平台</span> <span style = "color:red;font-weight: bold">云笔记系统</span></el-menu-item>
      <el-menu-item v-if="!user" index="/register" class="pull-right" key="register"><i
        class="text-icon glyphicon glyphicon-cloud"></i>注册
      </el-menu-item>
      <el-menu-item v-if="!user" index="/login" class="pull-right"><i
        class="text-icon glyphicon glyphicon-log-in"></i>登录
      </el-menu-item>
      <el-menu-item v-if="user" index="/" @click="logout()" class="pull-right" key="logout">
        <el-tooltip class="item" effect="dark" content="点击 退出云笔记系统" placement="bottom-end">
          <div style="position: relative;"><i class="text-icon glyphicon glyphicon-log-out"></i>退出</div>
        </el-tooltip>
      </el-menu-item>
      <el-menu-item v-if="user" index="/main/manage" class="pull-right">
        <el-tooltip class="item" effect="dark" content="点击 进入个人中心" placement="bottom-end" >
          <div style="position: relative;"><i class="text-icon glyphicon glyphicon-user"></i><span class="hidden-xs">欢迎您，<span
            v-text="user.name"></span>！</span><span class="visible-xs-inline-block">我</span>
          </div>
        </el-tooltip>
      </el-menu-item>
    </el-menu>
  </div>
</template>

<script type="text/ecmascript-6">
    // import { getCookie, delCookie } from '@/network/cookie';
  import { CommonService } from '@/service/CommonService';
  import { UserService } from '@/service/UserService';

  export default {
    created () {
      CommonService.isLogin(this.$store, () => {}, () => {});
    },
    methods: {
      logout () {
        UserService.logout(this.$store, () => {
          console.log('logout');
          this.$message.success('退出成功');
          window.location.href="http://127.0.0.1:8888/#/Login";
        });
      },

    },
    computed: {
      active () {
        return this.$store.state.currentPath;
      },
      user () {

        console.log(this.$store.state);
        return this.$store.state.user;
      }
    }
  };
</script>

<style lang="stylus" ref="stylesheet/stylus" scoped>
  .header
    position: fixed
    z-index: 100
    width: 100%
    top: 0
    left: 0
</style>
