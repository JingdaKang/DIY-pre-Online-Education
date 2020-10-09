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
    <div class="join-group">
      <p class="title">我加入的小组</p>
      <ul class="list">
        <li
          v-for="(item, index) in userGroup"
          :key="index"
          :class="item.id === activeItem ? 'item active-item' : 'item'"
          @click="handleClick('click', item)"
        >
          <span class="icon-box">
            <img v-if="item.image" :src="item.image" class="icon">
            <i v-else class="el-icon-albb-office" />
          </span>
          <span class="name">{{ item.name || item.title }}</span>
        </li>
      </ul>
    </div>

    <div class="join-group">
      <p class="title">为你推荐小组</p>
      <ul class="list">
        <li
          v-for="(item, index) in recommendGroups"
          :key="index"
          :class="item.id === activeItem ? 'item active-item' : 'item'"
          @click="handleClick('click', item)"
        >
          <span class="icon-box">
            <img v-if="item.image" :src="item.image" class="icon">
            <i v-else class="el-icon-albb-office" />
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
      user: window.localStorage.getItem('username'),
      activeItem: '',
      recommended: [
        { id: -1, type: 1, config: 1, name: '热门小组讨论', icon: 'el-icon-albb-good' },
        { id: 0, type: 1, config: 2, name: '我的小组动态', icon: 'el-icon-albb-calendar' },
      ],
      userGroup:[],
      recommendGroups: [
      ]
    }
  },

  mounted () {
    this.getTags()
    this.getUserGroup()
    this.handleClick('click', this.recommended[0])
  },
  methods: {
    handleClick (type, data) {
      switch (type) {
        case 'click':
          this.activeItem = data.id
          // 兄弟组件传参
          this.$eventBus.$emit('sidebar-click-group', data)
          console.log('emit')
          break
      }
    },
    getUserGroup () {
      this.axios.get("/forum/userGroup/", {
        params: {
          user: this.user,
        }
      }).then(response => {
        if (response.data.status === 0) {
          this.userGroup = response.data.data
        }
      })
    },
    getTags(){
      this.axios.get("/forum/recommendGroup", {
        params: {
          user: this.user,
        }
      }).then(response => {
        if (response.data.status === 0) {
          this.recommendGroups = response.data.data
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
    .join-group{
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
        background: rgba(1,126,102,0.08);
      }
    }
    .active-item{
      color: white;
      background: #009a61;
      font-weight: bold;
      &:hover{
        background: #009a61;
      }
      img{
        filter: brightness(0) invert(1)
      }
    }
  }
</style>
