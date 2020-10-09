<template>
    <el-table
      :data="tableData"
      border="true"
      style="width: 90%;margin-top:20px;margin-left:5%">
      <el-table-column prop="id" label="编号" width="180" v-if="idShow">
      </el-table-column>
      <el-table-column prop="name" label="试卷名">
      </el-table-column>
      <el-table-column fixed="right" prop="course" label="相关课程" width="180">
      </el-table-column>
      <el-table-column fixed="right" label="操作" width="100">
        <template slot-scope="scope">
          <el-button type="text" v-on:click="showPaper(scope.row)">查看</el-button>
        </template>
      </el-table-column>
    </el-table>
</template>

<script>
export default {
  name: 'SelectPaper',
  data () {
    return {
      tableData: [{
        id: '',
        course: '',
        name: ''
      }],
      idShow: false
    }
  },
  methods: {
    showPaper (row) {
      this.$router.push({
        path: '/showPaper',
        query: {
          'pid': row.id,
          'name': row.name,
          'count': '1'
        }
      })
    },
    deletePaper (pid) {
      this.axios.post('/exam/deletepaper', {pid: pid})
        .then(response => {
          alert(response.data.msg)
          this.reload()
        })
    },
    selectPaper () {
      this.axios.get('/exam/getpaper', {
        params: {username: this.username}
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
    this.selectPaper()
  }
}
</script>

<style scoped>

</style>
