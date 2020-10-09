<template>
  <div id="config">
    <div class="block">
      <el-carousel trigger="click" height="150px" style="border-radius: 8px;overflow: hidden">
        <el-carousel-item v-for="item in 2" :key="item">
          <router-link to="forum/discuss/16">
            <img src="@/assets/image/banner1.jpg" v-if="item  == 1" class="bannerImg"/></router-link>
          <img src="@/assets/image/banner2.jpg" v-if="item  == 2" class="bannerImg" />
        </el-carousel-item>
      </el-carousel>
    </div>
    <div class="topic-config">
      <template v-if="sidebarClickData.type === 1">
        <template v-if="sidebarClickData.config === 1">
          <h5 class="recommend">
            热门帖子
          </h5>
        </template>
        <template v-if="sidebarClickData.config === 2">
          <h5 class="new-content">我的动态</h5>
        </template>
        <template v-if="sidebarClickData.config === 3">
          <h5 class="new-content">最新帖子</h5>
        </template>
      </template>
      <template v-if="sidebarClickData.type === 2">
        <h5 class="recommend">
          分区帖子
        </h5>
      </template>
    </div>
  </div>

</template>

<script>
export default {
  data () {
    return {
      activeName: 'week',
      // 默认模式---为你推荐
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
      this.$eventBus.$on('sidebar-click', data => {
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
  .el-carousel__item h3 {
    color: #475669;
    font-size: 14px;
    opacity: 0.75;
    line-height: 150px;
    margin: 0;
  }

  .el-carousel__item:nth-child(2n) {
    background-color: #99a9bf;
  }

  .el-carousel__item:nth-child(2n+1) {
    background-color: #d3dce6;
  }
  .config{
    .block{

    }
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
  }

</style>
