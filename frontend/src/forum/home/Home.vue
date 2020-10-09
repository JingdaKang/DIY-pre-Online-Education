<template>
  <div class="page-container">
    <sidebar />
    <Main />
    <div class="right">
      <Right />
    </div>
  </div>
</template>


<script>
import Sidebar from './Sidebar'
import Main from './Main'
import Right from './Right'
export default {
  name: "Home",
  components: {
    Sidebar,
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
