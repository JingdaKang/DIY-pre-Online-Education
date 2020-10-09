<template>
  <div class="main">
    <group-config />
    <group-topic-list />
  </div>
</template>

<script>
import GroupConfig from './GroupConfig'
import GroupTopicList from './GroupTopicList'

export default {
  name: 'Main',
  components: {
    GroupConfig,
    GroupTopicList
  },
  data () {
    return {

    }
  },

  methods: {


  }
}
</script>

<style scoped lang="scss">
.main{
  flex: 1;
  padding: 0 15px;
  .carousel{
    width: 100%;
    border-radius: 8px;
    overflow: hidden;
  }
  .no-carousel{
    height: 100%;
    line-height: 150px;
    text-align: center;
    font-size: 24px;
  }
}
</style>
