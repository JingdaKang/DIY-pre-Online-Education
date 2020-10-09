<template>
  <el-dialog title="考试详情页" center="true" :visible.sync="dialogVisible">
    <el-form :model="Exam" ref="Exam">
      <el-form-item label="考试名称：">
        <el-input type="text" v-model="Exam.name" placeholder="请输入考试名称">考试名称</el-input>
      </el-form-item>
      <el-form-item label="开始时间：">
        <el-date-picker type="datetime" v-model="Exam.start_time"
                        format="yyyy-MM-dd HH:mm:ss" value-format="yyyy-MM-dd HH:mm:ss"></el-date-picker>
      </el-form-item>
      <el-form-item label="截止时间：">
        <el-date-picker type="datetime" v-model="Exam.end_time"
                        format="yyyy-MM-dd HH:mm:ss" value-format="yyyy-MM-dd HH:mm:ss"></el-date-picker>
      </el-form-item>
      <el-form-item>
        <el-button type="success" v-on:click="change">确定</el-button>
        <el-button type="primary" v-on:click="quit">取消</el-button>
      </el-form-item>
    </el-form>
  </el-dialog>
</template>

<script>
export default {
  name: 'ShowExam',
  data () {
    return {
      Exam: {
        name: '',
        start_time: '',
        end_time: ''
      },
      dialogVisible: true
    }
  },
  methods: {
    showExam () {
      this.Exam.name = this.$route.query.name
      this.Exam.start_time = this.$route.query.start_time
      this.Exam.end_time = this.$route.query.end_time
    },
    change () {
      console.log(this.Exam)
      this.axios.post('/exam/changeexam', {
        'eid': this.$route.query.id,
        'name': this.Exam.name,
        'start_time': this.Exam.start_time,
        'end_time': this.Exam.end_time
      }).then(response => {
        alert(response.data.msg)
      })
    },
    quit () {
      this.$router.push('/findExam')
    }
  },
  mounted () {
    this.showExam()
    console.log(this.Exam)
  }
}
</script>

<style scoped>

</style>
