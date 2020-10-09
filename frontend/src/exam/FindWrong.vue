<template>
  <div style="margin-top:20px">
    <el-form style="width: 80%;margin-left:10%">
      <el-form-item label="请选择考试： ">
        <el-select v-model="exam">
          <el-option
              v-for="item in examoption"
              :key="item"
              :label="item"
              :value="item">
            </el-option>
        </el-select>
        <el-button type="primary" v-on:click="getWrong">查询</el-button>
      </el-form-item>
    </el-form>
    <p></p>
    <el-table
      :data="tableData"
      border="true"
      stripe="true"
      style="width: 80%;margin-left:10%">
      <el-table-column prop="id" v-if="idShow"></el-table-column>
      <el-table-column prop="content" label="题干">
      </el-table-column>
      <el-table-column prop="answer" label="参考答案" width="180">
      </el-table-column>
      <el-table-column prop="stu_answer" label="你的答案" width="180">
      </el-table-column>
      <el-table-column label="操作" width="100">
        <template slot-scope="scope">
          <el-button type="text" v-on:click="goToCloud(scope.row)" v-show="cloudShow">上传云笔记</el-button>
        </template>
      </el-table-column>
    </el-table>
  </div>
</template>

<script>
export default {
  name: 'FindWrong',
  data () {
    return {
      tableData: [{
        id: '',
        content: '',
        answer: '',
        stu_answer: ''
      }],
      exam: '',
      examoption: [],
      cloudShow: false,
      idShow: false
    }
  },
  methods: {
    findStuExam () {
      this.axios.post('/exam/findstuexam', {username: this.username})
        .then(response => {
          this.examoption = response.data.nameList
        })
    },
    getWrong () {
      this.axios.get('/exam/getwrong', {
        params: {
          username: this.username,
          exam: this.exam
        }
      }).then(response => {
        this.cloudShow = true
        this.tableData = response.data
      })
    },
    goToCloud (row) {
      this.axios.post('/exam/gotocloud', {id: row.id})
        .then(response => {
          alert(response.data.msg)
        })
    }
  },
  mounted () {
    let user = sessionStorage.getItem('username')
    if (user) {
      this.username = user
    }
    this.findStuExam()
  }
}
</script>

<style scoped>

</style>
