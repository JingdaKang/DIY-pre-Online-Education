<template>
  <el-table
    :data="followData"
    class="table"
    stripe
    style="width: 100%">
    <el-table-column prop="follow_user_avatar" label="用户" width="120px" >
      <!-- 图片的显示 -->
      <template   slot-scope="scope">
        <img :src="'http://127.0.0.1:8888/media/' + scope.row.follow_user_avatar"  width="100" height="100" />
      </template>
    </el-table-column>
    <el-table-column
      prop="follow_user_username"
      label=""
      width="100">
    </el-table-column>
    <el-table-column
      prop="follow_user_credit"
      label="贡献度"
      width="80">
    </el-table-column>
    <el-table-column
      prop="follow_user_post_num"
      label="发帖数"
      width="80">
    </el-table-column>
    <el-table-column
      prop="follow_user_reply_num"
      label="回复数"
      width="80">
    </el-table-column>
    <el-table-column align="right">
      <template slot-scope="scope">
        <el-button
          size="mini"
          @click="getPostInfo(scope.$index, scope.row)"
          class="el-icon-albb-createtask">查看对方的帖子</el-button>


        <el-dialog :visible.sync="dialogTableVisible">
          <el-table :data="followUserData">
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


        <el-button
          size="mini"
          type="danger"
          class="el-icon-albb-delete1"
          @click="handleDelete(scope.$index, scope.row)">取消关注</el-button>
      </template>
    </el-table-column>

  </el-table>
</template>

<script>
  export default {
    name: "UserFollowing",
    data() {
      return {
        user: window.localStorage.getItem('username'),
        followData:[],
        followUserData:[],
        dialogTableVisible: false,
      }
    },
    created(){
      this.getInfo()
    },
    methods:{
      getInfo(){
        this.axios.get('/forum/userFollowing',{
          params: {
            user: this.user,
          }
        }).then((response)=>{
          if (response.data.status === 0) {
            console.log('userinfo', response)
            this.followData = response.data.data.follow
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
      getPostInfo(index, row){
        this.dialogTableVisible = true
        const getUser = row.follow_user_username
        this.axios.get('/forum/userPost',{
          params: {
            user: getUser,
          }
        }).then((response)=>{
          if (response.data.status === 0) {
            console.log('userinfo', response)
            this.followUserData = response.data.data.topics
          }

        })
          .catch((error)=>{
            console.error('获取信息异常', error)
          })
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
      handleDelete(index, row){
        const id = row.follow_user_id
        this.$confirm('将取消对其的关注, 请确认', '提示', {
          confirmButtonText: '确定',
          cancelButtonText: '取消',
          type: 'warning'
        }).then(() => {
          this.axios.post('/forum/unfollow',{
            follow_on_user: id
          }).then(response => {
            if (response.data.status === 0) {
              this.getInfo()
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
