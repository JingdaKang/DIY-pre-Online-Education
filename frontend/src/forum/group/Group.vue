<template>
  <div class="page-container">
    <group-sidebar />
    <Main />
    <div class="right">
      <Right />
    </div>
  </div>
</template>


<script>
  import GroupSidebar from './GroupSidebar'
  import Main from './Main'
  import Right from './Right'
  export default {
    name: "Group",
    components: {
      GroupSidebar,
      Main,
      Right
    },
    data () {
      return {
      }
    }
  }
</script>

<style scoped lang="scss">
  @import '@/common/style/base.scss';
  .page-container{
    display: flex;
    .right{
      padding: 0 15px;
      width: 25%;
    }
  }
</style>

