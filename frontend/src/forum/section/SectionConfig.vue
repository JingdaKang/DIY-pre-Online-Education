<template>
  <div class="topic-config">
    <template v-if="sidebarClickData.type === 1">
      <template v-if="sidebarClickData.config === 1">
        <h5 class="recommend">
        </h5>
      </template>
      <template v-if="sidebarClickData.config === 2">
        <h5 class="new-content"></h5>
      </template>
      <template v-if="sidebarClickData.config === 3">
        <h5 class="new-content"></h5>
      </template>
    </template>
    <template v-if="sidebarClickData.type === 2">
      <h5 class="recommend">
        分区帖子
      </h5>
    </template>
  </div>
</template>

<script>
export default {
  data () {
    return {
      activeName: '',
      sidebarClickData: {
        type: 1,
        config: 1
      }
    }
  },
  mounted () {
    this.receiveEventBus()
  },
  methods: {
    receiveEventBus () {
      // 接收eventBus
      this.$eventBus.$on('sidebar-click-section', data => {
        this.sidebarClickData = data
      })
    },
    handleClick () {

    }
  }
}
</script>

<style lang="scss" scoped>
  @import '@/common/style/mixin.scss';
  .topic-config{
    margin-top: 15px;
    .recommend, .new-content{
      position: relative;
      margin: 10px 0;
      height: 20px;
      line-height: 20px;
      &::after{
        @include border-1px('bottom');
        bottom: -10px;
      }
    }
  }
</style>
