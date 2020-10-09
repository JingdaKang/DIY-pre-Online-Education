<template>
    <el-table
      :data="tableData"
      border="true"
      style="width: 90%;margin-top:20px;margin-left:5%">
      <el-table-column prop="id" label="编号" width="50" v-if="idShow">
      </el-table-column>
      <el-table-column prop="name" label="考试名">
      </el-table-column>
      <el-table-column prop="course" label="相关课程" width="150">
      </el-table-column>
      <el-table-column prop="start_time" label="开始时间" width="180">
      </el-table-column>
      <el-table-column prop="end_time" label="截止时间" width="180">
      </el-table-column>
      <el-table-column prop="status" label="状态" width="180">
      </el-table-column>
      <el-table-column fixed="right" label="操作" width="100">
        <template slot-scope="scope">
          <el-button type="text" v-if="scope.row.status === '未开始'" v-on:click="changeExam(scope.row)">修改</el-button>
        </template>
      </el-table-column>
    </el-table>
</template>

<script>
export default {
  name: 'FindExam',
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
      idShow: false
    }
  },
  methods: {
    changeExam (row) {
      this.$router.push({
        path: '/showExam',
        query: {
          'id': row.id,
          'name': row.name,
          'start_time': row.start_time,
          'end_time': row.end_time
        }
      })
    },
    findExam () {
      console.log('find')
      this.axios.get('/exam/findexam', {
        params: {
          username: this.username
        }
      }).then(response => {
        console.log(response)
        this.tableData = response.data
      })
    }
  },
  beforeMount () {
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
