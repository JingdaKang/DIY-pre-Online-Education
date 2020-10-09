<template>
  <div class="page-container">
    <div class="main">
      <div class="">{{topicDetail.group_name}} / 讨论详情</div>
      <div class="author-info">
        <router-link :to="''" class="author">
          <img :src="'http://127.0.0.1:8888/media/' + topicDetail.discuss_avatar_url" class="avatar" />
        </router-link>
        <div class="release-info">
          <div class="">
            <router-link :to="''" class="author">{{ topicDetail.discuss_username }}</router-link>
            <span>&nbsp&nbsp 贡献度 {{topicDetail.discuss_user_credit}}</span>
            &nbsp&nbsp
            <el-button class="el-icon-albb-email" type="danger" size="mini" :disabled="!user"
                       @click="openCreateMessage(topicDetail.discuss_username)">&nbsp 私信
            </el-button>
            <el-dialog title="发送消息" :visible.sync="dialogFormVisible">
              <el-form :model="messageForm" label-width="100px">
                <el-form-item label="对方用户名: ">
                  <span v-model="messageForm.receive_username" readonly=true>{{messageForm.receive_username}}</span>
                </el-form-item>
                <el-form-item label="消息内容: ">
                  <el-input type="textarea" v-model="messageForm.message_content"></el-input>
                </el-form-item>
              </el-form>
              <div slot="footer" class="dialog-footer">
                <el-button @click="dialogFormVisible = false">取 消</el-button>
                <el-button type="primary" @click="createMessage()">确 定</el-button>
              </div>
            </el-dialog>


          </div>
          <span class="time">发布于 {{topicDetail.discuss_time | formatterDate}}</span>
        </div>
      </div>
      <p class="title">{{ topicDetail.discuss_title }}</p>
      <div class="topic-info">
        <span class="more">
          <span class="read-times">{{topicDetail.discuss_click_num}} 次浏览</span>
        </span>
      </div>
      <!-- 文章内容渲染 -->
      <div class="markdown" v-html="marked(topicDetail.discuss_content)" v-highlight/>

      <div class="file" v-if="topicDetail.discuss_content_file_check === true">
        <h3>附件下载</h3>
        <el-link :href="'http://127.0.0.1:8888/media/' + topicDetail.file_url">{{topicDetail.file_name}}</el-link>
      </div>
      <br><br>


      <div class="handle">
        <div class="">
          <span class="focus" @click="focusDiscuss()"><i class="el-icon-albb-group" >  {{topicDetail.if_focus === 1?"已关注该讨论贴":"关注该讨论贴"}}  </i></span>
        </div>
      </div>
      <!-- 评论 -->
      <div class="comments">
        <ul class="comments-list">
          <li v-for="(item, index) in replies" :key="index" class="items">
            <img :src="'http://127.0.0.1:8888/media/' + item.discuss_reply_avatar_url" class="avatar" />
            <div class="content">
              <div class="replier-head">
                <div class="replier-info">
                  <span class="replier-user">{{ item.discuss_reply_username }}</span>
                  <span v-if="item.discuss_reply_username === topicDetail.discuss_username" class="tag original">楼主</span>

                  <el-button class="el-icon-albb-email" type="danger" size="mini" :disabled="!user" circle
                             @click="openCreateMessage(item.discuss_reply_username)">
                  </el-button>
                  ·
                  <span class="replier-time">{{index + 1}}楼 • {{item.discuss_reply_time | formatterDate}}</span>
                </div>
                <div class="more">
                  <i v-if="item.discuss_reply_username === user" class="el-icon-albb-delete1" @click="handleClick('delete', item)">
                    删除
                  </i>
                </div>
              </div>
              <div class="replier-content">
                {{ item.discuss_reply_content }}
              </div>
            </div>
          </li>
        </ul>
        <div class="release">
          <div class="handle">
            <el-input v-model="commentsInfo.data.reply_content" type="textarea" :rows="3" placeholder="请输入你的回复（仅限小组成员或关注该讨论帖的用户发帖）" />
            <p style="width: 100%; text-align: right">
              <el-button type="primary" class="release-bt" :disabled="!user" @click="user ? handleClick('release') : ''">
                {{ user ? '发布回贴' : '登录后可发布回帖' }}
              </el-button>
            </p>
          </div>
        </div>
      </div>
    </div>
    <div class="right">
      <h2>作者的其他帖子</h2>
      <el-table
        class="table"
        :data="userOtherDiscuss"
        style="width: 100%"
        @row-click="openDiscuss"
        :show-header="false">
        <el-table-column
          prop="discuss_title"
          label="标题"
          width="200">
          <template slot-scope="scope">
            <span style="color: red">{{scope.row.discuss_title}}</span>
          </template>
        </el-table-column>

      </el-table>
    </div>
  </div>
</template>

<script>
  import marked from '@/common/js/marked'
  export default {
    components: {
    },
    data () {
      return {
        user: window.localStorage.getItem('username'),
        marked,
        listInfo: {
          data: [],
        },
        topicDetail: {},
        replies:[],
        commentsInfo: {
          listSuccess: true,
          list: [],
          totals: 0,
          data: {
            user: '',
            reply_topic_id: '',
            reply_content: ''
          }
        },
        userOtherDiscuss:[],
        dialogFormVisible: false,
        messageForm:{
          receive_username: '',
          message_content: ''
        }
      }
    },
    computed: {
    },
    created(){
      this.init()
      this.getTopicDetail()

    },
    methods: {
      init () {
        const commentsData = this.commentsInfo.data
        commentsData.reply_topic_id = this.$route.params.id
      },
      getTopicDetail () {
        this.axios.get('/forum/discuss/' + this.$route.params.id + '/')
          .then(response => {
            if (response.data.status === 0) {
              console.log("topicDetail", response.data.data)
              this.topicDetail = response.data.data
              this.replies = response.data.data.replies
              this.userOtherDiscuss = response.data.data.user_other_discuss

            }
          })
          .catch(err => {
            console.error("获取详情异常", err)
          });

      },


      handleClick (type, data) {
        const commentsData = this.commentsInfo.data
        switch (type) {
          case 'release':
            commentsData.user = this.user
            this.releaseComments(commentsData)
            break
          case 'delete':
            this.deleteComments(data.discuss_reply_id)
            break
        }
      },
      releaseComments (query) {
        const commentsData = this.commentsInfo.data
        this.axios.post('/forum/addDiscussReply',{
          discuss_id: commentsData.reply_topic_id,
          discuss_reply_content: commentsData.reply_content
        }).then(response => {
          if (response.data.status === 0) {
            commentsData.reply_content = ''
            this.$message({
              showClose: true,
              message: response.data.message,
              type: response.success === 0 ? 'success' : 'error',
              duration: 2000
            })
            this.getTopicDetail()
          } else {
            this.$message({
              showClose: true,
              message: response.data.message,
              type: response.success === 0 ? 'success' : 'error',
              duration: 2000
            })
          }
        })
      },
      deleteComments (id) {
        this.$confirm('此操作将永久删除该回复, 请确认', '提示', {
          confirmButtonText: '确定',
          cancelButtonText: '取消',
          type: 'warning'
        }).then(() => {
          this.axios.post('/forum/deleteDiscussReply',{
            discuss_reply_id: id
          }).then(response => {
            if (response.data.status === 0) {
              this.getTopicDetail()
            }
            this.$message({
              showClose: true,
              message: response.data.message,
              type: response.success === 0 ? 'success' : 'error',
              duration: 2000
            })
          })
        })
      },
      focusDiscuss () {
        const commentsData = this.commentsInfo.data
        this.axios.post('/forum/focusDiscuss',{
          discuss_id: commentsData.reply_topic_id
        }).then(response => {
          if (response.data.status === 0) {
            this.$message({
              showClose: true,
              message: response.data.message,
              type: response.success === 0 ? 'success' : 'error',
              duration: 2000
            })
            this.getTopicDetail()
          } else {
            this.$message({
              showClose: true,
              message: response.data.message,
              type: response.success === 0 ? 'success' : 'error',
              duration: 2000
            })
          }
        })
      },
      openDiscuss(row){
        const discuss_id = row.discuss_id
        const {href} = this.$router.resolve({
          name: "DiscussInfo",
          params: {
            id: discuss_id,
          }
        });
        window.open(href, '_blank');
      },
      openCreateMessage(name){
        this.messageForm ={brand_right:0}
        this.messageForm.receive_username = name
        this.dialogFormVisible = true
      },
      createMessage(){
        const data = this.messageForm
        this.axios.post('/forum/addMessage',{
          receive_username: data.receive_username,
          message_content: data.message_content
        }) .then(response => {
          if (response.data.status === 0) {
            this.dialogFormVisible = false
            this.form={brand_right:0}
            this.$message({
              showClose: true,
              message: response.data.message,
              type: response.success === 0 ? 'success' : 'error',
              duration: 2000
            })
          } else {
            this.$message({
              showClose: true,
              message: response.data.message,
              type: response.success === 0 ? 'success' : 'error',
              duration: 2000
            })
          }
        })

      },
    }
  }
</script>

<style lang="scss" scoped>
  .page-container{
    width: 75%;
    margin-left: 200px;
    display: flex;
    .main{
      width: 75%;
      padding-left: 10px;
      .author-info{
        display: flex;
        margin: 20px 0;
        .avatar{
          display: inline-block;
          width: 40px;
          height: 40px;
          border-radius: 50%;
          background-size: cover;
          background-position: center;
        }
        .release-info{
          margin-left: 10px;
          .author, .time{
            padding: 2px 0;
          }
          .author{
            display: inline-block;
            font-size: 16px;
            font-weight: bold;
            color: red;
            &:hover{
              text-decoration: underline;
            }
          }
          .focus{
            margin-left: 10px;
          }
          .time{
            display: block;
          }
        }
      }
      .title{
        font-size: 30px;
        font-weight: bold;
        color: black;
        margin-bottom: 20px;
      }
      .topic-info{
        margin-bottom: 40px;
        color: #999;
        .tag{
          display: inline-block;
          padding: 5px 10px;
        }
        .original{
          color: #017E66;
          background: rgba(1,126,102,0.08);
        }
        .more{
          margin-left: 10px;
          .update{
            margin: 10px 0;
            display: inline-block;
            color: red;
            opacity: .8;
            &:hover{
              opacity: 1;
              text-decoration: underline;
            }
          }
        }
      }
      .markdown{
        margin-bottom: 40px;
      }
      .handle{
        display: flex;
        flex-direction: column;
        align-items: center;
        margin-bottom: 40px;
        .focus{
          cursor: pointer;
          margin: 0 10px;
          margin-bottom: 10px;
          display: inline-flex;
          align-items: center;
          justify-content: center;
          padding: 10px 16px;
          height: 45px;
          min-width: 90px;
          color: white;
          border: 1px solid #ccc;
          border-radius: 5px;
          box-shadow: 0 1px 1px rgba(0,0,0,0.05);
          font-size: 18px;
          transition: all .2s linear;
          user-select: none;
        }

        .focus{
          background: #00965e;
        }
      }
      .recommended{
        margin-bottom: 40px;
        .title{
          font-size: 18px;
          font-weight: 300;
          color: rgb(50, 50, 50);
          margin-bottom: 20px;
        }
        .item{
          margin-bottom: 5px;
          .recommended-topic{
            padding-right: 10px;
            color: red;
            opacity: .8;;
          }
          &:hover{
            .recommended-topic{
              opacity: 1;
              text-decoration: underline;
            }
          }
        }
      }
      .original{
        color: #017E66;
        background: rgba(1,126,102,0.08);
      }
      .tag{
        display: inline-block;
        padding: 5px 10px;
      }
      .comments{
        margin-bottom: 40px;
        .title{
          font-size: 18px;
          font-weight: 300;
          color: rgb(50, 50, 50);
          margin-bottom: 20px;
        }
        .comments-list{
          padding: 10px;
          .items{
            display: flex;
            border-top: 1px solid rgb(230, 230, 230);
            padding-top: 10px;
            &:hover{
              .content{
                .replier-head{
                  .more{
                    display: block;
                    color: red;
                  }
                }
              }
            }
            .avatar{
              display: inline-block;
              width: 40px;
              height: 40px;
              border-radius: 50%;
              background-size: cover;
              background-position: center;
            }
            .content{
              margin-left: 10px;
              flex: 1;
              .replier-head, .replier-content, .replier-more, .reply-list{
                margin-bottom: 10px;
              }
              .replier-head{
                display: flex;
                justify-content: space-between;
                .replier-user, .replier-time{
                  cursor: pointer;
                }
                .replier-user{
                  color: red;
                  &:hover{
                    text-decoration: underline;
                  }
                }
                .more{
                  display: none;
                  cursor: pointer;
                }
              }
              .replier-more{
                .praise, .reply{
                  padding-right: 10px;
                  cursor: pointer;
                }
              }
              .reply-list{
                .reply-item{
                  padding: 10px 20px;
                  line-height: 1.5;
                  background-color: rgb(245, 245, 245);
                  border-bottom: 1px dashed rgb(200, 200, 200);
                  .reply-user, .by-reply-user{
                    color: red;
                    cursor: pointer;
                    &:hover{
                      text-decoration: underline;
                    }
                  }
                  .reply-more{
                    .praise, .reply{
                      padding-right: 10px;
                      cursor: pointer;
                    }
                  }
                }
                .reply-handle{
                  display: flex;
                  padding: 10px;
                  background-color: rgb(245, 245, 245);
                  .reply-bt{
                    margin-left: 10px;
                  }
                }
              }
            }
          }
        }
        .release{
          display: flex;
          padding: 10px;
          border: 1px solid rgb(240, 240, 240);
          border-radius: 5px;
          background: rgb(248, 248, 248);
          .avatar{
            display: inline-block;
            width: 40px;
            height: 40px;
            border-radius: 50%;
            background-size: cover;
            background-position: center;
          }
          .handle{
            margin-left: 10px;
            margin-bottom: 0px;
            flex: 1;
            .release-bt{
              margin-top: 10px;
              user-select: none;
            }
          }
        }
      }
    }
    .right{
      margin-left: 5%;
      width: 20%;
    }
  }
</style>

