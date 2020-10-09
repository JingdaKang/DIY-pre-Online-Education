<template>
    <div style="padding-left: 2%;padding-right: 2%">

<!--面包导航-->

         <navigate ref="navigate"></navigate>



<!--        文件列表-->
        <file-list ref="FileList"></file-list>




    </div>
</template>

<script>


    import Navigate from "@/cloudnote/pages/tag/components/navigate";
    import FileList from "@/cloudnote/pages/tag/components/file-list";
    export default {

        name: "tag",
        data:function () {
            return{



            }
        },
        methods:{

        },

        components:{
            FileList,
            Navigate,

        }


    }
</script>

<style scoped>

</style>
