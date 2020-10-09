<template>
  <div class="main">
    <section-config />
    <section-topic-list />
  </div>
</template>

<script>
import SectionConfig from './SectionConfig'
import SectionTopicList from './SectionTopicList'

export default {
  name: 'Main',
  components: {
    SectionConfig,
    SectionTopicList
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
}
</style>
