<template>
  <div>
    <el-main
      v-loading="loading"
      element-loading-text="加载中">
      <!--课程-作业界面-->
      <el-col
        :offset="0"
        :span="24">
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
          :data="courseData1"
          empty-text="暂无数据"
          row-key="courseid"
          :expand-row-keys="expands"
          @expand-change="rowExpand">
          <el-table-column type="expand">
            <template slot-scope="props">
              <el-table
                :data="WorkData"
                empty-text="暂无数据">
                <el-table-column
                  prop="wid"
                  label="作业编号"
                  width="80">
                </el-table-column>
                <el-table-column
                  prop="chapter"
                  label="所属章节"
                  width="100">
                </el-table-column>
                <el-table-column
                  prop="ctime"
                  label="作业次数"
                  width="100">
                </el-table-column>
                <el-table-column
                  prop="deadline"
                  label="截止日期"
                  width="160">
                </el-table-column>
                <el-table-column
                  prop="finishnum"
                  label="完成人数"
                  width="100">
                </el-table-column>
                <el-table-column
                  prop="release"
                  label="是否发布"
                  width="100">
                </el-table-column>
                <el-table-column
                  label="操作"
                  width="350">
                  <template slot-scope="scope">
                    <el-button size="small" @click="unfinished(scope.row.wid,scope.row.ctime)" v-if="scope.row.release==='是'">未完成名单
                      <i class="el-icon-tickets"></i></el-button>
                    <el-button size="small" @click="score(scope.row.wid,scope.row.ctime)" type="primary" v-if="scope.row.release==='是'">学生作业
                      <i class="el-icon-edit"></i></el-button>
                    <el-button size="small" @click="checkinfo(scope.row.wid)" type="success" v-if="scope.row.release==='是'">完成情况
                      <i class="el-icon-search"></i></el-button>
                    <el-button size="small" @click="rowClick(scope.row.wid,scope.row.ctime)"  type="primary" v-if="scope.row.release==='否'">编辑作业
                      <i class="el-icon-edit"></i></el-button>
                    <el-button size="small" @click="deletework(scope.row)"  type="danger" v-if="scope.row.release==='否'">删除作业
                      <i class="el-icon-delete"></i></el-button>
                  </template>
                </el-table-column>
              </el-table>
            </template>
          </el-table-column>
          <el-table-column
            prop="courseid"
            label="课程编号"
            width="160">
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
            prop="status"
            label="课程状态"
            column-key="课程状态"
            :filters="[{text: '进行中', value: '进行中'},{text: '已结束', value: '已结束'}]"
            :filter-method="filterHandler"
            width="100">
          </el-table-column>
          <el-table-column
            label="操作"
            width="240">
            <template slot-scope="scope">
              <el-button @click="arrange(scope.row.courseid)" type="text" >创建新作业
                <i class="el-icon-edit"></i></el-button>
              <el-button @click="ShareArea(scope.row.courseid)" type="text" >共享区管理
                <i class="el-icon-share"></i></el-button>
            </template>
          </el-table-column>
        </el-table>
      </el-col>
    </el-main>
    <!--设置管理员弹窗-->
    <el-dialog
      title="设置共享区管理员"
      :visible.sync="setAreadialog"
      width="20%">
      <template>
        <el-select
          @change="studentchange()"
          v-model="student"
          placeholder="请选择学生">
          <el-option
            v-for="item in students"
            :key="item.sid"
            :label="item.student"
            :value="item.sid">
            <span style="float: left">{{ item.student }}</span>
            <span style="float: right; color: #8492a6; font-size: 13px">{{ item.sid }}</span>
          </el-option>
        </el-select>
      </template>
    </el-dialog>
    <!--未完成名单弹窗-->
    <el-dialog
      :title="'第'+wtime+'次作业未完成名单'"
      :visible.sync="unfinishdialog"
      width="20%">
      <el-button
        type="primary"
        size="small"
        @click="sendmessage()">提醒</el-button>
      <el-table :data="unfinishData">
        <el-table-column
          property="number"
          label="学生编号"
          width="100">
        </el-table-column>
        <el-table-column
          property="name"
          label="姓名"
          width="140">
        </el-table-column>
      </el-table>
    </el-dialog>
    <!-- 学生作业弹窗-->
    <el-dialog
      :title="cname+'第'+wtime+'次作业完成情况'"
      :visible.sync="scoredialog"
      width="50%">
      <el-table :data="scoreData">
        <el-table-column
          property="number"
          label="学号"
          width="60">
        </el-table-column>
        <el-table-column
          property="name"
          label="姓名"
          width="100">
        </el-table-column>
        <el-table-column
          property="time"
          label="提交时间"
          width="160">
        </el-table-column>
        <el-table-column
          property="iss"
          label="是否批改"
          width="80">
        </el-table-column>
        <el-table-column
          property="file"
          label="附件"
          width="80">
        </el-table-column>
        <el-table-column label="操作">
          <template slot-scope="scope">
            <el-button size="small" @click="checkwork(scope.row.name)" type="text" >查看
              <i class="el-icon-search"></i></el-button>
            <el-button size="small" @click="scorework(scope.row.number)" type="text" v-if="scope.row.iss==='否'">评分
              <i class="el-icon-edit"></i></el-button>
            <el-button size="small" @click="uptoShare(scope.row.name)" type="text" v-if="scope.row.iss==='是'">上传共享区
            </el-button>
            <el-button size="small" @click="downloadthiswork(scope.row.name)" type="text" v-if="scope.row.file==='有'">下载
              <i class="el-icon-download"></i></el-button>
          </template>
        </el-table-column>
      </el-table>
    </el-dialog>
    <!--完成情况弹窗-->
    <el-dialog
      title="完成情况"
      :visible.sync="infodialog"
      width="60%">
      <div v-for="(a,i) in infoData" :key="i">
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
          <el-row><div style="float: left; font-size: 14px">
            答对人数：{{a.right}}</div></el-row>
          <el-row><div style="float: left; font-size: 14px">
            答错人数：{{a.wrong}}</div></el-row>
          <el-row><div style="float: left; font-size: 14px">
            本题答案：{{a.answer}}</div></el-row>
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
          <el-row><div style="float: left; font-size: 14px">
            答对人数：{{a.right}}</div></el-row>
          <el-row><div style="float: left; font-size: 14px">
            答错人数：{{a.wrong}}</div></el-row>
          <el-row><div style="float: left; font-size: 14px">
            本题答案：{{a.answer}}</div></el-row>
        </el-card>
      </div>
    </el-dialog>
    <!-- 布置作业弹窗-->
    <el-dialog
      :title="'布置'+cname+'第'+wtime+'次作业'"
      :visible.sync="arrangedialog"
      width="50%">
      <el-row>
        <el-col :span="16">
          <el-select
            v-model="value"
            @change="selectchange">
            <el-option
              v-for="item in options"
              :key="item.value"
              :label="item.label"
              :value="item.value">
            </el-option>
          </el-select>
          <el-date-picker
            v-model="date1"
            type="datetime"
            placeholder="设置截止日期"
            @change="setdeadline(workid)">
          </el-date-picker>
        </el-col>
        <el-col :span="8">
          <el-button
            type="primary"
            @click="preview(workid)">
            预览
          </el-button>
          <el-button
            type="primary"
            @click="sub(workid)">
            发布
          </el-button>
        </el-col>
      </el-row>
      <!--单选题表单-->
      <el-form
        v-if="questiondialog1"
        ref="radioform"
        :model="radioform"
        label-position="right"
        show-message>
        <el-form-item label="单选题干：" prop="radioquestion">
          <el-col :span="24">
            <el-input
              type="textarea"
              :rows="2"
              placeholder="请输入题干"
              v-model="radioform.question"
              clearable></el-input>
          </el-col>
        </el-form-item>
        <el-form-item label="选项A：" prop="A">
          <el-col :span="24">
            <el-input
              placeholder="请输入A选项内容"
              v-model="radioform.A"
              clearable></el-input>
          </el-col>
        </el-form-item>
        <el-form-item label="选项B：" prop="B">
          <el-col :span="24">
            <el-input
              placeholder="请输入B选项内容"
              v-model="radioform.B"
              clearable></el-input>
          </el-col>
        </el-form-item>
        <el-form-item label="选项C：" prop="C">
          <el-col :span="24">
            <el-input
              placeholder="请输入C选项内容"
              v-model="radioform.C"
              clearable></el-input>
          </el-col>
        </el-form-item>
        <el-form-item label="选项D：" prop="D">
          <el-col :span="24">
            <el-input
              placeholder="请输入D选项内容"
              v-model="radioform.D"
              clearable></el-input>
          </el-col>
        </el-form-item>
        <el-form-item label="上传图片：" prop="questionpicture">
          <el-col :span="8">
            <el-upload
              class="question-uploader"
              action="https://jsonplaceholder.typicode.com/posts/"
              :before-upload="beforeQuestionUpload1"
              list-type="picture"
              :file-list="QuestionList"
              :on-change="QuestionChange">
              <el-button size="small" type="primary">点击上传</el-button>
              <div class="el-upload__tip" slot="tip">只能上传jpg/png文件，且不超过10m</div>
            </el-upload>
          </el-col>
        </el-form-item>
        <el-form-item label="参考答案：" prop="radioanswer">
          <el-col :span="8">
            <el-radio-group v-model="radioform.radio1">
              <el-radio-button label="A"></el-radio-button>
              <el-radio-button label="B"></el-radio-button>
              <el-radio-button label="C"></el-radio-button>
              <el-radio-button label="D"></el-radio-button>
            </el-radio-group>
          </el-col>
        </el-form-item>
        <el-form-item label="解析：" prop="explain">
          <el-col :span="24">
            <el-input
              type="textarea"
              :rows="2"
              placeholder="请输入此题解析"
              v-model="radioform.explain"
              clearable></el-input>
          </el-col>
        </el-form-item>
        <el-form-item>
          <el-button type="primary" @click="upradio" round>提交该题</el-button>
          <el-button @click="clearForm" round>清空</el-button>
        </el-form-item>
      </el-form>

      <!--多选题表单-->
      <el-form
        v-if="questiondialog2"
        ref="Checkboxform"
        :model="Checkboxform"
        label-position="right"
        show-message>
        <el-form-item label="多选题干：" prop="Checkboxquestion">
          <el-col :span="24">
            <el-input
              type="textarea"
              :rows="2"
              placeholder="请输入题干"
              v-model="Checkboxform.question"
              clearable></el-input>
          </el-col>
        </el-form-item>
        <el-form-item label="选项A：" prop="A">
          <el-col :span="24">
            <el-input
              placeholder="请输入A选项内容"
              v-model="Checkboxform.A"
              clearable></el-input>
          </el-col>
        </el-form-item>
        <el-form-item label="选项B：" prop="B">
          <el-col :span="24">
            <el-input
              placeholder="请输入B选项内容"
              v-model="Checkboxform.B"
              clearable></el-input>
          </el-col>
        </el-form-item>
        <el-form-item label="选项C：" prop="C">
          <el-col :span="24">
            <el-input
              placeholder="请输入C选项内容"
              v-model="Checkboxform.C"
              clearable></el-input>
          </el-col>
        </el-form-item>
        <el-form-item label="选项D：" prop="D">
          <el-col :span="24">
            <el-input
              placeholder="请输入D选项内容"
              v-model="Checkboxform.D"
              clearable></el-input>
          </el-col>
        </el-form-item>
        <el-form-item label="上传图片：" prop="questionpicture">
          <el-col :span="8">
            <el-upload
              class="question-uploader"
              action="https://jsonplaceholder.typicode.com/posts/"
              :before-upload="beforeQuestionUpload2"
              list-type="picture"
              :file-list="QuestionList"
              :on-change="QuestionChange">
              <el-button size="small" type="primary">点击上传</el-button>
              <div class="el-upload__tip" slot="tip">只能上传jpg/png文件，且不超过10m</div>
            </el-upload>
          </el-col>
        </el-form-item>
        <el-form-item label="参考答案：" prop="Checkboxanswer">
          <el-col :span="8">
            <el-checkbox-group v-model="Checkboxform.Checkbox1">
              <el-checkbox-button label="A"></el-checkbox-button>
              <el-checkbox-button label="B"></el-checkbox-button>
              <el-checkbox-button label="C"></el-checkbox-button>
              <el-checkbox-button label="D"></el-checkbox-button>
            </el-checkbox-group>
          </el-col>
        </el-form-item>
        <el-form-item label="解析：" prop="explain">
          <el-col :span="24">
            <el-input
              type="textarea"
              :rows="2"
              placeholder="请输入此题解析"
              v-model="Checkboxform.explain"
              clearable></el-input>
          </el-col>
        </el-form-item>
        <el-form-item>
          <el-button type="primary" @click="upcheckbox" round>提交该题</el-button>
          <el-button @click="clearForm" round>清空</el-button>
        </el-form-item>
      </el-form>

      <!--判断题表单-->
      <el-form
        v-if="questiondialog3"
        ref="judgeform"
        :model="judgeform"
        label-position="right"
        show-message>
        <el-form-item label="判断题干：" prop="judgequestion">
          <el-col :span="24">
            <el-input
              type="textarea"
              :rows="2"
              placeholder="请输入题干"
              v-model="judgeform.question"
              clearable></el-input>
          </el-col>
        </el-form-item>
        <el-form-item label="上传图片：" prop="questionpicture">
          <el-col :span="8">
            <el-upload
              class="question-uploader"
              action="https://jsonplaceholder.typicode.com/posts/"
              :before-upload="beforeQuestionUpload3"
              list-type="picture"
              :file-list="QuestionList"
              :on-change="QuestionChange">
              <el-button size="small" type="primary">点击上传</el-button>
              <div class="el-upload__tip" slot="tip">只能上传jpg/png文件，且不超过10m</div>
            </el-upload>
          </el-col>
        </el-form-item>
        <el-form-item label="参考答案：" prop="judgeanswer">
          <el-col :span="6">
            <el-radio-group v-model="judgeform.radio1">
              <el-radio-button label="正确"></el-radio-button>
              <el-radio-button label="错误"></el-radio-button>
            </el-radio-group>
          </el-col>
        </el-form-item>
        <el-form-item label="解析：" prop="explain">
          <el-col :span="24">
            <el-input
              type="textarea"
              :rows="2"
              placeholder="请输入此题解析"
              v-model="judgeform.explain"
              clearable></el-input>
          </el-col>
        </el-form-item>
        <el-form-item>
          <el-button type="primary" @click="upjudge" round>提交该题</el-button>
          <el-button @click="clearForm" round>清空</el-button>
        </el-form-item>
      </el-form>

      <!--填空题表单-->
      <el-form
        v-if="questiondialog4"
        ref="packform"
        :model="packform"
        label-position="right"
        show-message>
        <el-form-item label="填空题干：" prop="packquestion">
          <el-col :span="24">
            <el-input
              type="textarea"
              :rows="4"
              placeholder="请输入题干"
              v-model="packform.question"
              clearable></el-input>
          </el-col>
        </el-form-item>
        <el-form-item label="上传图片：" prop="questionpicture">
          <el-col :span="8">
            <el-upload
              class="question-uploader"
              action="https://jsonplaceholder.typicode.com/posts/"
              :before-upload="beforeQuestionUpload4"
              list-type="picture"
              :file-list="QuestionList"
              :on-change="QuestionChange">
              <el-button size="small" type="primary">点击上传</el-button>
              <div class="el-upload__tip" slot="tip">只能上传jpg/png文件，且不超过10m</div>
            </el-upload>
          </el-col>
        </el-form-item>
        <el-form-item label="参考答案：" prop="packanswer">
          <el-col :span="24">
            <el-input
              placeholder="请输入参考答案"
              v-model="packform.answer"
              clearable></el-input>
          </el-col>
        </el-form-item>
        <el-form-item label="解析：" prop="explain">
          <el-col :span="24">
            <el-input
              type="textarea"
              :rows="2"
              placeholder="请输入此题解析"
              v-model="packform.explain"
              clearable></el-input>
          </el-col>
        </el-form-item>
        <el-form-item>
          <el-button type="primary" @click="uppack" round>提交该题</el-button>
          <el-button @click="clearForm" round>清空</el-button>
        </el-form-item>
      </el-form>

      <!--主观题表单-->
      <el-form
        v-if="questiondialog5"
        ref="subjectiveform"
        :model="subjectiveform"
        label-position="right"
        show-message>
        <el-form-item label="主观题干：" prop="subjectivequestion">
          <el-col :span="24">
            <el-input
              type="textarea"
              :rows="6"
              placeholder="请输入题干"
              v-model="subjectiveform.question"
              clearable></el-input>
          </el-col>
        </el-form-item>
        <el-form-item label="上传图片：" prop="questionpicture">
          <el-col :span="8">
            <el-upload
              class="question-uploader"
              action="https://jsonplaceholder.typicode.com/posts/"
              :before-upload="beforeQuestionUpload5"
              list-type="picture"
              :file-list="QuestionList"
              :on-change="QuestionChange">
              <el-button size="small" type="primary">点击上传</el-button>
              <div class="el-upload__tip" slot="tip">只能上传jpg/png文件，且不超过10m</div>
            </el-upload>
          </el-col>
        </el-form-item>
        <el-form-item label="参考答案：" prop="subjectiveanswer">
          <el-col :span="24">
            <el-input
              type="textarea"
              :rows="6"
              placeholder="请输入参考答案"
              v-model="subjectiveform.answer"
              clearable></el-input>
          </el-col>
        </el-form-item>
        <el-form-item label="解析：" prop="explain">
          <el-col :span="24">
            <el-input
              type="textarea"
              :rows="6"
              placeholder="请输入此题解析"
              v-model="subjectiveform.explain"
              clearable></el-input>
          </el-col>
        </el-form-item>
        <el-form-item>
          <el-button type="primary" @click="upsubjective" round>提交该题</el-button>
          <el-button @click="clearForm" round>清空</el-button>
        </el-form-item>
      </el-form>

    </el-dialog>
    <!--各题评分弹窗-->
    <el-dialog
      title="评分"
      :visible.sync="scorework1dialog"
      width="70%">
      <div>
        <!--    单选-->
        <div id="Simple" v-show="simpleShow">
          <el-form>
            <el-row><div style="text-align: left">
              <el-form-item>
                {{this.Count}}. {{Content}}（单项选择题）
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
                <el-radio disabled v-model="Answer" :label="1" border>A.{{Choice1}}</el-radio>
              </el-form-item>
            </div></el-row>
            <el-row><div style="text-align: left">
              <el-form-item>
                <el-radio disabled v-model="Answer" :label="2" border>B.{{Choice2}}</el-radio>
              </el-form-item>
            </div></el-row>
            <el-row><div style="text-align: left">
              <el-form-item>
                <el-radio disabled v-model="Answer" :label="3" border>C.{{Choice3}}</el-radio>
              </el-form-item>
            </div></el-row>
            <el-row><div style="text-align: left">
              <el-form-item>
                <el-radio disabled v-model="Answer" :label="4" border>D.{{Choice4}}</el-radio>
              </el-form-item>
            </div></el-row>
            <el-row><div style="text-align: center">
              <el-form-item>
                <label>标准答案：{{this.YAnswer}}    结果：{{this.Result}}</label>
              </el-form-item>
            </div></el-row>
            <el-row><div style="text-align: center">
              <el-form-item>
                <el-button type="primary" v-on:click="Before" v-if="this.Count > 1">上一题</el-button>
                <el-button type="primary" v-on:click="Next" v-if="this.nextCount <= this.Total1">下一题</el-button>
                <el-button type="success" v-on:click="subPaper" v-if="this.nextCount > this.Total1">提交</el-button>
              </el-form-item>
            </div></el-row>
          </el-form>
        </div>
        <!--    多选-->
        <div id="Multiple" v-show="multipleShow">
          <el-form>
            <el-row><div style="text-align: left">
              <el-form-item>
                {{this.Count}}. {{Content}}（多项选择题）
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
                  <el-checkbox disabled label="A" border>A.{{Choice1}}</el-checkbox>
                </el-form-item>
                <el-form-item>
                  <el-checkbox disabled label="B" border>B.{{Choice2}}</el-checkbox>
                </el-form-item>
                <el-form-item>
                  <el-checkbox disabled label="C" border>C.{{Choice3}}</el-checkbox>
                </el-form-item>
                <el-form-item>
                  <el-checkbox disabled label="D" border>D.{{Choice4}}</el-checkbox>
                </el-form-item>
              </el-checkbox-group>
            </div></el-row>
            <el-row><div style="text-align: center">
              <el-form-item>
                <label>标准答案：{{this.YAnswer}}    结果：{{this.Result}}</label>
              </el-form-item>
            </div></el-row>
            <el-row><div style="text-align: center">
              <el-form-item>
                <el-button type="primary" v-on:click="Before" v-if="this.Count > 1">上一题</el-button>
                <el-button type="primary" v-on:click="Next" v-if="this.nextCount <= this.Total1">下一题</el-button>
                <el-button type="success" v-on:click="subPaper" v-if="this.nextCount > this.Total1">提交</el-button>
              </el-form-item>
            </div></el-row>
          </el-form>
        </div>
        <!--    填空-->
        <div id="Blank" v-show="blankShow">
          <el-form>
            <el-row><div style="text-align: left">
              <el-form-item>
                {{this.Count}}. {{Content}}（填空题）
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
                <label>学生答案：{{this.Answer}}</label>
              </el-form-item>
            </div></el-row>
            <el-row><div style="text-align: center">
              <el-form-item>
                <label>标准答案：{{this.YAnswer}}    结果：{{this.Result}}</label>
              </el-form-item>
            </div></el-row>
            <el-row><div style="text-align: center">
              <el-form-item>
                <el-radio-group v-model="R">
                  <el-radio label="1">正确</el-radio>
                  <el-radio label="0">错误</el-radio>
                </el-radio-group>
              </el-form-item>
            </div></el-row>
            <el-row><div style="text-align: center">
              <el-form-item>
                <el-button type="primary" v-on:click="Before" v-if="this.Count > 1">上一题</el-button>
                <el-button type="primary" v-on:click="Next" v-if="this.nextCount <= this.Total1">下一题</el-button>
                <el-button type="success" v-on:click="subPaper" v-if="this.nextCount > this.Total1">提交</el-button>
              </el-form-item>
            </div></el-row>
          </el-form>
        </div>
        <!--    判断-->
        <div id="Judge" v-show="judgeShow">
          <el-form>
            <el-row><div style="text-align: left">
              <el-form-item>
                {{this.Count}}. {{Content}}（判断题）
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
                <el-radio-group v-model="Answer">
                  <el-radio disabled label="1">正确</el-radio>
                  <el-radio disabled label="0">错误</el-radio>
                </el-radio-group>
              </el-form-item>
            </div></el-row>
            <el-row><div style="text-align: center">
              <el-form-item>
                <label>标准答案：{{this.YAnswer}}    结果：{{this.Result}}</label>
              </el-form-item>
            </div></el-row>
            <el-row><div style="text-align: center">
              <el-form-item>
                <el-button type="primary" v-on:click="Before" v-if="this.Count > 1">上一题</el-button>
                <el-button type="primary" v-on:click="Next" v-if="this.nextCount <= this.Total1">下一题</el-button>
                <el-button type="success" v-on:click="subPaper" v-if="this.nextCount > this.Total1">提交</el-button>
              </el-form-item>
            </div></el-row>
          </el-form>
        </div>
        <!--    主观-->
        <div id="Subjective" v-show="subjectiveShow">
          <el-form>
            <el-row><div style="text-align: left">
              <el-form-item>
                {{this.Count}}. {{Content}}（主观题）
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
                <label>学生答案：{{this.Answer}}</label>
              </el-form-item>
            </div></el-row>
            <el-row><div style="text-align: center">
              <el-form-item>
                <el-button type="text" @click="uptoGood()">采纳为示范解法</el-button>
              </el-form-item>
            </div></el-row>
            <el-row><div style="text-align: center">
              <el-form-item>
                <label>标准答案：{{this.YAnswer}}    结果：{{this.Result}}</label>
              </el-form-item>
            </div></el-row>
            <el-row><div style="text-align: center">
              <el-form-item>
                <el-radio-group v-model="R">
                  <el-radio label="1">正确</el-radio>
                  <el-radio label="0">错误</el-radio>
                </el-radio-group>
              </el-form-item>
            </div></el-row>
            <el-row><div style="text-align: center">
              <el-form-item>
                <el-button type="primary" v-on:click="Before" v-if="this.Count > 1">上一题</el-button>
                <el-button type="primary" v-on:click="Next" v-if="this.nextCount <= this.Total1">下一题</el-button>
                <el-button type="success" v-on:click="subPaper" v-if="this.nextCount > this.Total1">提交</el-button>
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
            :current-page.sync="Count"
            :total="Total1"
            :page-size="1"
            :pager-count="20">
          </el-pagination>
        </div>
      </div>
    </el-dialog>
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
    <!--评分中的评语弹窗-->
    <el-dialog
      title="评语"
      :visible.sync="scoreworkdialog"
      width="30%">
      <el-input
        type="textarea"
        :rows="5"
        placeholder="请输入评语"
        v-model="textarea"
        clearable>
      </el-input>
      <el-row>
        <template>
          <el-input-number v-model="numb" @change="handleChange" :min="1" :max="10" label="描述文字"></el-input-number>
        </template>
        <el-button
          type="primary"
          @click="scorethis()">提交评价</el-button>
      </el-row>
    </el-dialog>
  </div>
</template>

<script>
    export default {
        name: "Course_Work",
      data() {
        return {
          user: '',
          loading: false,
          search1: '',
          expands:[],
          courseData: [],
          WorkData: [],
          scoreData: [],
          unfinishData: [],
          infoData: [],
          checkData:[],

          setAreadialog: false,
          unfinishdialog: false,
          scoredialog: false,
          infodialog: false,
          arrangedialog: false,
          temp:true,
          scorework1dialog: false,
          questiondialog1: true,
          questiondialog2: false,
          questiondialog3: false,
          questiondialog4: false,
          questiondialog5: false,
          checkdialog: false,
          scoreworkdialog: false,

          options: [{
            value: '选项1',
            label: '单项选择题'
          }, {
            value: '选项2',
            label: '多项选择题'
          }, {
            value: '选项3',
            label: '判断题'
          }, {
            value: '选项4',
            label: '填空题'
          }, {
            value: '选项5',
            label: '主观题'
          }],
          value: '选项1',
          date1: '',
          radioform: {
            question: '',
            A: '',
            B: '',
            C: '',
            D: '',
            radio1: 'A',
            explain:'',
          },
          Checkboxform: {
            question: '',
            A: '',
            B: '',
            C: '',
            D: '',
            Checkbox1: [''],
            explain:'',
          },
          judgeform: {
            question: '',
            radio1: '正确',
            explain:'',
          },
          packform: {
            question: '',
            answer: '',
            explain:'',
          },
          subjectiveform:{
            question: '',
            answer: '',
            explain:'',
          },
          QuestionList:[],
          questionimageUrl:'',

          cid:'',
          cname: '',
          workid: '',
          wid:'',
          wtime:'',
          tim: '',
          student:'',
          students:'',
          s:'',
          textarea: '',
          total: 0,
          numb: 10,

          qid: '',
          Answer: '',
          YAnswer: '',
          Result: '',
          answerList: [],
          simpleShow: false,
          multipleShow: false,
          blankShow: false,
          judgeShow: false,
          subjectiveShow: false,
          Choice1: '',
          Choice2: '',
          Choice3: '',
          Choice4: '',
          Content: '',
          Count: '1',
          nextCount: '',
          Total1: '',
          n:'',
          sid:'',
          R:'0',
          Ty:'',
          Picture:'',
        }
      },
      methods: {
        GetTCourse(){
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
                for (let i = 0; i < tt.length / 9; i++) {
                  let t = i * 9;
                  let ttt = {
                    courseid: tt[t],
                    coursename:tt[t+1],
                    number:tt[t+2],
                    maxnum:tt[t+3],
                    stime:this.judgeStime(tt[t+5]),
                    time:tt[t+6],
                    status:this.judgeStatus(tt[t+7]),
                    teachername:tt[t+8],
                  };
                  this.courseData.push(ttt);
                }
              }
            });
        },
        rowExpand(row, event, column) {
          this.cid=row.courseid;
          this.cname=row.coursename;
          this.WorkData = [];
          this.$axios.post('/api/GetTeacherWork', {
            courseid: row.courseid
          }).then((response) =>{
              var tt = unescape(response.data.worklist).split(',');
              for(var i=0; i<tt.length/6; i++){
                var t = i*6;
                var ttt={
                  wid:tt[t+5],
                  chapter:tt[t+1],
                  ctime:tt[t],
                  deadline:tt[t+2].substring(0,10)+" "+tt[t+2].substring(11,19),
                  finishnum:tt[t+4],
                  release:this.judgebool(tt[t+3])
                };
                this.WorkData.push(ttt);
              }
            });

          Array.prototype.remove = function (val) {
            let index = this.indexOf(val);
            if (index > -1) {
              this.splice(index, 1);
            }
          };

          if (this.expands.indexOf(row.courseid) < 0) {
            this.expands = [];
            this.expands.push(row.courseid);
          } else {
            this.expands.remove(row.courseid);
          }
        },
        arrange(courseid){
          this.WorkData = [];
          this.$axios.post('/api/GetTeacherWork?select=1', {courseid: courseid})
            .then((response) =>{
              var tt = unescape(response.data.worklist).split(',');
              for(var i=0; i<tt.length/6; i++){
                var t = i*6;
                var ttt={
                  wid:tt[t+5],
                  chapter:tt[t+1],
                  ctime:tt[t],
                  deadline:tt[t+2].substring(0,10)+" "+tt[t+2].substring(11,19),
                  finishnum:tt[t+4],
                  release:this.judgebool(tt[t+3])
                };
                this.WorkData.push(ttt);
              }
              this.$message.success("创建第"+tt.length/6+"次作业成功！");
            });
        },
        ShareArea(cid){
          this.$axios.post('/api/ShareArea?get=1',{
            cid:cid,
          }).then((res)=>{
            if(res.data.msg===0){
              this.$confirm('该课程暂未创建共享区，是否创建?', '提示', {
                confirmButtonText: '确定',
                cancelButtonText: '取消',
                type: 'warning'
              }).then(() => {
                this.$axios.post('/api/ShareArea?create=1',{
                  cid:cid,
                }).then((res)=>{
                  this.setArea(cid);
                  this.$message.success('创建成功!');
                });
              }).catch(() => {
                this.$message.info('取消创建');
              });
            }else{
              this.setArea(cid);
            }
          })
        },
        setArea(cid){
          this.student='';
          this.students=[];
          this.cid=cid;
          this.$axios.post('/api/ShareArea?getstudent=1',{
            cid:cid,
          }).then((res)=>{
            let tt = unescape(res.data.student).split(',');
            for(let i=0; i<tt.length/2; i++){
              let t = i*2;
              let ttt={
                sid:tt[t+1],
                student:tt[t]
              };
              this.students.push(ttt);
            }
            if(unescape(res.data.admin_id)==='None')
              this.student = '';
            else {
              this.student = unescape(res.data.admin_id);
              this.s = this.student;
            }
          });
          this.setAreadialog = true;
        },

        unfinished(wid,ctime){
          this.wid=wid;
          this.wtime=ctime;
          this.unfinishData = [];
          this.$axios.post('/api/Comment?select=1', {wid: wid})
            .then((res) =>{
              var tt = unescape(res.data.studentlist).split(',');
              for(var i=0; i<tt.length/2; i++){
                var t =i*2;
                var ttt={
                  number:tt[t],
                  name:tt[t+1]
                };
                this.unfinishData.push(ttt);
              }
            });
          this.unfinishdialog = true;
        },
        score(wid,ctime){
          this.wtime=ctime;
          this.scoreData = [];
          this.wid = wid;
          this.$axios.post('/api/Comment?finish=1', {wid: wid})
            .then((res) =>{
              let tt = unescape(res.data.studentlist).split(',');
              for(let i=0; i<tt.length/5; i++){
                let t =i*5;
                let ttt={
                  number:tt[t],
                  name:tt[t+1],
                  iss:this.judgebool(tt[t+3]),
                  time:tt[t+2].substring(0,10)+" "+tt[t+2].substring(11,19),
                  file:this.judgeFile(tt[t+4])
                };
                this.scoreData.push(ttt);
              }
            });
          this.scoredialog = true;
        },
        checkinfo(wid){
          this.infoData = [];
          this.$axios.post('/api/GetInfo', {
            wid:wid
          }).then((res)=>{
            let tt = unescape(res.data.qlist).split(',');
            for(let i=0; i<tt.length/10; i++) {
              let t = i * 10;
              let ttt = {
                content:tt[t+3],
                choice1:tt[t+4],
                choice2:tt[t+5],
                choice3:tt[t+6],
                choice4:tt[t+7],
                answer:this.judgeAnswer(tt[t+8]),
                picture:this.judgepicture(tt[t+9]),
                type:this.changeStype(tt[t]),
                right:tt[t+1],
                wrong:tt[t+2]
              };
              this.infoData.push(ttt);
              this.infodialog = true;
            }
          });
        },
        rowClick(wid,ctime){
          this.workid = wid;
          this.wtime = ctime;
          this.tim = ctime;
          this.arrangedialog = true;
        },
        deletework(row){
          this.$axios.post('/api/EditWork?select=1', {
            wid: row.wid
          });
          for(let i=0; i<this.WorkData.length; i++){
            if(this.WorkData[i].wid === row.wid)
              this.WorkData.splice(i,1);
          }
          this.$message.success("删除成功第"+row.ctime+"次作业成功！");
        },
        uptoGood(){
          this.$axios.post('/api/UpTo?goodcloud=1',{
            username:this.user,
            wid:this.wid,
            cid:this.cid,
            n:this.n,
            sid:this.sid
          }).then((res)=>{
            if(res.data.msg===1)
              this.$message.success("成功将该题作为示范题解添加至云笔记！");
            else{
              this.$message.error("云笔记系统已存在该题！");
            }
          });
        },

        studentchange(){
          this.$axios.post('/api/ShareArea?setstudent=1',{
            sid:this.student,
            cid:this.cid
          }).then((res)=>{
            if(res.data.msg===1)
              this.$message.success('设置管理员成功！');
            else{
              this.$confirm('该共享区已设置管理员，是否更改?', '提示', {
                confirmButtonText: '确定',
                cancelButtonText: '取消',
                type: 'warning'
              }).then(() => {
                this.$axios.post('/api/ShareArea?change=1',{
                  sid:this.student,
                  cid:this.cid
                }).then((res)=>{
                  this.$message.success('更改成功!');
                });
              }).catch(() => {
                this.student = this.s;
                this.$message.info('取消更改');
              });
            }
          })

        },
        sendmessage(){
          this.$axios.post('/api/Message?send=1', {
            user:this.user,
            wid:this.wid
          });
          this.$message.success('成功向未完成作业的学生发送通知！');
        },

        checkwork(username){
          this.temp = true;
          this.getwork(this.wid,username)
        },
        scorework(sid){
          this.$axios.post('/api/GetQuestionNumber',{wid:this.wid})
            .then((res) =>{
              this.Total1 = parseInt(res.data.qnum);
            });
          this.Count = 1;
          this.nextCount = this.Count+1;
          this.sid = sid;
          this.getQuestion();
          this.scorework1dialog = true;
        },
        uptoShare(username){
          this.$axios.post('/api/UpTo?share=1',{
            username:username,
            wid:this.wid
          }).then((res)=>{
            if(res.data.msg===1)
              this.$message.success("成功上传至共享区！");
            else
              this.$message.error("共享区已存在该份作业，请勿重复上传！");
          });
        },
        downloadthiswork(username){
          this.downloadwork(this.wid, username);
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

        selectchange(){
          if(this.value==='选项1'){
            this.questiondialog1 = true;
            this.questiondialog2 = false;
            this.questiondialog3 = false;
            this.questiondialog4 = false;
            this.questiondialog5 = false;
          }
          else if(this.value==='选项2'){
            this.questiondialog1 = false;
            this.questiondialog2 = true;
            this.questiondialog3 = false;
            this.questiondialog4 = false;
            this.questiondialog5 = false;
          }
          else if(this.value==='选项3'){
            this.questiondialog1 = false;
            this.questiondialog2 = false;
            this.questiondialog3 = true;
            this.questiondialog4 = false;
            this.questiondialog5 = false;
          }
          else if(this.value==='选项4'){
            this.questiondialog1 = false;
            this.questiondialog2 = false;
            this.questiondialog3 = false;
            this.questiondialog4 = true;
            this.questiondialog5 = false;
          }
          else if(this.value==='选项5'){
            this.questiondialog1 = false;
            this.questiondialog2 = false;
            this.questiondialog3 = false;
            this.questiondialog4 = false;
            this.questiondialog5 = true;
          }
        },
        setdeadline(wid){
          this.$axios.post('/api/EditWork?change=1', {
            wid: wid,
            deadline: this.date1
          });
          this.$message.success('第'+this.tim+'次作业截止日期设置成功!')
        },
        sub(wid){
          this.$axios.post('/api/EditWork?c=1', {
            wid: wid
          });
          this.arrangedialog = false;
          this.$message.success('发布第'+this.tim+'次作业成功!');
          this.GetTCourse();
        },
        preview(wid){
          this.temp = false;
          this.getwork(wid,this.user);
        },

        beforeQuestionUpload1(file) {
          const isJPG = file.type === 'image/jpeg'||'image/png';
          const isLt10M = file.size / 1024 / 1024 < 10;
          if (!isJPG) {
            this.$message.error('上传头像图片只能是 JPG或PNG 格式!');
          }
          if (!isLt10M) {
            this.$message.error('上传题目图片大小不能超过 10MB!');
          }
          if(isJPG&&isLt10M) {
            let fd = new FormData();
            fd.append('file',file);//传文件
            this.$axios.post('/api/CreateQuestion?picture1=1',fd)
              .then((res) =>{
                this.questionimageUrl=unescape(res.data.url);
                this.$message.success('上传成功！');
              });
          }
          return isJPG && isLt10M;
        },
        beforeQuestionUpload2(file) {
          const isJPG = file.type === 'image/jpeg'||'image/png';
          const isLt10M = file.size / 1024 / 1024 < 10;
          if (!isJPG) {
            this.$message.error('上传头像图片只能是 JPG或PNG 格式!');
          }
          if (!isLt10M) {
            this.$message.error('上传题目图片大小不能超过 10MB!');
          }
          if(isJPG&&isLt10M) {
            let fd = new FormData();
            fd.append('file',file);//传文件
            this.$axios.post('/api/CreateQuestion?picture2=1',fd)
              .then((res) =>{
                this.questionimageUrl=unescape(res.data.url);
                this.$message.success('上传成功！');
              });
          }
          return isJPG && isLt10M;
        },
        beforeQuestionUpload3(file) {
          const isJPG = file.type === 'image/jpeg'||'image/png';
          const isLt10M = file.size / 1024 / 1024 < 10;
          if (!isJPG) {
            this.$message.error('上传头像图片只能是 JPG或PNG 格式!');
          }
          if (!isLt10M) {
            this.$message.error('上传题目图片大小不能超过 10MB!');
          }
          if(isJPG&&isLt10M) {
            let fd = new FormData();
            fd.append('file',file);//传文件
            this.$axios.post('/api/CreateQuestion?picture3=1',fd)
              .then((res) =>{
                this.questionimageUrl=unescape(res.data.url);
                this.$message.success('上传成功！');
              });
          }
          return isJPG && isLt10M;
        },
        beforeQuestionUpload4(file) {
          const isJPG = file.type === 'image/jpeg'||'image/png';
          const isLt10M = file.size / 1024 / 1024 < 10;
          if (!isJPG) {
            this.$message.error('上传头像图片只能是 JPG或PNG 格式!');
          }
          if (!isLt10M) {
            this.$message.error('上传题目图片大小不能超过 10MB!');
          }
          if(isJPG&&isLt10M) {
            let fd = new FormData();
            fd.append('file',file);//传文件
            this.$axios.post('/api/CreateQuestion?picture4=1',fd)
              .then((res) =>{
                this.questionimageUrl=unescape(res.data.url);
                this.$message.success('上传成功！');
              });
          }
          return isJPG && isLt10M;
        },
        beforeQuestionUpload5(file) {
          const isJPG = file.type === 'image/jpeg'||'image/png';
          const isLt10M = file.size / 1024 / 1024 < 10;
          if (!isJPG) {
            this.$message.error('上传头像图片只能是 JPG或PNG 格式!');
          }
          if (!isLt10M) {
            this.$message.error('上传题目图片大小不能超过 10MB!');
          }
          if(isJPG&&isLt10M) {
            let fd = new FormData();
            fd.append('file',file);//传文件
            this.$axios.post('/api/CreateQuestion?picture5=1',fd)
              .then((res) =>{
                this.questionimageUrl=unescape(res.data.url);
                this.$message.success('上传成功！');
              });
          }
          return isJPG && isLt10M;
        },
        QuestionChange(file, QuestionList){
          this.QuestionList = QuestionList.slice(-1);
        },
        upradio(){
          this.$axios.post('/api/CreateQuestion?question1=1', {
            wid: this.workid,
            content: this.radioform.question,
            chioce1: this.radioform.A,
            chioce2: this.radioform.B,
            chioce3: this.radioform.C,
            chioce4: this.radioform.D,
            answer: this.radioform.radio1,
            explain: this.radioform.explain,
            questionimageUrl:this.questionimageUrl
          }).then((res) =>{
            if(res.data.code===0) {
              this.$message.error(res.data.msg);
            }
            else{
              this.$message.success(res.data.msg);
              this.radioform.question = '';
              this.radioform.A = '';
              this.radioform.B = '';
              this.radioform.C = '';
              this.radioform.D = '';
              this.radioform.radio1 = 'A';
              this.questionimageUrl = '';
              this.QuestionList=[];
              this.radioform.explain = '';
            }
          });
        },
        upcheckbox(){
          this.$axios.post('/api/CreateQuestion?question2=1', {
            wid: this.workid,
            content: this.Checkboxform.question,
            chioce1: this.Checkboxform.A,
            chioce2: this.Checkboxform.B,
            chioce3: this.Checkboxform.C,
            chioce4: this.Checkboxform.D,
            answer: this.Checkboxform.Checkbox1,
            explain: this.Checkboxform.explain,
            questionimageUrl:this.questionimageUrl
          }).then((res) =>{
            if(res.data.code===0) {
              this.$message.error(res.data.msg);
            }
            else{
              this.$message.success(res.data.msg);
              this.Checkboxform.question = '';
              this.Checkboxform.A = '';
              this.Checkboxform.B = '';
              this.Checkboxform.C = '';
              this.Checkboxform.D = '';
              this.Checkboxform.Checkbox1 = [''];
              this.questionimageUrl = '';
              this.QuestionList=[];
              this.Checkboxform.explain = '';
            }
          });
        },
        uppack(){
          this.$axios.post('/api/CreateQuestion?question3=1', {
            wid: this.workid,
            content: this.packform.question,
            answer: this.packform.answer,
            explain: this.packform.explain,
            questionimageUrl:this.questionimageUrl
          }).then((res) =>{
            if(res.data.code===0) {
              this.$message.error(res.data.msg);
            }
            else{
              this.$message.success(res.data.msg);
              this.packform.question = '';
              this.packform.answer = '';
              this.questionimageUrl = '';
              this.QuestionList=[];
              this.packform.explain = '';
            }
          });
        },
        upjudge(){
          this.$axios.post('/api/CreateQuestion?question4=1', {
            wid: this.workid,
            content: this.judgeform.question,
            answer: this.judgeform.radio1,
            explain: this.judgeform.explain,
            questionimageUrl:this.questionimageUrl
          }).then((res) =>{
            if(res.data.code===0) {
              this.$message.error(res.data.msg);
            }
            else{
              this.$message.success(res.data.msg);
              this.judgeform.question = '';
              this.judgeform.radio1 = '正确';
              this.questionimageUrl = '';
              this.QuestionList=[];
              this.judgeform.explain = '';
            }
          });
        },
        upsubjective(){
          this.$axios.post('/api/CreateQuestion?question5=1', {
            wid: this.workid,
            content: this.subjectiveform.question,
            answer: this.subjectiveform.answer,
            explain: this.subjectiveform.explain,
            questionimageUrl:this.questionimageUrl
          }).then((res) =>{
            if(res.data.code===0) {
              this.$message.error(res.data.msg);
            }
            else{
              this.$message.success(res.data.msg);
              this.subjectiveform.question = '';
              this.subjectiveform.answer = '';
              this.questionimageUrl = '';
              this.QuestionList=[];
              this.subjectiveform.explain = '';
            }
          });
        },
        clearForm(){
          this.radioform.question = '';
          this.radioform.A = '';
          this.radioform.B = '';
          this.radioform.C = '';
          this.radioform.D = '';
          this.radioform.radio1 = 'A';
          this.radioform.explain = '';
          this.questionimageUrl = '';
          this.Checkboxform.question = '';
          this.Checkboxform.A = '';
          this.Checkboxform.B = '';
          this.Checkboxform.C = '';
          this.Checkboxform.D = '';
          this.Checkboxform.Checkbox1 = [''];
          this.Checkboxform.explain = '';
          this.judgeform.question = '';
          this.judgeform.radio1 = '正确';
          this.judgeform.explain = '';
          this.packform.question = '';
          this.packform.answer = '';
          this.packform.explain = '';
          this.subjectiveform.question = '';
          this.subjectiveform.answer = '';
          this.subjectiveform.explain = '';
          this.QuestionList=[];
          this.$message.success('已清空表单');
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

        getQuestion(){
          this.$axios.post('/api/GetStudentQuestion',{
            sid:this.sid,
            wid:this.wid,
            number:this.Count
          })
            .then((response) =>{
              let type = response.data.type;
              this.Content = unescape(response.data.content);
              this.Picture = this.judgepicture(unescape(response.data.picture));
              if (type === '1') {
                this.Ty = 1;
                this.simpleShow = true;
                this.multipleShow = false;
                this.blankShow = false;
                this.judgeShow = false;
                this.subjectiveShow = false;
                this.Choice1 = unescape(response.data.choice1);
                this.Choice2 = unescape(response.data.choice2);
                this.Choice3 = unescape(response.data.choice3);
                this.Choice4 = unescape(response.data.choice4);
                this.Answer = this.changeAnswer(unescape(response.data.sanswer));
                this.YAnswer = unescape(response.data.answer);
                this.Result = this.changeResult(unescape(response.data.result));
              } else if (type === '2') {
                this.Ty = 2;
                this.simpleShow = false;
                this.multipleShow = true;
                this.blankShow = false;
                this.judgeShow = false;
                this.subjectiveShow = false;
                this.Choice1 = unescape(response.data.choice1);
                this.Choice2 = unescape(response.data.choice2);
                this.Choice3 = unescape(response.data.choice3);
                this.Choice4 = unescape(response.data.choice4);
                this.answerList = unescape(response.data.sanswer).split('');
                this.YAnswer = unescape(response.data.answer);
                this.Result = this.changeResult(unescape(response.data.result));
              } else if (type === '3') {
                this.Ty = 3;
                this.simpleShow = false;
                this.multipleShow = false;
                this.blankShow = false;
                this.judgeShow = true;
                this.subjectiveShow = false;
                this.Answer = this.changeJAnswer(unescape(response.data.sanswer));
                this.YAnswer = this.changeJResult(unescape(response.data.answer));
                this.Result = this.changeResult(unescape(response.data.result));
              } else if (type === '4') {
                this.Ty = 4;
                this.simpleShow = false;
                this.multipleShow = false;
                this.blankShow = true;
                this.judgeShow = false;
                this.subjectiveShow = false;
                this.Answer = unescape(response.data.sanswer);
                this.YAnswer = unescape(response.data.answer);
                this.Result = this.changeResult(unescape(response.data.result));
              } else if (type === '5') {
                this.Ty = 5;
                this.simpleShow = false;
                this.multipleShow = false;
                this.blankShow = false;
                this.judgeShow = false;
                this.subjectiveShow = true;
                this.Answer = unescape(response.data.sanswer);
                this.YAnswer = unescape(response.data.answer);
                this.Result = this.changeResult(unescape(response.data.result));
              }
            });
          this.n = this.Count;
          this.nextCount = this.Count+1;
        },
        gotoPage(Count){
          this.updataResult();
          this.Count = Count;
          this.getQuestion();
        },
        Before(){
          this.updataResult();
          this.Count = this.Count-1;
          this.nextCount = this.Count+1;
          this.getQuestion();
        },
        Next(){
          this.updataResult();
          this.Count = this.Count+1;
          this.nextCount = this.Count+1;
          this.getQuestion();
        },
        subPaper () {
          this.updataResult();
          this.scoreworkdialog = true;
        },
        updataResult(){
          if(this.Ty===4||this.Ty===5) {
            this.$axios.post('/api/UpdateResult', {
              sid: this.sid,
              wid: this.wid,
              number: this.n,
              result: this.R
            })
          }
          this.R = '0';
        },

        handleChange(value) {
          console.log(value);
        },
        scorethis(){
          this.$axios.post('/api/UpdateResult?s=1', {
            wid:this.wid,
            sid:this.sid,
            comment:this.textarea,
            score:this.numb
          });
          this.textarea = '';
          this.numb = 10;

          this.scoreworkdialog = false;
          this.scorework1dialog = false;
          this.scoredialog = false;
          this.$message.success("提交评价成功！");
          this.score(this.wid);
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
        judgebool(a){
          if(a==="true"||a==="True")
            return "是";
          else
            return "否";
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
        changeResult(a){
          if(a==='True'||a==='true')
            return "正确";
          else
            return "错误";
        },
        changeAnswer(a){
          if(a==='A')
            return 1;
          else if(a==='B')
            return 2;
          else if(a==='C')
            return 3;
          else if(a==='D')
            return 4;
        },
        changeJAnswer(a){
          if(a==='True'||a==='true')
            return '1';
          else
            return '0';
        },
        changeJResult(a){
          if(a==='True'||a==='true')
            return "正确";
          else
            return "错误";
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
      },
      mounted() {
        this.user=this.$cookies.get('username');
        this.GetTCourse();
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
      }
    }
</script>

<style scoped>

</style>
