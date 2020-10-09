<template>
  <div id="AllClass" v-loading="loading">
    <el-row>
      <p style="font-size:20px;font-weight:bold;margin-top:25px">
        所有课程
      </p>
    </el-row>
    <el-divider></el-divider>
    <el-row>
      <el-form label-width="80px">
        <el-col :span="6">
          <el-form-item prop="name" label="课程名">
            <el-input v-model="name" style="float:left;width:90%;margin-left:10px"></el-input>
          </el-form-item>
        </el-col>
        <el-col :span="6">
          <el-form-item prop="teacher" label="任课老师">
            <el-select v-model="teacher" placeholder=""
                       filterable
                       @blur="selectBlur">
              <el-option label="不限" value="0"></el-option>
              <el-option v-for="(item,index) in teacherList" :key="index" :label="item.username"
                         :value="item.id"></el-option>
            </el-select>
          </el-form-item>
        </el-col>
        <el-col :span="6">
          <el-form-item prop="status" label="课程状态">
            <el-select v-model="status" style="float: left;margin-left: 25px">
              <el-option label="不限" value=""></el-option>
              <el-option label="结束" value="0"></el-option>
              <el-option label="活跃" value="1"></el-option>
            </el-select>
          </el-form-item>
        </el-col>
        <el-col :span="6">
          <el-form-item>
            <el-button type="primary" icon="el-icon-search" style="float:left;margin-left: 0px"
                       v-on:click="get_all_class_by_condition">查询
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
      <el-table-column prop="teacher" label="教师" min-width="100" align="center">
        <template slot-scope="scope">
          {{scope.row.teacher}}
        </template>
      </el-table-column>
      <el-table-column prop="time" label="课时" min-width="100" align="center">
        <template slot-scope="scope">
          {{scope.row.time}}
        </template>
      </el-table-column>
      <el-table-column prop="number" label="选课人数" min-width="100" align="center">
        <template slot-scope="scope">
          {{scope.row.number}}
        </template>
      </el-table-column>
      <el-table-column prop="maxnum" label="最大人数" min-width="100" align="center">
        <template slot-scope="scope">
          {{scope.row.maxnum}}
        </template>
      </el-table-column>
      <el-table-column prop="status" label="课程状态" min-width="100" align="center">
        <template slot-scope="scope">
          <p v-if="scope.row.status==0">已结课</p>
          <p v-if="scope.row.status==1">教学中</p>
        </template>
      </el-table-column>
      <el-table-column v-if="this.$cookies.get('type')=='S'" prop="option" label="操作" min-width="100" align="center">
        <template slot-scope="scope">
          <el-row v-if="scope.row.status==1" style="text-align: center">
            <el-button v-if="scope.row.choose==0&&scope.row.number<scope.row.maxnum&&scope.row.operate!=1" size="medium"
                       type="success" plain
                       @click="select_class(scope.row.id)">选课
            </el-button>
            <p v-if="scope.row.choose==0&&scope.row.number>=scope.row.maxnum">人数已满</p>
            <p v-if="scope.row.choose==1">已选</p>
            <p v-if="scope.row.choose==0&&scope.row.operate==1">申请中</p>
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
    name: "AllClass",
    data() {
      return {
        name: '',
        teacher: '0',
        status: '',
        type: '',
        loading: false,
        currentPage: 1,
        totalCount: '',
        pageSize: 5,
        classList: [],
        page_classes: [],
        teacherList: []
      }
    },
    mounted() {
      this.get_teacher()
      this.get_all_class()
    },
    methods: {
      get_teacher() {
        let that = this
        that.$http.get('/api/get_teacher/')
          .then(function (res) {
            if (res.data.code === 1) {
              that.teacherList = res.data.teacherList
            } else if (res.data.code === 0) {
              that.$message.error('查询教师失败')
            }
          })
      },
      selectBlur(e) {
        this.teacher = e.target.value
      },
      select_class(value) {
        let that = this
        let class_id = value
        let user_id = that.$cookies.get('user_id')
        let type = 'J'
        let param = new URLSearchParams()
        param.append('class_id', class_id)
        param.append('user_id', user_id)
        param.append('type', type)
        that.axios({
          method: 'post',
          url: '/api/select_class/',
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
      get_all_class_by_condition() {
        let that = this
        let name = that.name
        let teacher = that.teacher
        let status = that.status
        let user_id = that.$cookies.get('user_id')
        let param = new URLSearchParams()
        param.append('user_id', user_id)
        param.append('name', name)
        param.append('teacher', teacher)
        param.append('status', status)
        that.axios({
          method: 'post',
          url: '/api/get_all_class_by_condition/',
          data: param
        })
          .then(function (res) {
            if (res.data.code === 1) {
              that.classList = res.data.condition_class
              that.totalCount = that.classList.length
              that.get_page_class()
              that.$message.success('查询成功')
            } else if (res.data.code === 0) {
              that.$message.error('查询失败')
            }
          })
      },
      get_all_class() {
        let that = this
        let user_id = that.$cookies.get('user_id')
        let param = new URLSearchParams()
        param.append('user_id', user_id)
        that.axios({
          method: 'post',
          url: '/api/get_all_class/',
          data: param
        })
          .then(function (res) {
            if (res.data.code === 1) {
              that.classList = res.data.classes
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
    }

  }
</script>

<style scoped>

</style>
