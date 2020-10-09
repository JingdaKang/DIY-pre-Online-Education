<template>
  <el-form style="width:80%;margin-top:20px;margin-left:10%">
    <el-form-item label="请选择课程： ">
      <el-select v-model="course">
        <el-option
          v-for="item in courseoption"
          :key="item"
          :value="item"
          :label="item">
        </el-option>
      </el-select>
    </el-form-item>
    <el-form-item label="请选择题目数量： ">
      <el-radio-group v-model="count">
        <el-radio label="5">5道</el-radio>
        <el-radio label="10">10道</el-radio>
        <el-radio label="20">20道</el-radio>
      </el-radio-group>
    </el-form-item>
    <el-form-item>
      <el-button type="primary" v-on:click="goTest">开始测验</el-button>
    </el-form-item>
  </el-form>
</template>

<script>
export default {
  name: 'AddTest',
  data () {
    return {
      course: '',
      count: '',
      courseoption: ''
    }
  },
  methods: {
    goTest () {
      this.axios.post('/exam/addtest', {
        username: this.username,
        course: this.course,
        count: this.count
      }).then(response => {
        alert('测验生成完毕，请前往考试查询模块进行测验')
      })
    },
    getStuCourse () {
      this.axios.post('/exam/getstucourse', {username: this.username})
        .then(response => {
          this.courseoption = response.data.nameList
        })
    }
  },
  mounted () {
    let user = sessionStorage.getItem('username')
    if (user) {
      this.username = user
    }
    this.getStuCourse()
  }
}
</script>

<style scoped>

</style>
