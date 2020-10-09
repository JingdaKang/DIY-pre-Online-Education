<template>
  <div>
    <el-main
      v-loading="loading"
      element-loading-text="加载中">
      <!-- 错题统计界面 -->
      <el-col
        :offset="3"
        :span="18">
        <div>
          <template>
            <el-col :span="10">
              <el-select
                @change="courseischange()"
                v-model="course"
                placeholder="请选择筛选课程">
                <el-option
                  v-for="item in courses"
                  :key="item.cid"
                  :label="item.course"
                  :value="item.cid">
                  <span style="float: left">{{ item.course }}</span>
                  <span style="float: right; color: #8492a6; font-size: 13px">{{ item.cid }}</span>
                </el-option>
              </el-select></el-col>
            <el-col :span="10">
              <el-select
                @change="widischange()"
                v-model="work"
                placeholder="筛选作业次数"
                v-if="course!==''">
                <el-option
                  v-for="item in works"
                  :key="item.wid"
                  :label="item.work"
                  :value="item.wid">
                </el-option>
              </el-select></el-col>
          </template>
        </div>
        <br><br><br><br>
        <!--错题卡片-->
        <div v-for="(a,i) in pageChangeData" :key="i" v-if="wrongData.length!==0">
          <!--单、多选-->
          <el-card class="boxes-card" shadow="hover" v-show="a.type==='单选题'||a.type==='多选题'">
            <div slot="header" class="clearfix">
              <span>{{i+1+(count-1)*10}}.《{{a.coursename}}》第{{a.times}}次作业第{{a.n}}题（{{a.type}}）</span>
              <el-button style="float: right; padding: 3px 0" type="text" @click="Recommend(a.wid,a.n)">类似题目推荐</el-button>
            </div>
            <el-row><div style="float: left">
              {{a.content}}</div></el-row>
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
            <el-row><div style="float: left; font-size: 14px">
              我的答案：{{a.Answer}}</div></el-row>
            <el-row><div>
              <el-tooltip :content="a.answer" effect="light">
                <el-button>查看标准答案</el-button>
              </el-tooltip>
              <el-tooltip :content="a.explain" effect="light">
                <el-button>查看该题解析</el-button>
              </el-tooltip>
              <el-button @click="uptocloud(a.wid,a.n)" type="text" >上传至云笔记系统
                <i class="el-icon-upload"></i></el-button>
            </div></el-row>
            <el-row><div style="float: right; font-size: 12px;">
              完成时间：{{a.upload}}
            </div></el-row>
          </el-card>

          <!--判断、填空、主观-->
          <el-card class="boxes-card" shadow="hover" v-show="a.type==='判断题'||a.type==='填空题'||a.type==='主观题'">
            <div slot="header" class="clearfix">
              <span>{{i+1+(count-1)*10}}.《{{a.coursename}}》第{{a.times}}次作业第{{a.n}}题（{{a.type}}）</span>
              <el-button style="float: right; padding: 3px 0" type="text" @click="Recommend(a.wid,a.n)">类似题目推荐</el-button>
            </div>
            <el-row><div style="float: left">
              {{a.content}}</div></el-row>
            <el-row>
              <div v-if="a.picture!=='无'">
                <el-image
                  :src="a.picture"
                  fit="contain"></el-image>
              </div>
            </el-row>
            <br><br>
            <el-row><div style="float: left; font-size: 14px">
              我的答案：{{a.Answer}}</div></el-row>
            <el-row><div>
              <el-tooltip :content="a.answer" effect="light">
                <el-button>查看标准答案</el-button>
              </el-tooltip>
              <el-tooltip :content="a.explain" effect="light">
                <el-button>查看该题解析</el-button>
              </el-tooltip>
              <el-button @click="uptocloud(a.wid,a.n)" type="text" >上传至云笔记系统
                <i class="el-icon-upload"></i></el-button>
            </div></el-row>
            <el-row><div style="float: right; font-size: 12px;">
              完成时间：{{a.upload}}
            </div></el-row>
          </el-card>
        </div>
        <br><br><br><br><br><br><br><br><br>
        <div v-if="wrongData.length===0">
          <span>未查询到相关题目</span>
        </div>
        <div style="text-align: center">
          <el-pagination
            :hide-on-single-page="total/10<1"
            background
            @current-change="wrongDataChange"
            layout="prev, pager, next, jumper"
            :current-page.sync="count"
            :total="total">
          </el-pagination>
        </div>
      </el-col>
    </el-main>

    <!--题目推荐弹窗-->
    <el-dialog
      title="推荐题目"
      :visible.sync="recommendialog"
      width="60%">
      <div v-for="(a,i) in recommendData" :key="i" v-if="recommendData.length!==0">
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
          <el-row><div>
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
          <el-row><div>
            <el-tooltip :content="a.answer" effect="light">
              <el-button>查看标准答案</el-button>
            </el-tooltip>
            <el-tooltip :content="a.explain" effect="light">
              <el-button>查看该题解析</el-button>
            </el-tooltip>
          </div></el-row>
        </el-card>
      </div>
      <div v-if="recommendData.length===0">
        <span>此题无推荐题目。</span>
      </div>
    </el-dialog>
  </div>
</template>

<script>
  export default {
    name: 'WrongQuestions',
    data(){
      return {
        user:'',
        loading: false,
        courses:[],
        course:'',
        wrongData:[],
        pageChangeData: [],
        recommendialog:false,
        recommendData:[],
        works:[],
        work:'',
        total: 0,
        count: 1
      }
    },

    methods: {
      GetWrongQuestion(){
        this.wrongData = [];
        this.$axios.post('/api/GetWrongQuestion',{
          username:this.user,
          cid:this.course,
          ctime:this.work
        }).then((res)=>{
          if(res.data.result===1) {
            this.wrongData = [];
            this.total=0;
          }
          else {
            let tt = unescape(res.data.result).split(',');
            this.total = tt.length/17;
            for (let i = 0; i < tt.length / 17; i++) {
              let t = i * 17;
              let ttt = {
                wid: tt[t],
                coursename: tt[t + 4],
                teacher: tt[t + 5],
                type: this.changeStype(tt[t + 1]),
                times: tt[t + 2],
                chapter: tt[t + 3],
                upload: tt[t + 6].substring(0, 10) + " " + tt[t + 6].substring(11, 19),
                n: tt[t + 7],
                content: tt[t + 8],
                choice1: tt[t + 9],
                choice2: tt[t + 10],
                choice3: tt[t + 11],
                choice4: tt[t + 12],
                answer: this.judgeAnswer(tt[t + 13]),
                Answer: this.judgeAnswer(tt[t + 14]),
                picture: this.judgepicture(tt[t + 15]),
                explain: this.judgeExplain(tt[t + 16])
              };
              this.wrongData.push(ttt);
            }
            this.wrongDataChange();
          }
        });
      },
      wrongDataChange(){
        this.pageChangeData=[];
        let start = (this.count-1)*10;
        for(let i=start;i<this.minn(start+10,this.wrongData.length);i++){
          this.pageChangeData.push(this.wrongData[i])
        }
      },
      getusercourse(){
        this.course='';
        this.courses=[];
        this.$axios.post('/api/GetMaterial?getcourse=1',{
          username:this.user
        }).then((res)=>{
          var tt = unescape(res.data.course).split(',');
          for(var i=0; i<tt.length/2; i++){
            var t = i*2;
            var ttt={
              cid:tt[t],
              course:tt[t+1]
            };
            this.courses.push(ttt);
          }
        });
      },
      minn(a,b){
        if(a>=b)
          return b;
        else
          return a;
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
      judgeExplain(a){
        if(a===''||a==='None')
          return '暂无解析';
        else
          return a;
      },

      courseischange(){
        this.count=1;
        this.GetWorkTime();
        this.GetWrongQuestion();
      },
      widischange(){
        this.GetWrongQuestion();
      },
      GetWorkTime(){
        this.work='';
        this.works=[];
        this.$axios.post('/api/GetMaterial?getwork=1',{
          cid:this.course
        }).then((res)=>{
          let tt = unescape(res.data.wid).split(',');
          for(let i=0; i<tt.length; i++){
            let ttt={
              wid:tt[i],
              work:tt[i]
            };
            this.works.push(ttt);
          }
        });
      },
      Recommend(wid,n){
        this.recommendData = [];
        this.$axios.post('/api/Recommend',{
          wid:wid,
          number:n,
        }).then((res)=>{
          if(res.data.qlist===1)
            this.recommendData = [];
          else {
            let tt = unescape(res.data.qlist).split(',');
            for (let i = 0; i < tt.length / 9; i++) {
              let t = i * 9;
              let ttt = {
                content: tt[t],
                choice1: tt[t + 1],
                choice2: tt[t + 2],
                choice3: tt[t + 3],
                choice4: tt[t + 4],
                answer: this.judgeAnswer(tt[t + 5]),
                picture: this.judgepicture(tt[t + 6]),
                type: this.changeStype(tt[t + 7]),
                explain: this.judgeExplain(tt[t + 8])
              };
              this.recommendData.push(ttt);
            }
          }
          this.recommendialog = true;
        });
      },
      uptocloud(wid,n){
        let myDate = new Date();
        this.$axios.post('/api/UpTo?cloud=1',{
          username:this.user,
          wid:wid,
          number:n,
          time:myDate
        }).then((res)=>{
          if(res.data.msg===1)
            this.$message.success('上传成功！上传时间为：'+myDate.toLocaleString());
          else
            this.$message.error('此题已经存在，请勿重复上传！');
        });

      },
    },

    mounted() {
      this.user=this.$cookies.get('username');
      this.count=1;
      this.loading = true;
      setTimeout(() => {
        this.getusercourse();
        this.GetWrongQuestion();
        this.loading = false;
      }, 1000);
    }
  }
</script>

<style>

</style>
