<template>
  <div id="cloudnote">
    <Header></Header>
    <div class="content" style="margin-top:60px">
      <router-view></router-view>
    </div>
  </div>
</template>

<script>
import Header from '@/cloudnote/header/Header.vue';
export default {
  name: 'cloudnote',
  components:{
            Header
  }
}
</script>

<style>

</style>
