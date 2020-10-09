<template>
  <el-form :model="Exam" ref="Exam" label-position="right" style="margin-top:20px" label-width="150px">
    <el-form-item label="请选择课程:">
      <el-select v-model="Exam.course" placeholder="请选择课程" @change="handleChange">
        <el-option
          v-for="item in courseoption"
          :key="item"
          :label="item"
          :value="item">
        </el-option>
      </el-select>
    </el-form-item>
    <el-form-item label="请选择试卷:">
      <el-select v-model="Exam.paper" placeholder="请选择试卷">
        <el-option
          v-for="item in paperoption"
          :key="item"
          :label="item"
          :value="item">
        </el-option>
      </el-select>
    </el-form-item>
    <el-form-item label="请输入考试名称:">
      <el-col :span="4" style="float:right">
        <el-input type="text" v-model="Exam.name" placeholder="请输入考试名称">考试名称</el-input>
      </el-col>
    </el-form-item>
    <el-form-item label="请选择开始时间">
      <el-date-picker type="datetime" v-model="Exam.start_time"
                      format="yyyy-MM-dd HH:mm:ss" value-format="yyyy-MM-dd HH:mm:ss"></el-date-picker>
    </el-form-item>
    <el-form-item label="请选择截止时间">
      <el-date-picker type="datetime" v-model="Exam.end_time"
                      format="yyyy-MM-dd HH:mm:ss" value-format="yyyy-MM-dd HH:mm:ss"></el-date-picker>
    </el-form-item>
    <el-form-item>
      <el-button type="primary" v-on:click="submited('Exam')">发布考试</el-button>
    </el-form-item>
  </el-form>
</template>

<script>
export default {
  name: 'AddExam',
  data () {
    return {
      Exam: {
        name: '',
        course: '',
        start_time: '',
        end_time: '',
        paper: ''
      },
      courseoption: [],
      paperoption: []
    }
  },
  methods: {
    submited (formdata) {
      this.$refs[formdata].validate((valid) => {
        if (valid) {
          let data = new FormData()
          data.append('username', this.username)
          data.append('name', this.Exam.name)
          data.append('course', this.Exam.course)
          data.append('start_time', this.Exam.start_time)
          data.append('end_time', this.Exam.end_time)
          data.append('paper', this.Exam.paper)
          this.axios.post('/exam/addexam', data).then(response => {
            alert(response.data.msg)
          })
        }
      })
    },
    findCourse () {
      this.axios.post('/exam/findcourse', {username: this.username})
        .then(response => {
          this.courseoption = response.data.nameList
        })
    },
    handleChange () {
      this.findPaper()
    },
    findPaper () {
      this.axios.post('/exam/findpaper', {
        username: this.username,
        course: this.Exam.course
      })
        .then(response => {
          this.paperoption = response.data.nameList
        })
    }
  },
  mounted: function () {
    let user = sessionStorage.getItem('username')
    if (user) {
      this.username = user
    }
    this.findCourse()
  }
}
</script>

<style scoped>

</style>
