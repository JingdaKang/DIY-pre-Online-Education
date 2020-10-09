<template>
  <div>
    <el-row  v-loading="loading"
    element-loading-text="拼命加载中"
    element-loading-spinner="el-icon-loading"

    style="padding-left: 1%;">
    <el-row >
      <el-pagination style="float: right;"

      :hide-on-single-page="false"
      layout="prev, pager, next"
      :total="Total"
      :page-size="8"
      :current-page="currentPage"
      @current-change="handleCurrentChange"
      >
    </el-pagination>


  </el-row>
  <el-table
  :data="tableData"
  style="width: 100%"
  @row-dblclick="getArticle">
  <el-table-column
  label="笔记信息"
  width="500">
  <template slot-scope="scope">
    <i class="el-icon-document"></i>
    <span style="margin-left: 10px">{{ scope.row.tNoteName }}</span>
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
    <el-link icon="el-icon-edit" @click="edit(scope.$index, scope.row)">编辑</el-link>
    <el-divider direction="vertical"></el-divider>
    <el-link class="el-icon-delete" @click="handleDelete(scope.$index, scope.row)">删除</el-link>
  </template>
</el-table-column>
</el-table>
<!--文章展示-->
<el-drawer
:title="articleDetail.title"
:visible.sync="dialogVisible"
size="auto"
direction="ttb"
style="overflow: auto"
>
<div style="">
  <makedown-show
  background="rgba(64, 158, 255, 0.2)"
  :mk-value="articleDetail.mkValue" ></makedown-show>
</div>
</el-drawer>
</el-row>
</div>
</template>


<script>
import request from "@/network/request";
import MakedownShow from "@/cloudnote/makedownShow";

export default {
  name:"TeamNote",
  components: {MakedownShow},
  props:["TeamNoteInfo"],
  data() {
    return {
      tableData: [],
      currentNotebook:null,
      currentPage:1,
      Total:1,
      loading:false,
      articleView:null,
      articleDetail:{
        mkValue:'',
        title:'',
        id:0,
      },
      dialogVisible:false,
    }
  },
  methods: {
    handleCurrentChange(val){
      this.currentPage = val;
      this.loading = true;
      request({
        url:"/note/listByNotebook/",
        params: {
          page:val,
          notebook_id:this.currentNotebook,
        }
      }).then(resp=>{
        this.tableData=[];
        var tNotes=resp.data.results;

        for(let index in tNotes){
          var temp = {}
          temp.tNoteId = tNotes[index].id;
          temp.tNoteName = tNotes[index].note_title;
          temp.createTime = tNotes[index].note_create;
          temp.modifyTime = tNotes[index].note_modify;
          temp.creator = tNotes[index].writer_id;
          temp.modifier = tNotes[index].modifier_id;
          this.tableData.push(temp);
        }
        this.Total = Number(resp.data.count);
        this.loading = false;
      })
      this.currentPage = val;

    },
    getArticle(row) {
      var id = row.tNoteId;
      request({
        url:'/note/'+id
      }).then(resp=>{
        var data = resp.data;
        this.articleDetail.mkValue  = data.note_text;
        this.articleDetail.title = data.note_title;
        this.articleDetail.id = data.id;
        this.dialogVisible=true;
      })
    },
    handleDelete(index, row) {
      console.log(index, row);
    },
    edit(index,row){
      console.log(index,row);
      request({
        url:"/note/isLock/",
        method:'post',
        data:{
          note_id:row.tNoteId
        }
      }).then(resp=>{
        if(resp.data.code=="no"){
          this.$message({
            type:"error",
            message:resp.data.msg
          });
        }else{
          request({
            url:'/note/'+ row.tNoteId
          }).then(resp=>{
            this.articleView= resp.data;
            this.$router.push({
              name:"write",
              params:{
                article:this.articleView
              }
            });

          });

        }
      })


    }
  }
}
</script>
