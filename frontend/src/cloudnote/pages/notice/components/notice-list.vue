<template>
    <div >
        <el-row  v-loading="loading"
        element-loading-text="拼命加载中"
        element-loading-spinner="el-icon-loading"

        style="padding-left: 2%;">


        <el-row  style = "height:28px"> </el-row>
    <!--            通知-->
    <el-table
    :data="tableData"
    style="width: 100%">
    <el-table-column
    label="通知内容"
    width="700">
    <template slot-scope="scope">
        <i class="el-icon-message"></i>
        <span style="margin-left: 10px;margin-right: 10px;color: #409EFF">{{ scope.row.actor }}</span>
        <span>{{scope.row.verb}}</span>
        <span style="margin-left: 10px;margin-right: 10px;color: #409EFF">{{ scope.row.targetName }}</span>
        <el-badge v-if = "scope.row.unread" is-dot class="item" />
    </template>
</el-table-column>
<el-table-column
label="通知时间"
width="250">
<template slot-scope="scope">
<el-tag style = "margin-left:0px" size="mini">{{ scope.row.time }}</el-tag>

</template>
</el-table-column>
<el-table-column label="操作">
    <template slot-scope="scope">
        <el-link icon="el-icon-thumb" @click="show(scope.$index,scope.row)" v-if = "!scope.row.isOperated">查看</el-link>
        <el-link icon="el-icon-check" @click="check(scope.$index,scope.row)" v-if = "scope.row.unread">标记已读</el-link>
    </template>
</el-table-column>

</el-table>
<!--            邀请加入团队通知框-->
<el-dialog
title="通知"
:visible.sync="dialogVisible"
width="30%"
:close-on-click-modal = "false"
>
<span>是否接受该邀请？</span>
<span slot="footer" class="dialog-footer">
  <el-button @click="refuse(curIndex,curRow)">拒 绝</el-button>
  <el-button type="primary" @click="accept(curIndex,curRow)">接 受</el-button>
</span>
</el-dialog>
</el-row>
</div>
</template>

<script>
import request from "@/network/request";

export default {
    name: "team-list",
    data: function () {
        return {
            loading:false,
            tableData: [],
            Nav:["首页"],
            currentPage:1,
            Total:1,
            currentTitle:"首页",
            dialogVisible:false,
            curIndex:null,
            curRow:null,


        }
    },

    created() {
        request({
          url:"/notice/getUnreadNotice/",
      }).then(resp=>{
        var notices=resp.data;
        for(let index in notices){
          var temp = {}
          temp.noticeId = notices[index].id;
          temp.actor = notices[index].actor.username;
          temp.actorId = notices[index].actor.id;
          temp.targetName = notices[index].target.team_name;
          temp.targetId = notices[index].target.id;
          temp.unread = notices[index].unread;
          temp.time = notices[index].timestamp;
          temp.verb = notices[index].verb;
          if(temp.verb == "邀请你加入"){
            temp.isOperated = false;
          }else{
            temp.isOperated = true;
          }
          this.tableData.push(temp);
      }

      this.Total = Number(resp.data.count);
request({
          url:"/notice/getReadNotice/",
      }).then(resp=>{
        var notices=resp.data;
        for(let index in notices){
          var temp = {}
          temp.noticeId = notices[index].id;
          temp.actor = notices[index].actor.username;
          temp.actorId = notices[index].actor.id;
          temp.targetName = notices[index].target.team_name;
          temp.targetId = notices[index].target.id;
          temp.unread = notices[index].unread;
          temp.time = notices[index].timestamp;
          temp.verb = notices[index].verb;
          if(temp.verb == "邀请你加入"){
            temp.isOperated = false;
          }else{
            temp.isOperated = true;
          }
          this.tableData.push(temp);
      }

      this.Total += Number(resp.data.count);
  }).catch(err=>{console.log(err)});
  }).catch(err=>{console.log(err)});

  },
  methods:{
    check(index,row){
        request({
            url:"/notice/readNotice/",
            data:{
                noticeId:row.noticeId,
            },
            method:'post',
        }).then(resp=>{
            console.log(resp);
            this.tableData[index].unread=false;
            console.log(this.$parent.$parent.$parent.$parent);
            if(resp.data.unreadCount==0){
              this.$parent.$parent.$parent.$parent.notices = false;
            }
        })
    },
    show(index,row){
        this.check(index,row);
        this.curIndex = index;
        this.curRow = row;
        this.dialogVisible = true;
        
        console.log(index,row);
    },
    refuse(index,row){
        console.log(index,row);
        request({
            url:"/team/refuseInvitation/",
            method:'post',
            data:{
                noticeId:row.noticeId,
                actorId:row.actorId,
                targetId:row.targetId,
            }
        }).then(resp=>{
            console.log(resp.data)
            this.$message({
                type: 'success',
                message:'邀请已拒绝！'
            });
            this.curIndex = null;
            this.curRow = null;
            this.tableData[index].isOperated = true;
            this.dialogVisible=false;
        }).catch(err=>{console.log(err)});
    },

    accept(index,row){
        console.log(index,row);
        request({
            url:"/team/acceptInvitation/",
            method:'post',
            data:{
                noticeId:row.noticeId,
                actorId:row.actorId,
                targetId:row.targetId,
            }
        }).then(resp=>{
            console.log(resp.data)
            this.$message({
                type: 'success',
                message:'邀请已接受！'
            });
            this.curIndex = null;
            this.curRow = null;
            this.tableData[index].isOperated = true;
            this.dialogVisible=false;
        }).catch(err=>{console.log(err)});
    },
    getDetail(){
        this.detail = true;
        console.log(this.detail)
    }
},
computed:{
},
components: {
},
}
</script>

<style scoped>

</style>