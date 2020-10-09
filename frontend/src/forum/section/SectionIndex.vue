<template>
  <div class="page-container">
    <section-sidebar />
    <Main />
  </div>
</template>


<script>
  import SectionSidebar from './SectionSidebar'
  import Main from './Main'
  export default {
    name: "SectionIndex",
    components: {
      SectionSidebar,
      Main,
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

