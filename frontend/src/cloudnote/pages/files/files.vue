<template>
    <div style="padding-left: 2%;padding-right: 2%">

<!--面包导航-->

         <navigate ref="navigate" ></navigate>


<!--查找过滤-->
        <filter-nav  ref="FilterNav" v-if="is_note" ></filter-nav>


<!--        文件列表-->
        <file-list ref="FileList" @ChangeDisplay = "ChangeDisplay"></file-list>




    </div>
</template>

<script>


    import Navigate from "@/cloudnote/pages/files/components/navigate";
    import FilterNav from "@/cloudnote/pages/files/components/filter-nav";
    import FileList from "@/cloudnote/pages/files/components/file-list";
    export default {

        name: "files",
        data:function () {
            return{
                is_note:false,


            }
        },
        methods:{
            ChangeDisplay(is_note){
                this.is_note=is_note;
            }
        },

        components:{
            FileList,
            FilterNav,
            Navigate,

        }


    }
</script>

<style scoped>

</style>
