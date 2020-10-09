<template>
  <div id="MyRelease" v-loading="loading">
    <el-row>
      <p style="font-size:20px;font-weight:bold;margin-top:25px">
        我的发布
      </p>
    </el-row>
    <el-tabs v-model="activeName" type="border-card" @tab-click="handleClick">
      <el-tab-pane label="问题" name="first">
        <div v-if="questions.length==0" style="width:100%;height:200px">
          <h1 style="margin-top: 50px">这里什么都没有哦</h1>
        </div>
        <div style="overflow-y:scroll;margin-top:20px;height: auto;width:100%">
          <el-card v-for="question in page_questions" class="box-card"
                   style="width:80%;margin-top:20px;margin-left:8%;padding-top:10px;text-align: center">
            <el-row>
              <el-avatar :size="40" src="iasystem/avatar/" style="float:left;margin-left:20px"></el-avatar>
              <p style="float:left;margin-left:20px;margin-top: 10px;line-height:22px">{{username}}</p>
              <p style="float:left;margin-left:20px;margin-top: 10px;line-height:22px">
                {{dateFormat(question.stime)}} 至
                {{dateFormat(question.etime)}}</p>
              <button v-if="question.status==1" style="float:right;margin-right:10px" type="button"
                      class="el-button el-button--mini el-button--success is-circle"><i
                class="el-icon-check"></i>
              </button>
              <button v-if="question.status==2" style="float:right;margin-right:10px" type="button"
                      class="el-button el-button--mini el-button--primary is-circle"><i
                class="el-icon-edit"></i>
              </button>
              <button v-if="question.status==3" style="float:right;margin-right:10px" type="button"
                      class="el-button el-button--mini el-button--warning is-circle">
                <i class="el-icon-star-off"></i>
              </button>
              <button v-if="question.status==0" style="float:right;margin-right:10px" type="button"
                      class="el-button el-button--mini el-button--info is-circle"><i
                class="el-icon-close"></i>
              </button>
              <el-tag effect="dark" type="primary" style="float: right;margin-right: 10px">{{question.score}}分
              </el-tag>
              <el-tag effect="dark" type="success" style="float: right;margin-right: 10px">{{question.subject}}
              </el-tag>
            </el-row>
            <el-divider></el-divider>
            <el-row>
              <p>{{question.context}}</p>
            </el-row>
            <el-row style="margin-top: 10px">
              <el-button type="primary" @click="question_Detail(question.question_id)"
                         style="float: right;margin-right: 60px">查看详情
              </el-button>
            </el-row>
          </el-card>
          <el-row style="margin-top:20px" v-if="page_questions.length!=0">
            <el-pagination
              @size-change="handleSizeChange1"
              @current-change="handleCurrentChange1"
              :current-page="currentPage1"
              :page-sizes="[3,4,5]"
              :page-size="3"
              layout="total, sizes, prev, pager, next, jumper"
              :total="totalCount1">
            </el-pagination>
          </el-row>
        </div>
      </el-tab-pane>
      <el-tab-pane label="需求" name="second">
        <div v-if="requests.length==0" style="width:100%;height:200px">
          <h1 style="margin-top: 50px">这里什么都没有哦</h1>
        </div>
        <div style="overflow-y:scroll;margin-top:20px;height: auto;width:100%">
          <el-card v-for="sub_request in page_requests" class="box-card"
                   style="width:80%;margin-top:20px;margin-left:8%;padding-top:10px;text-align: center">
            <el-row>
              <el-avatar :size="40" src="iasystem/avatar/" style="float:left;margin-left:20px"></el-avatar>
              <p style="float:left;margin-left:20px;margin-top: 10px;line-height:22px">{{username}}</p>
              <p style="float:left;margin-left:20px;margin-top: 10px;line-height:22px">
                {{dateFormat(sub_request.stime)}} 至
                {{dateFormat(sub_request.etime)}}</p>
              <button v-if="sub_request.status==1" style="float:right;margin-right:10px" type="button"
                      class="el-button el-button--mini el-button--success is-circle"><i
                class="el-icon-check"></i>
              </button>
              <button v-if="sub_request.status==0" style="float:right;margin-right:10px" type="button"
                      class="el-button el-button--mini el-button--info is-circle"><i
                class="el-icon-close"></i>
              </button>
              <el-tag effect="dark" type="primary" style="float: right;margin-right: 10px">
                {{sub_request.score}}分
              </el-tag>
              <el-tag effect="dark" type="success" style="float: right;margin-right: 10px">{{sub_request.subject}}
              </el-tag>
            </el-row>
            <el-divider></el-divider>
            <el-row>
              <p>{{sub_request.context}}</p>
            </el-row>
            <el-row style="margin-top: 10px">
              <el-button type="primary" @click="request_Detail(sub_request.request_id)"
                         style="float: right;margin-right: 60px">查看详情
              </el-button>
            </el-row>
          </el-card>
          <el-row style="margin-top:20px" v-if="page_requests.length!=0">
            <el-pagination
              @size-change="handleSizeChange2"
              @current-change="handleCurrentChange2"
              :current-page="currentPage2"
              :page-sizes="[3,4,5]"
              :page-size="3"
              layout="total, sizes, prev, pager, next, jumper"
              :total="totalCount2">
            </el-pagination>
          </el-row>
        </div>
      </el-tab-pane>
    </el-tabs>
  </div>
</template>

<script>
  export default {
    name: "MyRelease",
    data() {
      return {
        loading: true,
        activeName: 'first',
        type: true,
        username: '',
        currentPage1: 1,
        pageSize1: 3,
        totalCount1: '',
        currentPage2: 1,
        pageSize2: 3,
        totalCount2: '',
        requests: [],
        page_requests: [],
        questions: [],
        page_questions: [],
        pickerOptions: {
          disabledDate(time) {
            return time.getTime() <= Date.now();
          }
        },
      }
    },
    mounted() {
      if (this.$cookies.get('user_id')) {
        this.get_requests()
      } else {
        this.$router.push('/Login')
      }
    },
    methods: {
      handleClick(tab, event) {
      },
      dateFormat(value) {
        const t = new Date(value);
        const time = t.getFullYear() + '-' + (t.getMonth() + 1) + '-' + t.getDate() + " " + t.getHours() + ":" + t.getMinutes();
        return time;
      },
      get_requests() {
        let that = this
        let param = new URLSearchParams()
        let user_id = that.$cookies.get('user_id')
        param.append('user_id', user_id)
        that.axios({
          method: 'post',
          url: '/iasystem/get_requests/',
          data: param
        })
          .then(function (res) {
            if (res.data.code === 1) {
              that.username = that.$cookies.get('username')
              that.questions = res.data.questions
              that.requests = res.data.requests
              that.totalCount1 = res.data.questions.length
              that.totalCount2 = res.data.requests.length
              that.get_page_question()
              that.get_page_request()
              that.loading = false
            } else if (res.data.code === 0) {
              that.loading = false
              that.$message.error('查询失败')
            }
          })
      },
      get_avatar(value) {
        return "data:image/jpeg;base64," + value
      },
      question_Detail(value) {
        this.$router.push({
          path: `/Question/${value}`,
        })
      },
      request_Detail(value) {
        this.$router.push({
          path: `/Request/${value}`,
        })
      },
      get_page_question() {
        this.page_questions = [];
        for (let i = (this.currentPage1 - 1) * this.pageSize1; i < this.totalCount1; i++) {
          this.page_questions.push(this.questions[i])
          if (this.page_questions.length == this.pageSize1) break;
        }
      },
      get_page_request() {
        this.page_requests = [];
        for (let i = (this.currentPage2 - 1) * this.pageSize2; i < this.totalCount2; i++) {
          this.page_requests.push(this.requests[i])
          if (this.page_requests.length == this.pageSize2) break;
        }
      },
      handleSizeChange1(val) {
        this.pageSize1 = val;
        this.get_page_question()
      },
      handleCurrentChange1(val) {
        this.currentPage1 = val;
        this.get_page_question()
      },
      handleSizeChange2(val) {
        this.pageSize2 = val;
        this.get_page_request()
      },
      handleCurrentChange2(val) {
        this.currentPage2 = val;
        this.get_page_request()
      },
    }
  }
</script>

<style scoped>

</style>
