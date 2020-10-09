<template>
  <div class="Forum">
    <navbar v-show="!(path === '/forum/questionpage')"></navbar>
    <page-main />
  </div>
</template>

<script>
  import Navbar from './Navbar'
  import PageMain from './PageMain'
  export default {
    name: 'Layout',
    components: {
      Navbar,
      PageMain,
    },
    data() {
      return {
        path: ''
      }
    },
    mounted() {
      this.path = this.$route.path;
      console.log(this.$route.path)
    },
    watch:{
      $route(to,from){
        this.path = to.path
      }
    }
  }
</script>

<style scoped lang="scss">
  .Forum{
    height: 100%;
    background: #f6f6f6;
    .page-main{
      margin-top: 5px;
      background: white;
    }
  }
</style>
