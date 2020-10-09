<template>
  <div id="myAnswer" class="demo-block demo-zh-CN demo-form" v-loading="loading">
    <el-card class="box-card" style="width:100%;text-align: center;height:auto;min-height:700px">
      <p style="font-size:20px;font-weight:bold">
        我的回答
      </p>
      <el-divider></el-divider>
      <div v-if="page_answers.length==0" style="width:100%;height:200px">
        <h1 style="margin-top: 50px">这里什么都没有哦</h1>
      </div>
      <el-table :data="page_answers" v-if="page_answers.length!=0" ref="answer"
                style="width: 100%;margin-top:20px" border>

        <el-table-column prop="question" label="所属问题" min-width="100" align="center">
          <template slot-scope="scope">
            <a class="redirect" @click="gotoQuestion(scope.row.question_id)"> {{scope.row.question}}</a>
          </template>
        </el-table-column>
        <el-table-column prop="time" label="回答时间" min-width="80" align="center">
          <template slot-scope="scope">
            {{dateFormat(scope.row.time)}}
          </template>
        </el-table-column>
        <el-table-column prop="context" label="回答" min-width="100" align="center" style="text-align: left">
          <template slot-scope="scope">
            {{scope.row.context}}
          </template>
        </el-table-column>
        <el-table-column prop="score" label="评分"  align="center">
          <template slot-scope="scope">
            {{scope.row.score}}
          </template>
        </el-table-column>
        <el-table-column prop="score" label="上传至云笔记"  align="center">
          <template slot-scope="scope">
            <el-row style="text-align:center">
              <a v-if="scope.row.upload_time==null" class="upload" @click="send_to_note(scope.row.answer_id)">上传</a>
              <p v-if="scope.row.upload_time!=null">已上传</p>
            </el-row>
          </template>
        </el-table-column>
      </el-table>
      <el-row style="margin-top:20px" v-if="page_answers.length!=0">
        <el-pagination
          @size-change="handleSizeChange"
          @current-change="handleCurrentChange"
          :current-page="currentPage"
          :page-sizes="[10, 50, 100, 200]"
          :page-size="10"
          layout="total, sizes, prev, pager, next, jumper"
          :total="totalCount">
        </el-pagination>
      </el-row>
    </el-card>
  </div>
</template>

<script>
  export default {
    name: 'Home',
    data() {
      return {
        activeIndex: 1,
        loading:true,
        currentPage: 1,
        pageSize: 10,
        totalCount: '',
        answerList: [],
        page_answers: [],
      }
    },
    mounted() {
      let user_id = this.$cookies.get('user_id')
      if (user_id) {
        this.getAnswers()
      }  else {
        windows.location.href="http://127.0.0.1:8888/#/login"
      }
    },
    methods: {
      getAnswers() {
        let that = this
        let param = new URLSearchParams()
        param.append('user_id', that.$cookies.get('user_id'))
        that.loading = true
        that.axios({
          method: 'post',
          url: '/iasystem/answers/',
          data: param
        })
          .then(function (res) {
            if (res.data.code === 1) {
              that.answerList = res.data.answers
              that.totalCount = res.data.answers.length
              console.log(that.answerList)
              that.loading = false
              that.get_page_answer()
            } else if (res.data.code === 0) {
              that.loading = false
              that.$message.error('查询回答失败')
            }
          })
      },
      get_page_answer() {
        this.page_answers = [];
        for (let i = (this.currentPage - 1) * this.pageSize; i < this.totalCount; i++) {
          this.page_answers.push(this.answerList[i])
          if (this.page_answers.length == this.pageSize) break;
        }
      },
      handleSizeChange(val) {
        this.pageSize = val;
        this.get_page_answer()
      },
      handleCurrentChange(val) {
        this.currentPage = val;
        this.get_page_answer()
      },
      gotoQuestion(value) {
        this.$router.push({
          path: `/Question/${value}`,
        })
      },
      dateFormat(value) {
        const t = new Date(value);
        const time = t.getFullYear() + '-' + (t.getMonth() + 1) + '-' + t.getDate() + " " + t.getHours() + ":" + t.getMinutes();
        return time;
      },
      send_to_note(value){
        let that = this
        let param = new URLSearchParams()
        param.append('answer_id', value)
        that.loading = true
        that.axios({
          method: 'post',
          url: '/iasystem/send_to_note/',
          data: param
        })
          .then(function (res) {
            if (res.data.code === 1) {
              that.loading = false
              that.$message({
                message: '上传成功',
                type: 'success'
              })
               setTimeout(function () {
                that.$router.go(0)
              }.bind(that), 1000)

            } else if (res.data.code === 0) {
              that.loading = false
              that.$message.error('上传失败')
            }
          })
      }
    }
  }
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style scoped>
  h1, h2 {
    font-weight: normal;
  }

  ul {
    list-style: none;
    padding: 0;
  }

  li {
    display: inline-block;
    margin: 0 10px;
  }

  .upload {
    margin-left: 35%;
    display: block;
    border-radius: 5%;
    padding-top: 5px;
    padding-bottom: 5px;
    width: 60px;
    height: 20px;
    text-decoration: none;
    color: #409EFF;
    background-color: #ECF5FF;
    border-color: #B3D8FF;
    font-size: 12px;
  }

  .upload:hover {
    margin-left: 35%;
    display: block;
    border-radius: 5%;
    padding-top: 5px;
    padding-bottom: 5px;
    width: 60px;
    height: 20px;
    text-decoration: none;
    color: #FFFFFF;
    background-color: #409EFF;
    border-color: #409EFF;
    font-size: 12px;
  }

  .redirect {
    text-decoration: none;
    color: #000b16;
  }

  .redirect:hover {
    text-decoration: none;
    color: #409EFF;
  }
</style>
