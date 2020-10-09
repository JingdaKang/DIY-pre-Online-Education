<template>
  <el-table
    :data="applyData"
    class="table"
    stripe
    style="width: 100%">
    <el-table-column
      prop="apply_group_name"
      label="申请小组"
      width="150">
    </el-table-column>
    <el-table-column
      prop="apply_username"
      label="申请用户"
      width="100">
    </el-table-column>
    <el-table-column
      prop="apply_message"
      label="申请附言"
      width="300">
    </el-table-column>
    <el-table-column align="right">
      <template slot-scope="scope">

        <el-button
          size="mini"
          type="info"
          @click="getPostInfo(scope.$index, scope.row)"
          class="el-icon-albb-createtask">查看对方的帖子</el-button>
        <el-dialog :visible.sync="dialogTableVisible">
          <el-table :data="applyUserData">
            <el-table-column property="topic_title" label="标题" width="200"></el-table-column>
            <el-table-column property="section_name" label="板块"></el-table-column>
            <el-table-column property="topic_time" label="日期" width="120">      <template slot-scope="scope1">
              <span>{{timestampToTime(scope1.row.topic_time)}}</span>
            </template></el-table-column>
            <el-table-column align="right">
              <template slot-scope="scope1">
                <el-button
                  size="mini"
                  @click="openDetails(scope1.$index, scope1.row)"
                  class="el-icon-albb-skip">打开</el-button>
              </template>
            </el-table-column>
          </el-table>
        </el-dialog>

        &nbsp&nbsp
        <el-button
          size="mini"
          type="primary"
          @click="handle(scope.$index, scope.row, 1)"
          class="el-icon-albb-right">同意</el-button>
        <el-button
          size="mini"
          type="danger"
          class="el-icon-albb-close"
          @click="handle(scope.$index, scope.row, 0)">拒绝</el-button>
      </template>
    </el-table-column>

  </el-table>
</template>

<script>
  export default {
    name: "UserApply",
    data() {
      return {
        user: window.localStorage.getItem('username'),
        applyData:[],
        applyUserData:[],
        dialogTableVisible: false,

      }
    },
    created(){
      this.getApplyInfo()
    },
    methods:{
      getApplyInfo(){
        this.axios.get('/forum/receiveApply',{
        }).then((response)=>{
          if (response.data.status === 0) {
            console.log('userinfo', response)
            this.applyData = response.data.data.apply
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
        const openid = row.topic_id
        console.log("openid", openid)
        const {href} = this.$router.resolve({
          name: "TopicInfo",
          params: {
            id: openid,
          }
        });
        window.open(href, '_blank');
      },
      getPostInfo(index, row){
        this.dialogTableVisible = true
        const getUser = row.apply_username
        this.axios.get('/forum/userPost',{
          params: {
            user: getUser,
          }
        }).then((response)=>{
          if (response.data.status === 0) {
            console.log('userinfo', response)
            this.applyUserData = response.data.data.topics
          }

        })
          .catch((error)=>{
            console.error('获取信息异常', error)
          })
      },
      handle(index, row, handleResult){
        const id = row.apply_id
        this.$confirm('是否确认处理该请求', '提示', {
          confirmButtonText: '确定',
          cancelButtonText: '取消',
          type: 'warning'
        }).then(() => {
          this.axios.post('/forum/handleApply',{
            group_apply_id: id,
            handle_result: handleResult
          }).then(response => {
            if (response.data.status === 0) {
              this.getApplyInfo()
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
