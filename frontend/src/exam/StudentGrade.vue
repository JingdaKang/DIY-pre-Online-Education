<template>
    <div style="margin-top:20px;margin-left:20px">
      <el-form>
        <el-form-item label="请选择课程：">
          <el-select v-model="course">
            <el-option
                v-for="item in courseoption"
                :key="item"
                :label="item"
                :value="item">
              </el-option>
          </el-select>
        </el-form-item>
        <el-form-item>
          <el-button type="primary" v-on:click="getScore">查询</el-button>
        </el-form-item>
        <div v-show="scoreShow" id="studentscore" :style="{width: '800px', height: '600px'}"></div>
      </el-form>
    </div>
</template>

<script>
export default {
  name: 'StudentGrade',
  data () {
    return {
      courseoption: [],
      course: '',
      scoreShow: false,
      username: '',
      stuoptions: {
        title: {
          text: '课程成绩变化趋势图'
        },
        legend: {data: ['得分']},
        tooltip: {},
        dataset: {
          dimensions: ['name', 'score'],
          source: []
        },
        xAxis: {type: 'category'},
        yAxis: {},
        series: [
          {type: 'line'}
        ]
      }
    }
  },
  methods: {
    getScore () {
      this.axios.get('/exam/showstudentscore', {
        params: {
          username: this.username,
          course: this.course
        }
      }).then(response => {
        this.stuoptions.dataset.source = response.data
        console.log(this.stuoptions)
        this.drawStuScore()
      })
      this.scoreShow = true
    },
    getStuCourse () {
      this.axios.post('/exam/getstucourse', {username: this.username})
        .then(response => {
          this.courseoption = response.data.nameList
        })
    },
    drawStuScore () {
      let echart = require('echarts')
      let chart = echart.init(document.getElementById('studentscore'))
      chart.setOption(this.stuoptions)
    }
  },
  mounted () {
    let user = sessionStorage.getItem('username')
    if (user) {
      this.username = user
    }
    this.getStuCourse()
    this.drawStuScore()
  }
}
</script>

<style scoped>

</style>
