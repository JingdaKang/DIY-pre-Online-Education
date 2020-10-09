<template>
  <div>
    <el-main
      v-loading="loading"
      element-loading-text="加载中">
      <!-- 我的课程界面 -->
      <el-col
        v-if="myCourse"
        :offset="1"
        :span="22">
        <el-button @click="clearFilter()">清除过滤器</el-button>
        <el-input
          style="width:160px;"
          prefix-icon="el-icon-search"
          class="search"
          v-model="search1"
          placeholder="输入关键字搜索"/>
        <el-table
          ref="filterTable"
          stripe
          :data="tableData1"
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
            prop="status"
            label="课程状态"
            column-key="课程状态"
            :filters="[{text: '进行中', value: '进行中'},{text: '已结束', value: '已结束'}]"
            :filter-method="filterHandler"
            width="100">
          </el-table-column>
          <el-table-column
            label="作业"
            width="200">
            <template slot-scope="scope">
              <el-button @click="submit(scope.row.id)" type="text">作业
                <i class="el-icon-edit-outline el-icon--right"></i></el-button>
              <el-button @click="uploadmt(scope.row.id)" type="text">上传资料
                <i class="el-icon-upload el-icon--right"></i></el-button>
            </template>
          </el-table-column>
        </el-table>
      </el-col>

      <!-- 在线作业界面 -->
      <el-col
        v-if="Online">
        <el-col
          :span="16"
          :offset="4">
          <div>
            <!--    单选-->
            <div id="simple" v-show="simpleShow">
              <el-form>
                <el-row><div style="text-align: left">
                  <el-form-item>
                    {{this.count}}. {{content}}（单项选择题）
                  </el-form-item>
                </div></el-row>
                <el-row>
                  <div v-if="this.Picture!=='无'">
                    <el-image
                      :src="this.Picture"
                      fit="contain"></el-image>
                  </div>
                </el-row>
                <el-row><div style="text-align: left">
                  <el-form-item>
                    <el-radio v-model="answer" :label="1" border>A.{{choice1}}</el-radio>
                  </el-form-item>
                </div></el-row>
                <el-row><div style="text-align: left">
                  <el-form-item>
                    <el-radio v-model="answer" :label="2" border>B.{{choice2}}</el-radio>
                  </el-form-item>
                </div></el-row>
                <el-row><div style="text-align: left">
                  <el-form-item>
                    <el-radio v-model="answer" :label="3" border>C.{{choice3}}</el-radio>
                  </el-form-item>
                </div></el-row>
                <el-row><div style="text-align: left">
                  <el-form-item>
                    <el-radio v-model="answer" :label="4" border>D.{{choice4}}</el-radio>
                  </el-form-item>
                </div></el-row>
                <el-row><div style="text-align: center">
                  <el-form-item>
                    <el-button type="primary" v-on:click="before" v-if="this.count > 1">上一题</el-button>
                    <el-button type="primary" v-on:click="next" v-if="this.nextcount <= this.total1">下一题</el-button>
                    <el-button type="success" v-on:click="subPaper" v-if="this.nextcount > this.total1">提交作业</el-button>
                  </el-form-item>
                </div></el-row>
              </el-form>
            </div>
            <!--    多选-->
            <div id="multiple" v-show="multipleShow">
              <el-form>
                <el-row><div style="text-align: left">
                  <el-form-item>
                    {{this.count}}. {{content}}（多项选择题）
                  </el-form-item>
                </div></el-row>
                <el-row>
                  <div v-if="this.Picture!=='无'">
                    <el-image
                      :src="this.Picture"
                      fit="contain"></el-image>
                  </div>
                </el-row>
                <el-row><div style="text-align: left">
                  <el-checkbox-group v-model="answerList" style="display: block">
                    <el-form-item>
                      <el-checkbox label="A" border>A.{{choice1}}</el-checkbox>
                    </el-form-item>
                    <el-form-item>
                      <el-checkbox label="B" border>B.{{choice2}}</el-checkbox>
                    </el-form-item>
                    <el-form-item>
                      <el-checkbox label="C" border>C.{{choice3}}</el-checkbox>
                    </el-form-item>
                    <el-form-item>
                      <el-checkbox label="D" border>D.{{choice4}}</el-checkbox>
                    </el-form-item>
                  </el-checkbox-group>
                </div></el-row>
                <el-row><div style="text-align: center">
                  <el-form-item>
                    <el-button type="primary" v-on:click="before" v-if="this.count > 1">上一题</el-button>
                    <el-button type="primary" v-on:click="next" v-if="this.nextcount <= this.total1">下一题</el-button>
                    <el-button type="success" v-on:click="subPaper" v-if="this.nextcount > this.total1">提交作业</el-button>
                  </el-form-item>
                </div></el-row>
              </el-form>
            </div>
            <!--    填空-->
            <div id="blank" v-show="blankShow">
              <el-form>
                <el-row><div style="text-align: left">
                  <el-form-item>
                    {{this.count}}. {{content}}（填空题）
                  </el-form-item>
                </div></el-row>
                <el-row>
                  <div v-if="this.Picture!=='无'">
                    <el-image
                      :src="this.Picture"
                      fit="contain"></el-image>
                  </div>
                </el-row>
                <el-row><div style="text-align: left">
                  <el-form-item>
                    <el-input type="text" v-model="answer" placeholder="请输入答案"></el-input>
                  </el-form-item>
                </div></el-row>
                <el-row><div style="text-align: center">
                  <el-form-item>
                    <el-button type="primary" v-on:click="before" v-if="this.count > 1">上一题</el-button>
                    <el-button type="primary" v-on:click="next" v-if="this.nextcount <= this.total1">下一题</el-button>
                    <el-button type="success" v-on:click="subPaper" v-if="this.nextcount > this.total1">提交作业</el-button>
                  </el-form-item>
                </div></el-row>
              </el-form>
            </div>
            <!--    判断-->
            <div id="judge" v-show="judgeShow">
              <el-form>
                <el-row><div style="text-align: left">
                  <el-form-item>
                    {{this.count}}. {{content}}（判断题）
                  </el-form-item>
                </div></el-row>
                <el-row>
                  <div v-if="this.Picture!=='无'">
                    <el-image
                      :src="this.Picture"
                      fit="contain"></el-image>
                  </div>
                </el-row>
                <el-row><div style="text-align: left">
                  <el-form-item>
                    <el-radio-group v-model="answer">
                      <el-radio label="1">正确</el-radio>
                      <el-radio label="0">错误</el-radio>
                    </el-radio-group>
                  </el-form-item>
                </div></el-row>
                <el-row><div style="text-align: center">
                  <el-form-item>
                    <el-button type="primary" v-on:click="before" v-if="this.count > 1">上一题</el-button>
                    <el-button type="primary" v-on:click="next" v-if="this.nextcount <= this.total1">下一题</el-button>
                    <el-button type="success" v-on:click="subPaper" v-if="this.nextcount > this.total1">提交作业</el-button>
                  </el-form-item>
                </div></el-row>
              </el-form>
            </div>
            <!--    主观-->
            <div id="subjective" v-show="subjectiveShow">
              <el-form>
                <el-row><div style="text-align: left">
                  <el-form-item>
                    {{this.count}}. {{content}}（主观题）
                  </el-form-item>
                </div></el-row>
                <el-row>
                  <div v-if="this.Picture!=='无'">
                    <el-image
                      :src="this.Picture"
                      fit="contain"></el-image>
                  </div>
                </el-row>
                <el-row><div style="text-align: left">
                  <el-form-item>
                    <el-input type="textarea" :rows="10" v-model="answer" placeholder="请输入答案"></el-input>
                  </el-form-item>
                </div></el-row>
                <el-row><div style="text-align: center">
                  <el-form-item>
                    <el-button type="primary" v-on:click="before" v-if="this.count > 1">上一题</el-button>
                    <el-button type="primary" v-on:click="next" v-if="this.nextcount <= this.total1">下一题</el-button>
                    <el-button type="success" v-on:click="subPaper" v-if="this.nextcount > this.total1">提交作业</el-button>
                  </el-form-item>
                </div></el-row>
              </el-form>
            </div>
            <!--    分页-->
            <div>
              <el-pagination
                layout="prev, pager, next"
                background
                @current-change="gotoPage"
                :current-page.sync="count"
                :total="total1"
                :page-size="1"
                :pager-count="20">
              </el-pagination>
            </div>
          </div>
        </el-col>
      </el-col>
    </el-main>
    <!-- 作业弹窗-->
    <el-dialog
      title="完成作业"
      :visible.sync="submitdialog"
      width="54%">
      <el-table :data="submitData">
        <el-table-column property="wid" label="作业编号" width="80"></el-table-column>
        <el-table-column property="times" label="作业次数" width="80"></el-table-column>
        <el-table-column property="finish" label="是否完成" width="80"></el-table-column>
        <el-table-column property="deadline" label="截止时间" width="160"></el-table-column>
        <el-table-column label="操作">
          <template slot-scope="scope">
            <el-button size="small" @click="online(scope.row.wid)" type="text"
                       v-if="scope.row.finish==='否' && parseInt(scope.row.deadline.substring(0,4)+scope.row.deadline.substring(5,7)+scope.row.deadline.substring(8,10)+scope.row.deadline.substring(11,13)+scope.row.deadline.substring(14,16)+scope.row.deadline.substring(17,19))>mytime">在线作业
              <i class="el-icon-edit-outline el-icon--right"></i></el-button>
            <el-button size="small" @click="submitwork(scope.row.wid)" type="text" v-if="scope.row.finish==='否'&& parseInt(scope.row.deadline.substring(0,4)+scope.row.deadline.substring(5,7)+scope.row.deadline.substring(8,10)+scope.row.deadline.substring(11,13)+scope.row.deadline.substring(14,16)+scope.row.deadline.substring(17,19))>mytime">提交文件
              <i class="el-icon-upload el-icon--right"></i></el-button>
            <el-button size="small" @click="checkmywork(scope.row.wid,scope.row.finish)" type="text" >查看
              <i class="el-icon-search"></i></el-button>
            <el-button size="small" @click="downFile(scope.row.wid)" type="text" v-if="scope.row.finish==='是'">下载
              <i class="el-icon-download"></i></el-button>
            <el-button size="small" @click="checkcomment(scope.row.wid)" type="text" v-if="scope.row.finish==='是'">评语
              <i class="el-icon-edit"></i></el-button>
            <el-button size="small" @click="uptoShare(scope.row.wid)" type="text" v-if="scope.row.finish==='是'">上传共享区
              <i class="el-icon-upload2"></i></el-button>
          </template>
        </el-table-column>
      </el-table>
    </el-dialog>
    <!-- 提交弹窗-->
    <el-dialog
      title="提交"
      :visible.sync="submit2dialog"
      width="25%">
      <el-upload
        class="upload-demo"
        ref="upload"
        action="https://jsonplaceholder.typicode.com/posts/"
        :before-upload="beforeFileUpload"
        :file-list="fileList"
        list-type="text"
        accept=".xls,.xlsx,.doc,.docx,.pdf,.txt,.rar,.zip,.jpg,.jpeg,.png"
        :on-change="FileChange">
        <el-button slot="trigger" size="small" type="primary">选取文件</el-button>
        <el-button style="margin-left: 10px;" size="small" type="success" @click="submitUpload">上传到服务器</el-button>
        <div slot="tip" class="el-upload__tip">1.支持图片文档等各种形式<br>2.源代码请以txt或word文档形式上传<br>3.若已经上传文件，本次将覆盖之前文件</div>
      </el-upload>
    </el-dialog>
    <!-- 上传资料1弹窗-->
    <el-dialog
      title="上传资料"
      :visible.sync="uploadialog1"
      width="20%">
      <el-upload
        class="upload-demo"
        action="https://jsonplaceholder.typicode.com/posts/"
        list-type="text"
        accept=".xls,.xlsx,.doc,.docx,.pdf,.txt,.rar,.zip,.jpg,.jpeg,.png"
        :show-file-list="true"
        :file-list="fileList"
        :on-change="FileChange"
        :on-success="uploadSuccess"
        :before-upload="beforeUpload">
        <el-button size="small" type="primary">点击上传</el-button>
      </el-upload>
    </el-dialog>


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

    <!--客观题结果弹窗-->
    <el-dialog
      title="客观题结果"
      :visible.sync="resultdialog"
      width="15%">
      <el-table :data="resultData">
        <el-table-column property="number" label="题号" width="80"></el-table-column>
        <el-table-column property="result" label="正误" width="80"></el-table-column>
      </el-table>
    </el-dialog>
  </div>
</template>

<script>
    export default {
        name: "MyCourse",
      data() {
        return {
          user: '',
          loading: false,
          search1: '',
          mytime: '',
          tableData: [],
          submitData: [],
          submitdialog: false,
          uploadialog1: false,
          submit2dialog: false,
          commentdialog: false,
          cid: '',
          temp:true,
          tcomment: '',
          Max: 10,
          value1: 3,
          score: null,
          checkdialog:false,
          checkData:[],
          fileUrl: '',
          filename:'',
          fileList: [],
          myCourse: true,
          Online: false,
          resultdialog: false,
          resultData:[],

          wid: '',
          qid: '',
          answer: '',
          answerList: [],
          simpleShow: false,
          multipleShow: false,
          blankShow: false,
          judgeShow: false,
          subjectiveShow: false,
          choice1: '',
          choice2: '',
          choice3: '',
          choice4: '',
          content: '',
          count: 1,
          nextcount: '',
          total1: '',
          n:'',
          Picture:'',
        }
      },
      methods: {
        GetMyCourse(){
          this.tableData = [];
          this.Online = false;
          this.loading = true;
          setTimeout(() => {
            this.$axios.post('/api/GetMyCourse', {
              user: this.user
            }).then((response) =>{
                if(response.data.mes===1){
                  this.tableData = [];
                }
                else {
                  let tt = unescape(response.data.mes).split(',');
                  for (let i = 0; i < tt.length / 9; i++) {
                    let t = i * 9;
                    let ttt = {
                      id:tt[t],
                      coursename:tt[t+1],
                      number:tt[t+2],
                      maxnum:tt[t+3],
                      stime:this.judgeStime(tt[t+5]),
                      time:tt[t+6],
                      status:this.judgeStatus(tt[t+7]),
                      teachername:tt[t+8],
                    };
                    this.tableData.push(ttt);
                  }
                }
              });
            this.loading = false;
            this.myCourse = true;
          }, 1000);
        },
        submit(courseid){
          this.submitData = [];
          this.cid = courseid;
          this.$axios.post('/api/GetWorkTime', {
            courseid: courseid,
            username: this.user})
            .then((res) =>{
              let tt = unescape(res.data.finishlist).split(',');
              for(let i=0; i<tt.length/4; i++){
                let t = i*4;
                let ttt = {
                  wid: tt[t],
                  times: '第'+tt[t+2]+'次',
                  deadline: tt[t+3].substring(0,10)+" "+tt[t+3].substring(11,19),
                  finish: this.judgebool(tt[t+1])
                };
                this.submitData.push(ttt);
              }
            });
          this.submitdialog = true;
        },
        uploadmt(cid){
          this.$axios.post('/api/ShareArea?get=1',{
            cid:cid,
          }).then((res) =>{
            if(res.data.msg===0)
              this.$message.error('该课程暂未创建共享区，请联系教师！');
            else{
              this.cid = cid;
              this.uploadialog1 = true;
            }
          });
        },

        online(wid){
          this.wid = wid;
          this.$axios.post('/api/GetQuestionNumber',{wid:wid})
            .then((res) =>{
              this.total1 = parseInt(res.data.qnum);
            });
          this.submitdialog = false;
          this.myCourse = false;
          this.Online = true;
          this.count = 1;
          this.nextcount = this.count+1;
          this.getQuestion();
        },
        submitwork(wid){
          this.wid = wid;
          this.submit2dialog = true;
        },
        checkmywork(wid,finish){
          this.temp = finish === '是';
          this.getwork(wid,this.user);
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

        beforeFileUpload(file){
          let fd = new FormData();
          fd.append('file',file);//传文件
          this.$axios.post('/api/UploadFile?File=1',fd)
            .then((res) =>{
              this.fileUrl = unescape(res.data.url);
            });
        },
        submitUpload(){
          let yes = false;
          this.$confirm('提交后是否完成该作业?若完成，将不能再进行在线作业和提交文件。', '提示', {
            confirmButtonText: '完成',
            cancelButtonText: '不完成',
            type: 'warning'
          }).then(() => {
            yes = true;
            this.continueupload(yes);
            this.$message.success('已完成该作业!');
            this.submit2dialog = false;
            setTimeout(() => {
              this.submit(this.cid);
            }, 300);
          }).catch(() => {
            yes = false;
            this.continueupload(yes);
            this.$message.info('暂不完成该作业。');
          });
        },
        continueupload(yes){
          let datetime = new Date();
          this.$axios.post('/api/UploadFile?up=1',{
            username:this.user,
            wid:this.wid,
            fileUrl:this.fileUrl,
            datetime:datetime,
            yes:yes
          })
            .then((res) =>{
              this.$message.success('上传成功！');
              this.submit2dialog = false;
              this.fileUrl = '';
            });
        },
        FileChange(file, fileList){
          this.fileList = fileList.slice(-1);
        },

        beforeUpload(file){
          let fd = new FormData();
          fd.append('file',file);//传文件
          this.$axios.post('/api/UploadMaterial?File=1',fd)
            .then((res) =>{
              this.fileUrl = unescape(res.data.url);
              this.filename = unescape(res.data.file);
            });
        },
        uploadSuccess(){
          let myDate = new Date();
          this.$axios.post('/api/UploadMaterial?up=1',{
            username:this.user,
            cid:this.cid,
            file:this.fileUrl,
            filename:this.filename,
            time:myDate
          }).then((res)=>{
            this.$message.success('上传成功！');
            this.fileList=[];
          });
        },

        clearFilter() {
          this.$refs.filterTable.clearFilter();
        },
        filterHandler(value, row, column) {
          const property = column['property'];
          return row[property] === value;
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
        judgebool(a){
          if(a==="True")
            return "是";
          else
            return "否";
        },
        judgepicture(a){
          if(a==="")
            return '无';
          else return a;
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
        },

        getQuestion(){
          this.$axios.post('/api/GetQuestion',{
            username:this.user,
            wid:this.wid,
            number:this.count
          })
            .then((response) =>{
              let type = response.data.type;
              this.content = unescape(response.data.content);
              this.Picture = this.judgepicture(unescape(response.data.picture));
              if (type === '1') {
                this.simpleShow = true;
                this.multipleShow = false;
                this.blankShow = false;
                this.judgeShow = false;
                this.subjectiveShow = false;
                this.choice1 = unescape(response.data.choice1);
                this.choice2 = unescape(response.data.choice2);
                this.choice3 = unescape(response.data.choice3);
                this.choice4 = unescape(response.data.choice4);
              } else if (type === '2') {
                this.simpleShow = false;
                this.multipleShow = true;
                this.blankShow = false;
                this.judgeShow = false;
                this.subjectiveShow = false;
                this.choice1 = unescape(response.data.choice1);
                this.choice2 = unescape(response.data.choice2);
                this.choice3 = unescape(response.data.choice3);
                this.choice4 = unescape(response.data.choice4);
              } else if (type === '3') {
                this.simpleShow = false;
                this.multipleShow = false;
                this.blankShow = false;
                this.judgeShow = true;
                this.subjectiveShow = false;
              } else if (type === '4') {
                this.simpleShow = false;
                this.multipleShow = false;
                this.blankShow = true;
                this.judgeShow = false;
                this.subjectiveShow = false;
              } else if (type === '5') {
                this.simpleShow = false;
                this.multipleShow = false;
                this.blankShow = false;
                this.judgeShow = false;
                this.subjectiveShow = true;
              }
            });
          this.n = this.count;
          this.nextcount = this.count+1;
        },
        gotoPage(count){
          this.updataAnswer();
          this.count = count;
          this.getQuestion();
        },
        before(){
          this.updataAnswer();
          this.count = this.count-1;
          this.nextcount = this.count+1;
          this.getQuestion();
        },
        next(){
          this.updataAnswer();
          this.count = this.count+1;
          this.nextcount = this.count+1;
          this.getQuestion();
        },
        subPaper () {
          let myDate = new Date();
          this.resultData = [];
          this.updataAnswer();
          this.$axios.post('/api/CheckAnswer',{
            username: this.user,
            wid: this.wid,
            time:myDate
          }).then((res) =>{
            let tt = unescape(res.data.result).split(',');
            for(let i=0; i<tt.length/2; i++){
              let t = i*2;
              let ttt = {
                number:tt[t],
                result:this.judgeAnswer(tt[t+1])
              };
              this.resultData.push(ttt);
            }
          });
          this.GetMyCourse();
          this.checkgoodwork(this.wid,this.user);
          setTimeout(() => {
            this.resultdialog = true;
          }, 1000);
        },
        updataAnswer(){
          this.$axios.post('/api/UpdateAnswer',{
            username: this.user,
            wid: this.wid,
            number: this.n,
            answer: this.answer,
            answerList: this.answerList
          });
          this.answer = '';
          this.answerList = [];
        },
        checkgoodwork(wid, username){
          this.getwork(wid,username);
        },
      },
      mounted() {
        this.user=this.$cookies.get('username');
        this.GetMyCourse();

        let myDate = new Date();
        let year = myDate.getFullYear();
        let month =(myDate.getMonth() + 1).toString();
        let day = (myDate.getDate()).toString();
        let hour = (myDate.getHours()).toString();
        let min = (myDate.getMinutes()).toString();
        let sec = (myDate.getSeconds()).toString();
        if (month.length === 1) {
          month = "0" + month;
        }
        if (day.length === 1) {
          day = "0" + day;
        }
        if (hour.length === 1) {
          hour = "0" + hour;
        }
        if (min.length === 1) {
          min = "0" + min;
        }
        if (sec.length === 1) {
          sec = "0" + sec;
        }
        let dateTime = year+month+day+hour+min+sec;
        this.mytime = parseInt(dateTime);
      },
      computed: {
        tableData1:function () {
          let search=this.search1;
          if(search){
            return  this.tableData.filter(function(dataNews){
              return Object.keys(dataNews).some(function(key){
                return String(dataNews[key]).toLowerCase().indexOf(search) > -1
              })
            })
          }
          return this.tableData
        },
      }
    }
</script>

<style scoped>

</style>
