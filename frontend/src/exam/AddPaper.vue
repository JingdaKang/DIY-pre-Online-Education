<template>
  <el-main  style="margin-top:20px">
    <el-form :model="Paper" ref="Paper" :rules="scorerules" label-position="right" label-width="200px">
      <el-form-item label="课程" prop="class">
      <el-col :span="4">
        <el-select v-model="Paper.course" placeholder="请选择课程">
          <el-option
            v-for="item in courseoption"
            :key="item"
            :label="item"
            :value="item">
          </el-option>
        </el-select>
        </el-col>
      </el-form-item>
      <el-form-item label="总分：">
        <el-col :span="4">
          <el-input type="number" v-model.number="Paper.score" placeholder="请输入总分"></el-input>
        </el-col>
      </el-form-item>
      <el-form-item label="单项选择题数量:">
        <el-row>
          <el-col :span="4">
            <el-input type="number" v-model.number="Paper.simplecount" placeholder="请输入题目数量"></el-input>
          </el-col>
          <el-col :span="2" offset="4">每题分值：</el-col>
          <el-col :span="4" >
            <el-input type="number" v-model.number="Paper.simplescore" placeholder="请输入每题分值"></el-input>
          </el-col>
        </el-row>
      </el-form-item>
      <el-form-item label="多项选择题数量:">
        <el-col :span="4">
          <el-input type="number" v-model.number="Paper.multiplecount" placeholder="请输入题目数量"></el-input>
        </el-col>
        <el-col :span="2" offset="4">每题分值：</el-col>
        <el-col :span="4">
          <el-input type="number" v-model.number="Paper.multiplescore" placeholder="请输入每题分值"></el-input>
        </el-col>
      </el-form-item>
      <el-form-item label="填空题数量:">
        <el-col :span="4">
          <el-input type="number" v-model.number="Paper.blankcount" placeholder="请输入题目数量"></el-input>
        </el-col>
        <el-col :span="2" offset="4">每题分值：</el-col>
        <el-col :span="4">
          <el-input type="number" v-model.number="Paper.blankscore" placeholder="请输入每题分值"></el-input>
        </el-col>
      </el-form-item>
      <el-form-item label="判断题数量:">
        <el-col :span="4">
          <el-input type="number" v-model.number="Paper.judgecount" placeholder="请输入题目数量"></el-input>
        </el-col>
        <el-col :span="2" offset="4">每题分值：</el-col>
        <el-col :span="4">
          <el-input type="number" v-model.number="Paper.judgescore" placeholder="请输入每题分值"></el-input>
        </el-col>
      </el-form-item>
      <el-form-item label="主观题数量:" prop="subjectivecount">
        <el-col :span="4">
          <el-input type="number" v-model.number="Paper.subjectivecount" placeholder="请输入题目数量"></el-input>
        </el-col>
        <el-col :span="2" offset="4">每题分值：</el-col>
        <el-col :span="4">
          <el-input type="number" v-model.number="Paper.subjectivescore" placeholder="请输入每题分值"></el-input>
        </el-col>
      </el-form-item>
      <el-form-item>
        <el-button type="primary" v-on:click="chooseQuestion('Paper')">手动组卷</el-button>
        <el-button type="primary" v-on:click="autoPaper('Paper')">自动组卷</el-button>
      </el-form-item>
    </el-form>
    <el-dialog
      v-loading.fullscreen = "loading"
      element-loading-text="拼命生成试卷中"
      element-loading-spinner="el-icon-loading"
      element-loading-background="rgba(0, 0, 0, 0.8)"
      title="课程章节选择" center="true" :visible.sync="dialogVisible">
      <el-table :data="Course" @selection-change="select" border="true" :header-cell-style="{'text-align':'center'}">
        <el-table-column type="selection" width="55"></el-table-column>
        <el-table-column prop="id" label="编号" width="55"></el-table-column>
        <el-table-column prop="chapter" label="章"></el-table-column>
        <el-table-column prop="section" label="节"></el-table-column>
      </el-table>
      <p>请输入分数期望（以总分100为例）：</p>
      <el-input type="text" v-model="count"></el-input>
      <p>请输入试卷名：</p>
      <el-input type="text" v-model="papername"></el-input>
      <el-button type="primary" v-on:click="getPaperAuto">确认并提交</el-button>
    </el-dialog>
  </el-main>
</template>

<script>
export default {
  name: 'AddPaper',
  data () {
    return {
      username: '',
      Paper: {
        course: '',
        score: '',
        simplecount: '',
        simplescore: '',
        multiplecount: '',
        multiplescore: '',
        blankcount: '',
        blankscore: '',
        judgecount: '',
        judgescore: '',
        subjectivecount: '',
        subjectivescore: ''
      },
      Course: [{
        id: '',
        chapter: '',
        section: ''
      }],
      sectionoption: [],
      idList: [],
      courseoption: [],
      scorerules: {
        course: [{required: true, message: '请选择课程', trigger: 'blur'}]
      },
      papername: '',
      count: '',
      dialogVisible: false,
      loading: false
    }
  },
  methods: {
    findCourse () {
      this.axios.post('/exam/findcourse', {username: this.username})
        .then(response => {
          this.courseoption = response.data.nameList
        })
    },
    checkScore () {
      let score = this.Paper.simplescore * this.Paper.simplecount +
        this.Paper.multiplescore * this.Paper.multiplecount +
        this.Paper.blankscore * this.Paper.blankcount +
        this.Paper.judgescore * this.Paper.judgecount +
        this.Paper.subjectivescore * this.Paper.subjectivecount
      if (score !== this.Paper.score) {
        alert('总分不足，请重新设计试卷')
        this.reload()
      }
    },
    chooseQuestion (formData) {
      if (this.Paper.course === '') {
        alert('未选择课程')
        this.reload()
      }
      this.checkScore()
      this.$refs[formData].validate((valid) => {
        if (valid) {
          this.$router.push({
            path: '/chooseQuestion',
            query: {
              course: this.Paper.course,
              papername: this.papername,
              username: this.username,
              simplecount: this.Paper.simplecount,
              simplescore: this.Paper.simplescore,
              multiplecount: this.Paper.multiplecount,
              multiplescore: this.Paper.multiplescore,
              blankcount: this.Paper.blankcount,
              blankscore: this.Paper.blankscore,
              judgecount: this.Paper.judgecount,
              judgescore: this.Paper.judgescore,
              subjectivecount: this.Paper.subjectivecount,
              subjectivescore: this.Paper.subjectivescore
            }
          })
        }
      })
    },
    getSection () {
      this.axios.get('/exam/getsection', {
        params: {
          course: this.Paper.course
        }
      }).then(response => {
        this.Course = response.data
      })
    },
    autoPaper (formData) {
      if (this.Paper.course === '') {
        alert('未选择课程')
        this.reload()
      }
      this.checkScore()
      this.$refs[formData].validate((valid) => {
        if (valid) {
          this.getSection()
          this.dialogVisible = true
        }
      })
    },
    select (val) {
      this.sectionoption = ''
      this.sectionoption = val
    },
    getPaperAuto () {
      let sectionData = this.sectionoption
      this.idList = []
      for (let i = 0; i < sectionData.length; i++) {
        this.idList.push(sectionData[i].id)
      }
      console.log(this.idList)
      if ((this.papername !== '') && (this.sectionoption !== '')) {
        this.loading = true
        this.axios.post('/exam/autopaper', {
          username: this.username,
          papername: this.papername,
          sectionoption: this.idList,
          course: this.Paper.course,
          count: this.count,
          simplecount: this.Paper.simplecount,
          simplescore: this.Paper.simplescore,
          multiplecount: this.Paper.multiplecount,
          multiplescore: this.Paper.multiplescore,
          blankcount: this.Paper.blankcount,
          blankscore: this.Paper.blankscore,
          judgecount: this.Paper.judgecount,
          judgescore: this.Paper.judgescore,
          subjectivecount: this.Paper.subjectivecount,
          subjectivescore: this.Paper.subjectivescore
        }).then(response => {
          alert(response.data.msg)
          this.loading = false
          console.log(response.data.status)
          this.router.push({
            path: '/selectPaper'
          })
        })
      }
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
