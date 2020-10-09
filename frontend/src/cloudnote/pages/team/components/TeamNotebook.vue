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
  @row-dblclick="accessFolder"
  :row-class-name = "tableRowClassName">
  <el-table-column
  label="笔记本信息"
  width="500">
  <template slot-scope="scope">
    <i class="el-icon-folder"></i>
    <span style="margin-left: 10px">{{ scope.row.tNotebookName }}</span>
    <div style="margin-left: 24px;margin-top: 5px;color: #909399;">共{{ scope.row.tNoteNum }}篇笔记</div>
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
      <el-button type="primary" @click="updateTeamNotebook(scope.$index,scope.row)">确 定</el-button>
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
  name:"TeamNotebook",
  props:["TeamNotebookInfo"],
  data() {
    return {
      tableData: [],
      dialogVisible:false,
      current_title:"",
      currentId:null,
      currentPage:1,
      Total:1,
      loading:false,
      currentTeam:null,
      chooseRow:null,
      chooseIndex:null,
    }
  },
  methods: {
    handleCurrentChange(val){
      this.currentPage = val;
      this.loading = true;
      request({
        url:"/notebook/listTeamNotebook/",
        params: {
          page:val,
          team_id:this.currentTeam.teamId
        }
      }).then(resp=>{
        var tNotebooks=resp.data.results;
        this.tableData=[];
        for(let index in tNotebooks){
          var temp = {}
          temp.tNotebookId = tNotebooks[index].id;
          temp.tNotebookName = tNotebooks[index].notebook_name;
          temp.tNoteNum = tNotebooks[index].notebook_note.length;
          temp.createTime = tNotebooks[index].notebook_create;
          temp.modifyTime = tNotebooks[index].notebook_modify;
          temp.creator = tNotebooks[index].creator_id;
          temp.modifier = tNotebooks[index].modifier_id;
          this.tableData.push(temp);
        }
        this.Total = Number(resp.data.count);
        this.loading = false;
      })
      this.currentPage = val;

    },
    tableRowClassName({row,rowIndex}){
      row.index = rowIndex;
    },
    accessFolder(row) {
      this.$emit("accessFolder",row.index,row)
    },

    handleDelete(index, row) {
      console.log(index, row);
    },
    updateTeamNotebook(index,row){
      console.log('update',this.chooseIndex,this.chooseRow,index,row);
      request({
        url:"/notebook/updateTeamNotebookName/",
        method:'post',
        data:{
          notebook_name:this.current_title,
          notebook_id:this.chooseRow.tNotebookId
        }
      }).then(resp=>{
        this.tableData[this.chooseIndex].tNotebookName = resp.data.notebook_name;
        this.tableData[this.chooseIndex].modifyTime = resp.data.notebook_modify;
        this.tableData[this.chooseIndex].modifier = resp.data.modifier_id;
        this.$message({
          type:"success",
          message:"修改成功！"
        });

        this.current_title ="";
        this.dialogVisible=false
      })
    },
    checkLock(index,row){
      console.log('check',index,row);
      request({
        url:"/notebook/isLock/",
        method:'post',
        data:{
          notebook_id:row.tNotebookId
        }
      }).then(resp=>{
        if(resp.data.code=="no"){
          this.$message({
            type:"error",
            message:resp.data.msg
          });
        }else{
          this.chooseRow = row;
          this.chooseIndex = index;
          this.dialogVisible = true;
          this.currentId = row.tNotebookId;
        }
      })
    },
    cancelLock(currentId){
      request({
        url:"/notebook/cancelLock/",
        method:'post',
        data:{
          notebook_id:currentId
        }
      }).then(resp=>{
        if(resp.data.code=="yes"){
          this.currentId = null;
          this.chooseRow = null;
          this.chooseIndex = null;
          this.current_title = "";
          this.dialogVisible = false;

        }
      })
    },
  }
}
</script>