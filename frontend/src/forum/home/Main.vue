<template>
  <div class="main">
    <topic-config />
    <topic-list />
  </div>
</template>

<script>
import TopicConfig from './TopicConfig'
import TopicList from './TopicList'

export default {
  name: 'Main',
  components: {
    TopicConfig,
    TopicList
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
