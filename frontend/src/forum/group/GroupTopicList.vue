<template>
  <ul class="page-topic-list">
    <template v-if="listInfo.data.length > 0">
      <li v-for="(item, index) in listInfo.data.slice((curPage-1) * pageSize,
      curPage * pageSize)" :key="index" class="topic-item" @click="handleGoto(item.discuss_id)">
        <div class="from" />
        <div class="topic">
          <div class="content">
            <p class="title">{{ item.discuss_title }}</p>
          </div>
        </div>
        <div class="info" @click.stop="">

          <div class="click">
            <span class="wrap"><i class="el-icon-albb-browse" /></span>
            <span class="clicknums">{{ item.discuss_click_num }}</span>
            <span class="word">点击</span>
          </div>
          <span>&nbsp &nbsp &nbsp</span>
          <div class="reply">
            <span class="wrap"><i class="el-icon-albb-comments" /></span>
            <span class="replynums">{{ item.discuss_reply_num }}</span>
            <span class="word">回复</span>
          </div>


          <div class="author" @click.stop="handleClick('clickAuthor', item)">{{ item.discuss_username }}</div>
          <span class="dot" style="padding: 0 5px">·</span>
          <div class="release-time">{{item.discuss_reply_time | formatterDate}}</div>
        </div>
      </li>
    </template>
    <p v-else class="no-data">
    </p>
    <div class="pagination">
      <el-pagination
        background
        @current-change="handleCurrentChange"
        :current-page="curPage"
        :page-size="pageSize"
        layout="prev, pager, next"
        :total="totalCount">
      </el-pagination>
    </div>
  </ul>
</template>

<script>
export default {
  name: 'GroupTopicList',
  props: {
    bolgData: {
      type: Object
    }
  },
  data () {
    return {
      user: window.localStorage.getItem('username'),
      curPage: 1,
      totalCount:1,
      pageSize:6,
      tab: 1,
      listInfo: {
        data: [],
      }
    }
  },
  created () {
    this.receiveEventBus()
  },
  methods: {
    receiveEventBus () {
      // 接收eventBus （点击侧边栏，获取符合条件的数据）
      this.$eventBus.$off('sidebar-click-group');
      this.$eventBus.$on('sidebar-click-group', data => {
        this.tab = data.id
        this.listInfo.data=[]
        this.getList()
        this.curPage = 1

      })
    },
    getList () {
      this.axios.get("/forum/discuss/", {
        params: {
          user: this.user,
          page: this.page,
          tab: this.tab
        }
      }).then(response => {
        if (response.data.status === 0) {
          console.log("topics", response)
          this.listInfo.data = response.data.data
          console.log("list", this.listInfo)
          this.totalCount = this.listInfo.data.length
        } else {
          this.$message({
            showClose: true,
            message: response.message,
            type: response.success ? 'success' : 'error',
            duration: 3500
          })
        }
      })
    },
    handleGoto (id) {
      this.$router.push({
        path: `/forum/discuss/${id}`
      })
    },
    handleClick (type, data) {
      switch (type) {
        case 'praise':
          break
        case 'clickAuthor':
          break
      }
    },
    handleCurrentChange(val) {
      // 改变默认的页数
      this.curPage=val
      document.body.scrollTop = 0
      document.documentElement.scrollTop = 0
    },
  }
}
</script>

<style scoped lang="scss">
  @import '@/common/style/base.scss';
  .page-topic-list{
    font-size: 13px;
    .pagination{
      margin-top: 30px;
    }
    .topic-item{
      margin: 20px 0;
      .topic{
        cursor: pointer;
        display: flex;
        .content{
          margin: 10px 0;
          .title{
            margin-bottom: 10px;
            font-size: 18px;
            color: #212121;
          }
          .body{
            color: #888;
            line-height: 1.5;
            // 超出两行显示省略号
            overflow: hidden;
            display: -webkit-box;
            -webkit-line-clamp: 2;
            -webkit-box-orient: vertical;
          }
          &:hover{
            .title, .body{
              text-decoration: underline;
            }
          }
        }
        .img{
          margin-top: 15px;
          margin-left: 20px;
          width: 120px;
          height: 60px;
          border-radius: 4px;
          background-size: cover;
          background-position: center;
        }
      }
      .info{
        display: flex;
        align-items: center;
        transition: all .3s linear;
        .click{
          cursor: pointer;
          user-select: none;
          .wrap{
            display: inline-block;
            width: 24px;
            height: 24px;
            border-radius: 50%;
            background: rgba(1,126,102,0.08);
            text-align: center;
            line-height: 24px;
            .el-icon-browse{
              font-size: 14px;
              font-weight: bold;
              color: #009a61;
            }
          }
          &:hover{
            transform: all;
            transition: .3s;
            .wrap{
              transition: .3s;
              background: #009a61;
            }
            .el-icon-albb-browse{
              font-weight: bold;
              color: rgb(245, 245, 245);
            }
            .word{
              color: #009a61;
              text-decoration: underline;
            }
          }
        }

        .reply{
          cursor: pointer;
          user-select: none;
          .wrap{
            display: inline-block;
            width: 24px;
            height: 24px;
            border-radius: 50%;
            background: rgba(1,126,102,0.08);
            text-align: center;
            line-height: 24px;
            .el-icon-comments{
              font-size: 14px;
              font-weight: bold;
              color: #009a61;
            }
          }
          &:hover{
            transform: all;
            transition: .3s;
            .wrap{
              transition: .3s;
              background: #009a61;
            }
            .el-icon-albb-comments{
              font-weight: bold;
              color: rgb(245, 245, 245);
            }
            .word{
              color: #009a61;
              text-decoration: underline;
            }
          }
        }


        .praise{
          cursor: pointer;
          user-select: none;
          .wrap{
            display: inline-block;
            width: 24px;
            height: 24px;
            border-radius: 50%;
            background: rgba(1,126,102,0.08);
            text-align: center;
            line-height: 24px;
            .el-icon-good{
              font-size: 14px;
              font-weight: bold;
              color: #009a61;
            }
          }
          &:hover{
            transform: all;
            transition: .3s;
            .wrap{
              transition: .3s;
              background: #009a61;
            }
            .el-icon-albb-good{
              font-weight: bold;
              color: rgb(245, 245, 245);
            }
            .word{
              color: #009a61;
              text-decoration: underline;
            }
          }
        }
        .author{
          margin-left: 20px;
          font-weight: bold;
          cursor: pointer;
          &:hover{
            text-decoration: underline;
          }
        }
        .votes-word, .author{
          color: #666;
        }
        .release-time{
          color: #999;
        }
        .unit{
          padding: 0 5px;
        }
        .unit {
          font-weight: 400;
          color: #009a61;
        }
      }
    }
    .no-data{
      height: 100%;
      font-size: 36px;
      padding: 40px;
      text-align: center;
    }
  }
</style>
