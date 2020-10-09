<template>
  <el-table
    :data="repliesData"
    class="table"
    stripe
    style="width: 100%">
    <el-table-column
      prop="reply_discuss_title"
      label="小组讨论标题"
      width="300">
    </el-table-column>
    <el-table-column
      prop="reply_time"
      label="回复日期"
      width="120">
      <template slot-scope="scope">
        <span>{{timestampToTime(scope.row.reply_time)}}</span>
      </template>
    </el-table-column>
    <el-table-column
      prop="reply_content"
      label="回复内容"
      width="200"
      :show-overflow-tooltip="true">
    </el-table-column>
    <el-table-column align="right">
      <template slot-scope="scope">
        <el-button
          size="mini"
          @click="openDetails(scope.$index, scope.row)"
          class="el-icon-albb-skip">打开</el-button>
        <el-button
          size="mini"
          type="danger"
          class="el-icon-albb-delete1"
          @click="handleDelete(scope.$index, scope.row)">删除</el-button>
      </template>
    </el-table-column>

  </el-table>
</template>

<script>
  export default {
    name: "UserDiscussReply",
    data() {
      return {
        user: window.localStorage.getItem('username'),
        repliesData:[],

      }
    },
    created(){
      this.getPostInfo()
    },
    methods:{
      getPostInfo(){
        this.axios.get('/forum/userDiscuss',{
          params: {
            user: this.user,
          }
        }).then((response)=>{
          if (response.data.status === 0) {
            console.log('userinfo', response)
            this.repliesData = response.data.data.replies
          }

        })
          .catch((error)=>{
            console.error('获取信息异常', error)
          })
      },
      timestampToTime(timestamp) {
        var date = new Date(timestamp);//时间戳为10位需*1000，时间戳为13位的话不需乘1000
        var Y = date.getFullYear() + '-';
        var M = (date.getMonth()+1 < 10 ? '0'+(date.getMonth()+1) : date.getMonth()+1) + '-';
        var D = (date.getDate() < 10 ? '0'+date.getDate() : date.getDate()) + ' ';
        var h = (date.getHours() < 10 ? '0'+date.getHours() : date.getHours()) + ':';
        var m = (date.getMinutes() < 10 ? '0'+date.getMinutes() : date.getMinutes()) + ':';
        var s = (date.getSeconds() < 10 ? '0'+date.getSeconds() : date.getSeconds());
        return Y+M+D;
      },
      openDetails (index, row) {
        const openid = row.reply_discuss_id
        console.log("openid", openid)
        const {href} = this.$router.resolve({
          name: "DiscussInfo",
          params: {
            id: openid,
          }
        });
        window.open(href, '_blank');
      },
      handleDelete(index, row){
        const id = row.reply_id
        this.$confirm('此操作将永久删除该回复, 请确认', '提示', {
          confirmButtonText: '确定',
          cancelButtonText: '取消',
          type: 'warning'
        }).then(() => {
          this.axios.post('/forum/deleteDiscussReply',{
            discuss_reply_id: id
          }).then(response => {
            if (response.data.status === 0) {
              this.getPostInfo()
            }
            this.$message({
              showClose: true,
              message: response.data.message,
              type: response.success === 0 ? 'success' : 'error',
              duration: 2000
            })
          })
        })

      }
    }
  }
</script>



<style scoped lang="scss">
  .table{

  }
</style>
