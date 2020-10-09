<template>
  <div class="formstyle" style="margin-top:20px;margin-left:10px">
    <el-form>
      <el-form-item label="请选择数据类型：">
        <el-button-group>
          <el-button type="primary" v-on:click="showScore">学生成绩查询</el-button>
          <el-button type="primary" v-on:click="showQuestion">题目错误率查询</el-button>
        </el-button-group>
      </el-form-item>
    </el-form>
    <div v-show="scoreShow">
      <el-form>
        <el-form-item label="请选择考试：">
          <el-select v-model="exam">
            <el-option
                v-for="item in examoption"
                :key="item"
                :label="item"
                :value="item">
              </el-option>
          </el-select>
        </el-form-item>
        <el-form-item label="排序方式：">
          <el-radio-group v-model="order">
            <el-radio label="default">默认排序</el-radio>
            <el-radio label="up">成绩升序</el-radio>
            <el-radio label="down">成绩降序</el-radio>
          </el-radio-group>
        </el-form-item>
        <el-form-item>
          <el-button type="primary" v-on:click="getScore">查询</el-button>
        </el-form-item>
      </el-form>
      <div id="score" :style="{width: '800px', height: '600px'}"></div>
    </div>
    <div v-show="questionShow">
      <el-select v-model="exam" label="请选择考试">
        <el-option
            v-for="item in examoption"
            :key="item"
            :label="item"
            :value="item">
          </el-option>
      </el-select>
      <el-button type="primary" v-on:click="getQuestion">查询</el-button>
      <el-button type="primary" v-on:click="getQ">正确率查询</el-button>
      <div id="question" :style="{width: '800px', height: '600px'}"></div>
      <div id="q" :style="{width: '800px', height: '600px'}"></div>
    </div>
  </div>
</template>

<script>
export default {
  name: 'ShowGrade',
  data () {
    return {
      scoreoptions: {
        title: {
          text: '学生成绩分布图'
        },
        tooltip: {
          axisPointer: {
            type: 'shadow'
          }
        },
        dataset: {
          dimensions: ['name', 'score'],
          source: []
        },
        legend: {
          data: ['成绩']
        },
        xAxis: {
          type: 'category',
          axisLabel: {
            fontSize: 18
          }
        },
        yAxis: {
          axisLabel: {
            fontSize: 18
          }
        },
        series: [{
          name: '学生成绩',
          type: 'bar',
          barWidth: 40,
          label: {
            show: true
          },
          backgroundStyle: {
            color: 'rgba(220, 220, 220, 0.8)'
          }
        }]
      },
      questionoptions: {
        title: {
          text: '题目错误人数分布图'
        },
        tooltip: {
          trigger: 'axis',
          axisPointer: {
            type: 'shadow'
          }
        },
        legend: {
          data: ['正确人数', '错误人数']
        },
        grid: {
          left: '3%',
          right: '4%',
          bottom: '3%',
          containLabel: true
        },
        dataset: {
          dimensions: ['count', 'right', 'wrong'],
          source: []
        },
        xAxis: [
          {
            type: 'value',
            axisLabel: {
              show: true,
              fontSize: 18,
              formatter: (value) => {
                return Math.abs(value)
              }
            }
          }
        ],
        yAxis: [
          {
            type: 'category',
            axisTick: {
              show: false
            },
            axisLabel: {
              fontSize: 18
            }
          }
        ],
        series: [
          {
            name: '正确人数',
            type: 'bar',
            barWidth: 40,
            stack: '总人数',
            label: {
              show: true
            }
          },
          {
            name: '错误人数',
            type: 'bar',
            barWidth: 40,
            stack: '总人数',
            label: {
              show: true,
              formatter: (params) => {
                return Math.abs(params.value[params.dimensionNames[params.encode.x]])
              }
            }
          }
        ]
      },
      qoptions: {
        title: {
          text: '题目正确率分布图'
        },
        tooltip: {
          axisPointer: {
            type: 'shadow'
          }
        },
        dataset: {
          dimensions: ['count', 'percentage'],
          source: []
        },
        legend: {
          data: ['正确率']
        },
        xAxis: {
          type: 'category',
          axisLabel: {
            fontSize: 18
          }
        },
        yAxis: {
          axisLabel: {
            fontSize: 18,
            formatter: (value) => {
              return value + '%'
            }
          }
        },
        series: [{
          name: '正确率',
          type: 'bar',
          barWidth: 40,
          label: {
            show: true,
            formatter: '{@percentage}%'
          },
          backgroundStyle: {
            color: 'rgba(220, 220, 220, 0.8)'
          }
        }]
      },
      exam: '',
      examoption: [],
      order: 'default',
      scoreShow: false,
      questionShow: false
    }
  },
  methods: {
    findExam () {
      this.axios.post('/exam/findexam', {username: this.username})
        .then(response => {
          this.examoption = response.data.nameList
        })
    },
    showScore () {
      this.scoreShow = true
      this.questionShow = false
    },
    showQuestion () {
      this.questionShow = true
      this.scoreShow = false
    },
    getScore () {
      if (this.exam === '') {
        alert('未选择考试')
        this.reload()
      } else {
        this.axios.get('/exam/showscore', {
          params: {
            exam: this.exam,
            order: this.order
          }
        }).then(response => {
          this.scoreoptions.dataset.source = response.data
          this.drawScore()
        })
      }
    },
    getQuestion () {
      if (this.exam === '') {
        alert('未选择考试')
        this.reload()
      } else {
        this.axios.get('/exam/showquestion', {
          params: {
            exam: this.exam,
            type: 1
          }
        }).then(response => {
          this.questionoptions.dataset.source = response.data
          this.drawQuestion()
        })
      }
    },
    getQ () {
      if (this.exam === '') {
        alert('未选择考试')
        this.reload()
      } else {
        this.axios.get('/exam/showquestion', {
          params: {
            exam: this.exam,
            type: 2
          }
        }).then(response => {
          this.qoptions.dataset.source = response.data
          console.log(this.qoptions.dataset.source)
          this.drawQ()
        })
      }
    },
    drawScore () {
      let echart = require('echarts')
      let chart = echart.init(document.getElementById('score'))
      chart.setOption(this.scoreoptions)
    },
    drawQuestion () {
      let echart = require('echarts')
      let chart = echart.init(document.getElementById('question'), 'light')
      chart.setOption(this.questionoptions)
    },
    drawQ () {
      let echart = require('echarts')
      let chart = echart.init(document.getElementById('q'))
      chart.setOption(this.qoptions)
    }
  },
  mounted () {
    let user = sessionStorage.getItem('username')
    if (user) {
      this.username = user
    }
    this.findExam()
    this.drawScore()
    this.drawQuestion()
    this.drawQ()
  }
}
</script>

<style scoped>

</style>
