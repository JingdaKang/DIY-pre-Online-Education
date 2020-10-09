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
          <el-button type="primary" v-on:click="getTotalScore">查询</el-button>
        </el-form-item>
      </el-form>
      <el-table
        :data="tableData"
        border="true"
        style="width: 50%;margin-left:25%">
        <el-table-column prop="username" label="学生名">
        </el-table-column>
        <el-table-column prop="objscore" label="客观题成绩" width="180">
        </el-table-column>
        <el-table-column prop="subscore" label="主观题成绩" width="180">
        </el-table-column>
        <el-table-column prop="totalscore" label="总成绩" width="180">
        </el-table-column>
      </el-table>
    </div>
</template>

<script>
export default {
  name: 'ShowScore',
  data () {
    return {
      tableData: {
        username: '',
        objscore: '',
        subscore: '',
        totalscore: ''
      },
      exam: '',
      examoption: ''
    }
  },
  methods: {
    findExam () {
      this.axios.post('/exam/findexam', {username: this.username})
        .then(response => {
          this.examoption = response.data.nameList
        })
    },
    getTotalScore () {
      this.axios.get('/exam/gettotalscore', {
        params: {
          exam: this.exam
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
    this.findExam()
  }
}
</script>

<style scoped>

</style>
