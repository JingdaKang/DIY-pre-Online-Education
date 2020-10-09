<template>
  <div>
    <el-main
      v-loading="loading"
      element-loading-text="加载中">
      <!-- 我的作业界面 -->
      <el-col
        :offset="0"
        :span="24">
        <el-input
          style="width:160px;"
          prefix-icon="el-icon-search"
          class="search"
          v-model="search3"
          placeholder="输入关键字搜索"/>
        <el-table
          ref="worktable"
          stripe
          :data="myData1"
          empty-text="暂无数据">
          <el-table-column
            prop="workId"
            label="作业编号"
            width="80">
          </el-table-column>
          <el-table-column
            prop="coursename"
            label="作业课程名"
            width="160">
          </el-table-column>
          <el-table-column
            prop="teacher"
            label="教师"
            width="90">
          </el-table-column>
          <el-table-column
            prop="times"
            label="作业次数"
            sortable
            width="100">
          </el-table-column>
          <el-table-column
            prop="updata"
            label="上传日期"
            width="160">
          </el-table-column>
          <el-table-column
            prop="score"
            label="评分"
            width="50">
          </el-table-column>
          <el-table-column
            prop="comment"
            label="是否批改"
            width="80">
          </el-table-column>
          <el-table-column
            prop="finish"
            label="是否完成"
            width="80">
          </el-table-column>
          <el-table-column
            prop="file"
            label="附件"
            width="80">
          </el-table-column>
          <el-table-column
            label="操作"
            width="340">
            <template slot-scope="scope">
              <el-button @click="checkwork(scope.row.workId,scope.row.finish)" type="text" >查看
                <i class="el-icon-search"></i></el-button>
              <el-button @click="checkcomment(scope.row.workId)" type="text" v-if="scope.row.comment==='是'">教师评语
                <i class="el-icon-edit"></i></el-button>
              <el-button @click="uptoShare(scope.row.workId)" type="text" v-if="scope.row.comment==='是'">上传共享区
                <i class="el-icon-upload2"></i></el-button>
              <el-button @click="downFile(scope.row.workId)" type="text" v-if="scope.row.file==='有'">下载
                <i class="el-icon-download"></i></el-button>
            </template>
          </el-table-column>
        </el-table>
      </el-col>
    </el-main>

    <!--教师评语弹窗-->
    <el-dialog
      title="评语"
      :visible.sync="commentdialog"
      width="30%">
      <el-form>
        <el-form-item label="教师评语：">
          <label style="float: left;">{{this.tcomment}}</label>
        </el-form-item>
        <el-form-item label="得分：">
          <el-rate
            v-model="score"
            disabled
            show-score
            :max="Max"
            text-color="#ff9900"
            score-template="{value}">
          </el-rate>
        </el-form-item>
      </el-form>
    </el-dialog>
    <!--查看题目弹窗-->
    <el-dialog
      title="完成情况"
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
          <el-row><div v-if="temp">
            <el-tooltip :content="a.answer" effect="light">
              <el-button>查看标准答案</el-button>
            </el-tooltip>
            <el-tooltip :content="a.explain" effect="light">
              <el-button>查看该题解析</el-button>
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
          <el-row><div v-if="temp">
            <el-tooltip :content="a.answer" effect="light">
              <el-button>查看标准答案</el-button>
            </el-tooltip>
            <el-tooltip :content="a.explain" effect="light">
              <el-button>查看该题解析</el-button>
            </el-tooltip>
          </div></el-row>
        </el-card>
      </div>
    </el-dialog>

  </div>
</template>

<script>
  export default{
    name: 'MyWork',
    data() {
      return{
        user:'',
        loading: false,
        search3: '',
        myData: [],
        tcomment: '',
        Max: 10,
        value1: 3,
        score: null,
        commentdialog: false,
        checkdialog:false,
        checkData:[],
        temp:true,
      }
    },

    methods: {
      checkwork(wid,finish){
        this.temp = finish === '是';
        this.getwork(wid,this.user);
      },
      checkcomment(wid){
        this.$axios.post('/api/GetC',{
          username:this.user,
          wid:wid
        })
          .then((res)=>{
            this.tcomment = this.judgeNoComment(unescape(res.data.comment));
            this.score = parseInt(unescape(res.data.score));

          });
        this.commentdialog = true;
      },
      uptoShare(wid){
        this.$axios.post('/api/UpTo?share=1',{
          username:this.user,
          wid:wid
        }).then((res)=>{
          if(res.data.msg===1)
            this.$message.success("成功上传至共享区！");
          else
            this.$message.error("共享区已存在该份作业，请勿重复上传！");
        });
      },
      downFile(wid){
        this.$axios.post('/api/GetGood?download=1',{
          wid:wid,
          username:this.user
        }).then((res)=>{
          if(res.data.file==="")
            this.$message.error("下载失败，该作业无附件！");
          else {
            window.location=res.data.file;
          }
        });
      },

      judgenull(a){
        if(a==="true"||a==="True")
          return '是';
        else
          return '否';
      },
      judgefile(a){
        if(a===''||a==='None')
          return '无';
        else
          return '有';
      },
      judgeNoComment(a){
        if(a==="")
          return "暂未评分";
        else
          return a;
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
              result:this.judgeresult(tt[t+2]),
              explain:this.judgeExplain(tt[t+10])
            };
            this.checkData.push(ttt);
          }
          this.checkdialog = true;
        });
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
      judgeExplain(a){
        if(a===''||a==='None')
          return '暂无解析';
        else
          return a;
      },
    },

    mounted() {
      this.user=this.$cookies.get('username');
      this.myData = [];
      this.loading = true;
      setTimeout(() => {
        this.$axios.post('/api/GetMyWork', {
          username: this.user
        }).then((res) =>{
          let tt = unescape(res.data.worklist).split(',');
          for(let i=0; i<tt.length/10; i++){
            let t = i*10;
            let ttt={
              coursename:tt[t],
              teacher:tt[t+1],
              chapter:tt[t+3],
              times:tt[t+2],
              updata:tt[t+4].substring(0,10)+" "+tt[t+4].substring(11,19),
              score:tt[t+5],
              comment:this.judgenull(tt[t+7]),
              finish:this.judgenull(tt[t+6]),
              workId:tt[t+8],
              file:this.judgefile(tt[t+9])
            };
            this.myData.push(ttt);
          }
        });
        this.loading = false;
      },1000);
    },

    computed: {
      myData1:function () {
        let search=this.search3;
        if(search){
          return  this.myData.filter(function(dataNews){
            return Object.keys(dataNews).some(function(key){
              return String(dataNews[key]).toLowerCase().indexOf(search) > -1
            })
          })
        }
        return this.myData
      },
    }
  }

</script>

<style>

</style>
