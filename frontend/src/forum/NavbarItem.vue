<template>
  <nav class="menu">
    <template>
      <!-- 一级菜单循环 -->
      <el-menu :default-active="activeIndex" class="el-menu-demo" background-color="#fafafa" mode="horizontal" @select="handleSelect">
        <el-menu-item index="1"><router-link to="/forum">首页</router-link></el-menu-item>
        <el-menu-item index="2"><router-link to="/forum/section">板块</router-link></el-menu-item>
        <el-menu-item index="3"><router-link to="/forum/group">小组</router-link></el-menu-item>
        <el-menu-item index="4" :disabled="!user"><router-link to="/forum/userhome">我的论坛</router-link></el-menu-item>
      </el-menu>
    </template>
  </nav>
</template>

<script>
export default {
  name: 'NavbarItem',
  data () {
    return {
      activeIndex: '1',
      user: window.localStorage.getItem('username'),
    }
  },

  methods: {
    handleSelect(key, keyPath) {
      console.log(key, keyPath);
    }
  }
}
</script>

<style lang="scss" scoped>
  .router-link-exact-active{
    font-weight: bold!important;
  }
  .menu{
    .el-menu-demo, .el-menu-item {
      border-bottom-color: #ffffff !important;
      font-size: 16px;
    }

      width: 400px;
    padding-right: 35px;
    transition: width 0.25s ease;
    white-space: nowrap;
    &.hide{
      width: 0px;
      font-size: 0;
    }
    .menu-title{
      padding: 10px 20px;
      cursor: pointer;
      font-weight: bold!important;
      &:first-child{
        padding-left: 15px;
      }
    }
    .el-icon-caret-bottom{
      transform: rotate(0deg);
      transition: transform .3s;
    }
    .icon-rorate-v{
      transform: rotate(180deg);
    }


  }
</style>
