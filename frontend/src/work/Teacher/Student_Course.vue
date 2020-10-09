<template>
  <div>
    <el-main
      v-loading="loading"
      element-loading-text="加载中">
      <!--学生-课程管理界面-->
      <el-col
        :offset="0"
        :span="24">
        <el-col :span="2" >
          <el-button @click="addCourse()" type="primary">添加课程</el-button>
        </el-col>
        <el-col :span="20">
          <el-button @click="clearFilter()">清除过滤器</el-button>
          <el-input
            style="width:160px;"
            prefix-icon="el-icon-search"
            class="search"
            v-model="search1"
            placeholder="输入关键字搜索"/>
        </el-col>
        <el-table
          ref="filterTable"
          stripe
          :data="courseData1"
          empty-text="暂无数据">
          <el-table-column
            prop="courseid"
            label="课程编号"
            width="150">
          </el-table-column>
          <el-table-column
            prop="coursename"
            label="课程名"
            width="200">
          </el-table-column>
          <el-table-column
            prop="grade"
            label="年级"
            sortable
            column-key="年级"
            :filters="[
                  {text: '2018', value: '2018'},{text: '2019', value: '2019'},
                  {text: '2020', value: '2020'},{text: '2021', value: '2021'},]"
            :filter-method="filterHandler"
            width="100">
          </el-table-column>
          <el-table-column
            prop="semester"
            label="学期"
            width="80">
          </el-table-column>
          <el-table-column
            prop="number"
            label="选课人数"
            width="80">
          </el-table-column>
          <el-table-column
            prop="maxnum"
            label="最大人数"
            width="80">
          </el-table-column>
          <el-table-column
            prop="credit"
            label="学分"
            width="100">
          </el-table-column>
          <el-table-column
            prop="type"
            label="课程类型"
            column-key="type"
            :filters="[
                  {text: '公共必修', value: '公共必修'},{text: '公共选修', value: '公共选修'},
                  {text: '专业必修', value: '专业必修'},{text: '专业选修', value: '专业选修'}]"
            :filter-method="filterHandler"
            width="100">
          </el-table-column>
          <el-table-column
            label="操作"
            width="320">
            <template slot-scope="scope">
              <el-button @click="editStudent(scope.row.courseid)" type="primary" >管理学生
                <i class="el-icon-user"></i></el-button>
              <el-button @click="deleteCourse(scope.row.courseid)" type="danger" >删除
                <i class="el-icon-delete"></i></el-button>
            </template>
          </el-table-column>
        </el-table>
      </el-col>
    </el-main>
    <!-- 添加课程弹窗-->
    <el-dialog
      title="添加课程"
      :visible.sync="addCoursedialog">
      <div>
        <el-form :model="addForm">
          <el-form-item
            label="课程名：">
            <el-input
              v-model="addForm.Coursename"
              clearable
              placeholder="请输入课程名">
            </el-input>
          </el-form-item>

          <el-form-item
            label="年级：">
            <el-input
              v-model="addForm.year"
              clearable
              placeholder="请输入年级">
            </el-input>
          </el-form-item>

          <el-form-item
            label="学期：">
            <el-radio v-model="addForm.Semester" :label="1" border>1</el-radio>
            <el-radio v-model="addForm.Semester" :label="2" border>2</el-radio>
          </el-form-item>

          <el-form-item
            label="课程类型：">
            <el-radio v-model="addForm.type" :label="1" border>公共必修</el-radio>
            <el-radio v-model="addForm.type" :label="2" border>公共选修</el-radio>
            <el-radio v-model="addForm.type" :label="3" border>专业必修</el-radio>
            <el-radio v-model="addForm.type" :label="4" border>专业选修</el-radio>
          </el-form-item>

          <el-form-item
            label="最大人数：">
            <el-input
              v-model="addForm.maxnum"
              clearable
              placeholder="请输入最大人数：">
            </el-input>
          </el-form-item>

          <el-form-item
            label="教师姓名：">
            <el-input
              v-model="addForm.tname"
              clearable
              placeholder="请输入教师姓名：">
            </el-input>
          </el-form-item>

          <el-form-item
            label="学分：">
            <el-input
              v-model="addForm.credit"
              clearable
              placeholder="请输入学分：">
            </el-input>
          </el-form-item>

          <el-form-item>
            <el-button type="primary" @click="upCourse" round>提交</el-button>
            <el-button @click="clearaddForm" round>清空</el-button>
          </el-form-item>

        </el-form>
      </div>
    </el-dialog>
    <!--学生de课程管理弹窗-->
    <el-dialog
      title="学生管理"
      :visible.sync="studentdialog"
      width="40%">
      <div style="height:400px">
        <el-col
          :span="12">
          <el-row>
            <label>未选课学生</label>
          </el-row>
          <el-table
            :data="weiData"
            empty-text="暂无数据">
            <el-table-column
              prop="username"
              label="用户名"
              width="160">
            </el-table-column>
            <el-table-column
              label="操作"
              width="80">
              <template slot-scope="scope">
                <el-button size="small" @click="getin(scope.row.username)" type="primary" >移入</el-button>
              </template>
            </el-table-column>
          </el-table>
        </el-col>

        <el-col
          :span="12">
          <el-row>
            <label>已选课学生</label>
          </el-row>
          <el-table
            :data="yiData"
            empty-text="暂无数据">
            <el-table-column
              prop="username"
              label="用户名"
              width="160">
            </el-table-column>
            <el-table-column
              label="操作"
              width="80">
              <template slot-scope="scope">
                <el-button size="small" @click="getout(scope.row.username)" type="danger" >移出</el-button>
              </template>
            </el-table-column>

          </el-table>
        </el-col>
      </div>
    </el-dialog>
  </div>
</template>

<script>
    export default {
        name: "Student_Course",
      data() {
        return {
          user: '',
          loading: false,
          search1: '',
          courseData: [],
          weiData:[],
          yiData:[],
          addCoursedialog: false,
          studentdialog: false,
          courseid: '',

          addForm:{
            Coursename:'',
            year:2020,
            Semester:1,
            type:1,
            maxnum:null,
            tname: '',
            credit:null,
          },
        }
      },
      methods: {
        GetCourse(){
          this.GetTeacherCourse();
          setTimeout(() => {
            this.loading = false;
          }, 1000);
        },
        GetTeacherCourse(){
          this.courseData = [];
          this.loading = true;
          this.$axios.post('/api/GetTeacherCourse', {user: this.user})
            .then((response) =>{
              if(response.data.mes===1)
                this.courseData=[];
              else {
                let tt = unescape(response.data.mes).split(',');
                for (let i = 0; i < tt.length / 10; i++) {
                  let t = i * 10;
                  let ttt = {
                    courseid: tt[t],
                    coursename: tt[t + 1],
                    credit: tt[t + 2],
                    number: tt[t + 3],
                    maxnum: tt[t + 4],
                    teachername: tt[t + 5],
                    type: this.changetype(tt[t + 6]),
                    grade: tt[t + 7],
                    semester: tt[t + 8]
                  };
                  this.courseData.push(ttt);
                }
              }
            });
        },
        addCourse(){
          this.addCoursedialog = true;
        },
        editStudent(cid){
          this.yiData=[];
          this.weiData=[];
          this.courseid = cid;
          this.studentdialog=true;
          this.$axios.post('/api/AddCourse?edit=1',{
            cid:cid
          }).then((res)=>{
            let tt=unescape(res.data.yilist).split(',');
            for(let i=0; i<tt.length; i++){
              let ttt = {username:tt[i]};
              this.yiData.push(ttt);
            }
            let tt1=unescape(res.data.weilist).split(',');
            for(let i=0; i<tt1.length; i++){
              let ttt = {username:tt1[i]};
              this.weiData.push(ttt);
            }
          });
        },
        deleteCourse(cid){
          this.$axios.post('/api/AddCourse?delete=1', {
            cid:cid
          }).then((res)=>{
            this.$message.success("删除成功！");
            this.GetCourse();
          })
        },

        upCourse(){
          this.$axios.post('/api/AddCourse', {
            username: this.user,
            coursename: this.addForm.Coursename,
            year: this.addForm.year,
            semester: this.addForm.Semester,
            type: this.addForm.type,
            maxnum: this.addForm.maxnum,
            tname: this.addForm.tname,
            credit: this.addForm.credit
          })
            .then((res) =>{
              if(res.data.code===0)
                this.$message.error(res.data.msg);
              else if(res.data.code===1) {
                this.$message.success((res.data.msg));
                this.addCoursedialog = false;
                this.addForm.Coursename='';
                this.addForm.year=2020;
                this.addForm.Semester=1;
                this.addForm.type=1;
                this.addForm.maxnum=null;
                this.addForm.tname= '';
                this.addForm.credit=null;
                this.GetCourse();
              }
            });
        },
        clearaddForm(){
          this.addForm.Coursename='';
          this.addForm.year=2020;
          this.addForm.Semester=1;
          this.addForm.type=1;
          this.addForm.maxnum=null;
          this.addForm.tname= '';
          this.addForm.credit=null;
        },
        getin(username){
          this.$axios.post('/api/AddCourse?getin=1',{
            username:username,
            cid:this.courseid,
          }).then((res)=>{
            this.$message.success("移入成功！");
            this.editStudent(this.courseid);
          })
        },
        getout(username){
          this.$axios.post('/api/AddCourse?getout=1',{
            username:username,
            cid:this.courseid,
          }).then((res)=>{
            this.$message.success("移出成功！");
            this.editStudent(this.courseid);
          })
        },

        changetype(a){
          if(a==="MR")
            return '专业必修';
          else if(a==="ME")
            return '专业选修';
          else if(a==="PR")
            return '公共必修';
          else if(a==="PE")
            return '公共选修';
        },
        clearFilter() {
          this.$refs.filterTable.clearFilter();
        },
        filterHandler(value, row, column) {
          const property = column['property'];
          return row[property] === value;
        },
      },
      mounted() {
        this.user=this.$cookies.get('username');
        this.GetCourse();
      },
      computed: {
        courseData1:function () {
          let search=this.search1;
          if(search){
            return  this.courseData.filter(function(dataNews){
              return Object.keys(dataNews).some(function(key){
                return String(dataNews[key]).toLowerCase().indexOf(search) > -1
              })
            })
          }
          return this.courseData
        },
      },
    }
</script>

<style scoped>

</style>
