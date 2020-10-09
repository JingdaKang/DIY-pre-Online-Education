<template>
  <div id="AddRelease" v-loading="loading">
    <el-card class="box-card" style="width:80%;margin-top:20px;margin-left:8%;text-align: center">
      <p style="font-size:20px;font-weight:bold">
        新增发布
      </p>
      <el-form label-width="80px"
               style="text-align:center;margin-top:20px;margin-left:15px;padding-top: 10px;padding-bottom: 10px"
               :model="formData"
               :rules="rule">
        <el-form-item label="需求类型" prop="type">
          <el-col :span="14">
            <el-select v-model="formData.type">
              <el-option label="问题" value="Q"></el-option>
              <el-option label="资源" value="R"></el-option>
            </el-select>
          </el-col>
        </el-form-item>
        <el-form-item label="所属科目" prop="subject">
          <el-col :span="14">
            <el-select v-model="formData.subject" placeholder=""
                       filterable
                       @blur="selectBlur">
              <el-option v-for="(item,index) in subjectList" :key="index" :label="item.subject_name"
                         :value="item.subject_id"></el-option>
            </el-select>
          </el-col>
        </el-form-item>
        <el-form-item label="积分" prop="score">
          <el-col :span="14">
            <el-input-number v-model="formData.score" @change="handleChange" :min="1" :max="5"></el-input-number>
          </el-col>
        </el-form-item>
        <el-form-item label="截止时间" prop="deadline">
          <el-col :span="14">
            <el-date-picker
              v-model="formData.deadline"
              type="datetime"
              placeholder="选择截止时间"
              :picker-options="pickerOptions">
            </el-date-picker>
          </el-col>
        </el-form-item>
        <el-form-item label="内容描述" prop="context">
          <el-input v-model="formData.context">
          </el-input>
        </el-form-item>
        <el-row style="text-align: center;margin-top:30px">
          <el-button type="success" @click="submit()">提交</el-button>
          <el-button type="info" @click="cancel()" style="margin-left:10%">取消</el-button>
        </el-row>
      </el-form>
    </el-card>
  </div>
</template>

<script>
  export default {
    name: "AddRequest",
    data() {
      return {
        formData: {
          type: '',
          subject: '',
          deadline: '',
          score: '',
          context: '',
        },
        loading: false,
        subjectList: [],
        pickerOptions: {
          disabledDate(time) {
            return time.getTime() <= Date.now();
          }
        },
        rule: {
          type: [
            {required: true, message: '请选择类型', trigger: 'blur'}
          ],
          subject: [
            {required: true, message: '请选择科目', trigger: 'blur'}
          ],
          score: [
            {
              required: true, message: '请选择分值', trigger: 'blur'
            }
          ],
          context: [
            {
              required: true, message: '请输入内容', trigger: 'blur'
            },
            {
              max: 60, message: '超过限定字数', trigger: 'blur'
            }
          ]
        }
      }
    },
    mounted(){
    this.getSubject()
    },
    methods: {
      selectBlur(e) {
        this.subject = e.target.value
      },
      handleChange(value) {
      },
      getSubject() {
        let that = this
        that.$http.get('/iasystem/subjects/')
          .then(function (res) {
            if (res.data.code === 1) {
              that.subjectList = res.data.subjects
            } else if (res.data.code === 0) {
              that.$message.error('查询类别失败')
            }
          })
      },
      submit() {
        let that = this
        that.loading = true
        let param = new URLSearchParams()
        let user_id = that.$cookies.get('user_id')
        param.append('user_id', user_id)
        param.append('type', this.formData.type)
        param.append('subject', this.formData.subject)
        param.append('deadline', that.dateConversion(this.formData.deadline))
        param.append('score', this.formData.score)
        param.append('context', this.formData.context)
        that.axios({
          method: 'post',
          url: '/iasystem/release_request/',
          data: param
        })
          .then(function (res) {
            if (res.data.code === 1) {
            that.loading=false
              that.$message(
                {
                  message: res.data.msg,
                  type: 'success'
                }
              )
               setTimeout(function () {
                that.$router.go(0)
              }.bind(that), 1000)
            } else if (res.data.code === 0) {
              that.loading=false
               that.$message(
                {
                  message: res.data.msg,
                  type: 'error'
                }
              )
            } else if (res.data.code === 2) {
              that.loading=false
              that.$message(
                {
                  message: res.data.msg,
                  type: 'info'
                })
            } else if (res.data.code === 3) {
              that.loading=false
              that.$message(
                {
                  message: res.data.msg,
                  type: 'info'
                })
            }
          })
      },
      dateConversion(value) {
        const t = new Date(value);
        const time = t.getFullYear() + '-' + (t.getMonth() + 1) + '-' + t.getDate() + " " + t.getHours() + ":" + t.getMinutes() + ":" + t.getSeconds();
        return time;
      },
      cancel() {
        this.formData = ''
      },
    }
  }
</script>

<style scoped>

</style>
