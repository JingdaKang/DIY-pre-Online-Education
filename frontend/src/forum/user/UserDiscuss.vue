<template>
  <el-table
    :data="discussData"
    class="table"
    stripe
    style="width: 100%">
    <el-table-column
      prop="discuss_title"
      label="标题"
      width="300">
    </el-table-column>
    <el-table-column
      prop="group_name"
      label="小组"
      width="120">
    </el-table-column>
    <el-table-column
      prop="discuss_time"
      label="发布日期"
      width="120">
      <template slot-scope="scope">
        <span>{{timestampToTime(scope.row.discuss_time)}}</span>
      </template>
    </el-table-column>
    <el-table-column
      prop="discuss_reply_num"
      label="讨论量"
      width="70">
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
          class="el-icon-albb-survey"
          @click="edit(scope.$index, scope.row)">编辑</el-button>
      </template>
    </el-table-column>
  </el-table>
</template>

<script>
  export default {
    name: "UserDiscuss",
    data() {
      return {
        user: window.localStorage.getItem('username'),
        discussData:[],
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
            this.discussData = response.data.data.discuss
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
        const openid = row.discuss_id
        console.log("openid", openid)
        const {href} = this.$router.resolve({
          name: "DiscussInfo",
          params: {
            id: openid,
          }
        });
        window.open(href, '_blank');
      },
      edit (index, row) {
        const openid = row.discuss_id
        console.log("openid", openid)
        const {href} = this.$router.resolve({
          name: "EditDiscuss",
          params: {
            id: openid,
          }
        });
        window.open(href, '_blank');
      },
    }
  }
</script>



<style scoped lang="scss">
  .table{
  }
</style>
