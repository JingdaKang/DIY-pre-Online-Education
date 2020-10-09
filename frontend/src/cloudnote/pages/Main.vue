<template>
  <div id="main">

    <el-row style="margin-bottom: 1%">

      <!--          侧边导航-->
      <el-col :span="3">


        <el-menu :default-active="navIndex" class="el-menu-vertical-demo"  :collapse="true" @select = "AccessTag" style="width:150px">
          <el-menu-item class = "mystyle" index="write" @click="Link('write')">
            <i class="el-icon-edit menu-icon"> 笔记编辑</i>
            <span slot="title" >Write</span>
          </el-menu-item>

          <el-menu-item class = "mystyle" index="files" @click="Link('files')">
            <i class="el-icon-folder-opened menu-icon"> 笔记本</i>
            <span slot="title">Folder</span>
          </el-menu-item>

          <el-menu-item class = "mystyle" index="rubbish" @click="Link('rubbish')">
            <i class="el-icon-delete menu-icon"> 回收站</i>
            <span slot="title">Rubbish</span>
          </el-menu-item>

          <el-menu-item class = "mystyle" index="team" @click="Link('team')">
            <i class="el-icon-s-cooperation menu-icon"> 团队</i>
            <span slot="title">Team</span>
          </el-menu-item>
          <el-menu-item class = "mystyle" index="usercenter" @click="Link('manage')">
            <i class="el-icon-user menu-icon"> 个人中心</i>
            <span slot="title">UserCenter</span>
          </el-menu-item>
          <el-menu-item class = "mystyle" index="notice" @click="Link('notice')">
            <i class="el-icon-message menu-icon"> 通知中心</i>
            <span slot="title">Notice</span>
            <el-badge is-dot class="item" v-if = "notices"/>
          </el-menu-item>
          <el-submenu  class = "mystyle" index="tag">
            <template slot="title">
              <i class="el-icon-collection-tag menu-icon"> 标签</i>
            </template>
            <el-menu-item-group>
              <template slot="title">Tag</template>
              <el-menu-item :index="tag.id.toString()" v-for = "tag in tags" :key = "tag.id" >{{tag.tag_name}}</el-menu-item>
            </el-menu-item-group>
          </el-submenu>
        </el-menu>



      </el-col>


      <!--         页面-->
      <el-col :span="21" >


        <router-view @ListTag = 'ListTag' ></router-view>


      </el-col>

    </el-row>



  </div>
</template>

<script>

import { UserService } from '@/service/UserService';
//import { CommonService } from '@/service/CommonService';
import request from "@/network/request";
import store from '@/store';

export default {
  name: 'main',
  created(){

    console.log('login');
    let that = this;
    let id = that.$cookies.get('user_id');
    let name = that.$cookies.get('username');
    let type = that.$cookies.get('type');
    let pw = that.$cookies.get('pw');
    let user = {id,name}
    store.commit('user', user);
    console.log(this.$cookies.get('user_id'));
    UserService.login(name,pw,type,() => {
    this.ListTag();
    this.checkNotice();
    this.loadErrorBook();
  });



  },
  data() {
   return{
     rate:null,
     tags:null,
     notices:false,
   }
 },
 methods:{
  loadErrorBook(){
  console.log('loaderrorbook');
  var type = this.$cookies.get('type')
    console.log(type);
    if(type=='S'){
        request({
      url:'/errorbook/work/',
    });
    request({
      url:'/errorbook/exam/',
    });
    }else if(type=='T'){
        request({
      url:'/goodanswer/work/',
    });
    request({
      url:'/goodanswer/exam/',
    });
    }



  },
  Link(path){
    this.$router.push({
      name:path
    })
  },
  AccessTag(key){
    console.log(key);
    window.router.push({
      name:"tag",
      query:{
        tag_id:key
      }
    });
  },
  checkNotice(){
      console.log('checknotice');
    console.log(this.$cookies.get('type'));

    request({
      url:'/notice/getUnreadNotice/',
    }).then(resp=>{
      var data = resp.data;
      if(data.length!=0){
        this.notices = true;
      }
    })
  },
  ListTag(){
    console.log('listtag');
    console.log(this.$cookies.get('type'));
    request({
      url:'/tag/',
    }).then(resp=>{
      this.tags = resp.data.results;
    })
  }

},
computed:{
  navIndex() {
    return this.$route.name;
  },
}



}
</script>

<style>


.card{

  background-color: white;
  box-shadow: 0 4px 8px 0 rgba(0, 0, 0, 0.2), 0 6px 20px 0 rgba(0, 0, 0, 0.19);
  border-radius: 4px;
  display: inline-block;
  margin-right: 4%;
  margin-top: 20%;
  vertical-align: top;
}
.card span {
  font-size: 12px;
  color: deepskyblue;
  display: block;
  letter-spacing: 2px;
  padding: 30px 20px;
}
.mystyle{
  margin:25px 0;
}
.el-menu--collapse{
  width:unset;
}
.el-menu-item.is-active {
    background-color: #3370ff !important;
    color: #ffffff;
  }
.menu-icon{
  margin: 0 50% 0 15% !important;
}
</style>
