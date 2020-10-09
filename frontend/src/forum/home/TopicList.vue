<template>
  <div>
    <ul class="page-topic-list">
      <template v-if="listInfo.data.length > 0">
        <li v-for="(item, index) in listInfo.data.slice((curPage-1) * pageSize,
      curPage * pageSize)" :key="index" class="topic-item" @click="handleGoto(item.topic_id)">
          <div class="from" />
          <div class="topic">
            <div class="content">
              <p class="title">{{ item.topic_title }}</p>
              <p class="body">{{ item.topic_content }}</p>
            </div>
          </div>
          <div class="info" @click.stop="">

            <div class="click">
              <span class="wrap"><i class="el-icon-albb-browse" /></span>
              <span class="clicknums">{{ item.topic_click_num }}</span>
              <span class="word">点击</span>
            </div>
            <span>&nbsp &nbsp &nbsp</span>
            <div class="reply">
              <span class="wrap"><i class="el-icon-albb-comments" /></span>
              <span class="replynums">{{ item.topic_reply_num }}</span>
              <span class="word">回复</span>
            </div>
            <span>&nbsp &nbsp &nbsp</span>
            <div class="praise">
              <span class="wrap"><i class="el-icon-albb-good" /></span>
              <span class="praisenums">{{ item.topic_like_num }}</span>
              <span class="word">赞</span>
            </div>
            &nbsp&nbsp&nbsp&nbsp&nbsp&nbsp
            <img :src="'http://127.0.0.1:8888/media/' + item.topic_avatar_url" class="avatar" />
            <div class="author" @click.stop="handleClick('clickAuthor', item)">{{ item.topic_username }}</div>
            <span class="dot" style="padding: 0 5px">·</span>
            <div class="release-time">{{item.topic_create_time | formatterDate}}</div>
          </div>
        </li>
      </template>

    </ul>
    <el-pagination
      background
      @current-change="handleCurrentChange"
      :current-page="curPage"
      :page-size="pageSize"
      layout="prev, pager, next"
      :total="totalCount">
    </el-pagination>
  </div>

</template>

<script>
export default {
  name: 'TopicList',
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
      pageSize:5,
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
      this.$eventBus.$off('sidebar-click');
      this.$eventBus.$on('sidebar-click', data => {
        this.tab = data.id
        this.listInfo.data=[]
        this.getList()
        this.curPage = 1
      })
    },
    getList () {
      this.axios.get("/forum/topics/", {
        params: {
          tab: this.tab,
        }
      }).then(response => {
        if (response.data.status === 0) {
          console.log("topics", response)
          this.listInfo.data = response.data.data
          console.log("list", this.listInfo.data.length)
          this.totalCount = this.listInfo.data.length
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
    handleGoto (id) {
      this.$router.push({
        path: `/forum/topic/${id}`
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
      document.body.scrollTop = 200
      document.documentElement.scrollTop = 200
    },
  }
}
</script>

<style scoped lang="scss">
  @import '@/common/style/base.scss';
  .page-topic-list{
    font-size: 13px;
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
            background: rgba(218, 133, 133, .2);
            text-align: center;
            line-height: 24px;
            .el-icon-browse{
              font-size: 14px;
              font-weight: bold;
              color: $theme;
            }
          }
          &:hover{
            transform: all;
            transition: .3s;
            .wrap{
              transition: .3s;
              background: $theme;
            }
            .el-icon-albb-browse{
              font-weight: bold;
              color: rgb(245, 245, 245);
            }
            .word{
              color: $theme;
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
            background: rgba(218, 133, 133, .2);
            text-align: center;
            line-height: 24px;
            .el-icon-comments{
              font-size: 14px;
              font-weight: bold;
              color: $theme;
            }
          }
          &:hover{
            transform: all;
            transition: .3s;
            .wrap{
              transition: .3s;
              background: $theme;
            }
            .el-icon-albb-comments{
              font-weight: bold;
              color: rgb(245, 245, 245);
            }
            .word{
              color: $theme;
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
            background: rgba(218, 133, 133, .2);
            text-align: center;
            line-height: 24px;
            .el-icon-good{
              font-size: 14px;
              font-weight: bold;
              color: $theme;
            }
          }
          &:hover{
            transform: all;
            transition: .3s;
            .wrap{
              transition: .3s;
              background: $theme;
            }
            .el-icon-albb-good{
              font-weight: bold;
              color: rgb(245, 245, 245);
            }
            .word{
              color: $theme;
              text-decoration: underline;
            }
          }
        }
        .avatar{
          display: inline-block;
          width: 30px;
          height: 30px;
          border-radius: 50%;
          background-size: cover;
          background-position: center;
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
          color: $theme;
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
