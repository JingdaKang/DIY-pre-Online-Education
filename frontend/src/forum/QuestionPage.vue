<template>
    <div>
      <div>
        <h1>问答系统</h1>
        <h2>搜索</h2>
        <el-input v-model="input" placeholder="请输入内容" style="width: 500px"></el-input>
        <el-button type="primary" @click="search" >搜索</el-button>
        <br>
        <br>
        <div v-show="submitButton">
          没有找到相关内容，是否要发布到论坛提问 &nbsp &nbsp
          <el-button type="danger" @click="submit" >提问</el-button>
        </div>
      </div>
    </div>
</template>

<script>
    export default {
      name: "QuestionPage",
      data() {
        return {
          input: '',
          submitButton: false,

        }
      },
      methods: {
        search(){
          this.submitButton = true;
        },
        submit(){
          const data = this.input
          console.log("input", this.input)
          this.axios.post('/forum/addQuestion',{
            question_title: this.input,
            question_id: 9999
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
          })
        }
      }
    }
</script>

<style scoped>

</style>
