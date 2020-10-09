<template>
  <div>
    <el-main
      v-loading="loading"
      element-loading-text="加载中">
      <!-- 优秀作业界面 -->
      <el-col
        :offset="1"
        :span="22">
        <el-input
          style="width:160px;"
          prefix-icon="el-icon-search"
          class="search"
          v-model="search4"
          placeholder="输入关键字搜索"/>
        <el-table
          ref="goodTable"
          stripe
          :data="goodData1"
          empty-text="暂无数据">
          <el-table-column
            prop="worknumber"
            label="作业编号"
            width="150">
          </el-table-column>
          <el-table-column
            prop="coursename"
            label="作业课程名"
            width="200">
          </el-table-column>
          <el-table-column
            prop="teacher"
            label="教师"
            width="100">
          </el-table-column>
          <el-table-column
            prop="times"
            label="作业次数"
            sortable
            width="100">
          </el-table-column>
          <el-table-column
            prop="uploaduser"
            label="上传者"
            width="100">
          </el-table-column>
          <el-table-column
            prop="uploaddata"
            label="上传日期"
            sortable
            width="160">
          </el-table-column>
          <el-table-column
            prop="file"
            label="附件"
            width="80">
          </el-table-column>
          <el-table-column
            label="操作"
            width="200">
            <template slot-scope="scope">
              <el-button @click="checkgoodwork(scope.row.worknumber,scope.row.uploaduser)" type="text">查看
                <i class="el-icon-search"></i></el-button>
              <el-button @click="downloadwork(scope.row.worknumber,scope.row.uploaduser)" type="text">下载
                <i class="el-icon-download"></i></el-button>
              <el-button @click="deletegoodwork(scope.row.worknumber,scope.row.uploaduser)" type="text">删除
                <i class="el-icon-delete"></i></el-button>
            </template>
          </el-table-column>
        </el-table>
      </el-col>
    </el-main>
    <!--查看作业弹窗-->
    <el-dialog
      title="查看作业"
      :visible.sync="checkdialog"
      width="60%">
      <div v-for="(a,i) in checkData" :key="i">
        <!--单、多选-->
        <el-card class="box-card" shadow="hover" v-show="a.type==='单选题'||a.type==='多选题'">
          <el-row><div style="float: left">
            {{i+1}}.{{a.content}}（{{a.type}}）</div></el-row>
          <el-row>
            <div v-if="a.picture!=='无'">
              <el-image
                :src="a.picture"
                fit="contain"></el-image>
            </div>
          </el-row>
          <br>
          <el-row><div style="float: left">
            A.{{a.choice1}}</div></el-row>
          <el-row><div style="float: left">
            B.{{a.choice2}}<br></div></el-row>
          <el-row><div style="float: left">
            C.{{a.choice3}}<br></div></el-row>
          <el-row><div style="float: left">
            D.{{a.choice4}}<br></div></el-row>
          <br><br>
          <el-row><div style="float: left; font-size: 14px" v-if="temp">
            回答：{{a.Answer}}</div></el-row>
          <el-row><div style="float: left; font-size: 14px" v-if="temp">
            结果：{{a.result}}</div></el-row>
          <el-row><div style="float: left; font-size: 14px" v-if="temp===false">
            答案：{{a.answer}}</div></el-row>
          <el-row><div v-if="temp">
            <el-tooltip :content="a.answer" effect="light">
              <el-button>查看标准答案</el-button>
            </el-tooltip>
          </div></el-row>
        </el-card>

        <!--判断、填空、主观-->
        <el-card class="box-card" shadow="hover" v-show="a.type==='判断题'||a.type==='填空题'||a.type==='主观题'">
          <el-row><div style="float: left">
            {{i+1}}.{{a.content}}（{{a.type}}）</div></el-row>
          <el-row>
            <div v-if="a.picture!=='无'">
              <el-image
                :src="a.picture"
                fit="contain"></el-image>
            </div>
          </el-row>
          <br><br>
          <el-row><div style="float: left; font-size: 14px" v-if="temp">
            回答：{{a.Answer}}</div></el-row>
          <el-row><div style="float: left; font-size: 14px" v-if="temp">
            结果：{{a.result}}</div></el-row>
          <el-row><div style="float: left; font-size: 14px" v-if="temp===false">
            答案：{{a.answer}}</div></el-row>
          <el-row><div>
            <el-tooltip :content="a.answer" effect="light" v-if="temp">
              <el-button>查看标准答案</el-button>
            </el-tooltip>
          </div></el-row>
        </el-card>
      </div>
    </el-dialog>
  </div>
</template>

<script>
    export default {
        name: "TGoodWork",
      data() {
        return {
          user: '',
          loading: false,
          search4: '',
          goodData: [],
          checkdialog: false,
          checkData:[],
          temp: true,
        }
      },
      methods: {
        GetGoodWork(){
          this.goodData = [];
          this.loading = true;
          setTimeout(() => {
            this.$axios.post('/api/GetGood?T=1',{
              username:this.user
            }).then((res)=>{
              let tt = unescape(res.data.goodwork).split(',');
              for(let i=0; i<tt.length/8; i++){
                let t = i*8;
                let ttt={
                  worknumber:tt[t],
                  coursename:tt[t+1],
                  teacher:tt[t+2],
                  belongcp:tt[t+4],
                  times:tt[t+3],
                  uploaduser:tt[t+5],
                  uploaddata:tt[t+6].substring(0,10)+" "+tt[t+6].substring(11,19),
                  file:this.judgeFile(tt[t+7])
                };
                this.goodData.push(ttt);
              }
            });
            this.loading = false;
          }, 1000);
        },
        checkgoodwork(wid, username){
          this.temp = true;
          this.getwork(wid,username);
        },
        downloadwork(wid, username){
          this.$axios.post('/api/GetGood?download=1',{
            wid:wid,
            username:username
          }).then((res)=>{
            if(res.data.file==="")
              this.$message.error("下载失败，该作业无附件！");
            else {
              window.location=res.data.file;
            }
          });
        },
        deletegoodwork(wid, username){
          this.$confirm('此操作将使该作业从共享区移除, 是否继续?', '提示', {
            confirmButtonText: '确定',
            cancelButtonText: '取消',
            type: 'warning'
          }).then(() => {
            this.$axios.post('/api/GetGood?delete=1',{
              wid:wid,
              username:username
            }).then((res)=>{
              if(res.data.msg===1){
                this.$message.success("成功移除该作业！");
                this.GetGoodWork();
              }
            });
          }).catch(() => {
            this.$message.info('已取消删除');
          });

        },
        getwork(wid,username){
          this.checkData=[];
          this.$axios.post('/api/GetAnyWork',{
            username:username,
            wid:wid
          }).then((res)=>{
            let tt = unescape(res.data.qlist).split(',');
            for(let i=0; i<tt.length/11; i++){
              let t = i*11;
              let ttt={
                content:tt[t+3],
                choice1:tt[t+4],
                choice2:tt[t+5],
                choice3:tt[t+6],
                choice4:tt[t+7],
                answer:this.judgeAnswer(tt[t+8]),
                Answer:this.judgeAnswer(tt[t+1]),
                picture:this.judgepicture(tt[t+9]),
                type:this.changeStype(tt[t]),
                result:this.judgeresult(tt[t+2])
              };
              this.checkData.push(ttt);
            }
            this.checkdialog = true;
          });
        },

        judgeFile(a){
          if(a===''||a==='None')
            return '无';
          else
            return '有';
        },
        judgeAnswer(a){
          if(a==='true'||a==='True')
            return '正确';
          else if(a==='false'||a==='False')
            return '错误';
          else if(a==='')
            return '无';
          else
            return a;
        },
        judgepicture(a){
          if(a==="")
            return '无';
          else return a;
        },
        changeStype(a){
          if(a==='1'||a===1)
            return "单选题";
          else if(a==='2'||a===2)
            return "多选题";
          else if(a==='3'||a===3)
            return "判断题";
          else if(a==='4'||a===4)
            return "填空题";
          else if(a==='5'||a===5)
            return "主观题";
        },
        judgeresult(a){
          if(a==='True'||a==='true')
            return '正确';
          else if(a==='False'||a==='false')
            return '错误';
          else if(a==='')
            return '未完成';
        },
      },
      mounted() {
        this.user=this.$cookies.get('username');
        this.GetGoodWork();
      },
      computed: {
        goodData1:function () {
          let search=this.search4;
          if(search){
            return  this.goodData.filter(function(dataNews){
              return Object.keys(dataNews).some(function(key){
                return String(dataNews[key]).toLowerCase().indexOf(search) > -1
              })
            })
          }
          return this.goodData
        },
      }
    }
</script>

<style scoped>

</style>
