<template>
  <div id="ReleaseClass" v-loading="loading">
    <el-card class="box-card" style="width:80%;margin-top:20px;margin-left:8%;text-align: center">
      <p style="font-size:20px;font-weight:bold">
        发布课程
      </p>
      <el-form label-width="80px"
               style="text-align:center;margin-top:20px;margin-left:15px;padding-top: 10px;padding-bottom: 10px"
               :model="class_info"
               :rules="rule">
        <el-form-item label="课程名称" prop="name">
          <el-col :span="14">
            <el-input v-model="class_info.name"></el-input>
          </el-col>
        </el-form-item>
        <el-form-item label="课时" prop="time">
          <el-col :span="14">
            <el-input-number v-model="class_info.time" @change="handleChange" :min="2" :max="200"></el-input-number>
          </el-col>
        </el-form-item>
        <el-form-item label="最大人数" prop="maxnum">
          <el-col :span="14">
            <el-input-number v-model="class_info.maxnum" @change="handleChange" :min="30" :max="300"></el-input-number>
          </el-col>
        </el-form-item>
        <el-form-item label="开课时间" prop="stime">
          <el-col :span="14">
            <el-date-picker
              v-model="class_info.stime"
              type="date"
              placeholder="选择开课时间"
              :picker-options="pickerOptions">
            </el-date-picker>
          </el-col>
        </el-form-item>
        <el-form-item label="开课理由" prop="reason">
          <el-input v-model="class_info.reason">
          </el-input>
        </el-form-item>
        <el-row style="text-align: center;margin-top:30px">
          <el-button type="success" @click="submit()">提交</el-button>
          <el-button type="info" @click="cancel()" style="margin-left:10%">取消</el-button>
        </el-row>
      </el-form>
    </el-card>
    <el-divider></el-divider>
    <h3>申请记录</h3>
    <el-divider></el-divider>
    <el-row>
      <el-form label-width="80px" style="width: 60%;margin-left: 20%">
        <el-col :span="12">
          <el-form-item prop="status" label="状态">
            <el-select v-model="status">
              <el-option label="不限" value=""></el-option>
              <el-option label="已拒绝" value="0"></el-option>
              <el-option label="待处理" value="1"></el-option>
              <el-option label="已同意" value="2"></el-option>
            </el-select>
          </el-form-item>
        </el-col>
        <el-col :span="12">
          <el-form-item>
            <el-button type="primary" icon="el-icon-search" style="float:left;margin-left: 0px"
                       v-on:click="get_teacher_apply_by_condition">查询
            </el-button>
          </el-form-item>
        </el-col>
      </el-form>
    </el-row>
    <el-table :data="page_classes" ref="class"
              style="width: 100%;margin-top:20px" border>
      <el-table-column prop="name" label="课程名" min-width="100" align="center">
        <template slot-scope="scope">
          {{scope.row.name}}
        </template>
      </el-table-column>
      <el-table-column prop="time" label="课时" align="center">
        <template slot-scope="scope">
          {{scope.row.time}}
        </template>
      </el-table-column>
      <el-table-column prop="maxnum" label="最大人数" align="center">
        <template slot-scope="scope">
          {{scope.row.maxnum}}
        </template>
      </el-table-column>
      <el-table-column prop="stime" label="申请时间" align="center">
        <template slot-scope="scope">
          {{scope.row.stime}}
        </template>
      </el-table-column>
      <el-table-column label="开课理由" prop="reason" min-width="100" align="center">
        <template slot-scope="scope">
          {{scope.row.reason}}
        </template>
      </el-table-column>
      <el-table-column prop="option" label="操作" min-width="100" align="center">
        <template slot-scope="scope">
          <p v-if="scope.row.status==0">已拒绝</p>
          <p v-if="scope.row.status==2">已同意</p>
          <p v-if="scope.row.status==1">待处理</p>
        </template>
      </el-table-column>
    </el-table>
    <el-row style="margin-top:20px">
      <el-pagination
        @size-change="handleSizeChange"
        @current-change="handleCurrentChange"
        :current-page="currentPage"
        :page-sizes="[5, 6, 8, 10]"
        :page-size="5"
        layout="total, sizes, prev, pager, next, jumper"
        :total="totalCount">
      </el-pagination>
    </el-row>
  </div>
</template>

<script>
  export default {
    name: "ReleaseClass",
    data() {
      return {
        class_info: {
          name: '',
          stime: '',
          time: '',
          maxnum: '',
          reason: '',
        },
        status:'',
        loading: false,
        currentPage: 1,
        totalCount: '',
        pageSize: 5,
        classList: [],
        page_classes: [],
        pickerOptions: {
          disabledDate(time) {
            return time.getTime() <= Date.now();
          }
        },
        rule: {
          name: [
            {required: true, message: '请输入课程名', trigger: 'blur'}
          ],
          stime: [
            {required: true, message: '请输入开课时间', trigger: 'blur'}
          ],
          time: [
            {
              required: true, message: '请输入课时', trigger: 'blur'
            }
          ],
          maxnum: [
            {
              required: true, message: '请输入最大人数', trigger: 'blur'
            }
          ],
          reason: [
            {
              required: true, message: '请输入开课理由', trigger: 'blur'
            }
          ]
        }
      }
    },
    mounted: function () {
      this.get_teacher_apply()
    }
    ,
    methods: {
      handleChange(value) {
      },
      get_teacher_apply_by_condition() {
        let that = this
        let user_id = that.$cookies.get('user_id')
        let status = that.status
        let param = new URLSearchParams()
        param.append('user_id', user_id)
        param.append('status', status)
        that.axios({
          method: 'post',
          url: '/api/get_teacher_apply_by_condition/',
          data: param
        })
          .then(function (res) {
            if (res.data.code === 1) {
              that.classList = res.data.condition_apply
              that.totalCount = that.classList.length
              that.get_page_class()
            } else if (res.data.code === 0) {
              that.$message.error('查询失败')
            }
          })
      },
      get_teacher_apply() {
        let that = this
        let user_id = that.$cookies.get('user_id')
        let param = new URLSearchParams()
        param.append('user_id', user_id)
        that.axios({
          method: 'post',
          url: '/api/get_teacher_apply/',
          data: param
        })
          .then(function (res) {
            if (res.data.code === 1) {
              that.classList = res.data.apply_list
              that.totalCount = that.classList.length
              that.get_page_class()
            } else if (res.data.code === 0) {
              that.$message.error('查询失败')
            }
          })
      },
      get_page_class() {
        this.page_classes = [];
        for (let i = (this.currentPage - 1) * this.pageSize; i < this.totalCount; i++) {
          this.page_classes.push(this.classList[i])
          if (this.page_classes.length == this.pageSize) break;
        }
      },
      handleSizeChange(val) {
        this.pageSize = val;
        this.get_page_class()
      },
      handleCurrentChange(val) {
        this.currentPage = val;
        this.get_page_class()
      },
      submit() {
        let that = this
        that.loading = true
        let param = new URLSearchParams()
        let user_id = that.$cookies.get('user_id')
        param.append('user_id', user_id)
        param.append('name', that.class_info.name)
        param.append('stime', that.dateConversion(that.class_info.stime))
        param.append('time', that.class_info.time)
        param.append('maxnum', that.class_info.maxnum)
        param.append('reason', that.class_info.reason)
        that.axios({
          method: 'post',
          url: '/api/apply_class/',
          data: param
        })
          .then(function (res) {
            if (res.data.code === 1) {
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
              that.loading = false
              that.$message.error('发布失败')
            } else if (res.data.code === 2) {
              that.loading = false
              that.$message(
                {
                  message: res.data.msg,
                  type: 'info'
                })
            } else if (res.data.code === 3) {
              that.loading = false
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
        const time = t.getFullYear() + '-' + (t.getMonth() + 1) + '-' + t.getDate();
        return time;
      },
      cancel() {
        this.class_info = ''
      },
    }
  }
</script>

<style scoped>

</style>
