<template>
  <el-main>
    <el-table
      :data="tableData"
      border="true"
      style="width: 100%">
      <el-table-column prop="id" label="编号" width="180" v-if="idShow">
      </el-table-column>
      <el-table-column prop="course" label="课程" width="180">
      </el-table-column>
      <el-table-column prop="start_time" label="开始时间" width="180">
      </el-table-column>
      <el-table-column prop="end_time" label="截止时间" width="180">
      </el-table-column>
      <el-table-column prop="status" label="状态" width="180">
      </el-table-column>
      <el-table-column prop="name" label="考试">
      </el-table-column>
      <el-table-column fixed="right" label="操作" width="100">
        <template slot-scope="scope">
          <el-button type="text" @click="goToExam(scope.row)"
                     size="small" v-if="scope.row.status === '进行中'">进入考试</el-button>
        </template>
      </el-table-column>
    </el-table>
  </el-main>
</template>

<script>
export default {
  name: 'SelectExam',
  data () {
    return {
      tableData: [{
        id: '',
        name: '',
        course: '',
        start_time: '',
        end_time: '',
        status: ''
      }],
      username: '',
      idShow: false
    }
  },
  methods: {
    selectExam () {
      this.axios.get('/exam/selectexam', {
        params: {username: this.username}
      })
        .then(response => {
          console.log(response.data)
          this.tableData = response.data
        })
    },
    goToExam (row) {
      this.$router.push({
        path: '/doExam',
        query: {
          eid: row.id,
          username: this.username,
          name: row.name
        }
      })
    }
  },
  beforeMount () {
    let user = sessionStorage.getItem('username')
    if (user) {
      this.username = user
    }
    this.selectExam()
  }
}
</script>

<style scoped>

</style>
