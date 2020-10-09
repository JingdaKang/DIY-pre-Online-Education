<template>
  <div class="home-sidebar">
    <div class="all-section">
      <p class="title">所有板块</p>
      <ul class="list">
        <li
          v-for="(item, index) in allSection"
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
      activeItem: 1,
      allSection: [
      ]
    }
  },

  mounted () {
    this.getTags()
    this.handleClick('click', this.recommended[0])
  },
  methods: {
    handleClick (type, data) {
      switch (type) {
        case 'click':
          this.activeItem = data.id
          // 兄弟组件传参
          this.$eventBus.$emit('sidebar-click-section', data)
          break
      }
    },
    getTags () {
      this.axios.get("/forum/sections/", {
      }).then(response => {
        if (response.data.status === 0) {
          this.allSection = response.data.data
        }
      })
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
    .all-section{
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
