<template>
  <div class="Nav-header">
    <div class="navbar">
      <p class="logo" @click="$router.push('/forum')">
        <span class="logo1">在线教育平台</span>
        <span class="logo2">论坛系统</span>
      </p>
      <div class="mid">
        <navbar-item />
        <search />
      </div>
      <UserNav />
    </div>
  </div>
</template>

<script>
  import NavbarItem from './NavbarItem'
  import Search from './Search'
  import UserNav from './UserNav'
  export default {
    name: 'Navbar',
    components: {
      NavbarItem,
      Search,
      UserNav
    }
  }
</script>

<style scoped lang="scss">
  @import '@/common/style/base.scss';
  .Nav-header{
    border-top: 3px solid $theme;
    box-shadow: 0px 2px 10px 0px rgba(0,0,0,0.1), 0 1px rgba(0,0,0,0.1);
    height: 64px;
    background: #fafafa;
    .navbar{
      margin: auto;
      display: flex;
      // justify-content: center;
      align-items: center;
      max-width: $maxWidth;
      min-width: $minWidth;
      height: 100%;
      font-size: 16px;
      .logo{
        width: 20%;
        padding: 0 15px;
        font-size: 0;
        cursor: pointer;
        .logo1, .logo2{
          font-size: 24px;
        }
        .logo1{
          color: #212121;
        }
        .logo2{
          color: $theme;
        }
      }
      .mid{
        display: flex;
        flex: 1;
        .hide{
          width: 0;
          transition: width .3s;
        }
      }
    }

  }
</style>
