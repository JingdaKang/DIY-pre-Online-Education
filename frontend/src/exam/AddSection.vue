<template>
  <div>
    <el-form :model="Section" ref="Section" label-position="right" label-width="100px">
      <el-form-item label="课程： ">
        <el-select v-model="course" placeholder="请选择课程" @change="getSection">
          <el-option
            v-for="item in courseoption"
            :key="item"
            :label="item"
            :value="item">
          </el-option>
        </el-select>
      </el-form-item>
      <el-form-item label="章数： ">
        <el-col :span="8">
          <el-input type="number" v-model="Section.chapterCount" placeholder="请输入章数，第一章即输入1，只能输入数字"></el-input>
        </el-col>
      </el-form-item>
      <el-form-item label="章名： ">
        <el-col :span="8">
          <el-input type="text" v-model="Section.chapterName" placeholder="请输入章名"></el-input>
        </el-col>
      </el-form-item>
      <el-form-item label="节数： ">
        <el-col :span="8">
          <el-input type="number" v-model="Section.sectionCount" placeholder="请输入节数，第一节即输入1，只能输入数字"></el-input>
        </el-col>
      </el-form-item>
      <el-form-item label="节名： ">
        <el-col :span="8">
          <el-input type="text" v-model="Section.sectionName" placeholder="请输入节名"></el-input>
        </el-col>
      </el-form-item>
      <el-form-item>
        <el-button type="primary" v-on:click="AddSection">提交</el-button>
      </el-form-item>
    </el-form>
    <div v-show="courseShow">
      <span style="font-size: 24px;text-align: center;display:block;">{{this.course}}</span>
      <el-table :data="Course" border="true" :header-cell-style="{'text-align':'center'}">
        <el-table-column prop="chapter" label="章"></el-table-column>
        <el-table-column prop="section" label="节"></el-table-column>
      </el-table>
    </div>
  </div>
</template>

<script>
export default {
  name: 'AddSection',
  data () {
    return {
      courseoption: [],
      course: '',
      Section: {
        chapterCount: '',
        chapterName: '',
        sectionCount: '',
        sectionName: ''
      },
      Course: [{
        id: '',
        chapter: '',
        section: ''
      }],
      courseShow: false
    }
  },
  methods: {
    AddSection () {
      this.axios.post('/exam/addsection', {
        course: this.course,
        chapterCount: this.Section.chapterCount,
        chapterName: this.Section.chapterName,
        sectionCount: this.Section.sectionCount,
        sectionName: this.Section.sectionName
      }).then(response => {
        alert(response.data.msg)
        location.reload()
      })
    },
    findCourse () {
      this.axios.post('/exam/findcourse', {username: this.username})
        .then(response => {
          this.courseoption = response.data.nameList
        })
    },
    getSection () {
      this.courseShow = true
      this.axios.get('/exam/getsection', {
        params: {
          course: this.course
        }
      }).then(response => {
        this.Course = response.data
      })
    }
  },
  mounted () {
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
