<template>
  <div>
    <el-table
      :data="tableData"
      border="true"
      style="width: 80%;margin-top:20px;margin-left:10%">
      <el-table-column prop="exam" label="考试名">
      </el-table-column>
      <el-table-column prop="course" label="课程名" width="180">
      </el-table-column>
      <el-table-column prop="obj_score" label="客观题成绩" width="180">
      </el-table-column>
      <el-table-column prop="sub_score" label="主观题成绩" width="180">
      </el-table-column>
      <el-table-column prop="total_score" label="总成绩" width="180">
      </el-table-column>
    </el-table>
  </div>
</template>

<script>
export default {
  name: 'StudentScore', // 学生查询考试成绩页面
  data () {
    return {
      tableData: [{
        exam: '',
        course: '',
        obj_score: '',
        sub_score: '',
        total_score: ''
      }]
    }
  },
  methods: {
    getStudentScore () {
      this.axios.get('/exam/getstudentscore', {
        params: {
          username: this.username
        }
      }).then(response => {
        this.tableData = response.data
      })
    }
  },
  mounted () {
    let user = sessionStorage.getItem('username')
    if (user) {
      this.username = user
    }
    this.getStudentScore()
  }
}
</script>

<style scoped>

</style>
