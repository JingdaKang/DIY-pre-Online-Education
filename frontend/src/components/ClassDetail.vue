<template>
  <div id="ClassDetail" v-loading="loading">
    <h3>课程详情</h3>
    <el-row>
      <label @click="activate_form" style="float:right;margin-right:30px">编辑 <i class="el-icon-edit"></i></label>
    </el-row>
    <el-divider></el-divider>
    <el-form ref="course" style="margin-left: 10%;width: 80%" :disabled="disabled" :model="course" :rules="rules">
      <el-row style="text-align: center">
        <el-col :span="12">
          <el-form-item style="width: 70%" label="课程名称" prop="name">
            <el-input style="width: 70%" v-model="course.name"></el-input>
          </el-form-item>
        </el-col>
        <el-col :span="12">
          <el-form-item label="开课时间" prop="stime">
            {{course.stime}}
          </el-form-item>
        </el-col>
      </el-row>
      <el-row style="text-align: center">
        <el-col :span="12">
          <el-form-item style="width: 70%" label="当前人数" prop="number">
            {{course.number}}
          </el-form-item>
        </el-col>
        <el-col :span="12">
          <el-form-item style="width: 70%" label="最大人数" prop="maxnum">
            <el-input-number style="width: 70%" v-model="course.maxnum" @change="handleChange" :min="course.number"
                             :max="300"></el-input-number>
          </el-form-item>
        </el-col>
      </el-row>
      <el-row style="text-align: center;">
        <el-col :span="12">
          <el-form-item style="width: 70%" label="课程状态" prop="status">
            {{course.status==0?'已结课':'教学中'}}
          </el-form-item>
        </el-col>
        <el-col :span="12">
          <el-form-item style="width: 70%" label="课程时长" prop="time">
            <el-input-number style="width: 70%" v-model="course.time" @change="handleChange" :min="2"
                             :max="200"></el-input-number>
          </el-form-item>
        </el-col>
      </el-row>
      <el-row style="text-align: center;margin-top:30px">
        <el-button type="success" @click="modify_course()">修改</el-button>
        <el-button type="info" @click="lock_form()" style="margin-left:10%">取消</el-button>
      </el-row>
    </el-form>
    <el-divider></el-divider>
    <h3>课程管理</h3>
    <el-divider></el-divider>
    <el-row style="width: 80%;margin-left: 10%">
      <el-form label-width="80px">
        <el-col :span="6">
          <el-form-item prop="type" label="申请类型">
            <el-select v-model="type">
              <el-option label="不限" value=""></el-option>
              <el-option label="撤课" value="O"></el-option>
              <el-option label="选课" value="J"></el-option>
            </el-select>
          </el-form-item>
        </el-col>
        <el-col :span="6">
          <el-form-item prop="status" label="状态">
            <el-select v-model="status">
              <el-option label="不限" value=""></el-option>
              <el-option label="已拒绝" value="0"></el-option>
              <el-option label="待处理" value="1"></el-option>
              <el-option label="已同意" value="2"></el-option>
            </el-select>
          </el-form-item>
        </el-col>
        <el-col :span="6">
          <el-form-item>
            <el-button type="primary" icon="el-icon-search" style="float:left;margin-left: 0px"
                       @click="get_student_apply_by_condition">查询
            </el-button>
          </el-form-item>
        </el-col>
      </el-form>
    </el-row>
    <el-table :data="page_apply" ref="class"
              style="width: 80%;margin-left:10%;margin-top:20px" border>
      <el-table-column prop="username" label="学生名" min-width="100" align="center">
        <template slot-scope="scope">
          {{scope.row.username}}
        </template>
      </el-table-column>
      <el-table-column prop="type" label="申请类型" min-width="100" align="center">
        <template slot-scope="scope">
          <p v-if="scope.row.type=='J'">选课</p>
          <p v-if="scope.row.type=='O'">撤课</p>
        </template>
      </el-table-column>
      <el-table-column prop="stime" label="申请时间" min-width="100px" align="center">
        <template slot-scope="scope">
          {{dateFormat(scope.row.time)}}
        </template>
      </el-table-column>
      <el-table-column prop="etime" label="处理时间" min-width="100px" align="center">
        <template slot-scope="scope">
          {{dateFormat(scope.row.etime)}}
        </template>
      </el-table-column>
      <el-table-column prop="option" label="处理" min-width="100" align="center">
        <template slot-scope="scope">
          <p v-if="scope.row.status==0">已拒绝</p>
          <p v-if="scope.row.status==2">已同意</p>
          <el-row v-if="scope.row.status==1" style="text-align: center">
            <el-button size="medium" type="success" plain
                       @click="accept_student_apply(scope.row.id)">同意
            </el-button>
          </el-row>
          <el-row v-if="scope.row.status==1" style="text-align: center;margin-top: 8px">
            <el-button size="medium" type="danger" plain
                       @click="refuse_student_apply(scope.row.id)">拒绝
            </el-button>
          </el-row>
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
    name: "ClassDetail",
    data() {
      return {
        loading: false,
        type: '',
        status: '',
        disabled: true,
        currentPage: 1,
        totalCount: '',
        pageSize: 5,
        course: {
          name: '',
          stime: '',
          number: '',
          maxnum: '',
          status: '',
          time: ''
        },
        student_apply: [],
        page_apply: [],
        pickerOptions: {
          disabledDate(time) {
            return time.getTime() <= Date.now();
          }
        },
        rules: {}
      }
    },
    mounted: function () {
      this.get_class_detail(this.$route.params.id)
      this.get_student_apply(this.$route.params.id)
    },
    methods: {
      activate_form() {
        this.disabled = false
      },
      lock_form() {
        this.disabled = true
      },
      handleChange(value) {
      },
      get_class_detail(value) {
        let class_id = value
        let that = this
        let param = new URLSearchParams()
        param.append('class_id', class_id)
        that.axios({
          method: 'post',
          url: '/api/get_class_detail/',
          data: param
        })
          .then(function (res) {
            if (res.data.code === 1) {
              that.course = res.data.course[0]
            } else if (res.data.code === 0) {
              that.$message.error('查询失败')
            }
          })
      },
      get_student_apply(value) {
        let class_id = value
        let that = this
        let param = new URLSearchParams()
        param.append('class_id', class_id)
        that.axios({
          method: 'post',
          url: '/api/get_student_apply/',
          data: param
        })
          .then(function (res) {
            if (res.data.code === 1) {
              that.student_apply = res.data.student_apply
              console.log(that.student_apply)
              that.totalCount = that.student_apply.length
              that.get_page_student_apply()
            } else if (res.data.code === 0) {
              that.$message.error('查询失败')
            }
          })
      },
      get_student_apply_by_condition() {
        let that = this
        let class_id = that.$route.params.id
        let param = new URLSearchParams()
        let type = that.type
        let status = that.status
        param.append('class_id', class_id)
        param.append('type', type)
        param.append('status', status)
        that.axios({
          method: 'post',
          url: '/api/get_student_apply_by_condition/',
          data: param
        })
          .then(function (res) {
            if (res.data.code === 1) {
              that.$message.success('查询成功')
              that.student_apply = res.data.condition_apply
              that.totalCount = that.student_apply.length
              that.get_page_student_apply()
            } else if (res.data.code === 0) {
              that.$message.error('查询失败')
            }
          })
      },
      get_page_student_apply() {
        this.page_apply = [];
        for (let i = (this.currentPage - 1) * this.pageSize; i < this.totalCount; i++) {
          this.page_apply.push(this.student_apply[i])
          if (this.student_apply.length == this.pageSize) break;
        }
      },
      dateFormat(value) {
        if (value == null)
          return '暂未处理'
        const t = new Date(value);
        const time = t.getFullYear() + '-' + (t.getMonth() + 1) + '-' + t.getDate() + " " + t.getHours() + ":" + t.getMinutes();
        return time;
      },
      accept_student_apply(value) {
        let apply_id = value
        let that = this
        let param = new URLSearchParams()
        param.append('apply_id', apply_id)
        that.axios({
          method: 'post',
          url: '/api/accept_student_apply/',
          data: param
        })
          .then(function (res) {
            if (res.data.code === 1) {
              that.$message.success('操作成功')
              setTimeout(function () {
                that.$router.go(0)
              }.bind(that), 1000)
            } else if (res.data.code === 0) {
              that.$message.error('操作失败')
            }
          })
      },
      refuse_student_apply(value) {
        let apply_id = value
        let that = this
        let param = new URLSearchParams()
        param.append('apply_id', apply_id)
        that.axios({
          method: 'post',
          url: '/api/refuse_student_apply/',
          data: param
        })
          .then(function (res) {
            if (res.data.code === 1) {
              that.$message.success('操作成功')
              setTimeout(function () {
                that.$router.go(0)
              }.bind(that), 1000)
            } else if (res.data.code === 0) {
              that.$message.error('操作失败')
            }
          })
      },
      handleSizeChange(val) {
        this.pageSize = val;
        this.get_page_student_apply()
      },
      handleCurrentChange(val) {
        this.currentPage = val;
        this.get_page_student_apply()
      },
      modify_course() {
        let that = this
        let class_id = that.$route.params.id
        let name = that.course.name
        let maxnum = that.course.maxnum
        let time = that.course.time
        let param = new URLSearchParams()
        param.append('class_id', class_id)
        param.append('name', name)
        param.append('maxnum', maxnum)
        param.append('time', time)
        that.axios({
          method: 'post',
          url: '/api/modify_course/',
          data: param
        })
          .then(function (res) {
            if (res.data.code === 1) {
              that.$message.success('操作成功')
            } else if (res.data.code === 0) {
              that.$message.error('操作失败')
            } else if (res.data.code === 2) {
              that.$message.info('你已创建该课程名')
            }
          })
      }

    }

  }
</script>

<style scoped>

</style>
