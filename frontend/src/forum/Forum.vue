<template>
  <div id="Forum">
   <layout></layout>
  </div>
</template>

<script>
 import Layout from './Layout';

  export default {
    name: 'App',
    data() {
      return {
        path: ''
      }
    },
      components: {
      Layout
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

<style scope lang="scss">
  @import '@/common/style/base.scss';
  #app {
    height: 100%;
    font-family: 'Avenir', Helvetica, Arial, sans-serif;
    font-size: 14px;
    color: #757575;
    -webkit-font-smoothing: antialiased;
    -moz-osx-font-smoothing: grayscale;
  }
</style>
