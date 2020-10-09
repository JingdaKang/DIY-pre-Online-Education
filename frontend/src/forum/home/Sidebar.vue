<template>
  <div class="home-sidebar">
    <ul class="recommended">
      <li
        v-for="(item, index) in recommended"
        :key="index"
        :class="item.id === activeItem ? 'item active-item' : 'item'"
        @click="handleClick('click', item)"
      >
        <span class="icon-box">
          <i :class="item.icon" />
        </span>
        <span class="name">{{ item.name }}</span>
      </li>
    </ul>
    <div class="hot-section">
      <p class="title">热门板块</p>
      <ul class="list">
        <li
          v-for="(item, index) in hotSection"
          :key="index"
          :class="item.id === activeItem ? 'item active-item' : 'item'"
          @click="handleClick('click', item)"
        >
          <span class="icon-box">
            <img v-if="item.image" :src="item.image" class="icon">
            <i v-else class="el-icon-albb-discount" />
          </span>
          <span class="name">{{ item.name || item.title }}</span>
        </li>
      </ul>
    </div>
  </div>
</template>

<script>
export default {
  data () {
    return {
      activeItem: '',
      recommended: [
        { id: 1, type: 1, config: 1, name: '热门话题', icon: 'el-icon-albb-good' },
        { id: 2, type: 1, config: 2, name: '我的动态', icon: 'el-icon-albb-calendar' },
        { id: 3, type: 1, config: 3, name: '最新内容', icon: 'el-icon-albb-int' }
      ],
      hotSection: [
        { id: 4, type: 2, name: '综合' },
        { id: 6, type: 2, name: 'Python程序设计' },
        { id: 7, type: 2, name: 'Java程序设计' },
        { id: 8, type: 2, name: '数据结构与算法' },
        { id: 999, type: 3, name: '更多板块'}
      ]
    }
  },
  mounted () {
    this.handleClick('click', this.recommended[0])
  },
  methods: {
    handleClick (type, data) {
      switch (type) {
        case 'click':
          if (data.type === 3) {
            this.$router.push('/forum/section')
          } else {
            this.activeItem = data.id
            // 兄弟组件传参
            this.$eventBus.$emit('sidebar-click', data)
          }
          break
      }
    }
  }
}
</script>

<style lang="scss" scoped>
  @import '@/common/style/base.scss';
  .home-sidebar{
    padding: 0 15px;
    padding-left: 10px;
    width: 16.66667%;
    .recommended{
      .item{
        .icon-box{
          display: inline-block;
          width: 35px;
          text-align: center;
          .icon{
            height: 16px;
            widows: 16px;
          }
        }
        .name{
          flex: 1;
          text-align: left;
        }
      }
    }
    .hot-section{
      .title{
        position: relative;
        margin: 10px 0;
        padding-left: 10px;
        text-align: left;
      }
      .list{
        .item{
          .icon-box{
            display: inline-block;
            width: 35px;
            text-align: center;
            .icon{
              height: 16px;
              widows: 16px;
            }
          }
          .name{
            flex: 1;
            text-align: left;
          }
        }
      }
    }
    .item{
      display: flex;
      align-items: center;
      padding: 10px 0;
      border-radius: 4px;
      cursor: pointer;
      &:hover{
        background: rgba(218, 133, 133, .2);
      }
    }
    .active-item{
      color: white;
      background: $theme;
      font-weight: bold;
      &:hover{
        background: $theme;
      }
      img{
        filter: brightness(0) invert(1)
      }
    }
  }
</style>
