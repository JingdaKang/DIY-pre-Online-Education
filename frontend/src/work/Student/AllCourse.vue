<template>
  <div>
    <el-main
      v-loading="loading"
      element-loading-text="加载中">
      <!-- 所有课程界面 -->
      <el-col
        :offset="1"
        :span="22">
        <el-button @click="clearFilter()">清除过滤器</el-button>
        <el-input
          style="width:160px;"
          prefix-icon="el-icon-search"
          class="search"
          v-model="search2"
          placeholder="输入关键字搜索"/>
        <el-table
          ref="filterTable"
          stripe
          :data="AllCourseData1"
          empty-text="暂无数据">
          <el-table-column
            prop="id"
            label="课头号"
            width="200">
          </el-table-column>
          <el-table-column
            prop="coursename"
            label="课程名"
            width="200">
          </el-table-column>
          <el-table-column
            prop="stime"
            label="开课时间"
            sortable
            width="160">
          </el-table-column>
          <el-table-column
            prop="time"
            label="学时"
            sortable
            width="100">
          </el-table-column>
          <el-table-column
            prop="teachername"
            label="教师姓名"
            width="160">
          </el-table-column>
          <el-table-column
            prop="number"
            label="选课人数"
            sortable
            width="100">
          </el-table-column>
          <el-table-column
            prop="maxnum"
            label="最大人数"
            sortable
            width="100">
          </el-table-column>
          <el-table-column
            prop="status"
            label="课程状态"
            column-key="课程状态"
            :filters="[{text: '进行中', value: '进行中'},{text: '已结束', value: '已结束'}]"
            :filter-method="filterHandler"
            width="100">
          </el-table-column>
        </el-table>
      </el-col>
    </el-main>
  </div>
</template>

<script>
    export default {
        name: "AllCourse",
      data(){
        return {
          user:'',
          loading: false,
          search2: '',
          AllCourseData: [],

        }
      },

      methods: {
        clearFilter() {
          this.$refs.filterTable.clearFilter();
        },
        filterHandler(value, row, column) {
          const property = column['property'];
          return row[property] === value;
        },
        judgeStatus(a){
          if(a==="1")
            return "进行中";
          else if(a==="0")
            return  "已结束";
        },
        judgeStime(a){
          if(a==="")
            return "未定";
          else
            return a;
        }
      },


      mounted() {
        this.user=this.$cookies.get('username');
        this.AllCourseData = [];
        this.loading = true;
        setTimeout(() => {
          this.$axios.get('/api/GetCourse')
            .then((response) =>{
              let tt = unescape(response.data.courses).split(',');
              for(let i=0; i<tt.length/9; i++){
                let t = i*9;
                let ttt={
                  id:tt[t],
                  coursename:tt[t+1],
                  number:tt[t+2],
                  maxnum:tt[t+3],
                  stime:this.judgeStime(tt[t+5]),
                  time:tt[t+6],
                  status:this.judgeStatus(tt[t+7]),
                  teachername:tt[t+8],
                };
                this.AllCourseData.push(ttt);
              }
            });
          this.loading = false;
        }, 1000);
      },
      computed: {
        AllCourseData1:function () {
          let search=this.search2;
          if(search){
            return  this.AllCourseData.filter(function(dataNews){
              return Object.keys(dataNews).some(function(key){
                return String(dataNews[key]).toLowerCase().indexOf(search) > -1
              })
            })
          }
          return this.AllCourseData
        },
      }
    }
</script>

<style scoped>

</style>
