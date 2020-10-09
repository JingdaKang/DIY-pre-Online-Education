<template>
    <div>
      <div class="new">
        <h1 class="el-icon-albb-brush"><router-link to="/forum/newtopic">创作新帖子</router-link></h1>
      </div>


      <br><br>
      <div class="activity">
        <div class="head">
          <span class="title">活动推荐</span>
        </div>
        <div v-for="(item, index) in list" :key="index" class="item">
          <div class="time">
            <p class="month">{{ getEngMonth(item.date) }}</p>
            <p class="day">{{ $fn.switchTime(item.date, 'DD') }}</p>
          </div>
          <div class="content">
            <p class="title">{{ item.title }}</p>
            <div class="info">
              <span class="date">{{ $fn.switchTime(item.date, 'MM-DD') }}</span>
              <span class="week">{{ getWeek(item.date) }}</span>
              <span class="dot">·</span>
              <span class="status" v-if="item.status == 1">
                <router-link v-bind:to="item.link" style="color: #F5A623;text-decoration:none">点击参与</router-link>
              </span>
              <span class="status" v-if="item.status == 0">敬请期待</span>
            </div>
          </div>
        </div>
      </div>

      <br><br>
      <span class="title">用户贡献度排行榜</span>
      <br><br>
      <div class="rank">
        <el-table
          class="table"
          border
          stripe
          :data="userRank"
          style="width: 100%;">
          <el-table-column
            prop="username"
            label="用户名"
            width="160">
          </el-table-column>
          <el-table-column
            prop="user_credit"
            label="贡献度"
            width="90">
          </el-table-column>
          <el-table-column
            type="index"
            label="排名"
            width="85">
          </el-table-column>

        </el-table>
      </div>
    </div>
</template>

<script>
    export default {
      name: "Right",
      data () {
        return {
          list: [],
          userRank: []
        }
      },
      created(){
        this.getUserRank()
      },
      mounted () {
        this.getList()
      },
      methods: {
        getList () {
          const obj = [
            {
              date: '2020-05-29',
              title: '论坛沙龙第3期：Python+Vue的搭配',
              status: 0,
              link: ''
            },
            {
              date: '2020-05-22',
              title: '论坛沙龙第2期：学习Java的路径',
              status: 0,
              link: ''
            },
            {
              date: '2020-05-01',
              title: '论坛沙龙第1期：JavaScript的实用窍门',
              status: 1,
              link: '/forum/topic/42'
            },
          ]
          this.list = obj.map(item => {
            item.weekDay = this.getWeek(item.date)
            return item
          })
        },
        // 得到月份的英文
        getEngMonth (date) {
          switch (new Date(date).getMonth()) {
            case 0: return 'JAN'
            case 1: return 'FEB'
            case 2: return 'MAR'
            case 3: return 'APR'
            case 4: return 'MAY'
            case 5: return 'JUN'
            case 6: return 'JUL'
            case 7: return 'AUG'
            case 8: return 'SEP'
            case 9: return 'OCT'
            case 10: return 'NOV'
            case 11: return 'DEC'
          }
        },
        // 得到星期几
        getWeek (date) {
          let result
          switch (new Date(date).getDay()) {
            case 0:
              result = '日'
              break
            case 1:
              result = '一'
              break
            case 2:
              result = '二'
              break
            case 3:
              result = '三'
              break
            case 4:
              result = '四'
              break
            case 5:
              result = '五'
              break
            case 6:
              result = '六'
              break
          }
          return `星期${result}`
        },
        getUserRank () {
          this.axios.get("/forum/userRank", {
          }).then(response => {
            if (response.data.status === 0) {
              this.userRank = response.data.data
            } else {
              this.$message({
                showClose: true,
                message: res.message,
                type: res.success ? 'success' : 'error',
                duration: 3500
              })
            }
          })
        },
      }
    }
</script>

<style lang="scss" scoped>
  @import '@/common/style/base.scss';
  .title{
    .title{
      flex: 1;
      margin-bottom: 15px;
    }
  }
  .activity{
    .head{
      display: flex;
      .title{
        flex: 1;
        margin-bottom: 15px;
      }
      .more{
        color: $theme;
      }
    }
    .item{
      padding: 8px 0;
      display: flex;
      border-bottom: 1px dashed #eee;
      &:last-child{
        border-bottom: none;
      }
      .time{
        height: 36px;
        color: $theme;
        margin-right: 10px;
        background: rgba(218, 133, 133, .5);
        .month, .day{
          width: 32px;
          text-align: center;
        }
        .month{
          height: 16px;
          line-height: 16px;
          font-size: 12px;
          transform: scale(0.833);
        }
        .day{
          height: 20px;
          line-height: 20px;
          background: rgb(255, 233, 233);
        }
      }
      .content{
        color: #999;
        font-size: 12px;
        .title{
          color: #212121;
          font-weight: 500;
          font-size: 14px;
          margin-bottom: 2px;
          line-height: 1.5;
        }
        .status{
          color: #F5A623;
        }
      }
    }
  }
  .new{
    a {
      text-decoration: none;
      color: black;
    }
    .router-link-active{
      text-decoration: none;
    }
  }
</style>
