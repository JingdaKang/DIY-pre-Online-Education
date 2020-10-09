<template>
  <div>

    <h1 class="el-icon-albb-edit"><router-link to="/forum/newdiscuss">发布小组讨论</router-link></h1>
    <br><br>
    <h2 class="el-icon-albb-group"><el-button type="text" @click="open" :disabled="!user">
      <h1 style="color: black">{{ user ? '创建新小组' : '登录后可创建新小组' }}</h1>
    </el-button></h2>
    <br>
    <h2 class="el-icon-albb-add">
      <el-button type="text" @click="dialogFormVisible = true" :disabled="!user">
        <h1 style="color: black">{{ user ? '加入新小组' : '登录后可加入小组' }}</h1>
      </el-button>
      <el-dialog title="请选择要加入的小组" :visible.sync="dialogFormVisible">
        <el-form :model="form" label-width="80px">
          <el-form-item label="小组" >
            <el-select v-model="form.group_id" placeholder="请选择要加入的小组">
              <el-option
                v-for="item in groupData"
                :key="item.id"
                :label="item.name"
                :value="item.id"
              />
            </el-select>
          </el-form-item>
          <el-form-item label="申请附言">
            <el-input type="textarea" v-model="form.apply_message"></el-input>
          </el-form-item>
        </el-form>
        <div slot="footer" class="dialog-footer">
          <el-button @click="dialogFormVisible = false">取 消</el-button>
          <el-button type="primary" @click="applyGroup()">确 定</el-button>
        </div>
      </el-dialog>
    </h2>



    <div class="notices">
      <span>
        只有加入小组后，或是关注了该讨论帖，<br>才能参与小组内的讨论帖哦
      </span>
    </div>



  </div>
</template>

<script>

export default {
  name: 'Right',
  data () {
    return {
      user: window.localStorage.getItem('username'),
      groupData:[],
      form: {
        group_id: '',
        apply_message: ''
      },
      formLabelWidth: '120px',
      dialogFormVisible: false,
    }
  },
  mounted () {
    this.getTags()
  },
  methods: {
    open() {
      this.$prompt('请输入小组名', '创建新的小组', {
        confirmButtonText: '确定',
        cancelButtonText: '取消',
        inputPattern: /^[\s\S]*.*[^\s][\s\S]*$/,
        inputErrorMessage: '请输入小组名'
      }).then(({ value }) => {
        console.log("value", value)
        console.log("type", typeof value)
        this.axios.post('/forum/addGroup',{
          group_name: value
        }).then(response => {
          if (response.data.status === 0) {
            this.$message({
              showClose: true,
              message: response.data.message,
              type: response.success === 0 ? 'success' : 'error',
              duration: 2000
            })
            location.reload()
          } else {
            this.$message({
              showClose: true,
              message: response.data.message,
              type: response.success === 0 ? 'success' : 'error',
              duration: 2000
            })
          }
        })
      }).catch(() => {
        this.$message({
          type: 'info',
          message: '取消创建'
        });
      });
    },
    getTags(){
      this.axios.get("/forum/userNotInGroup/", {
        params: {
          user: this.user,
        }
      }).then(response => {
        if (response.data.status === 0) {
          console.log('not', response)
          this.groupData = response.data.data
        }
      })
    },
    applyGroup(){
      this.dialogFormVisible = false
      const data = this.form
      console.log("apply_group", data.group_id)
      this.axios.post('/forum/applyGroup',{
        group_id: data.group_id,
        apply_message: data.apply_message
      }) .then(response => {
        if (response.data.status === 0) {
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
        this.form.group_id =''
        this.form.apply_message=''
      })
    }

  }
}
</script>

<style lang="scss" scoped>
  a {
    text-decoration: none;
    color: black;
  }
  .notices{
    .post{
      text-decoration: none;
      text-decoration-style: solid;
      color: grey;
    }
    .router-link-active{
      text-decoration: none;
    }
  }

  .notices{
    cursor: pointer;
    padding: 15px;
    margin-bottom: 20px;
    font-size: 12px;
    border: 1px solid #faebcc;
    background-color: #fcf8e3;
    border-radius: 4px;
    &:hover{
      text-decoration: underline;
    }
  }
</style>
