<template>
  <el-table
    :data="focusData"
    class="table"
    stripe
    style="width: 100%">
    <el-table-column
      prop="discuss_title"
      label="讨论帖标题"
      width="300">
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
      label="回复数"
      width="80">
    </el-table-column>
    <el-table-column align="right">
      <template slot-scope="scope">
        <el-button
          size="mini"
          @click="openDetails(scope.$index, scope.row)"
          class="el-icon-albb-skip">打开</el-button>
      </template>
    </el-table-column>

  </el-table>
</template>

<script>
  export default {
    name: "UserFocus",
    data() {
      return {
        user: window.localStorage.getItem('username'),
        focusData:[],

      }
    },
    created(){
      this.getInfo()
    },
    methods:{
      getInfo(){
        this.axios.get('/forum/userFocus',{
          params: {
            user: this.user,
          }
        }).then((response)=>{
          if (response.data.status === 0) {
            console.log('userinfo', response)
            this.focusData = response.data.data.focus
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
    }
  }
</script>



<style scoped lang="scss">
  .table{

  }
</style>
