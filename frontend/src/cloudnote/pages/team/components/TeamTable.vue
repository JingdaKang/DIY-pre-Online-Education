<template>
  <div>
        <el-row  v-loading="loading"
        element-loading-text="拼命加载中"
        element-loading-spinner="el-icon-loading"

        style="padding-left: 1%;">
    <el-row  >
      <el-pagination style="float: right;"

      :hide-on-single-page="false"
      layout="prev, pager, next"
      :total="Total"
      :page-size="6"
      :current-page="currentPage"
      @current-change="handleCurrentChange"
      >
    </el-pagination>


  </el-row>
  <el-table
  :data="tableData"
  style="width: 100%"
  @row-dblclick="openTeam"
  :row-class-name = "tableRowClassName">
  <el-table-column
  label="团队信息"
  width="500">
  <template slot-scope="scope">
    <i class="el-icon-share"></i>
    <span style="margin-left: 10px">{{ scope.row.teamName }}</span>
    <div style="margin-left: 24px;margin-top: 5px;color: #909399;">共{{ scope.row.notebookNum }}个笔记本，{{ scope.row.noteNum }}篇笔记</div>
  </template>
</el-table-column>
<el-table-column
label="创建时间"
width="200">
<template slot-scope="scope">
  <el-popover trigger="hover" placement="top">
    <p>创建者: {{ scope.row.creator }}</p>
    <div slot="reference" class="name-wrapper">
      <el-tag style = "margin-left:0px" size="mini">{{ scope.row.createTime }}</el-tag>
    </div>
  </el-popover>
</template>
</el-table-column>
<el-table-column
label="更新时间"
width="200">
<template slot-scope="scope">
  <el-popover trigger="hover" placement="top">
    <p>更新者: {{ scope.row.modifier }}</p>
    <div slot="reference" class="name-wrapper">
      <el-tag style = "margin-left:0px" size="mini">{{ scope.row.modifyTime }}</el-tag>
    </div>
  </el-popover>
</template>
</el-table-column>
<el-table-column
label="成员"
width="120">
<template slot-scope="scope">
  <i class="el-icon-user-solid"></i>
  <span style="margin-left: 10px">{{ scope.row.memberNum }}个成员</span>
</template>
</el-table-column>

<el-table-column label="操作">
  <template slot-scope="scope">
    <el-link icon="el-icon-edit" @click="checkLock(scope.$index, scope.row)">编辑</el-link>
    <el-divider direction="vertical"></el-divider>
    <el-link class="el-icon-delete" @click="handleDelete(scope.$index, scope.row)">删除</el-link>
    <!--            编辑框-->
    <el-dialog
    title="修改"
    :visible.sync="dialogVisible"
    width="30%"
    :close-on-click-modal = "false"
    >
    <el-input v-model="current_title"></el-input>
    <span slot="footer" class="dialog-footer">
      <el-button @click="cancelLock(currentId)">取 消</el-button>
      <el-button type="primary" @click="updateTeam(scope.$index,scope.row)">确 定</el-button>
    </span>
  </el-dialog>
</template>
</el-table-column>
</el-table>


</el-row>
</div>
</template>

<script>
import request from "@/network/request";
export default {
  name:"TeamTable",
  props:["TeamInfo"],
  data() {
    return {
      tableData: [],
      dialogVisible:false,
      current_title:"",
      currentId:null,
      currentIndex:null,
      currentPage:1,
      Total:1,
      loading:false,
    }
  },
  created() {
    this.loading=true;
    request({
      url:"/team/listByUser/",
    }).then(resp=>{
      var teams=resp.data.results;
            // this.ArticleList=resp.data.Articles;
            for(let index in teams){
              var temp = {}
              temp.teamName = teams[index].team_name;
              temp.notebookNum = teams[index].notebooks.length;
              temp.noteNum = teams[index].notes.length;
              temp.createTime = teams[index].team_create;
              temp.modifyTime = teams[index].team_modify;
              temp.creator = teams[index].leader_id;
              temp.modifier = teams[index].modifier_id;
              temp.memberNum = teams[index].members.length;
              temp.members = teams[index].members;
              temp.teamId = teams[index].id;
              this.tableData.push(temp);
            }

            this.Total = Number(resp.data.count)
            this.loading=false;

          }).catch(err=>{console.log(err)});
  },
  methods: {
    handleDetail(index, row) {
      console.log(index, row);
      this.$emit("getdetail",row)
    },
    handleDelete(index, row) {
      console.log(index, row);
    },
    tableRowClassName({row,rowIndex}){
      row.index = rowIndex;
    },
    openTeam(row){
      this.$emit("getdetail",row.index,row);
    },
    checkLock(index,row){
      console.log(index,row);
      request({
        url:"/team/isLock/",
        method:'post',
        data:{
          team_id:row.teamId
        }
      }).then(resp=>{
        if(resp.data.code=="no"){
          this.$message({
            type:"error",
            message:resp.data.msg
          });
        }else{
          this.dialogVisible = true;
          this.currentId = row.teamId;
          this.currentIndex = index;
        }
      })
    },
    cancelLock(currentId){

      request({
        url:"/team/cancelLock/",
        method:'post',
        data:{
          team_id:currentId
        }
      }).then(resp=>{
        if(resp.data.code=="yes"){
          this.currentId = null;
          this.currentIndex = null;
          this.dialogVisible = false;
        }
      })
    },
    updateTeam(index,row){
      console.log(index,row);
      request({
        url:"/team/updateName/",
        method:'post',
        data:{
          team_name:this.current_title,
          team_id:this.currentId
        }
      }).then(resp=>{
        this.tableData[this.currentIndex].teamName = resp.data.team_name;
        this.tableData[this.currentIndex].modifyTime = resp.data.team_modify;
        this.tableData[this.currentIndex].modifier = resp.data.modifier_id;
        this.$message({
          type:"success",
          message:"修改成功！"
        });

        this.current_title ="";
        this.currentId = null;
        this.currentIndex = null;
        this.dialogVisible=false
      })
    },
    handleCurrentChange(val){
      this.currentPage = val;
      this.loading = true;
      request({
        url:"/team/listByUser/",
        params: {
          page:val
        }
      }).then(resp=>{
      var teams=resp.data.results;
            // this.ArticleList=resp.data.Articles;
            this.tableData = [];
            for(let index in teams){
              var temp = {}
              temp.teamName = teams[index].team_name;
              temp.notebookNum = teams[index].notebooks.length;
              temp.noteNum = teams[index].notes.length;
              temp.createTime = teams[index].team_create;
              temp.modifyTime = teams[index].team_modify;
              temp.creator = teams[index].leader_id;
              temp.modifier = teams[index].modifier_id;
              temp.memberNum = teams[index].members.length;
              temp.members = teams[index].members;
              temp.teamId = teams[index].id;
              this.tableData.push(temp);
            }

            this.Total = Number(resp.data.count);
            this.loading = false;
      })
      this.currentPage = val;

    },
  }
}
</script>