<template>
    <div  style="padding-top: 1%;"
    v-loading.fullscreen.lock="loading"
    element-loading-text="拼命加载中"
    element-loading-spinner="el-icon-loading"

    >
    <el-row>
        <el-col :span="20">
            <span style="font-weight: bold;font-size:20px">通知中心</span>



        </el-col>

        <el-col :span="4">
            <el-button style = "float:right" type="primary"  round size="mini" @click="readAll"><i class="el-icon-check" style="margin-right: 4px"></i>一键已读</el-button>

        </el-col>
    </el-row>
</div>
</template>

<script>

import request from "@/network/request";
export default {
    name: "navigate",
    data:function(){
      return{
          Nav:['首页',],
          loading:false
      }
  },
  methods:{
    readAll(){
        request({
            url:"/notice/readAll/",
        }).then(resp=>{
            if(resp.data.length==0){
                this.$parent.$parent.$parent.$parent.notices = false;
                this.$parent.$refs.NoticeList.tableData.forEach(function(e){  
                    e.unread = false;
                });
                this.$message({
                    type: 'success',
                    message:'全部标为已读！'
                });
            }
        });
    }
}
}
</script>

<style scoped>

</style>