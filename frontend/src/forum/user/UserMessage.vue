<template>
  <div>
    <el-button class="el-icon-albb-email" type="primary" @click="openCreateMessage()">&nbsp 发送新消息
    </el-button>
    <el-dialog title="发送新消息" :visible.sync="dialogFormVisible">
      <el-form :model="form" label-width="100px">
        <el-form-item label="对方用户名">
          <el-input v-model="form.receive_username"></el-input>
        </el-form-item>
        <el-form-item label="消息内容">
          <el-input type="textarea" v-model="form.message_content"></el-input>
        </el-form-item>
      </el-form>
      <div slot="footer" class="dialog-footer">
        <el-button @click="dialogFormVisible = false">取 消</el-button>
        <el-button type="primary" @click="createMessage()">确 定</el-button>
      </div>
    </el-dialog>

    <br><br>
    <h2>我的消息</h2>
    <el-table
      :data="messageData"
      class="table"
      stripe
      style="width: 100%">
      <el-table-column
        label=""
        width="50">
        <template slot-scope="scope">
          <span v-if="scope.row.message_read == false"
             style="background-color: #f13f40;
             color: white;
             font-size: 13px;
                   ">未读</span>
        </template>
      </el-table-column>
      <el-table-column
        prop="message_send_user"
        label="发送人"
        width="120">
      </el-table-column>
      <el-table-column
        prop="message_time"
        label="发送时间"
        width="120">
        <template slot-scope="scope">
          <span>{{timestampToTime(scope.row.message_time)}}</span>
        </template>
      </el-table-column>
      <el-table-column
        prop="message_content"
        label="内容"
        width="200">
      </el-table-column>
      <el-table-column align="right">
        <template slot-scope="scope">
          <el-button v-if="scope.row.message_related_type === 0"
            size="mini"
            type="info"
            @click="getMessageDetail(scope.$index, scope.row);
            handleRead(scope.$index, scope.row, 0)"
            class="el-icon-albb-createtask">消息详情</el-button>

          <el-button v-if="scope.row.message_related_type === 1"
                     size="mini"
                     @click="openTopic(scope.$index, scope.row);
                     handleRead(scope.$index, scope.row, 0)"
                     class="el-icon-albb-skip">查看此帖子</el-button>
          <el-button v-if="scope.row.message_related_type === 2"
                     size="mini"
                     @click="openDiscuss(scope.$index, scope.row);
                     handleRead(scope.$index, scope.row, 0)"
                     class="el-icon-albb-skip">查看此小组讨论</el-button>

          <el-dialog title="消息详情" :visible.sync="messageInfoFormVisible" align="left">
            <el-form label-width="100px">
              <el-form-item label="对方用户名">
                <span>{{messageInfoform.message_send_user}}</span>
              </el-form-item>
              <el-form-item label="发送时间">
                <span>{{timestampToTime(scope.row.message_time)}}</span>
              </el-form-item>
              <el-form-item label="消息内容">
                <span>{{messageInfoform.message_content}}</span>
              </el-form-item>
              <el-form-item>
                <el-button type="primary" @click="replyMessage(messageInfoform.message_send_user)">回复</el-button>
              </el-form-item>
            </el-form>
          </el-dialog>
          &nbsp&nbsp

          <el-button
            v-if="scope.row.message_read == false"
            size="mini"
            type="success"
            @click="handleRead(scope.$index, scope.row, 1)"
            class="el-icon-albb-selected">
            标为已读</el-button>

          <el-button
            size="mini"
            type="danger"
            @click="handleDelete(scope.$index, scope.row)"
            class="el-icon-albb-delete1">
            删除</el-button>
        </template>
      </el-table-column>

    </el-table>
  </div>

</template>

<script>
  export default {
    name: "UserMessage",
    data() {
      return {
        user: window.localStorage.getItem('username'),
        messageData:[],
        dialogTableVisible: false,
        dialogFormVisible: false,
        messageInfoFormVisible: false,
        form: {
          receive_username: '',
          message_content: ''
        },
        messageInfoform: {
          message_send_user: '',
          message_content: ''
        },
      }
    },
    created(){
      this.getMessageInfo()
    },
    methods:{
      getMessageInfo(){
        this.axios.get('/forum/message',{
        }).then((response)=>{
          if (response.data.status === 0) {
            console.log('userinfo', response)
            this.messageData = response.data.data.message
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
      getMessageDetail(index, row){
        this.messageInfoform.message_send_user = row.message_send_user
        this.messageInfoform.message_content = row.message_content
        this.messageInfoFormVisible = true

      },
      openTopic (index, row) {
        const openid = row.message_related_id
        console.log("openid", openid)
        const {href} = this.$router.resolve({
          name: "TopicInfo",
          params: {
            id: openid,
          }
        });
        window.open(href, '_blank');
      },
      openDiscuss (index, row) {
        const openid = row.message_related_id
        console.log("openid", openid)
        const {href} = this.$router.resolve({
          name: "DiscussInfo",
          params: {
            id: openid,
          }
        });
        window.open(href, '_blank');
      },
      handleRead(index, row, type){
        const id = row.message_id
        this.axios.post('/forum/readMessage',{
          message_id: id
        }).then(response => {
          if (response.data.status === 0) {
            this.getMessageInfo()
          }
          if(type === 1){
            this.$message({
              showClose: true,
              message: response.data.message,
              type: response.success === 0 ? 'success' : 'error',
              duration: 2000
            })
          }
        })
      },


      handleDelete(index, row){
        const id = row.message_id
        this.$confirm('确定要删除该消息吗', '提示', {
          confirmButtonText: '确定',
          cancelButtonText: '取消',
          type: 'warning'
        }).then(() => {
          this.axios.post('/forum/deleteMessage',{
            message_id: id
          }).then(response => {
            if (response.data.status === 0) {
              this.getMessageInfo()
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
      createMessage(){
        const data = this.form
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
      replyMessage(replyToUser){
        this.form={brand_right:0}
        const replyToUsername = replyToUser
        this.messageInfoFormVisible = false
        this.form.receive_username = replyToUsername
        this.dialogFormVisible = true
      },
      openCreateMessage(){
        this.form = {brand_right:0}
        this.dialogFormVisible = true
      }
    }
  }
</script>



<style scoped lang="scss">
  .table{

  }
</style>
