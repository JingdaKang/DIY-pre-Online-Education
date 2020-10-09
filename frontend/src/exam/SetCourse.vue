<template>
  <div>
    <div>课程添加： </div>
    <el-form :model="Course" ref="Course">
      <el-form-item label="课程名：">
        <el-input type="text" v-model="Course.name"></el-input>
      </el-form-item>
      <el-form-item>
        <el-button type="primary" v-on:click="addCourse">添加</el-button>
      </el-form-item>
    </el-form>
    <div>课程章节添加： </div>
    <el-form :model="Section">
      <el-form-item label="课程：">
        <el-input type="text" v-model="Section.course"></el-input>
      </el-form-item>
      <el-form-item label="章数：">
        <el-input type="number" v-model="Section.chapter_count"></el-input>
      </el-form-item>
      <el-form-item label="章名：">
        <el-input type="text" v-model="Section.chapter_name"></el-input>
      </el-form-item>
      <el-form-item label="节数：">
        <el-input type="number" v-model="Section.section_count"></el-input>
      </el-form-item>
      <el-form-item label="节名：">
        <el-input type="text" v-model="Section.section_name"></el-input>
      </el-form-item>
      <el-form-item>
        <el-button type="primary" v-on:click="addSection">添加</el-button>
      </el-form-item>
    </el-form>
    <div>学生课程选择： </div>
    <el-form :model="S_C_C">
      <el-form-item label="学生名：">
        <el-input type="text" v-model="S_C_C.student"></el-input>
      </el-form-item>
      <el-form-item label="课程名：">
        <el-input type="text" v-model="S_C_C.course"></el-input>
      </el-form-item>
      <el-form-item>
        <el-button type="primary" v-on:click="addSCC">添加</el-button>
      </el-form-item>
    </el-form>
  </div>
</template>

<script>
export default {
  name: 'SetCourse',
  data () {
    return {
      Course: {
        name: ''
      },
      Section: {
        course: '',
        chapter_name: '',
        chapter_count: '',
        section_name: '',
        section_count: ''
      },
      S_C_C: {
        student: '',
        course: ''
      }
    }
  },
  methods: {
    addCourse () {
      this.$axios.post('/addcourse', {teacher: this.username, name: this.Course.name})
        .then(response => {
          alert('添加成功')
        })
    },
    addSection () {
      this.$axios.post('/addsection', {
        course: this.Section.course,
        chapter_count: this.Section.chapter_count,
        chapter_name: this.Section.chapter_name,
        section_count: this.Section.section_count,
        section_name: this.Section.section_name
      }).then(response => {
        alert(response.data.msg)
      })
    },
    addSCC () {
      this.$axios.post('/addscc', {student: this.S_C_C.student, course: this.S_C_C.course})
        .then(response => {
          alert('添加成功')
        })
    }
  },
  mounted () {
    let user = sessionStorage.getItem('username')
    if (user) {
      this.username = user
    }
    console.log(this.username)
  }
}
</script>

<style scoped>

</style>
