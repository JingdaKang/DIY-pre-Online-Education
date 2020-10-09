<template>
    <div style="margin-top:20px;margin-left:10px">
      <el-form style="width: 50%;margin-left:25%">
        <el-form-item label="请选择考试：">
          <el-select v-model="exam">
            <el-option
                v-for="item in examoption"
                :key="item"
                :label="item"
                :value="item">
              </el-option>
          </el-select>
          <el-button type="primary" v-on:click="getScore">查询</el-button>
        </el-form-item>
      </el-form>
      <p></p>
      <el-table
        :data="tableData"
        border="true"
        style="width: 50%;margin-left:25%">
        <el-table-column prop="examname" label="考试名">
        </el-table-column>
        <el-table-column prop="username" label="学生名" width="180">
        </el-table-column>
        <el-table-column prop="score" label="客观题成绩" width="180">
        </el-table-column>
        <el-table-column fixed="right" label="操作" width="100">
          <template slot-scope="scope">
            <el-button type="text" @click="goToCorrect(scope.row)"
                       size="small" v-if="scope.row.status === '0'">主观题批改</el-button>
          </template>
        </el-table-column>
      </el-table>
    </div>
</template>

<script>
export default {
  name: 'SelectScore',
  data () {
    return {
      course: '',
      exam: '',
      tableData: [{
        examname: '',
        username: '',
        score: '',
        status: ''
      }],
      total: '',
      examoption: []
    }
  },
  methods: {
    findExam () {
      this.axios.post('/exam/findexam', {username: this.username})
        .then(response => {
          this.examoption = response.data.nameList
        })
    },
    getScore () {
      this.axios.get('/exam/getscore', {
        params: {
          exam: this.exam
        }
      }).then(response => {
        this.tableData = response.data
        this.total = response.data.get('total')
        console.log(this.total)
      })
    },
    goToCorrect (row) {
      this.$router.push({
        path: '/showAnswer',
        query: {
          examname: row.examname,
          username: row.username,
          total: this.total,
          count: 1
        }
      })
    }
  },
  mounted () {
    let user = sessionStorage.getItem('username')
    if (user) {
      this.username = user
    }
    this.findExam()
  }
}
</script>

<style scoped>

</style>
